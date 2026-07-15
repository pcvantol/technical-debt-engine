import json, tempfile, unittest
from pathlib import Path
from tde_runtime.software_assurance import SoftwareAssurance
class SoftwareAssuranceTests(unittest.TestCase):
 def test_missing_required_sources_fail_closed(self):
  with tempfile.TemporaryDirectory() as root:
   self.assertEqual("FAIL",SoftwareAssurance().assure(root)["qualification"])

 def test_candidate_artifacts_require_checksums_provenance_and_reproducibility(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary); first=root/"first"; second=root/"second"; first.mkdir(); second.mkdir()
   for directory in (first,second):
    wheel=directory/"tde-0.1.0-py3-none-any.whl"; sdist=directory/"tde-0.1.0.tar.gz"
    wheel.write_bytes(b"wheel"); sdist.write_bytes(b"sdist")
    from hashlib import sha256
    records=[{"filename":item.name,"digest":"sha256:"+sha256(item.read_bytes()).hexdigest()} for item in (wheel,sdist)]
    (directory/"SHA256SUMS").write_text("".join(f"{item['digest'][7:]}  {item['filename']}\n" for item in records),encoding="utf-8")
    (directory/"build-provenance.json").write_text(json.dumps({"candidateSha":"a"*40,"artifacts":records}),encoding="utf-8")
   evidence=SoftwareAssurance()._artifacts((first,second),[])
   self.assertTrue(evidence["integrity"]); self.assertTrue(evidence["reproducible"])

 def test_invalid_candidate_directories_are_not_reproducible(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary); first=root/"first"; second=root/"second"; first.mkdir(); second.mkdir()
   evidence=SoftwareAssurance()._artifacts((first,second),[])
   self.assertFalse(evidence["integrity"]); self.assertFalse(evidence["reproducible"])
