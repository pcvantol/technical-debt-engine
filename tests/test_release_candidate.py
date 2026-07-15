import subprocess
import tempfile
import unittest
from pathlib import Path

from tde_runtime.release_candidate import candidate_superseded, validate_snapshot


class MainlineCandidateTests(unittest.TestCase):
    def repository(self) -> tuple[Path, str]:
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for command in (("init", "-b", "main"), ("config", "user.email", "test@example.invalid"),
                        ("config", "user.name", "Test")):
            subprocess.run(["git", "-C", str(root), *command], check=True, capture_output=True)
        (root / "candidate.txt").write_text("candidate\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(root), "commit", "-m", "candidate"], check=True, capture_output=True)
        sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        return root, sha

    def test_mainline_snapshot_accepts_an_exact_ancestor_sha(self):
        root, sha = self.repository()
        result = validate_snapshot(root, sha, "0.1.0", "internal")
        self.assertEqual(sha, result["candidateSha"])
        self.assertTrue(result["ancestryVerified"])

    def test_sibling_and_unmerged_candidates_are_rejected(self):
        root, main_sha = self.repository()
        subprocess.run(["git", "-C", str(root), "switch", "-c", "release-side"], check=True, capture_output=True)
        (root / "side.txt").write_text("side\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(root), "commit", "-m", "side"], check=True, capture_output=True)
        sibling = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        subprocess.run(["git", "-C", str(root), "switch", "main"], check=True, capture_output=True)
        self.assertNotEqual(main_sha, sibling)
        with self.assertRaisesRegex(ValueError, "not an ancestor"):
            validate_snapshot(root, sibling, "0.1.0", "internal")

    def test_administrative_paths_do_not_supersede_but_product_paths_do(self):
        candidate = "a" * 40
        self.assertFalse(candidate_superseded(candidate, ["ENGINEERING_STATUS.md", "docs/history/prompts/x.md"]))
        self.assertTrue(candidate_superseded(candidate, ["Dockerfile"]))
        self.assertTrue(candidate_superseded(candidate, ["src/tde_runtime/main.py"]))
