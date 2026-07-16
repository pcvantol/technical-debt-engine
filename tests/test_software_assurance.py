import json, tempfile, unittest
from pathlib import Path
from tde_runtime.software_assurance import SoftwareAssurance, parse_action_reference
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

 def test_action_reference_parser_normalizes_complete_sha_references(self):
  sha="A"*40
  for reference, path in ((f"Actions/Checkout@{sha}",None),
                          (f"owner/repository/.github/workflows/reusable.yml@{sha}","/.github/workflows/reusable.yml")):
   with self.subTest(reference=reference):
    parsed=parse_action_reference(reference)
    self.assertEqual({"owner":"actions" if path is None else "owner",
                      "repository":"checkout" if path is None else "repository",
                      "path":path,"commitSha":sha.lower(),"immutable":True},parsed)

 def test_workflow_parser_accepts_step_job_and_reusable_workflow_sha_references(self):
  sha="a"*40
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary); workflows=root/".github"/"workflows"; workflows.mkdir(parents=True)
   (workflows/"immutable.yml").write_text(
    f"jobs:\n  step:\n    steps:\n      - uses: actions/checkout@{sha}\n  reusable:\n    uses: owner/repository/.github/workflows/reusable.yml@{sha}\n  called:\n    uses: owner/repository@{sha}\n",encoding="utf-8")
   evidence=SoftwareAssurance()._workflows(root,[])
   self.assertTrue(evidence["immutableActions"])
   self.assertEqual(3,len(evidence["actionReferences"]))

 def test_workflow_parser_rejects_mutable_references(self):
  mutable=("owner/repository@main","owner/repository@v1.2.3","owner/repository@latest",
           "owner/repository","owner/repository@abc1234","${{ matrix.action }}",
           "owner/repository@${{ matrix.sha }}","actions/${{ matrix.action }}@"+"a"*40)
  for reference in mutable:
   with self.subTest(reference=reference): self.assertFalse(parse_action_reference(reference)["immutable"])
