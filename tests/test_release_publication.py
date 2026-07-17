from hashlib import sha256
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tde_runtime.release_publication import canonical, validate_authorization, validate_authorization_record, verify_publication_bundle


class ReleasePublicationTests(unittest.TestCase):
    candidate = "a" * 40
    tagger_name = "Technical Debt Engine Release Automation"
    tagger_email = "technical-debt-engine-release[bot]@users.noreply.github.com"

    def bundle(self, root):
        inputs = root / "inputs"; inputs.mkdir()
        files = {"wheel.whl": b"wheel", "source.tar.gz": b"sdist", "image.tar": b"oci", "docker-provenance.json": b"{}",
                 "manifest.json": b"{}", "evidence.json": b"{}"}
        qualification = {"decision": "RELEASE_QUALIFIED", "releaseDecision": "READY", "releaseCandidate": {"sha": self.candidate}}
        certification = {"decision": "RELEASE_CERTIFIED", "candidate": {"sha": self.candidate}}
        files["qualification.json"] = json.dumps(qualification).encode(); files["certification.json"] = json.dumps(certification).encode()
        for name, value in files.items(): (inputs / name).write_bytes(value)
        output = root / "bundle"
        command = ["python", "tools/assemble_release_bundle.py", "--candidate-sha", self.candidate, "--release-version", "0.2.0", "--output", str(output),
                   "--wheel", str(inputs / "wheel.whl"), "--sdist", str(inputs / "source.tar.gz"), "--oci-archive", str(inputs / "image.tar"),
                   "--docker-provenance", str(inputs / "docker-provenance.json"), "--release-manifest", str(inputs / "manifest.json"),
                   "--release-qualification", str(inputs / "qualification.json"), "--release-certification", str(inputs / "certification.json"), "--release-evidence", str(inputs / "evidence.json")]
        subprocess.run(command, check=True, env={**__import__("os").environ, "PYTHONPATH": "src"}, capture_output=True)
        return output

    def authorization(self, bundle):
        manifest = json.loads((bundle / "bundle-manifest.json").read_text())
        return {"authorizedBy": "release-reviewer", "authorizedAt": "2026-07-16T00:00:00Z", "candidateSha": self.candidate,
                "releaseVersion": "0.2.0", "bundleId": manifest["bundleId"], "bundleChecksum": manifest["bundleChecksum"],
                "targets": ["github_release", "pypi", "docker_hub"]}

    def test_preflight_reads_existing_bundle_and_writes_no_bundle_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); bundle = self.bundle(root); before = sorted(item.name for item in bundle.iterdir())
            result = verify_publication_bundle(bundle, self.candidate, "0.2.0", self.authorization(bundle))
            self.assertEqual("PUBLICATION_PREFLIGHT_READY", result["decision"])
            self.assertEqual(before, sorted(item.name for item in bundle.iterdir()))

    def test_authorization_must_bind_all_targets_and_selected_bundle(self):
        errors = validate_authorization({"authorizedBy": "a", "authorizedAt": "now", "candidateSha": self.candidate,
                                        "releaseVersion": "0.1.0", "bundleId": "bundle", "bundleChecksum": "sha256:test",
                                        "targets": ["pypi"]}, self.candidate, "0.1.0", "bundle", "sha256:test")
        self.assertTrue(errors)

    def test_authorization_record_requires_each_explicit_target_approval(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = self.bundle(Path(temporary)); record = self.authorization(bundle)
            record.update({"schemaId": "tde.internal-release-authorization",
                           "approvedGitTag": "0.2.0", "approvedGitHubRelease": "0.2.0", "approvedPyPI": "0.2.0",
                           "approvedDockerHub": "docker.io/pcvantol/technical-debt-engine:0.2.0", "protectedEnvironment": "internal-release",
                           "publicationWorkflow": ".github/workflows/internal-release-publish.yml", "targetApprovals": {"github_release": True, "pypi": True, "docker_hub": True}})
            record["authorizationId"] = "authorization.sha256." + sha256(canonical(record)).hexdigest()
            self.assertFalse(validate_authorization_record(record, self.candidate, "0.2.0", record["bundleId"], record["bundleChecksum"]))
            record["targetApprovals"]["pypi"] = False
            self.assertTrue(validate_authorization_record(record, self.candidate, "0.2.0", record["bundleId"], record["bundleChecksum"]))

    def test_workflow_is_manual_dry_run_and_never_rebuilds(self):
        workflow = Path(".github/workflows/internal-release-publish.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow); self.assertNotIn("pull_request:", workflow); self.assertNotIn("push:", workflow)
        self.assertIn("environment: internal-release", workflow); self.assertIn("inputs.dry_run == false", workflow)
        self.assertIn("resume_pypi_only", workflow)
        self.assertIn("Verify completed immutable targets for PyPI resume", workflow)
        self.assertIn("inputs.resume_pypi_only == true", workflow)
        self.assertIn("inputs.resume_pypi_only == false", workflow)
        self.assertIn("actions/download-artifact@", workflow)
        self.assertIn("gh release create", workflow); self.assertIn("pypa/gh-action-pypi-publish@", workflow)
        self.assertIn("pypa/gh-action-pypi-publish@cef221092ed1bacb1cc03d23a2d87d1d172e277b", workflow)
        self.assertIn("secrets.PYPI_API_TOKEN", workflow)
        self.assertIn("docker.io/pcvantol/technical-debt-engine:$VERSION", workflow)
        self.assertIn("Configure and verify deterministic Git tagger identity", workflow)
        self.assertIn("git config --local user.name", workflow)
        self.assertIn("git config --local user.email", workflow)
        self.assertIn("Technical Debt Engine Release Automation", workflow)
        self.assertIn("technical-debt-engine-release[bot]@users.noreply.github.com", workflow)
        self.assertIn("tagger-identity.json", workflow)
        self.assertNotIn("docker.io/pcvantol/technical-debt-engine:latest", workflow)
        self.assertNotIn("package_build.py", workflow); self.assertNotIn("build_docker_candidate.py", workflow)

    def test_missing_tagger_identity_fails_closed_before_tag_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {"PATH": __import__("os").environ["PATH"], "HOME": str(root / "empty-home"), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
            (root / "empty-home").mkdir()
            subprocess.run(["git", "init", "--quiet", str(root / "repository")], check=True, env=environment)
            repository = root / "repository"
            (repository / "evidence.txt").write_text("candidate", encoding="utf-8")
            subprocess.run(["git", "-C", str(repository), "add", "evidence.txt"], check=True, env=environment)
            subprocess.run(["git", "-C", str(repository), "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "fixture"], check=True, env=environment)
            subprocess.run(["git", "-C", str(repository), "config", "--unset-all", "user.name"], check=False, env=environment)
            subprocess.run(["git", "-C", str(repository), "config", "--unset-all", "user.email"], check=False, env=environment)
            result = subprocess.run(["sh", "-c", 'test "$(git -C "$1" config --local --get user.name || true)" = "$2" && test "$(git -C "$1" config --local --get user.email || true)" = "$3"', "identity-guard", str(repository), self.tagger_name, self.tagger_email], env=environment, capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((repository / ".git" / "refs" / "tags" / "0.1.0").exists())

    def test_repository_local_identity_creates_annotated_tag_at_selected_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {"PATH": __import__("os").environ["PATH"], "HOME": str(root / "empty-home"), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
            (root / "empty-home").mkdir()
            subprocess.run(["git", "init", "--quiet", str(root / "repository")], check=True, env=environment)
            repository = root / "repository"
            (repository / "evidence.txt").write_text("candidate", encoding="utf-8")
            subprocess.run(["git", "-C", str(repository), "add", "evidence.txt"], check=True, env=environment)
            subprocess.run(["git", "-C", str(repository), "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "fixture"], check=True, env=environment)
            candidate = subprocess.run(["git", "-C", str(repository), "rev-parse", "HEAD"], check=True, env=environment, capture_output=True, text=True).stdout.strip()
            subprocess.run(["git", "-C", str(repository), "config", "--local", "user.name", self.tagger_name], check=True, env=environment)
            subprocess.run(["git", "-C", str(repository), "config", "--local", "user.email", self.tagger_email], check=True, env=environment)
            subprocess.run(["git", "-C", str(repository), "tag", "--annotate", "0.1.0", candidate, "--message", "release"], check=True, env=environment)
            tagged = subprocess.run(["git", "-C", str(repository), "rev-parse", "0.1.0^{}"], check=True, env=environment, capture_output=True, text=True).stdout.strip()
            identity = subprocess.run(["git", "-C", str(repository), "for-each-ref", "--format=%(taggername) %(taggeremail)", "refs/tags/0.1.0"], check=True, env=environment, capture_output=True, text=True).stdout.strip()
            self.assertEqual(candidate, tagged)
            self.assertEqual(f"{self.tagger_name} <{self.tagger_email}>", identity)
