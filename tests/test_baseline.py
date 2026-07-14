from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tde_runtime import Runtime
from tde_runtime.baseline import BaselineError, BaselineRepository, ComparisonEngine


class BaselineAndComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.evidence = Runtime().execute(self.root).evidence

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_baseline_is_persisted_and_immutable(self) -> None:
        repository = BaselineRepository(self.root / "baselines")
        baseline = repository.create(self.evidence, "initial")
        self.assertEqual("initial", repository.load("initial")["baselineId"])
        with self.assertRaises(BaselineError):
            repository.create(self.evidence, "initial")
        self.assertEqual(self.evidence, baseline["evidence"])

    def test_comparison_detects_metric_regression_and_improvement(self) -> None:
        baseline = {"baselineId": "initial", "evidence": self._evidence(10, [{"findingId": "old", "severity": "HIGH"}])}
        current = self._evidence(15, [{"findingId": "new", "severity": "HIGH"}])
        comparison = ComparisonEngine().compare(current, baseline)
        self.assertEqual(5, comparison["metricDeltas"][0]["numericDelta"])
        self.assertIn("new", comparison["regressions"])
        self.assertIn("old", comparison["improvements"])

    def test_comparison_detects_severity_change_and_capability_support(self) -> None:
        baseline = {"baselineId": "initial", "evidence": self._evidence(10, [{"findingId": "same", "severity": "LOW"}])}
        current = self._evidence(10, [{"findingId": "same", "severity": "CRITICAL"}])
        comparison = ComparisonEngine().compare(current, baseline)
        self.assertEqual("SEVERITY_INCREASED", comparison["findingTransitions"][0]["transition"])
        self.assertEqual("SUPPORTED", comparison["capabilityComparison"][0]["comparisonSupport"])

    def _evidence(self, metric_value: int, findings: list[dict[str, str]]) -> dict:
        evidence = dict(self.evidence)
        evidence["measurements"] = [{"metricKey": "example.metric", "scope": "repository", "targetEntityId": self.evidence["repository"]["id"], "value": metric_value}]
        evidence["findings"] = findings
        evidence["capabilityResults"] = [{"capabilityId": "example", "status": "VALID"}]
        return evidence
