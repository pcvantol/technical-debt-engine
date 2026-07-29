from __future__ import annotations
from io import StringIO
import json
import tempfile, unittest
from unittest.mock import patch
from pathlib import Path
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.code_size import analyze as analyze_code_size
from tde_runtime.complexity import _lizard, _portable_native_output, analyze, classify_path
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
            (root / "sample.py").write_text("def sample():\n    return 1\n", encoding="utf-8")
            with patch("tde_runtime.complexity.discover", return_value={"status": "ANALYZER_NOT_FOUND", "limitation": {"id": "analyzer.radon.unavailable", "description": "radon unavailable", "cause": "analyzer unavailable"}}):
                self.assertEqual("ANALYZER_NOT_FOUND",analyze(root)["status"])
            with patch("tde_runtime.complexity.discover", return_value={"status": "ANALYZER_NOT_FOUND", "limitation": {"id": "analyzer.radon.unsupported_version", "description": "unsupported", "cause": "unsupported analyzer version"}}):
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

    def test_lizard_normalizes_typescript_symbols_with_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"; source.mkdir()
            target = source / "service.ts"
            target.write_text("export function branch(value: boolean) { if (value) return 1; return 0; }\n", encoding="utf-8")
            native = f'1,2,12,1,1,"branch@1@{target}","{target}",branch,"branch(value: boolean)",1,1\n'
            with patch("tde_runtime.complexity.discover", return_value={"status": "VALID", "executable": "lizard", "version": "1.23.0"}), \
                 patch("tde_runtime.complexity.subprocess.run") as run:
                run.return_value.stdout = native
                result = _lizard(root, [target], ("TypeScript",), 10)
            self.assertEqual("VALID", result["status"])
            self.assertEqual("TypeScript", result["symbols"][0]["language"])
            self.assertEqual(2, result["symbols"][0]["complexity"])
            self.assertEqual("complexity.lizard", result["symbols"][0]["adapterId"])
            self.assertEqual("lizard==1.23.0", result["adapter"]["analyzer"]["package"])

    def test_lizard_ignores_synthetic_csharp_file_statistics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "Program.cs"
            target.write_text("class Program {}\n", encoding="utf-8")
            native = (
                f'116,1,117,0,1372,"*global*@0-1371@{target}","{target}",*global*,*global*,0,1371\n'
                f'4,2,20,0,5,"Branch@2-6@{target}","{target}",Branch,Branch(),2,6\n'
            )
            with patch("tde_runtime.complexity.discover", return_value={"status": "VALID", "executable": "lizard", "version": "1.23.0"}), \
                 patch("tde_runtime.complexity.subprocess.run") as run:
                run.return_value.stdout = native
                result = _lizard(root, [target], ("C#",), 10)
            self.assertEqual("VALID", result["status"])
            self.assertEqual(["Branch"], [symbol["name"] for symbol in result["symbols"]])

    def test_identical_analyzer_symbols_are_normalized_but_conflicts_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Program.cs").write_text("class Program {}\n", encoding="utf-8")
            base = {"path": "Program.cs", "classification": "PRODUCT_SOURCE", "language": "C#", "name": "Branch", "type": "function", "line": 2, "endLine": 6, "complexity": 2, "adapterId": "complexity.lizard", "toolId": "lizard"}
            adapter = {"id": "complexity.lizard", "version": "1.1.1", "analyzer": {"id": "lizard", "version": "1.23.0"}, "rawOutput": "", "rawOutputHash": "sha256:test"}
            with patch("tde_runtime.complexity._lizard", return_value={"status": "VALID", "symbols": [base, dict(base)], "adapter": adapter}):
                valid = analyze(root)
            self.assertEqual("VALID", valid["status"])
            self.assertEqual(1, len(valid["symbols"]))
            conflicting = dict(base, complexity=3)
            with patch("tde_runtime.complexity._lizard", return_value={"status": "VALID", "symbols": [base, conflicting], "adapter": adapter}):
                invalid = analyze(root)
            self.assertEqual("INVALID_EVIDENCE", invalid["status"])
            self.assertEqual("complexity.symbol.duplicate", invalid["limitations"][0]["id"])

    def test_primary_language_prevents_auxiliary_python_from_qualifying_csharp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Program.cs").write_text("class Program {\n  static int Branch(bool value) {\n    if (value) return 1;\n    return 0;\n  }\n}\n", encoding="utf-8")
            (root / "tools").mkdir()
            (root / "tools" / "helper.py").write_text("def branch(value): return 1\n", encoding="utf-8")
            with patch("tde_runtime.complexity._lizard") as lizard:
                lizard.return_value = {"status": "VALID", "symbols": [{"path": "Program.cs", "classification": "PRODUCT_SOURCE", "language": "C#", "name": "Branch", "type": "function", "line": 1, "endLine": 1, "complexity": 2, "adapterId": "complexity.lizard", "toolId": "lizard"}], "adapter": {"id": "complexity.lizard", "version": "1.1.0", "analyzer": {"id": "lizard", "version": "1.23.0"}, "rawOutput": "", "rawOutputHash": "sha256:test"}}
                result = analyze(root)
            self.assertEqual(["C#"], result["primaryLanguages"])
            self.assertEqual(["C#"], sorted({symbol["language"] for symbol in result["symbols"]}))

    def test_coverage_and_generated_paths_do_not_contaminate_complexity_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text("def app():\n    return 1\n", encoding="utf-8")
            (root / "coverage").mkdir(); (root / "coverage" / "generated.py").write_text("def generated():\n    return 1\n", encoding="utf-8")
            (root / "verification").mkdir(); (root / "verification" / "verify.py").write_text("def verify():\n    return 1\n", encoding="utf-8")
            with patch("tde_runtime.complexity._radon") as radon:
                radon.return_value = {"status": "VALID", "symbols": [{"path": "app.py", "classification": "PRODUCT_SOURCE", "language": "Python", "name": "app", "type": "function", "line": 1, "endLine": 2, "complexity": 1, "adapterId": "complexity.radon", "toolId": "radon"}], "adapter": {"id": "complexity.radon", "version": "1.1.0", "analyzer": {"id": "radon", "version": "6.0.1"}, "rawOutput": "{}", "rawOutputHash": "sha256:test"}}
                result = analyze(root)
            supplied = [path.relative_to(root).as_posix() for path in radon.call_args.args[1]]
            self.assertEqual(["app.py"], supplied)
            self.assertEqual("VALID", result["status"])
