from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tde_cli.main import ExitCode, _policy_exit_code
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.evidence_store import EvidenceStore
from tde_runtime.policy import PolicyEngine, PolicyError
from tde_runtime.query import QueryEngine


def policy(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "identifier": "test.policy", "version": "1.0.0", "scope": "repository", "owner": "test",
        "description": "deterministic policy fixture", "supportedCapabilities": ["code_size", "complexity"],
        "supportedSchemas": ["1.0.0"], "supportedRuntimeVersions": ["0.1.0"], "rules": [],
    }
    value.update(changes)
    return value


class PolicyEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = PolicyEngine()

    def evaluate(self, rules: list[dict[str, object]], measurements: list[dict[str, object]] = [],
                 findings: list[dict[str, object]] = [], results: list[dict[str, object]] = []) -> dict[str, object]:
        return self.engine.evaluate(policy(rules=rules), {"measurements": measurements, "findings": findings,
                                    "capabilityResults": results, "executionEvidence": {}}, {"executionOptions": {}})

    def test_threshold_outcomes_and_canonical_evidence(self) -> None:
        rule = {"id": "code-size", "type": "threshold", "metricKey": "code_size.code_lines", "warning": 10, "blocking": 20}
        measurement = {"measurementId": "code-size.lines", "capabilityId": "code_size", "metricKey": "code_size.code_lines", "targetEntityId": "repository", "value": 15}
        warning = self.evaluate([rule], [measurement])
        self.assertEqual("PASS_WITH_WARNINGS", warning["decision"])
        self.assertEqual(["code_size"], warning["affectedCapabilities"])
        self.assertEqual(15, warning["triggeredRules"][0]["measuredValue"])
        self.assertEqual(10, warning["triggeredRules"][0]["threshold"])
        measurement["value"] = 20
        self.assertEqual("FAIL", self.evaluate([rule], [measurement])["decision"])
        measurement["value"] = 9
        self.assertEqual("PASS", self.evaluate([rule], [measurement])["decision"])

    def test_multiple_rules_and_missing_evidence_are_deterministic(self) -> None:
        rules = [
            {"id": "code-size", "type": "threshold", "metricKey": "code_size.code_lines", "warning": 1, "blocking": 2},
            {"id": "complexity", "type": "threshold", "metricKey": "complexity.cyclomatic.maximum", "warning": 1, "blocking": 2},
            {"id": "required-complexity", "type": "capability", "capabilityId": "complexity", "required": True, "outcome": "BLOCKED"},
        ]
        evidence = [{"measurementId": "size", "capabilityId": "code_size", "metricKey": "code_size.code_lines", "value": 2}]
        result = self.evaluate(rules, evidence, results=[{"capabilityId": "code_size"}])
        self.assertEqual("BLOCKED", result["decision"])
        self.assertEqual(2, len(result["triggeredRules"]))
        self.assertEqual("NOT_APPLICABLE", self.evaluate([])["decision"])

    def test_policy_precedence_validation_and_missing_policy_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace, repository = root / "workspace", root / "repository"
            workspace.mkdir(); repository.mkdir()
            (workspace / "policy.json").write_text(json.dumps(policy(version="1.1.0")), encoding="utf-8")
            (repository / "policy.json").write_text(json.dumps(policy(version="1.2.0")), encoding="utf-8")
            loaded = self.engine.load({"policy": {"id": "test.policy", "workspace": str(workspace), "repository": str(repository)}}, root, "0.1.0", "1.0.0")
            self.assertEqual("1.2.0", loaded["version"])
            (repository / "invalid.json").write_text('{"identifier": "bad"}', encoding="utf-8")
            with self.assertRaises(PolicyError):
                self.engine.load({"policy": {"repository": str(repository)}}, root, "0.1.0", "1.0.0")
        with self.assertRaisesRegex(PolicyError, "no policy"):
            PolicyEngine(policy_directories=()).load({}, Path.cwd(), "0.1.0", "1.0.0")

    def test_cli_exit_codes_match_every_policy_decision(self) -> None:
        self.assertEqual({"PASS": ExitCode.SUCCESS, "PASS_WITH_WARNINGS": ExitCode.WARNING, "FAIL": ExitCode.FAILED,
                          "BLOCKED": ExitCode.BLOCKED, "NOT_APPLICABLE": ExitCode.NOT_SUPPORTED},
                         {decision: _policy_exit_code(decision) for decision in ("PASS", "PASS_WITH_WARNINGS", "FAIL", "BLOCKED", "NOT_APPLICABLE")})

    def test_real_code_size_and_complexity_evidence_drives_policy_and_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n", encoding="utf-8")
            configuration = RuntimeConfiguration.load({"capabilities": {"code_size": {"enabled": True}, "complexity": {"enabled": True}},
                "policy": {"overrides": {"code_size.repository_lines": {"warning": 0, "blocking": 100000},
                                           "complexity.maximum": {"warning": 0, "blocking": 100000}}}})
            evidence = Runtime().execute(root, configuration).evidence
            self.assertEqual({"code_size", "complexity"}, {item["capabilityId"] for item in evidence["capabilityResults"]})
            self.assertEqual("PASS_WITH_WARNINGS", evidence["policyEvidence"]["decision"])
            store = EvidenceStore(root / "store")
            record = store.persist(evidence)
            persisted = store.retrieve(record["id"])["evidence"]
            policies = QueryEngine().execute(persisted, {"resource": "policies"})
            self.assertEqual("PASS_WITH_WARNINGS", policies["results"][0]["decision"])


if __name__ == "__main__":
    unittest.main()
