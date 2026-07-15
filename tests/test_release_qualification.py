import json, os, subprocess, tempfile, unittest
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
from tde_cli.main import ExitCode, main
from tde_runtime.release_qualification import ReleaseQualification, _candidate_branch

class ReleaseQualificationTests(unittest.TestCase):
 def test_detached_candidate_uses_validated_source_branch(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary)/"repo"; root.mkdir(); subprocess.run(["git","init","-q","-b","main",str(root)],check=True)
   for key,value in (("user.email","test@example.invalid"),("user.name","Test")): subprocess.run(["git","-C",str(root),"config",key,value],check=True)
   (root/"x").write_text("x"); subprocess.run(["git","-C",str(root),"add","."],check=True); subprocess.run(["git","-C",str(root),"commit","-qm","x"],check=True)
   subprocess.run(["git","-C",str(root),"switch","--detach","HEAD"],check=True,stdout=subprocess.DEVNULL)
   with patch.dict(os.environ,{"TDE_CANDIDATE_SOURCE_BRANCH":"main"}): self.assertEqual("main",_candidate_branch(root))

 def test_cli_blocks_missing_release_capability(self):
  output=[]
  class Stream:
   def write(self,value): output.append(value)
   def flush(self): pass
  self.assertEqual(ExitCode.BLOCKED,main(["--format","json","release-qualify",".","--manifest-output","/tmp/release.json"],Stream()))
  self.assertIn("requires one or more supported",''.join(output))

 def test_release_evidence_binds_manifest_and_blocks_without_passing_assurance(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary)/"repo"; root.mkdir(); subprocess.run(["git","init","-q","-b","main",str(root)],check=True)
   for key,value in (("user.email","test@example.invalid"),("user.name","Test")): subprocess.run(["git","-C",str(root),"config",key,value],check=True)
   subprocess.run(["git","-C",str(root),"remote","add","origin","https://example.invalid/tde.git"],check=True)
   (root/"x").write_text("x"); subprocess.run(["git","-C",str(root),"add","."],check=True); subprocess.run(["git","-C",str(root),"commit","-qm","x"],check=True)
   artifact=Path(temporary)/"artifacts"; artifact.mkdir(); (artifact/"t.whl").write_bytes(b"x"); (artifact/"t.tar.gz").write_bytes(b"y")
   records=[(p.name,"sha256:"+sha256(p.read_bytes()).hexdigest()) for p in (artifact/"t.whl",artifact/"t.tar.gz")]
   (artifact/"SHA256SUMS").write_text("".join(f"{d[7:]}  {n}\n" for n,d in records)); (artifact/"build-provenance.json").write_text(json.dumps({"candidateSha":"a"*40,"artifacts":[{"filename":n,"digest":d} for n,d in records]}))
   result=ReleaseQualification().qualify(root,{"validation":{"status":"VALID"}},[artifact],Path(temporary)/"release.json")
   self.assertEqual("RELEASE_BLOCKED",result["decision"]); self.assertFalse(result["checks"]["capabilitySelection"]); self.assertTrue(Path(result["manifest"]["path"]).is_file())

 def test_release_evidence_persists_selection_and_rejects_mutation(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary)/"repo"; root.mkdir(); subprocess.run(["git","init","-q","-b","main",str(root)],check=True)
   for key,value in (("user.email","test@example.invalid"),("user.name","Test")): subprocess.run(["git","-C",str(root),"config",key,value],check=True)
   (root/"x").write_text("x"); subprocess.run(["git","-C",str(root),"add","."],check=True); subprocess.run(["git","-C",str(root),"commit","-qm","x"],check=True)
   artifact=Path(temporary)/"artifacts"; artifact.mkdir(); (artifact/"t.whl").write_bytes(b"x"); (artifact/"t.tar.gz").write_bytes(b"y")
   records=[(p.name,"sha256:"+sha256(p.read_bytes()).hexdigest()) for p in (artifact/"t.whl",artifact/"t.tar.gz")]
   (artifact/"SHA256SUMS").write_text("".join(f"{d[7:]}  {n}\n" for n,d in records)); (artifact/"build-provenance.json").write_text(json.dumps({"candidateSha":"a"*40,"artifacts":[{"filename":n,"digest":d} for n,d in records]}))
   runtime={"validation":{"status":"VALID"},"executionEvidence":{"executedCapabilities":["code_size"]},"runtimeQualification":{"level":"QUALIFIED"},"policyEvidence":{"decision":"PASS"},"integrity":{"contentDigest":"sha256:test"}}
   output=Path(temporary)/"release.json"; result=ReleaseQualification().qualify(root,runtime,[artifact],output,["code_size"])
   self.assertEqual(["code_size"],result["releaseCandidate"]["selectedCapabilities"]); self.assertTrue(Path(result["releaseEvidence"]["path"]).is_file())
   with self.assertRaises(ValueError): ReleaseQualification().qualify(root,runtime,[artifact],output,["complexity"])
