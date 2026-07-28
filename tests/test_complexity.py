from __future__ import annotations
from io import StringIO
import json
import tempfile, unittest
from unittest.mock import patch
from pathlib import Path
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.code_size import analyze as analyze_code_size
from tde_runtime.complexity import _portable_native_output, analyze, classify_path
from tde_cli.main import ExitCode, main

class ComplexityTests(unittest.TestCase):
    def test_classifies_product_test_fixture_and_verification_symbols(self):
        self.assertEqual("PRODUCT_SOURCE", classify_path("src/djconnect/service.py"))
        self.assertEqual("TEST", classify_path("tests/test_service.py"))
        self.assertEqual("FIXTURE", classify_path("tests/fixtures/sample.py"))
        self.assertEqual("VERIFICATION", classify_path("scripts/validate_release.py"))

    def test_python_complexity_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n",encoding="utf-8")
            config=RuntimeConfiguration.load({"capabilities":{"complexity":{"enabled":True}}})
            evidence=Runtime().execute(root,config).evidence
            self.assertEqual("complexity",evidence["capabilityResults"][0]["capabilityId"])
            self.assertTrue(evidence["measurements"])

    def test_normalizes_repository_language_file_and_symbol_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n",encoding="utf-8")
            evidence=Runtime().execute(root, RuntimeConfiguration.load({"capabilities":{"complexity":{"enabled":True}}})).evidence
            scopes={item["scope"] for item in evidence["measurements"]}
            self.assertTrue({"repository", "repository_product", "language", "file", "symbol"}.issubset(scopes))
            self.assertTrue(any(item["metricKey"] == "complexity.cyclomatic.distribution" for item in evidence["measurements"]))
            self.assertTrue(any(item["metricKey"] == "complexity.cyclomatic.product.maximum" for item in evidence["measurements"]))
            adapter=evidence["adapterResults"][0]
            self.assertEqual("radon",adapter["analyzer"]["id"]); self.assertTrue(adapter["rawOutputHash"].startswith("sha256:"))

    def test_thresholds_create_canonical_finding(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(a,b,c):\n    if a: pass\n    if b: pass\n    if c: pass\n",encoding="utf-8")
            config=RuntimeConfiguration.load({"capabilities":{"complexity":{"enabled":True,"thresholds":{"high":2,"veryHigh":4,"critical":6}}}})
            findings=Runtime().execute(root,config).evidence["findings"]
            self.assertTrue(findings); self.assertEqual("complexity.very_high",findings[0]["ruleId"])
            self.assertTrue(findings[0]["evidenceReferences"])
            self.assertEqual("PRODUCT_SOURCE", findings[0]["classification"])

    def test_default_policy_keeps_critical_test_complexity_visible_without_blocking_product_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sample.py").write_text("def branch(value):\n    return value\n", encoding="utf-8")
            tests = root / "tests"
            tests.mkdir()
            branches = "".join(f"    if value == {index}:\n        return {index}\n" for index in range(41))
            (tests / "test_complex_harness.py").write_text(
                "def harness(value):\n" + branches + "    return -1\n", encoding="utf-8"
            )
            evidence = Runtime().execute(root, RuntimeConfiguration.load({"capabilities": {"complexity": {"enabled": True}}})).evidence
            critical = [item for item in evidence["findings"] if item["severity"] == "CRITICAL"]
            self.assertTrue(critical)
            self.assertTrue(all(item["classification"] == "TEST" for item in critical))
            self.assertEqual("PASS", evidence["assessmentDecision"]["decision"])

    def test_missing_analyzer_and_unsupported_version_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch("tde_runtime.analyzer_discovery.shutil.which",return_value=None):
                self.assertEqual("ANALYZER_NOT_FOUND",analyze(root)["status"])
            with patch("tde_runtime.analyzer_discovery.shutil.which",return_value="radon"), patch("tde_runtime.analyzer_discovery.subprocess.run") as run:
                run.return_value.stdout="5.0.0"
                self.assertEqual("analyzer.radon.unsupported_version",analyze(root)["limitations"][0]["id"])

    def test_native_output_is_relative_and_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, normalized = _portable_native_output(root, {str(root / "nested" / "sample.py"): []})
            self.assertEqual({"nested/sample.py": []}, normalized)
            self.assertNotIn(str(root), raw)
            self.assertEqual("nested/sample.py", _portable_native_output(root, {"nested/sample.py": []})[1].popitem()[0])

    def test_configuration_discovery_persistence_query_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n",encoding="utf-8")
            (root/".tde.yml").write_text("capabilities:\n  complexity:\n    enabled: true\n    thresholds:\n      high: 2\n      veryHigh: 4\n      critical: 6\n",encoding="utf-8")
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","json","assess","--capability","complexity",str(root)],stream))
            assessment=json.loads(stream.getvalue()); self.assertEqual("QUALIFIED",assessment["runtimeQualification"]["level"])
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","json","query",str(root),"--resource","findings"],stream)); self.assertGreater(json.loads(stream.getvalue())["queryEvidence"]["resultCount"],0)
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","markdown","report","--capability","complexity",str(root)],stream)); self.assertIn("# Complexity Report",stream.getvalue())
