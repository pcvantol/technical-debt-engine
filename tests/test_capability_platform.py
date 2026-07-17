from __future__ import annotations

import unittest

from tde_runtime.registries import AdapterRegistry


class CapabilityPlatformTests(unittest.TestCase):
    def test_selection_is_priority_ordered_and_reproducible(self) -> None:
        class MultipleAdapters(AdapterRegistry):
            def discover(self):
                return (
                    {"id": "code_size.alt", "capabilities": ("code_size",), "priority": 10},
                    {"id": "code_size.primary", "capabilities": ("code_size",), "priority": 20},
                )
        capability = {"id": "code_size", "supportedAnalyzers": ("code_size.alt", "code_size.primary")}
        self.assertEqual("code_size.primary", MultipleAdapters().select(capability)["id"])

    def test_selection_requires_mutual_capability_binding(self) -> None:
        capability = {"id": "code_size", "supportedAnalyzers": ("complexity.radon",)}
        self.assertIsNone(AdapterRegistry().select(capability))
