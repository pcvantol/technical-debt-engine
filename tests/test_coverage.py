from __future__ import annotations

from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from tde_cli.main import ExitCode, main


COBERTURA = '''<coverage line-rate="0.5" branch-rate="0.5"><packages><package><classes><class><lines><line number="1" hits="1" branch="true" condition-coverage="50% (1/2)"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>'''
COVERAGE_PY = '''<coverage version="7.0" line-rate="0.5" branch-rate="0.5" lines-valid="2" lines-covered="1" branches-valid="2" branches-covered="1"><packages><package><classes><class><lines><line number="1" hits="1" branch="true" condition-coverage="50% (1/2)"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>'''
LCOV = "SF:sample.py\nDA:1,1\nDA:2,0\nBRDA:1,0,0,1\nBRDA:1,0,1,0\nend_of_record\n"
COBERTURA_METHOD_DUPLICATES = '''<coverage version="0.1" line-rate="0.5" branch-rate="0" lines-valid="2" lines-covered="1" branches-valid="0" branches-covered="0"><packages><package><classes><class><methods><method><lines><line number="1" hits="1"/><line number="2" hits="0"/></lines></method></methods><lines><line number="1" hits="1"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>'''
COBERTURA_ROOT_BRANCH_SUMMARY = '''<coverage version="0.1" line-rate="0.5" branch-rate="0.75" lines-valid="2" lines-covered="1" branches-valid="4" branches-covered="3"><packages><package><classes><class><lines><line number="1" hits="1" branch="true" condition-coverage="50% (1/2)"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>'''
XCCOV = '{"coveredLines": 3, "executableLines": 4, "lineCoverage": 0.75, "targets": []}'


class CoverageBlackBoxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "sample.py").write_text("value = 1\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, dict]:
        stream = StringIO()
        code = main(("--format", "json", *arguments), stream)
        return code, json.loads(stream.getvalue())

    def assess(self) -> tuple[int, dict]:
        return self.invoke("assess", "--capability", "coverage", str(self.root))

    def test_cobertura_evidence_is_canonical(self) -> None:
        (self.root / "coverage.xml").write_text(COBERTURA, encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        adapter = result["evidence"]["adapterResults"][0]
        self.assertEqual("cobertura-xml", adapter["evidence"]["parser"])
        self.assertEqual(50.0, next(item["value"] for item in result["evidence"]["measurements"] if item["metricKey"] == "coverage.line_coverage"))

    def test_coverage_py_xml_and_explicit_path_are_supported(self) -> None:
        report = self.root / "artifacts" / "python.xml"; report.parent.mkdir(); report.write_text(COVERAGE_PY, encoding="utf-8")
        (self.root / ".tde.yml").write_text("capabilities:\n  coverage:\n    path: artifacts/python.xml\n", encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("coverage.py-xml", result["evidence"]["adapterResults"][0]["evidence"]["parser"])

    def test_lcov_is_supported(self) -> None:
        (self.root / "lcov.info").write_text(LCOV, encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("lcov", result["evidence"]["adapterResults"][0]["evidence"]["parser"])
        values = {item["metricKey"]: item["value"] for item in result["evidence"]["measurements"]}
        self.assertEqual(1, values["coverage.covered_lines"])
        self.assertEqual(2, values["coverage.total_branches"])

    def test_cobertura_method_lines_are_not_double_counted_and_zero_branch_summary_is_unavailable(self) -> None:
        (self.root / "coverage.xml").write_text(COBERTURA_METHOD_DUPLICATES, encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        values = {item["metricKey"]: item for item in result["evidence"]["measurements"]}
        self.assertEqual("cobertura-xml", result["evidence"]["adapterResults"][0]["evidence"]["parser"])
        self.assertEqual(50.0, values["coverage.line_coverage"]["value"])
        self.assertIsNone(values["coverage.branch_coverage"]["value"])
        self.assertEqual("UNAVAILABLE", values["coverage.branch_coverage"]["availability"])

    def test_xccov_json_is_supported_with_explicit_unavailable_branch_coverage(self) -> None:
        report = self.root / "coverage.json"
        report.write_text(XCCOV, encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        adapter = result["evidence"]["adapterResults"][0]
        values = {item["metricKey"]: item for item in result["evidence"]["measurements"]}
        self.assertEqual("xccov-json", adapter["evidence"]["parser"])
        self.assertEqual("json", adapter["evidence"]["sourceFormat"])
        self.assertEqual(75.0, values["coverage.line_coverage"]["value"])
        self.assertEqual("UNAVAILABLE", values["coverage.branch_coverage"]["availability"])

    def test_cobertura_root_branch_summary_is_authoritative(self) -> None:
        (self.root / "coverage.xml").write_text(COBERTURA_ROOT_BRANCH_SUMMARY, encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        values = {item["metricKey"]: item for item in result["evidence"]["measurements"]}
        self.assertEqual(75.0, values["coverage.branch_coverage"]["value"])

    def test_missing_coverage_is_available_as_explicit_unavailable_evidence(self) -> None:
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        metrics = result["evidence"]["measurements"]
        self.assertTrue(all(item["availability"] == "UNAVAILABLE" and item["value"] is None for item in metrics))

    def test_corrupt_coverage_fails_closed(self) -> None:
        (self.root / "coverage.xml").write_text("<coverage><line", encoding="utf-8")
        code, result = self.assess()
        self.assertEqual(ExitCode.FAILED_CLOSED, code)
        self.assertEqual("FAILED_CLOSED", result["evidence"]["capabilityResults"][0]["status"])

    def test_policy_threshold_uses_coverage_without_runtime_specific_policy_logic(self) -> None:
        (self.root / "coverage.xml").write_text(COBERTURA, encoding="utf-8")
        policy = {"identifier": "coverage-policy", "version": "1.0.0", "scope": "repository", "owner": "tests", "description": "coverage threshold", "supportedCapabilities": ["coverage"], "supportedSchemas": ["1.0.0"], "supportedRuntimeVersions": ["1.1.1"], "rules": [{"id": "minimum-line-coverage", "type": "threshold", "capability": "coverage", "metric": "coverage.line_coverage", "operator": "less_than", "threshold": {"warning": 80, "blocking": 60}, "severity": {"warning": "WARNING", "blocking": "BLOCKING"}, "enabled": True, "rationale": "coverage floor"}]}
        path = self.root / "policy.json"; path.write_text(json.dumps(policy), encoding="utf-8")
        code, result = self.invoke("--policy", str(path), "assess", "--capability", "coverage", str(self.root))
        self.assertEqual(ExitCode.FAILED, code)
        self.assertEqual("FAIL", result["evidence"]["assessmentDecision"]["decision"])

    def test_differential_includes_coverage(self) -> None:
        (self.root / "coverage.xml").write_text(COBERTURA, encoding="utf-8")
        code, _ = self.invoke("baseline", "--name", "coverage", "--capability", "coverage", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        improved = COBERTURA.replace('line-rate="0.5"', 'line-rate="1"').replace('branch-rate="0.5"', 'branch-rate="1"').replace('hits="0"', 'hits="1"').replace('(1/2)', '(2/2)')
        (self.root / "coverage.xml").write_text(improved, encoding="utf-8")
        code, result = self.invoke("assess", "--baseline", "coverage", "--capability", "coverage", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("coverage", result["differentialEvidence"]["capabilityDeltas"][0]["capabilityId"])
