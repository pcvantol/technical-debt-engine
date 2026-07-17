import tempfile, unittest
from tde_runtime import Runtime
from tde_runtime.runtime_qualification import RuntimeQualificationEngine
class RuntimeQualificationTests(unittest.TestCase):
 def test_qualified_and_unsupported(self):
  with tempfile.TemporaryDirectory() as root:
   evidence=Runtime().execute(root).evidence
   self.assertEqual("BLOCKED",RuntimeQualificationEngine().qualify(evidence)["level"])
  self.assertEqual("NOT_SUPPORTED",RuntimeQualificationEngine().qualify(evidence,"code_size")["level"])

 def test_missing_adapter_evidence_blocks_qualification(self):
  evidence={"validation":{"status":"VALID"},"integrity":{"contentDigest":"sha256:test"},"capabilityResults":[{"capabilityId":"code_size","status":"VALID","completeness":1}],"executionEvidence":{"plannedCapabilities":["code_size"],"executedCapabilities":["code_size"],"plannedAdapters":["code_size.cloc"],"executedAdapters":[],"workItems":[{"capabilityId":"code_size","state":"COMPLETED"}]}}
  qualification=RuntimeQualificationEngine().qualify(evidence,"code_size")
  self.assertEqual("BLOCKED",qualification["level"])
  self.assertEqual(["code_size.cloc"],qualification["missingAdapters"])
