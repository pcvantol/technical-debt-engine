from __future__ import annotations
import tempfile, unittest
from pathlib import Path
from tde_runtime import Runtime, RuntimeConfiguration

class ComplexityTests(unittest.TestCase):
    def test_python_complexity_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"sample.py").write_text("def branch(value):\n    if value:\n        return 1\n    return 0\n",encoding="utf-8")
            config=RuntimeConfiguration.load({"capabilities":{"complexity":{"enabled":True}}})
            evidence=Runtime().execute(root,config).evidence
            self.assertEqual("complexity",evidence["capabilityResults"][0]["capabilityId"])
            self.assertTrue(evidence["measurements"])
