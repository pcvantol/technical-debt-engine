from __future__ import annotations

from pathlib import Path
import tarfile
import tempfile
import unittest
import zipfile

from tools.package_build import canonical_json, digest, normalize_sdist, normalize_wheel


class BuildReproducibilityTests(unittest.TestCase):
    def test_canonical_json_has_stable_key_order(self) -> None:
        self.assertEqual(b'{"a":1,"b":2}\n', canonical_json({"b": 2, "a": 1}))

    def test_wheel_normalization_removes_timestamp_variation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, second = root / "first.whl", root / "second.whl"
            for path, timestamp in ((first, (2025, 1, 1, 0, 0, 0)), (second, (2026, 1, 1, 0, 0, 0))):
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr(zipfile.ZipInfo("package/module.py", timestamp), "VALUE = 1\n")
            normalize_wheel(first, 1_700_000_000); normalize_wheel(second, 1_700_000_000)
            self.assertEqual(digest(first), digest(second))

    def test_sdist_normalization_removes_owner_and_timestamp_variation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, second = root / "first.tar.gz", root / "second.tar.gz"
            for path, timestamp, owner in ((first, 1_700_000_000, 1), (second, 1_800_000_000, 2)):
                with tarfile.open(path, "w:gz") as archive:
                    info = tarfile.TarInfo("package/module.py"); info.size = len(b"VALUE = 1\n")
                    info.mtime = timestamp; info.uid = owner; info.gid = owner; info.uname = "builder"
                    import io
                    archive.addfile(info, io.BytesIO(b"VALUE = 1\n"))
            normalize_sdist(first, 1_700_000_000); normalize_sdist(second, 1_700_000_000)
            self.assertEqual(digest(first), digest(second))


if __name__ == "__main__":
    unittest.main()
