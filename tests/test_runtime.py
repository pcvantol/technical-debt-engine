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

    def test_runtime_initializes_with_empty_registries(self) -> None:
        runtime = Runtime()
        self.assertEqual((), runtime._capability_registry.discover())
        self.assertEqual((), runtime._adapter_registry.discover())

    def test_pipeline_executes_all_generic_stages(self) -> None:
        result = Runtime().execute(self.root)
        self.assertEqual(13, len(result.stages))
        self.assertTrue(all(stage.status.value == "SUCCESS" for stage in result.stages))
        self.assertEqual("execution-planning", result.stages[5].identifier)

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

    def test_registries_remain_empty(self) -> None:
        self.assertEqual((), CapabilityRegistry().discover())
        self.assertEqual((), AdapterRegistry().discover())


if __name__ == "__main__":
    unittest.main()
