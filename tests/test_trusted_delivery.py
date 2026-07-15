import json, subprocess, tempfile, unittest
from hashlib import sha256
from pathlib import Path

from tde_runtime import Runtime
from tde_runtime.trusted_delivery import TrustedDelivery


class TrustedDeliveryTests(unittest.TestCase):
    def candidate(self, root: Path) -> tuple[str, str]:
        subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(root), "remote", "add", "origin", "https://example.invalid/tde.git"], check=True)
        (root / "candidate.txt").write_text("candidate\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "candidate"], check=True)
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(), "https://example.invalid/tde.git"

    @staticmethod
    def runtime() -> dict:
        return {"validation": {"status": "VALID"}, "integrity": {"contentDigest": "sha256:runtime"}}

    @staticmethod
    def assurance(records: list[dict]) -> dict:
        return {"schemaId": "tde.software-assurance", "assuranceId": "assurance.sha256.test", "decision": "PASS",
                "checks": {"artifactIntegrity": True, "buildProvenanceVerification": True},
                "artifacts": {"records": [{"artifacts": records}]},
                "workflows": {"immutableActions": True, "leastPrivilege": True}}

    def manifest(self, root: Path, sha: str, repository: str, records: list[dict]) -> Path:
        path = root.parent / f"{root.name}-delivery-manifest.json"
        path.write_text(json.dumps({"schemaId": "tde.trusted-delivery-manifest", "schemaVersion": "1.0.0",
                                    "candidate": {"sha": sha, "repository": repository, "branch": "main"},
                                    "artifacts": records}), encoding="utf-8")
        return path

    @staticmethod
    def commit_workflow(root: Path) -> str:
        subprocess.run(["git", "-C", str(root), "add", ".github"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "workflow"], check=True)
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

    def test_missing_git_candidate_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            evidence = Runtime().execute(root).evidence
            self.assertEqual("FAIL", TrustedDelivery().validate(root, evidence)["qualification"])

    def test_valid_candidate_manifest_artifact_workflow_and_assurance_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); sha, repository = self.candidate(root)
            workflow = root / ".github" / "workflows"; workflow.mkdir(parents=True)
            (workflow / "trusted.yml").write_text("permissions:\n  contents: read\n", encoding="utf-8")
            sha = self.commit_workflow(root)
            digest = "sha256:" + sha256(b"wheel").hexdigest(); records = [{"filename": "tde.whl", "digest": digest}]
            manifest = self.manifest(root, sha, repository, records)
            result = TrustedDelivery().validate(root, self.runtime(), self.assurance(records), manifest)
            self.assertEqual("PASS", result["qualification"])
            self.assertTrue(result["checks"]["buildProvenanceValidation"])
            self.assertEqual("assurance.sha256.test", result["softwareAssurance"]["assuranceId"])

    def test_candidate_manifest_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); sha, repository = self.candidate(root)
            workflow = root / ".github" / "workflows"; workflow.mkdir(parents=True)
            (workflow / "trusted.yml").write_text("permissions:\n  contents: read\n", encoding="utf-8")
            self.commit_workflow(root)
            records = [{"filename": "tde.whl", "digest": "sha256:" + "a" * 64}]
            manifest = self.manifest(root, "b" * 40, repository, records)
            result = TrustedDelivery().validate(root, self.runtime(), self.assurance(records), manifest)
            self.assertEqual("FAIL", result["qualification"])
            self.assertFalse(result["checks"]["manifestIntegrity"])
