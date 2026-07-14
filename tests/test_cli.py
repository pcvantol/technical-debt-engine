from __future__ import annotations

from io import StringIO
import json
import tempfile
import unittest
from pathlib import Path

from tde_cli.main import ExitCode, main


class CliFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str]:
        stream = StringIO()
        return main(list(arguments), stream), stream.getvalue()

    def test_top_level_help(self) -> None:
        code, output = self.invoke()
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertIn("validate", output)
        self.assertIn("assess", output)

    def test_help_command_is_available(self) -> None:
        code, output = self.invoke("help")
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertIn("commands", output)

    def test_command_help_is_available(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            main(["inspect", "--help"], StringIO())
        self.assertEqual(0, raised.exception.code)

    def test_version_includes_cli_runtime_schema_and_generation(self) -> None:
        code, output = self.invoke("--format", "json", "--version")
        self.assertEqual(ExitCode.SUCCESS, code)
        version = json.loads(output)
        self.assertEqual("0.1.0", version["cliVersion"])
        self.assertEqual("0.1.0", version["runtimeVersion"])
        self.assertEqual("1.0.0", version["schemaVersion"])
        self.assertEqual("1", version["generation"])

    def test_validate_invokes_runtime(self) -> None:
        code, output = self.invoke("--format", "json", "validate", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        response = json.loads(output)
        self.assertEqual("RUNTIME_READY", response["runtime"]["status"])
        self.assertEqual("VALID", response["validation"]["status"])

    def test_inspect_invokes_runtime(self) -> None:
        code, output = self.invoke("--format", "json", "inspect", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("inspect", json.loads(output)["command"])

    def test_unimplemented_command_returns_canonical_not_supported(self) -> None:
        code, output = self.invoke("--format", "json", "assess", str(self.root))
        self.assertEqual(ExitCode.NOT_SUPPORTED, code)
        self.assertEqual("NOT_IMPLEMENTED", json.loads(output)["status"])

    def test_invalid_configuration_blocks_execution(self) -> None:
        config = self.root / "invalid.tde.yml"
        config.write_text('{"schemaVersion": "2.0.0"}', encoding="utf-8")
        code, output = self.invoke("--format", "json", "--config", str(config), "validate", str(self.root))
        self.assertEqual(ExitCode.BLOCKED, code)
        self.assertEqual("BLOCKED", json.loads(output)["status"])

    def test_policy_override_is_accepted(self) -> None:
        code, output = self.invoke("--format", "json", "--policy-override", 'dependency.count={"warning":0,"blocking":0}', "inspect", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("NOT_APPLICABLE", json.loads(output)["qualification"]["status"])

    def test_baseline_and_compare_commands_are_operational(self) -> None:
        code, output = self.invoke("--format", "json", "baseline", str(self.root), "--name", "initial")
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("initial", json.loads(output)["baseline"]["baselineId"])
        code, output = self.invoke("--format", "json", "compare", str(self.root), "--baseline", "initial")
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("VALID", json.loads(output)["comparison"]["status"])

    def test_trend_command_is_operational(self) -> None:
        self.invoke("--format", "json", "baseline", str(self.root), "--name", "initial")
        code, output = self.invoke("--format", "json", "trend", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("rolling", json.loads(output)["trendEvidence"]["window"])

    def test_query_command_is_operational(self) -> None:
        code, output = self.invoke("--format", "json", "query", str(self.root), "--resource", "repositories")
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual(1, json.loads(output)["queryEvidence"]["resultCount"])

    def test_store_and_history_commands_are_operational(self) -> None:
        code, _ = self.invoke("--format", "json", "store", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        code, output = self.invoke("--format", "json", "history", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code); self.assertEqual(1, len(json.loads(output)["records"]))

    def test_run_command_is_operational(self) -> None:
        code, output = self.invoke("--format", "json", "run", str(self.root), "--capability", "dependency-health")
        self.assertEqual(ExitCode.SUCCESS, code); self.assertEqual("run", json.loads(output)["command"])


if __name__ == "__main__":
    unittest.main()
