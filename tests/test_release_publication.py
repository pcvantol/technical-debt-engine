import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tde_runtime.release_publication import validate_authorization, verify_publication_bundle


class ReleasePublicationTests(unittest.TestCase):
    candidate = "a" * 40

    def bundle(self, root):
        inputs = root / "inputs"; inputs.mkdir()
        files = {"wheel.whl": b"wheel", "source.tar.gz": b"sdist", "image.tar": b"oci", "docker-provenance.json": b"{}",
                 "manifest.json": b"{}", "evidence.json": b"{}"}
        qualification = {"decision": "RELEASE_QUALIFIED", "releaseDecision": "READY", "releaseCandidate": {"sha": self.candidate}}
        certification = {"decision": "RELEASE_CERTIFIED", "candidate": {"sha": self.candidate}}
        files["qualification.json"] = json.dumps(qualification).encode(); files["certification.json"] = json.dumps(certification).encode()
        for name, value in files.items(): (inputs / name).write_bytes(value)
        output = root / "bundle"
        command = ["python", "tools/assemble_release_bundle.py", "--candidate-sha", self.candidate, "--output", str(output),
                   "--wheel", str(inputs / "wheel.whl"), "--sdist", str(inputs / "source.tar.gz"), "--oci-archive", str(inputs / "image.tar"),
                   "--docker-provenance", str(inputs / "docker-provenance.json"), "--release-manifest", str(inputs / "manifest.json"),
                   "--release-qualification", str(inputs / "qualification.json"), "--release-certification", str(inputs / "certification.json"), "--release-evidence", str(inputs / "evidence.json")]
        subprocess.run(command, check=True, env={**__import__("os").environ, "PYTHONPATH": "src"}, capture_output=True)
        return output

    def authorization(self, bundle):
        manifest = json.loads((bundle / "bundle-manifest.json").read_text())
        return {"authorizedBy": "release-reviewer", "authorizedAt": "2026-07-16T00:00:00Z", "candidateSha": self.candidate,
                "releaseVersion": "0.1.0", "bundleId": manifest["bundleId"], "bundleChecksum": manifest["bundleChecksum"],
                "targets": ["github_release", "pypi", "docker_hub"]}

    def test_preflight_reads_existing_bundle_and_writes_no_bundle_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); bundle = self.bundle(root); before = sorted(item.name for item in bundle.iterdir())
            result = verify_publication_bundle(bundle, self.candidate, "0.1.0", self.authorization(bundle))
            self.assertEqual("PUBLICATION_PREFLIGHT_READY", result["decision"])
            self.assertEqual(before, sorted(item.name for item in bundle.iterdir()))

    def test_authorization_must_bind_all_targets_and_selected_bundle(self):
        errors = validate_authorization({"authorizedBy": "a", "authorizedAt": "now", "candidateSha": self.candidate,
                                        "releaseVersion": "0.1.0", "bundleId": "bundle", "bundleChecksum": "sha256:test",
                                        "targets": ["pypi"]}, self.candidate, "0.1.0", "bundle", "sha256:test")
        self.assertTrue(errors)

    def test_workflow_is_manual_dry_run_and_never_rebuilds(self):
        workflow = Path(".github/workflows/internal-release-publish.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow); self.assertNotIn("pull_request:", workflow); self.assertNotIn("push:", workflow)
        self.assertIn("environment: internal-release", workflow); self.assertIn("inputs.dry_run == false", workflow)
        self.assertIn("actions/download-artifact@", workflow)
        self.assertIn("gh release create", workflow); self.assertIn("pypa/gh-action-pypi-publish@", workflow)
        self.assertIn("secrets.PYPI_API_TOKEN", workflow)
        self.assertIn("docker.io/pcvantol/technical-debt-engine:$VERSION", workflow)
        self.assertNotIn("docker.io/pcvantol/technical-debt-engine:latest", workflow)
        self.assertNotIn("package_build.py", workflow); self.assertNotIn("build_docker_candidate.py", workflow)
