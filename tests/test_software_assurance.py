import tempfile, unittest
from pathlib import Path
from tde_runtime.software_assurance import SoftwareAssurance
class SoftwareAssuranceTests(unittest.TestCase):
 def test_missing_required_sources_fail_closed(self):
  with tempfile.TemporaryDirectory() as root:
   self.assertEqual("FAIL",SoftwareAssurance().assure(root)["qualification"])
