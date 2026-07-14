import tempfile, unittest
from pathlib import Path
from tde_runtime import Runtime
from tde_runtime.trusted_delivery import TrustedDelivery
class TrustedDeliveryTests(unittest.TestCase):
 def test_missing_git_candidate_fails_closed(self):
  with tempfile.TemporaryDirectory() as root:
   evidence=Runtime().execute(root).evidence
   self.assertEqual("FAIL",TrustedDelivery().validate(root,evidence)["qualification"])
