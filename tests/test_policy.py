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

    def test_declarative_configuration_rejects_unknown_duplicate_and_conflicting_rules(self) -> None:
        base = {"id": "size", "type": "threshold", "capability": "code_size", "metric": "code_size.code_lines",
                "operator": "greater_than", "threshold": {"warning": 10, "blocking": 20},
                "severity": {"warning": "WARNING", "blocking": "BLOCKING"}, "enabled": True,
                "rationale": "Keep changes reviewable."}
        valid = policy(rules=[base])
        self.engine.validate(valid)
        for mutation, message in (
            ({"capability": "unknown"}, "unknown policy capability"),
            ({"operator": "equals"}, "invalid policy operator"),
            ({"threshold": {"warning": 20, "blocking": 10}}, "conflicting thresholds"),
        ):
            candidate = json.loads(json.dumps(valid))
            candidate["rules"][0].update(mutation)
            with self.assertRaisesRegex(PolicyError, message):
                self.engine.validate(candidate)
        duplicate = json.loads(json.dumps(valid))
        duplicate["rules"].append({**base, "id": "size-second"})
        with self.assertRaisesRegex(PolicyError, "conflicting enabled policies"):
            self.engine.validate(duplicate)

    def test_cli_exit_codes_match_every_policy_decision(self) -> None:
        self.assertEqual({"PASS": ExitCode.SUCCESS, "PASS_WITH_WARNINGS": ExitCode.WARNING, "FAIL": ExitCode.FAILED,
                          "BLOCKED": ExitCode.BLOCKED, "NOT_APPLICABLE": ExitCode.NOT_SUPPORTED},
                         {decision: _policy_exit_code(decision) for decision in ("PASS", "PASS_WITH_WARNINGS", "FAIL", "BLOCKED", "NOT_APPLICABLE")})

    def test_bundled_code_size_policy_has_product_repository_thresholds(self) -> None:
        bundled = Path(__file__).parents[1] / "src" / "tde_runtime" / "policies" / "generation-1.json"
        rule = next(item for item in json.loads(bundled.read_text(encoding="utf-8"))["rules"] if item["id"] == "code_size.repository_lines")
        self.assertEqual({"warning": 25000, "blocking": 50000}, rule["threshold"])

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
