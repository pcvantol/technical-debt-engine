import tempfile, unittest
from tde_runtime import Runtime, RuntimeConfiguration
class ExecutionTests(unittest.TestCase):
 def test_plan_and_evidence(self):
  with tempfile.TemporaryDirectory() as root:
   result=Runtime().execute(root,RuntimeConfiguration.load({"capabilities":{"code_size":{"enabled":True}}}))
   execution=next(stage.outputs for stage in result.stages if stage.identifier=="pipeline-execution")
   self.assertEqual("COMPLETED",execution["executionEvidence"]["state"])
   self.assertEqual(["code_size"],execution["executionEvidence"]["executedCapabilities"])
   self.assertEqual(["code_size.cloc"],execution["executionEvidence"]["executedAdapters"])
   self.assertEqual(1,len(execution["executionEvidence"]["workItems"]))
