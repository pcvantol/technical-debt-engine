from __future__ import annotations

import json
from io import StringIO
import tempfile
import unittest
import os
import shutil
import subprocess
import sys
from unittest.mock import patch
from pathlib import Path

from tde_cli.main import ExitCode, main
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.code_size import analyze, classify


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
        self.assertTrue(evidence["adapterResults"][0]["rawOutputHash"].startswith("sha256:"))
        self.assertTrue(any(item["scope"] == "language" for item in evidence["measurements"]))
        self.assertTrue(any(item["scope"] == "file" for item in evidence["measurements"]))

    def test_evidence_digest_is_stable_for_same_repository_and_configuration(self) -> None:
        configuration = RuntimeConfiguration.load({"capabilities": {"code_size": {"enabled": True}}})
        first = Runtime().execute(self.root, configuration).evidence["integrity"]["contentDigest"]
        second = Runtime().execute(self.root, configuration).evidence["integrity"]["contentDigest"]
        self.assertEqual(first, second)

    def test_missing_analyzer_blocks_without_fabricated_metrics(self) -> None:
        with patch("tde_runtime.analyzer_discovery.shutil.which", return_value=None):
            result = analyze(self.root)
        self.assertEqual("ANALYZER_NOT_FOUND", result["status"])
        self.assertIn("analyzer.cloc.unavailable", result["limitations"][0]["id"])

    def test_unsupported_analyzer_version_blocks(self) -> None:
        with patch("tde_runtime.analyzer_discovery.shutil.which", return_value="/tools/cloc"), \
             patch("tde_runtime.analyzer_discovery.subprocess.run") as run:
            run.return_value.stdout = "2.09"
            result = analyze(self.root)
        self.assertEqual("ANALYZER_NOT_FOUND", result["status"])
        self.assertEqual("analyzer.cloc.unsupported_version", result["limitations"][0]["id"])

    def test_analyzer_timeout_is_a_structured_blocker(self) -> None:
        with patch("tde_runtime.code_size.discover", return_value={"status": "VALID", "executable": "/tools/cloc", "version": "2.10"}), \
             patch("tde_runtime.code_size.subprocess.run", side_effect=subprocess.TimeoutExpired(["cloc"], 1)):
            result = analyze(self.root, timeout=1)
        self.assertEqual("FAILED_CLOSED", result["status"])
        self.assertEqual("analyzer.cloc.failed", result["limitations"][0]["id"])

    def test_cli_assess_emits_canonical_evidence_fields(self) -> None:
        stream = StringIO(); code = main(["--format", "json", "assess", "--capability", "code_size", str(self.root)], stream)
        self.assertEqual(ExitCode.SUCCESS, code)
        response = json.loads(stream.getvalue())
        self.assertEqual("RUNTIME_READY", response["runtime"]["status"])
        self.assertEqual(1, response["execution"]["workItems"])
        self.assertEqual(["code_size"], response["evidence"]["executionEvidence"]["executedCapabilities"])
        self.assertTrue(any(item["metricKey"] == "code_size.code_lines" for item in response["evidence"]["measurements"]))
        self.assertEqual("QUALIFIED", response["runtimeQualification"]["level"])

    def test_cli_assess_does_not_require_a_git_repository(self) -> None:
        stream = StringIO()
        code = main(["--format", "json", "assess", "--capability", "code-size", str(self.root)], stream)
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("QUALIFIED", json.loads(stream.getvalue())["runtimeQualification"]["level"])

    def test_cli_assess_accepts_a_dirty_git_repository(self) -> None:
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        (self.root / "src" / "dirty.py").write_text("value = 2\n", encoding="utf-8")
        stream = StringIO()
        code = main(["--format", "json", "assess", "--capability", "code-size", str(self.root)], stream)
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("QUALIFIED", json.loads(stream.getvalue())["runtimeQualification"]["level"])

    @unittest.skipUnless(shutil.which("cloc"), "installed CLI integration requires cloc on PATH")
    def test_installed_wheel_assess_executes_code_size(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            environment = temporary_root / "venv"
            wheel_directory = temporary_root / "wheel"
            child_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, env=child_environment)
            executable_directory = environment / ("Scripts" if os.name == "nt" else "bin")
            pip = executable_directory / ("pip.exe" if os.name == "nt" else "pip")
            tde = executable_directory / ("tde.exe" if os.name == "nt" else "tde")
            subprocess.run([str(pip), "wheel", "--no-deps", "--wheel-dir", str(wheel_directory), str(repository)], check=True, capture_output=True, text=True, env=child_environment)
            wheel = next(wheel_directory.glob("technical_debt_engine_runtime-*.whl"))
            subprocess.run([str(pip), "install", "--no-deps", str(wheel)], check=True, capture_output=True, text=True, env=child_environment)
            self.assertTrue(tde.is_file(), "wheel installation did not create the tde console script")
            store = temporary_root / "evidence"
            completed = subprocess.run([str(tde), "--format", "json", "--store-location", str(store), "assess", "--capability", "code-size", str(self.root)], check=False, capture_output=True, text=True, env=child_environment)
            self.assertEqual(ExitCode.SUCCESS, completed.returncode, completed.stderr)
            response = json.loads(completed.stdout)
            self.assertEqual(1, response["execution"]["workItems"])
            self.assertEqual(["code_size"], response["evidence"]["executionEvidence"]["executedCapabilities"])
            self.assertTrue((store / "evidence").is_dir())
            queried = subprocess.run([str(tde), "--format", "json", "--store-location", str(store), "query", str(self.root), "--resource", "metrics"], check=False, capture_output=True, text=True, env=child_environment)
            self.assertEqual(ExitCode.SUCCESS, queried.returncode, queried.stderr)
            self.assertGreater(json.loads(queried.stdout)["queryEvidence"]["resultCount"], 0)
            reported = subprocess.run([str(tde), "--format", "markdown", "--store-location", str(store), "report", "--capability", "code-size", str(self.root)], check=False, capture_output=True, text=True, env=child_environment)
            self.assertEqual(ExitCode.SUCCESS, reported.returncode, reported.stderr)
            self.assertIn("# Code Size Report", reported.stdout)

    def test_assess_without_capability_runs_the_default_profile(self) -> None:
        stream = StringIO()
        self.assertEqual(ExitCode.SUCCESS, main(["--format", "json", "assess", str(self.root)], stream))
        evidence = json.loads(stream.getvalue())["evidence"]
        self.assertEqual(["code_size", "complexity"], evidence["assessment"]["executionPlan"]["plannedCapabilities"])
        self.assertEqual("standard", evidence["assessment"]["profile"])

    def test_unknown_capability_is_resolved_by_runtime(self) -> None:
        stream = StringIO()
        code = main(["--format", "json", "assess", "--capability", "not_a_capability", str(self.root)], stream)
        response = json.loads(stream.getvalue())
        self.assertEqual(ExitCode.NOT_SUPPORTED, code)
        self.assertEqual("NOT_SUPPORTED", response["evidence"]["capabilityResults"][0]["status"])
        self.assertEqual(["not_a_capability"], response["evidence"]["executionEvidence"]["unsupportedCapabilities"])

    def test_policy_decision_controls_successful_execution_exit_code(self) -> None:
        stream = StringIO()
        code = main(["--format", "json", "--policy-override", 'code_size.repository_lines={"warning":0,"blocking":0}', "assess", "--capability", "code_size", str(self.root)], stream)
        self.assertEqual(ExitCode.FAILED, code)
        self.assertEqual("FAIL", json.loads(stream.getvalue())["evidence"]["assessmentDecision"]["decision"])
