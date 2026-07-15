import json
import tempfile
import unittest
from pathlib import Path

from tde_cli.main import ExitCode, main
from tde_runtime.release_certification import ReleaseCertification


def qualification(**changes):
    value = {"schemaId": "tde.release-qualification", "schemaVersion": "1.0.0", "releaseCandidate": {"sha": "a" * 40, "repository": "https://example.invalid/tde.git"},
             "artifacts": [{"filename": "tde.whl", "digest": "sha256:" + "b" * 64}], "manifest": {"integrity": True},
             "softwareAssurance": {"assuranceId": "assurance.sha256.test", "decision": "PASS"},
             "trustedDelivery": {"trustedDeliveryId": "trusted-delivery.sha256.test", "decision": "PASS"},
             "runtimeEvidence": {"validation": {"status": "VALID"}, "policyDecision": "PASS", "runtimeQualification": "QUALIFIED", "identity": "sha256:test"},
             "checks": {"artifactIntegrity": True, "buildReproducibility": True}, "releaseDecision": "READY", "decision": "RELEASE_QUALIFIED"}
    value.update(changes); return value


class ReleaseCertificationTests(unittest.TestCase):
    def write(self, directory, value):
        path = Path(directory) / "qualification.json"; path.write_text(json.dumps(value), encoding="utf-8"); return path

    def test_certification_evaluates_complete_canonical_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            report = ReleaseCertification().certify(self.write(directory, qualification()), Path(directory) / "report.json")
            self.assertEqual("RELEASE_CERTIFIED", report["decision"]); self.assertTrue(report["report"]["integrity"])

    def test_missing_or_invalid_evidence_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            report = ReleaseCertification().certify(Path(directory) / "missing.json", Path(directory) / "report.json")
            self.assertEqual("RELEASE_NOT_CERTIFIED", report["decision"]); self.assertIn("release qualification evidence is missing or invalid JSON", report["limitations"])

    def test_decision_mapping_and_cli_are_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(directory, qualification(checks={"artifactIntegrity": False, "buildReproducibility": True}))
            output = []
            class Stream:
                def write(self, value): output.append(value)
                def flush(self): pass
            code = main(["--format", "json", "certify", ".", "--qualification-evidence", str(path), "--report-output", str(Path(directory) / "report.json")], Stream())
            self.assertEqual(ExitCode.BLOCKED, code); self.assertIn("RELEASE_NOT_CERTIFIED", "".join(output))

    def test_cli_envelope_is_canonical_certification_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(directory, {"command": "release-qualify", "releaseQualificationEvidence": qualification()})
            report = ReleaseCertification().certify(path, Path(directory) / "report.json")
            self.assertEqual("RELEASE_CERTIFIED", report["decision"])
