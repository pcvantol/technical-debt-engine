import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from tde_cli.main import ExitCode, main
from tde_runtime.release_certification import ReleaseCertification


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def qualification(directory, **changes):
    checks = {"artifactIntegrity": True, "buildReproducibility": True, "capabilitySelection": True,
              "requiredCapabilitiesExecuted": True, "runtimeQualification": True, "policyEvidence": True}
    candidate = {"sha": "a" * 40, "repository": "https://example.invalid/tde.git", "selectedCapabilities": ["code_size"]}
    evidence = {"schemaId": "tde.release-evidence", "schemaVersion": "1.0.0", "candidate": candidate,
                "artifacts": [{"filename": "tde.whl", "digest": "sha256:" + "b" * 64}],
                "runtimeQualification": {}, "policyEvidence": {}, "softwareAssurance": {"decision": "PASS"},
                "trustedDelivery": {"decision": "PASS"}, "releaseQualification": {"checks": checks}}
    evidence["releaseEvidenceId"] = "release-evidence.sha256." + sha256(canonical(evidence)).hexdigest()
    evidence_path = Path(directory) / "release-evidence.json"; evidence_path.write_bytes(canonical(evidence))
    value = {"schemaId": "tde.release-qualification", "schemaVersion": "1.0.0", "releaseCandidate": candidate,
             "artifacts": evidence["artifacts"], "manifest": {"integrity": True},
             "softwareAssurance": {"assuranceId": "assurance.sha256.test", "decision": "PASS"},
             "trustedDelivery": {"trustedDeliveryId": "trusted-delivery.sha256.test", "decision": "PASS"},
             "runtimeEvidence": {"validation": {"status": "VALID"}, "policyDecision": "PASS", "runtimeQualification": "QUALIFIED", "identity": "sha256:test"},
             "releaseEvidence": {"path": str(evidence_path), "digest": "sha256:" + sha256(evidence_path.read_bytes()).hexdigest(), "id": evidence["releaseEvidenceId"]},
             "checks": checks, "releaseDecision": "READY", "decision": "RELEASE_QUALIFIED"}
    value.update(changes)
    return value


class ReleaseCertificationTests(unittest.TestCase):
    def write(self, directory, value):
        path = Path(directory) / "qualification.json"; path.write_text(json.dumps(value), encoding="utf-8"); return path

    def test_certification_evaluates_complete_canonical_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            report = ReleaseCertification().certify(self.write(directory, qualification(directory)), Path(directory) / "report.json")
            self.assertEqual("RELEASE_CERTIFIED", report["decision"]); self.assertTrue(report["report"]["integrity"])

    def test_missing_or_invalid_evidence_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            report = ReleaseCertification().certify(Path(directory) / "missing.json", Path(directory) / "report.json")
            self.assertEqual("RELEASE_NOT_CERTIFIED", report["decision"]); self.assertIn("release qualification evidence is missing or invalid JSON", report["limitations"])

    def test_tampered_persisted_release_evidence_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            value = qualification(directory); Path(value["releaseEvidence"]["path"]).write_text("{}", encoding="utf-8")
            report = ReleaseCertification().certify(self.write(directory, value), Path(directory) / "report.json")
            self.assertEqual("RELEASE_NOT_CERTIFIED", report["decision"]); self.assertFalse(report["checks"]["releaseEvidence"])

    def test_decision_mapping_and_cli_are_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(directory, qualification(directory, checks={"artifactIntegrity": False, "buildReproducibility": True}))
            output = []
            class Stream:
                def write(self, value): output.append(value)
                def flush(self): pass
            code = main(["--format", "json", "certify", ".", "--qualification-evidence", str(path), "--report-output", str(Path(directory) / "report.json")], Stream())
            self.assertEqual(ExitCode.BLOCKED, code); self.assertIn("RELEASE_NOT_CERTIFIED", "".join(output))

    def test_cli_envelope_is_canonical_certification_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(directory, {"command": "release-qualify", "releaseQualificationEvidence": qualification(directory)})
            report = ReleaseCertification().certify(path, Path(directory) / "report.json")
            self.assertEqual("RELEASE_CERTIFIED", report["decision"])
