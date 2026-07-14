from __future__ import annotations

import tempfile
import unittest
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
        self.assertTrue(all(stage.status.value == "SUCCESS" for stage in result.stages))
        self.assertEqual("execution-planning", result.stages[5].identifier)

    def test_qualification_consumes_policy_evidence(self) -> None:
        result = Runtime().execute(self.root)
        policy_stage = next(stage for stage in result.stages if stage.identifier == "policy-evaluation")
        qualification_stage = next(stage for stage in result.stages if stage.identifier == "qualification")
        self.assertEqual(policy_stage.outputs["decision"], qualification_stage.outputs["policyDecision"])
        self.assertEqual(policy_stage.outputs, result.evidence["policyEvidence"])

    def test_policy_override_can_block_a_measurement(self) -> None:
        (self.root / "requirements.txt").write_text("example==1.0\n", encoding="utf-8")
        configuration = RuntimeConfiguration.load({
            "capabilities": {"dependency_health": {"enabled": True}},
            "policy": {"overrides": {"dependency.count": {"warning": 0, "blocking": 0}}},
        })
        result = Runtime().execute(self.root, configuration)
        qualification = next(stage for stage in result.stages if stage.identifier == "qualification")
        self.assertEqual("BLOCKED", qualification.outputs["status"])

    def test_context_contains_canonical_runtime_values(self) -> None:
        result = Runtime().execute(self.root)
        self.assertEqual("0.1.0", result.context.runtime_version)
        self.assertEqual("1.0.0", result.context.schema_version)
        self.assertTrue(result.context.execution_id.startswith("execution."))
        self.assertEqual("content_digest", result.context.candidate["identityType"])

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
        self.assertEqual("RUNTIME_READY", result.qualification.value)
        self.assertEqual("RUNTIME_READY", result.report["runtimeSummary"]["status"])

    def test_registries_discover_code_size_without_runtime_branching(self) -> None:
        self.assertEqual("code_size", CapabilityRegistry().discover()[0]["id"])
        self.assertEqual("code_size.cloc", AdapterRegistry().discover()[0]["id"])


if __name__ == "__main__":
    unittest.main()
