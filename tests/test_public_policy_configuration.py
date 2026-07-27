"""Black-box coverage for the installed public policy configuration contract."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(shutil.which("cloc"), "public policy integration requires cloc on PATH")
class PublicPolicyConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tde-public-policy-")
        self.root = Path(self.temporary.name)
        self.repository = self.root / "repository"
        self.repository.mkdir()
        (self.repository / "sample.py").write_text("value = 1\n", encoding="utf-8")
        self.venv = self.root / "venv"
        self.environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        subprocess.run([sys.executable, "-m", "venv", str(self.venv)], check=True, env=self.environment)
        executable_directory = self.venv / ("Scripts" if os.name == "nt" else "bin")
        self.pip = executable_directory / ("pip.exe" if os.name == "nt" else "pip")
        self.tde = executable_directory / ("tde.exe" if os.name == "nt" else "tde")
        wheels = self.root / "wheels"
        repository_root = Path(__file__).resolve().parents[1]
        subprocess.run([str(self.pip), "wheel", "--no-deps", "--wheel-dir", str(wheels), str(repository_root)],
                       check=True, capture_output=True, text=True, env=self.environment)
        wheel = next(wheels.glob("technical_debt_engine_runtime-*.whl"))
        subprocess.run([str(self.pip), "install", "--no-deps", str(wheel)], check=True,
                       capture_output=True, text=True, env=self.environment)
        subprocess.run([str(self.pip), "install", "radon==6.0.1"], check=True,
                       capture_output=True, text=True, env=self.environment)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, policy: Path) -> tuple[int, dict[str, object]]:
        completed = subprocess.run([str(self.tde), "--format", "json", "--policy", str(policy), "assess",
                                    "--capability", "code-size", str(self.repository)], capture_output=True,
                                   text=True, check=False, env=self.environment)
        return completed.returncode, json.loads(completed.stdout)

    @staticmethod
    def configuration(threshold: int) -> dict[str, object]:
        return {
            "identifier": "example.code-size", "version": "2026.1", "scope": "repository",
            "owner": "example", "description": "Example organization policy.",
            "supportedCapabilities": ["code_size"], "supportedSchemas": ["1.0.0"],
            "supportedRuntimeVersions": ["1.0.0rc3"],
            "rules": [{"id": "example.code-size.lines", "type": "threshold", "capability": "code_size",
                       "metric": "code_size.code_lines", "operator": "greater_than",
                       "threshold": {"warning": threshold, "blocking": threshold + 1000},
                       "severity": {"warning": "WARNING", "blocking": "BLOCKING"}, "enabled": True,
                       "rationale": "Keep repositories understandable."}],
        }

    def test_public_cli_uses_policy_file_and_records_its_identity(self) -> None:
        policy = self.root / "policy.json"
        policy.write_text(json.dumps(self.configuration(0)), encoding="utf-8")
        first_code, first = self.invoke(policy)
        second_code, second = self.invoke(policy)
        self.assertEqual(1, first_code)
        self.assertEqual(first_code, second_code)
        first_evidence = first["evidence"]
        second_evidence = second["evidence"]
        self.assertEqual("PASS_WITH_WARNINGS", first_evidence["assessmentDecision"]["decision"])
        self.assertEqual(first_evidence["assessmentDecision"]["decision"], second_evidence["assessmentDecision"]["decision"])
        self.assertEqual(first_evidence["policyEvidence"]["policyConfiguration"]["hash"],
                         second_evidence["policyEvidence"]["policyConfiguration"]["hash"])
        self.assertEqual(first_evidence["policyEvidence"]["policyConfiguration"],
                         first_evidence["assessmentDecision"]["policyConfiguration"])
        self.assertTrue(any(item["metricKey"] == "code_size.code_lines" for item in first_evidence["measurements"]))

    def test_installed_wheel_publishes_and_enforces_the_schema_contract(self) -> None:
        listed = subprocess.run([str(self.tde), "--format", "json", "schema"], capture_output=True,
                                text=True, check=False, env=self.environment)
        self.assertEqual(0, listed.returncode, listed.stderr)
        schemas = json.loads(listed.stdout)["schemas"]
        self.assertEqual(6, len(schemas))
        self.assertTrue(all(item["compatibilityVersion"] == "1" and Path(item["location"]).is_file() for item in schemas))
        location = self.root / "evidence"
        completed = subprocess.run([str(self.tde), "--format", "json", "--store-location", str(location),
                                    "--profile", "minimal", "assess", str(self.repository)], capture_output=True,
                                   text=True, check=False, env=self.environment)
        self.assertEqual(0, completed.returncode, completed.stderr)
        evidence = json.loads(completed.stdout)["evidence"]
        for item in [evidence["assessment"], evidence["policyEvidence"], evidence["assessmentDecision"],
                     *evidence["assessment"]["capabilityExecutions"]]:
            self.assertEqual("1.0.0", item["schema"]["version"])
            self.assertEqual("1", item["schema"]["compatibilityVersion"])
            self.assertEqual("1.0.0rc3", item["schema"]["runtimeVersion"])
        record = next((location / "evidence").glob("*.json"))
        persisted = json.loads(record.read_text(encoding="utf-8"))
        persisted["evidence"]["policyEvidence"]["schema"]["version"] = "999.0.0"
        record.write_text(json.dumps(persisted), encoding="utf-8")
        rejected = subprocess.run([str(self.tde), "--format", "json", "--store-location", str(location), "history", str(self.repository)],
                                  capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(3, rejected.returncode)
        self.assertIn("incompatible schema version", json.loads(rejected.stdout)["reason"])

    def test_installed_wheel_qualifies_declarative_repositories_with_profiles(self) -> None:
        definition = self.root / "repository.json"
        definition.write_text(json.dumps({
            "identifier": "fixture.python", "name": "Fixture Python", "repositoryRoot": str(self.repository),
            "repositoryType": "source", "primaryLanguage": "Python", "defaultAssessmentProfile": "minimal",
            "metadata": {"fixture": True},
        }), encoding="utf-8")
        minimal = subprocess.run([str(self.tde), "--format", "json", "--repository-definition", str(definition),
                                  "qualify"], capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(0, minimal.returncode, minimal.stderr)
        result = json.loads(minimal.stdout)
        qualification = result["repositoryQualification"]
        self.assertEqual("fixture.python", qualification["repository"]["identifier"])
        self.assertEqual("minimal", qualification["assessmentProfile"]["identifier"])
        self.assertEqual("QUALIFIED", qualification["qualificationStatus"])
        self.assertEqual("tde.repository-qualification-evidence", qualification["schema"]["name"])
        self.assertTrue(Path(result["qualificationRegistry"]["path"]).is_file())
        standard = subprocess.run([str(self.tde), "--format", "json", "--repository-definition", str(definition),
                                   "--profile", "standard", "qualify"], capture_output=True, text=True,
                                  check=False, env=self.environment)
        self.assertEqual(0, standard.returncode, standard.stderr)
        self.assertEqual("standard", json.loads(standard.stdout)["repositoryQualification"]["assessmentProfile"]["identifier"])
        unsupported = self.root / "unsupported"
        unsupported.mkdir()
        (unsupported / "README.txt").write_text("no supported source", encoding="utf-8")
        definition_data = json.loads(definition.read_text(encoding="utf-8"))
        definition_data.update({"identifier": "fixture.unsupported", "repositoryRoot": str(unsupported)})
        definition.write_text(json.dumps(definition_data), encoding="utf-8")
        qualified = subprocess.run([str(self.tde), "--format", "json", "--repository-definition", str(definition),
                                    "qualify"], capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(0, qualified.returncode, qualified.stderr)
        unsupported_evidence = json.loads(qualified.stdout)["assessmentEvidence"]
        self.assertEqual("QUALIFIED", json.loads(qualified.stdout)["repositoryQualification"]["qualificationStatus"])
        self.assertEqual(["code_size"], unsupported_evidence["assessment"]["executionPlan"]["plannedCapabilities"])

    def test_public_cli_fails_closed_for_invalid_or_missing_policy_file(self) -> None:
        invalid = self.root / "invalid-policy.json"
        value = self.configuration(100)
        value["rules"][0]["metric"] = "code_size.unknown"  # type: ignore[index]
        invalid.write_text(json.dumps(value), encoding="utf-8")
        code, response = self.invoke(invalid)
        self.assertEqual(3, code)
        self.assertIn("unknown metric", response["reason"])
        code, response = self.invoke(self.root / "missing-policy.json")
        self.assertEqual(3, code)
        self.assertIn("does not exist", response["reason"])

    def test_public_cli_runs_default_multi_capability_assessment_and_collects_failure(self) -> None:
        completed = subprocess.run([str(self.tde), "--format", "json", "assess", str(self.repository)],
                                   capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(0, completed.returncode, completed.stderr)
        evidence = json.loads(completed.stdout)["evidence"]
        assessment = evidence["assessment"]
        self.assertEqual("standard", assessment["profile"])
        self.assertEqual("1.2.0", assessment["profileVersion"])
        self.assertTrue(assessment["profileHash"].startswith("sha256:"))
        self.assertEqual(["code_size", "complexity", "coverage", "dependency_health"], assessment["executionPlan"]["plannedCapabilities"])
        self.assertEqual({"code_size", "complexity", "coverage", "dependency_health"},
                         {item["capability"] for item in assessment["capabilityExecutions"]})
        self.assertTrue(assessment["startedAt"])
        self.assertTrue(assessment["completedAt"])
        isolated = {**self.environment, "PATH": str(self.tde.parent)}
        failed = subprocess.run([str(self.tde), "--format", "json", "assess", str(self.repository)],
                                capture_output=True, text=True, check=False, env=isolated)
        self.assertEqual(5, failed.returncode, failed.stderr)
        failed_evidence = json.loads(failed.stdout)["evidence"]
        statuses = {item["capability"]: item["executionStatus"]
                    for item in failed_evidence["assessment"]["capabilityExecutions"]}
        self.assertEqual("ANALYZER_NOT_FOUND", statuses["code_size"])
        self.assertEqual("VALID", statuses["complexity"])

    def test_public_cli_selects_and_validates_declarative_profiles(self) -> None:
        minimal = subprocess.run([str(self.tde), "--format", "json", "--profile", "minimal", "assess", str(self.repository)],
                                 capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(0, minimal.returncode, minimal.stderr)
        evidence = json.loads(minimal.stdout)["evidence"]
        self.assertEqual("minimal", evidence["assessment"]["profile"])
        self.assertEqual(["code_size"], evidence["assessment"]["executionPlan"]["plannedCapabilities"])
        invalid = self.root / "invalid-profile.json"
        invalid.write_text(json.dumps({"identifier": "invalid"}), encoding="utf-8")
        failed = subprocess.run([str(self.tde), "--format", "json", "--profile", str(invalid), "assess", str(self.repository)],
                                capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(3, failed.returncode)
        self.assertIn("missing required fields", json.loads(failed.stdout)["reason"])
        (self.root / "profile-policy.json").write_text("{}", encoding="utf-8")
        profile = {
            "identifier": "invalid", "version": "1.0.0", "description": "invalid",
            "capabilities": [{"identifier": "unknown", "required": True, "optional": False}],
            "policy": {"file": "profile-policy.json"}, "metadata": {"default": False},
        }
        invalid.write_text(json.dumps(profile), encoding="utf-8")
        failed = subprocess.run([str(self.tde), "--format", "json", "--profile", str(invalid), "assess", str(self.repository)],
                                capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(3, failed.returncode)
        self.assertIn("unknown capability", json.loads(failed.stdout)["reason"])
        profile["capabilities"] = [{"identifier": "code_size", "required": True, "optional": False},
                                   {"identifier": "code_size", "required": True, "optional": False}]
        invalid.write_text(json.dumps(profile), encoding="utf-8")
        failed = subprocess.run([str(self.tde), "--format", "json", "--profile", str(invalid), "assess", str(self.repository)],
                                capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(3, failed.returncode)
        self.assertIn("duplicate capability", json.loads(failed.stdout)["reason"])
        failed = subprocess.run([str(self.tde), "--format", "json", "--profile", "does-not-exist", "assess", str(self.repository)],
                                capture_output=True, text=True, check=False, env=self.environment)
        self.assertEqual(3, failed.returncode)
        self.assertIn("not registered", json.loads(failed.stdout)["reason"])


if __name__ == "__main__":
    unittest.main()
