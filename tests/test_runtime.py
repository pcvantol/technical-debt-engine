from __future__ import annotations

import tempfile
import unittest
import subprocess
from pathlib import Path

from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.registries import AdapterRegistry, CapabilityRegistry


class RuntimeFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_runtime_initializes_with_registered_code_size_capability(self) -> None:
        runtime = Runtime()
        self.assertEqual("code_size", runtime._capability_registry.discover()[0]["id"])
        self.assertEqual("code_size.cloc", runtime._adapter_registry.discover()[0]["id"])

    def test_pipeline_executes_all_generic_stages(self) -> None:
        result = Runtime().execute(self.root)
        self.assertEqual(14, len(result.stages))
        self.assertEqual("BLOCKED", next(stage for stage in result.stages if stage.identifier == "pipeline-execution").status.value)
        self.assertEqual("BLOCKED", next(stage for stage in result.stages if stage.identifier == "validation").status.value)
        self.assertEqual("execution-planning", result.stages[5].identifier)

    def test_qualification_consumes_policy_evidence(self) -> None:
        result = Runtime().execute(self.root)
        policy_stage = next(stage for stage in result.stages if stage.identifier == "policy-evaluation")
        qualification_stage = next(stage for stage in result.stages if stage.identifier == "qualification")
        self.assertEqual(policy_stage.outputs["decision"], qualification_stage.outputs["policyDecision"])
        self.assertEqual(policy_stage.outputs, result.evidence["policyEvidence"])
        self.assertEqual(policy_stage.outputs["decision"], result.evidence["assessmentDecision"]["decision"])
        self.assertTrue(result.evidence["assessmentDecision"]["assessmentId"].startswith("assessment."))
        self.assertEqual(result.evidence["policyEvidence"]["policyConfiguration"],
                         result.evidence["assessmentDecision"]["policyConfiguration"])

    def test_assessment_evidence_references_capability_executions(self) -> None:
        configuration = RuntimeConfiguration.load({"capabilities": {"code_size": {"enabled": True}, "complexity": {"enabled": True}},
                                                   "assessment": {"profile": "default", "capabilities": ["code_size", "complexity"]}})
        assessment = Runtime().execute(self.root, configuration).evidence["assessment"]
        self.assertEqual("default", assessment["profile"])
        self.assertEqual(["code_size", "complexity"], assessment["executionPlan"]["plannedCapabilities"])
        self.assertEqual({"code_size", "complexity"}, {item["capability"] for item in assessment["capabilityExecutions"]})
        self.assertTrue(all(item["capabilityEvidenceId"].startswith("sha256:") for item in assessment["capabilityExecutions"]))

    def test_policy_override_can_block_a_measurement(self) -> None:
        (self.root / "sample.py").write_text("value = 1\n", encoding="utf-8")
        configuration = RuntimeConfiguration.load({
            "capabilities": {"code_size": {"enabled": True}},
            "policy": {"overrides": {"code_size.repository_lines": {"warning": 0, "blocking": 0}}},
        })
        result = Runtime().execute(self.root, configuration)
        qualification = next(stage for stage in result.stages if stage.identifier == "qualification")
        self.assertEqual("FAIL", qualification.outputs["status"])

    def test_context_contains_canonical_runtime_values(self) -> None:
        result = Runtime().execute(self.root)
        self.assertEqual("1.0.0rc1", result.context.runtime_version)
        self.assertEqual("1.0.0", result.context.schema_version)
        self.assertTrue(result.context.execution_id.startswith("execution."))
        self.assertEqual("content_digest", result.context.candidate["identityType"])

    def test_repository_identity_is_independent_of_checkout_path(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            for directory in (Path(first), Path(second)):
                (directory / "sample.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.assertEqual(Runtime._repository_digest(Path(first)), Runtime._repository_digest(Path(second)))

    def test_repository_identity_normalizes_windows_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            (Path(first) / "sample.py").write_bytes(b"VALUE = 1\n")
            (Path(second) / "sample.py").write_bytes(b"VALUE = 1\r\n")
            self.assertEqual(Runtime._repository_digest(Path(first)), Runtime._repository_digest(Path(second)))

    def test_repository_digest_ignores_generated_dependency_artifacts(self) -> None:
        (self.root / "sample.py").write_text("VALUE = 1\n", encoding="utf-8")
        original = Runtime._repository_digest(self.root)
        generated = self.root / ".xcode-derived-build" / "Build"
        generated.mkdir(parents=True)
        (generated / "generated.bin").write_bytes(b"generated output")
        (self.root / ".build").mkdir()
        (self.root / ".build" / "manifest.db").write_bytes(b"generated output")
        (self.root / "obj").mkdir()
        (self.root / "obj" / "generated.dll.s").write_bytes(b"generated output")
        (self.root / "bin").mkdir()
        (self.root / "bin" / "generated.dll.s").write_bytes(b"generated output")
        self.assertEqual(original, Runtime._repository_digest(self.root))

    def test_repository_identity_uses_git_origin_across_checkouts(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            for directory in (Path(first), Path(second)):
                subprocess.run(["git", "init", "--quiet", str(directory)], check=True)
                subprocess.run(["git", "-C", str(directory), "remote", "add", "origin", "https://github.com/example/tde.git"], check=True)
            self.assertEqual(Runtime._repository_identity(Path(first)), Runtime._repository_identity(Path(second)))

    def test_default_and_invalid_configuration(self) -> None:
        configuration = RuntimeConfiguration.load()
        self.assertEqual("1.0.0", configuration.schema_version)
        with self.assertRaises(ValueError):
            RuntimeConfiguration.load({"capabilities": ["code_size"]})
        with self.assertRaises(ValueError):
            RuntimeConfiguration.load({"schemaVersion": "2.0.0"})

    def test_runtime_evidence_has_no_capabilities_or_adapters(self) -> None:
        evidence = Runtime().execute(self.root).evidence
        self.assertEqual("tde.evidence", evidence["schemaId"])
        self.assertEqual([], evidence["capabilityResults"])
        self.assertEqual([], evidence["measurements"])
        self.assertEqual([], evidence["findings"])
        self.assertEqual("VALID", evidence["validation"]["status"])

    def test_runtime_validation_and_qualification_are_ready(self) -> None:
        result = Runtime().execute(self.root)
        self.assertEqual("VALID", result.validation["status"])
        self.assertEqual("RUNTIME_FAILED", result.qualification.value)
        self.assertEqual("RUNTIME_READY", result.report["runtimeSummary"]["status"])

    def test_registries_discover_code_size_without_runtime_branching(self) -> None:
        self.assertEqual("code_size", CapabilityRegistry().discover()[0]["id"])
        self.assertEqual("code_size.cloc", AdapterRegistry().discover()[0]["id"])


if __name__ == "__main__":
    unittest.main()
