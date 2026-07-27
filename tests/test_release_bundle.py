import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tde_runtime.release_bundle import verify


class ReleaseBundleTests(unittest.TestCase):
    def test_complete_bundle_is_integrity_bound_and_tampering_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); inputs = root / "inputs"; inputs.mkdir()
            files = {"wheel.whl": b"wheel", "source.tar.gz": b"sdist", "image.tar": b"oci", "docker-provenance.json": b"{}",
                     "manifest.json": b"{}", "qualification.json": b"{}", "certification.json": b"{}", "evidence.json": b"{}"}
            for name, value in files.items(): (inputs / name).write_bytes(value)
            output = root / "bundle"
            command = ["python", "tools/assemble_release_bundle.py", "--candidate-sha", "a" * 40, "--release-version", "1.0.0", "--output", str(output),
                       "--wheel", str(inputs / "wheel.whl"), "--sdist", str(inputs / "source.tar.gz"), "--oci-archive", str(inputs / "image.tar"),
                       "--docker-provenance", str(inputs / "docker-provenance.json"), "--release-manifest", str(inputs / "manifest.json"),
                       "--release-qualification", str(inputs / "qualification.json"), "--release-certification", str(inputs / "certification.json"), "--release-evidence", str(inputs / "evidence.json")]
            subprocess.run(command, check=True, env={**__import__("os").environ, "PYTHONPATH": "src"}, capture_output=True)
            self.assertTrue(verify(output)["integrity"])
            self.assertEqual("1.0.0", verify(output)["bundle"]["bundleVersion"])
            (output / "wheel.whl").write_bytes(b"tampered")
            self.assertFalse(verify(output)["integrity"])

    def test_bundle_rejects_a_version_that_does_not_match_the_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); inputs = root / "inputs"; inputs.mkdir()
            files = {"wheel.whl": b"wheel", "source.tar.gz": b"sdist", "image.tar": b"oci", "docker-provenance.json": b"{}",
                     "manifest.json": b"{}", "qualification.json": b"{}", "certification.json": b"{}", "evidence.json": b"{}"}
            for name, value in files.items(): (inputs / name).write_bytes(value)
            command = ["python", "tools/assemble_release_bundle.py", "--candidate-sha", "a" * 40, "--release-version", "9.9.9", "--output", str(root / "bundle"),
                       "--wheel", str(inputs / "wheel.whl"), "--sdist", str(inputs / "source.tar.gz"), "--oci-archive", str(inputs / "image.tar"),
                       "--docker-provenance", str(inputs / "docker-provenance.json"), "--release-manifest", str(inputs / "manifest.json"),
                       "--release-qualification", str(inputs / "qualification.json"), "--release-certification", str(inputs / "certification.json"), "--release-evidence", str(inputs / "evidence.json")]
            result = subprocess.run(command, env={**__import__("os").environ, "PYTHONPATH": "src"}, capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("must match", result.stderr)
