import io
import json
import tarfile
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from tde_runtime.docker_artifact import digest, validate


class DockerArtifactTests(unittest.TestCase):
    def test_dockerfile_is_pinned_non_root_and_binds_the_wheel(self):
        source = Path("Dockerfile").read_text(encoding="utf-8")
        self.assertIn("@sha256:", source)
        self.assertIn("COPY wheel/${WHEEL_FILE}", source)
        self.assertIn("USER tde", source)
        self.assertIn("radon==6.0.1", source)
        self.assertIn("cloc-2.10.pl", source)

    def test_candidate_bound_oci_provenance_validates(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); archive = root / "tde-oci.tar"
            index = {"schemaVersion": 2, "manifests": [
                {"digest": "sha256:" + "a" * 64, "platform": {"os": "linux", "architecture": "amd64"}},
                {"digest": "sha256:" + "b" * 64, "platform": {"os": "linux", "architecture": "arm64"}},
            ]}
            raw = json.dumps(index, sort_keys=True).encode()
            with tarfile.open(archive, "w") as output:
                member = tarfile.TarInfo("index.json"); member.size = len(raw); output.addfile(member, io.BytesIO(raw))
            candidate = "c" * 40
            provenance = {"schemaId": "tde.docker-provenance", "schemaVersion": "1.0.0", "candidateSha": candidate,
                          "ociArchive": {"digest": digest(archive)}, "baseImage": {"digest": "sha256:" + "d" * 64},
                          "wheel": {"digest": "sha256:" + "e" * 64}, "dockerfile": {"digest": "sha256:" + "f" * 64},
                          "ociIndex": {"digest": "sha256:" + sha256((json.dumps(index, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()},
                          "platforms": [{"platform": "linux/amd64", "digest": "sha256:" + "a" * 64},
                                        {"platform": "linux/arm64", "digest": "sha256:" + "b" * 64}]}
            (root / "docker-provenance.json").write_text(json.dumps(provenance), encoding="utf-8")
            result = validate(root, candidate)
            self.assertTrue(result["verified"])
            self.assertEqual("oci_archive", result["kind"])

    def test_missing_or_unbound_archive_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.assertFalse(validate(temporary, "a" * 40)["verified"])
