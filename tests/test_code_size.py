from __future__ import annotations

import json
from io import StringIO
import tempfile
import unittest
from pathlib import Path

from tde_cli.main import ExitCode, main
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.code_size import classify


class CodeSizeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "src").mkdir(); (self.root / "tests").mkdir(); (self.root / "docs").mkdir(); (self.root / "vendor").mkdir()
        (self.root / "src" / "app.py").write_text("# comment\nvalue = 1\n", encoding="utf-8")
        (self.root / "tests" / "test_app.py").write_text("def test_value():\n    assert 1 == 1\n", encoding="utf-8")
        (self.root / "docs" / "readme.md").write_text("# Documentation\n", encoding="utf-8")
        (self.root / "vendor" / "library.py").write_text("x = 1\n", encoding="utf-8")

    def tearDown(self) -> None: self.directory.cleanup()

    def test_classification_is_deterministic(self) -> None:
        self.assertEqual("TEST", classify("tests/test_app.py")); self.assertEqual("VENDOR", classify("vendor/lib.py")); self.assertEqual("DOCUMENTATION", classify("docs/a.md")); self.assertEqual("SOURCE", classify("src/app.py"))

    def test_runtime_produces_code_size_evidence(self) -> None:
        configuration = RuntimeConfiguration.load({"capabilities": {"code_size": {"enabled": True}}})
        evidence = Runtime().execute(self.root, configuration).evidence
        self.assertEqual("VALID", evidence["capabilityResults"][0]["status"])
        self.assertTrue(any(item["metricKey"] == "code_size.code_lines" for item in evidence["measurements"]))
        self.assertEqual("cloc", evidence["capabilityResults"][0]["adapterIds"][0].split(".")[-1])

    def test_cli_assess_emits_canonical_evidence_fields(self) -> None:
        stream = StringIO(); code = main(["--format", "json", "assess", "--capability", "code-size", str(self.root)], stream)
        self.assertEqual(ExitCode.SUCCESS, code)
        response = json.loads(stream.getvalue())
        self.assertEqual("RUNTIME_READY", response["runtime"]["status"])

    def test_assess_without_code_size_is_not_supported(self) -> None:
        self.assertEqual(ExitCode.NOT_SUPPORTED, main(["assess", str(self.root)], StringIO()))
