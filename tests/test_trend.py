from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tde_runtime import Runtime
from tde_runtime.baseline import BaselineRepository
from tde_runtime.trend import TrendEngine


class TrendTests(unittest.TestCase):
    def test_history_metric_capability_and_repository_trends(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = Runtime().execute(root).evidence
            evidence["measurements"] = [{"metricKey": "code_size.code_lines", "value": 10}]
            evidence["capabilityResults"] = [{"capabilityId": "code_size", "status": "VALID"}]
            baselines = BaselineRepository(root / "baselines")
            baselines.create(evidence, "first")
            current = Runtime().execute(root).evidence
            current["measurements"] = [{"metricKey": "code_size.code_lines", "value": 15}]
            current["capabilityResults"] = [{"capabilityId": "code_size", "status": "VALID"}]
            trend = TrendEngine().build(current, root / "baselines")
            self.assertEqual(5, trend["repositoryTrend"]["growth"])
            self.assertEqual("INCREASING", trend["metricTrends"][0]["direction"])
            self.assertEqual("code_size", trend["capabilityTrends"][0]["capabilityId"])
            self.assertEqual("rolling", trend["window"])
