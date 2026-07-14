import tempfile, unittest
from tde_runtime import Runtime
from tde_runtime.runtime_qualification import RuntimeQualificationEngine
class RuntimeQualificationTests(unittest.TestCase):
 def test_qualified_and_unsupported(self):
  with tempfile.TemporaryDirectory() as root:
   evidence=Runtime().execute(root).evidence
   self.assertEqual("QUALIFIED",RuntimeQualificationEngine().qualify(evidence)["level"])
   self.assertEqual("NOT_SUPPORTED",RuntimeQualificationEngine().qualify(evidence,"missing")["level"])
