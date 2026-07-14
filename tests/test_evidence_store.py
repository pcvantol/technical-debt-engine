import tempfile, unittest
from pathlib import Path
from tde_runtime import Runtime
from tde_runtime.evidence_store import EvidenceStore
class EvidenceStoreTests(unittest.TestCase):
 def test_persistence_is_immutable_and_history_is_ordered(self):
  with tempfile.TemporaryDirectory() as directory:
   store=EvidenceStore(Path(directory)); evidence=Runtime().execute(directory).evidence
   self.assertFalse(store.persist(evidence)["existing"]); self.assertTrue(store.persist(evidence)["existing"]); self.assertEqual(1,len(store.history()))
