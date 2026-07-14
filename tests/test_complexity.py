from __future__ import annotations
from io import StringIO
import json
import tempfile, unittest
from unittest.mock import patch
from pathlib import Path
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.code_size import analyze as analyze_code_size
from tde_runtime.complexity import analyze
from tde_cli.main import ExitCode, main

class ComplexityTests(unittest.TestCase):
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
            self.assertTrue({"repository","language","file","symbol"}.issubset(scopes))
            self.assertTrue(any(item["metricKey"] == "complexity.cyclomatic.distribution" for item in evidence["measurements"]))
            adapter=evidence["adapterResults"][0]
            self.assertEqual("radon",adapter["analyzer"]["id"]); self.assertTrue(adapter["rawOutputHash"].startswith("sha256:"))

    def test_thresholds_create_canonical_finding(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(a,b,c):\n    if a: pass\n    if b: pass\n    if c: pass\n",encoding="utf-8")
            config=RuntimeConfiguration.load({"capabilities":{"complexity":{"enabled":True,"thresholds":{"high":2,"veryHigh":4,"critical":6}}}})
            findings=Runtime().execute(root,config).evidence["findings"]
            self.assertTrue(findings); self.assertEqual("complexity.very_high",findings[0]["ruleId"])
            self.assertTrue(findings[0]["evidenceReferences"])

    def test_missing_analyzer_and_unsupported_version_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch("tde_runtime.complexity.shutil.which",return_value=None):
                self.assertEqual("BLOCKED",analyze(root)["status"])
            with patch("tde_runtime.complexity.shutil.which",return_value="radon"), patch("tde_runtime.complexity.subprocess.run") as run:
                run.return_value.stdout="5.0.0"
                self.assertEqual("analyzer.radon.unsupported_version",analyze(root)["limitations"][0]["id"])

    def test_configuration_discovery_persistence_query_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n",encoding="utf-8")
            (root/".tde.yml").write_text("capabilities:\n  complexity:\n    enabled: true\n    thresholds:\n      high: 2\n      veryHigh: 4\n      critical: 6\n",encoding="utf-8")
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","json","assess","--capability","complexity",str(root)],stream))
            assessment=json.loads(stream.getvalue()); self.assertEqual("QUALIFIED",assessment["runtimeQualification"]["level"])
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","json","query",str(root),"--resource","findings"],stream)); self.assertGreater(json.loads(stream.getvalue())["queryEvidence"]["resultCount"],0)
            stream=StringIO(); self.assertEqual(ExitCode.SUCCESS,main(["--format","markdown","report","--capability","complexity",str(root)],stream)); self.assertIn("# Complexity Report",stream.getvalue())
