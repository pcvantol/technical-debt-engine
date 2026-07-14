import tempfile, unittest
from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.execution import CapabilityExecutionEngine
class ExecutionTests(unittest.TestCase):
 def test_plan_and_evidence(self):
  with tempfile.TemporaryDirectory() as root:
   result=Runtime().execute(root,RuntimeConfiguration.load({"capabilities":{"dependency_health":{"enabled":True}}}))
   execution=next(stage.outputs for stage in result.stages if stage.identifier=="pipeline-execution")
   self.assertEqual("COMPLETED",execution["executionEvidence"]["state"])
   self.assertEqual(["dependency_health"],execution["executionEvidence"]["executedCapabilities"])
