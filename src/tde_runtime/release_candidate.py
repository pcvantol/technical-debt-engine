"""Fail-closed validation for immutable mainline release-candidate snapshots."""
from __future__ import annotations

from datetime import datetime, timezone
import re
import subprocess
from pathlib import Path
from typing import Any


SHA = re.compile(r"^[0-9a-f]{40}$")
VERSION = re.compile(r"^\d+\.\d+\.\d+(?:[A-Za-z0-9.+-]+)?$")


def _git(root: Path, *arguments: str) -> tuple[bool, str]:
    result = subprocess.run(["git", "-C", str(root), *arguments], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.returncode == 0, result.stdout.strip()


def validate_snapshot(root: str | Path, candidate_sha: str, version: str, profile: str,
                      main_ref: str = "main") -> dict[str, Any]:
    """Return an independently-verifiable candidate record or fail closed.

    A candidate is a reference only: it creates neither a tag nor source changes.
    """
    repository = Path(root).resolve()
    if not SHA.fullmatch(candidate_sha):
        raise ValueError("candidate SHA must be an exact lowercase 40-character Git SHA")
    if not VERSION.fullmatch(version):
        raise ValueError("candidate version is invalid")
    if not profile:
        raise ValueError("candidate release profile is required")
    exists, object_type = _git(repository, "cat-file", "-t", candidate_sha)
    if not exists or object_type != "commit":
        raise ValueError("candidate SHA does not identify a commit")
    main_exists, _ = _git(repository, "rev-parse", "--verify", f"{main_ref}^{{commit}}")
    if not main_exists:
        raise ValueError(f"mainline reference {main_ref!r} is unavailable")
    ancestor, _ = _git(repository, "merge-base", "--is-ancestor", candidate_sha, main_ref)
    if not ancestor:
        raise ValueError("candidate SHA is not an ancestor of main; sibling and unmerged candidates are prohibited")
    clean, status = _git(repository, "status", "--porcelain")
    if not clean or status:
        raise ValueError("candidate repository must be clean")
    main_sha_ok, main_sha = _git(repository, "rev-parse", f"{main_ref}^{{commit}}")
    source_ref_ok, source_ref = _git(repository, "branch", "--show-current")
    actor_ok, actor = _git(repository, "config", "user.email")
    return {
        "schemaId": "tde.mainline-candidate-snapshot",
        "schemaVersion": "1.0.0",
        "candidateSha": candidate_sha,
        "version": version,
        "profile": profile,
        "sourceBranch": source_ref if source_ref_ok and source_ref else main_ref,
        "mainlineSha": main_sha if main_sha_ok else None,
        "actor": actor if actor_ok and actor else "github-actions",
        "createdAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "ancestryVerified": True,
        "immutable": True,
        "publicationSource": "exact candidate SHA only",
    }


def candidate_superseded(candidate_sha: str, changed_paths: list[str]) -> bool:
    """Classify later intended-release changes without changing candidate identity."""
    if not SHA.fullmatch(candidate_sha):
        raise ValueError("candidate SHA must be exact")
    administrative_prefixes = ("docs/history/prompts/",)
    administrative_files = {
        "ENGINEERING_STATUS.md", "REPOSITORY_STATUS.md", "MANAGEMENT_SUMMARY.md",
        "PROMPT_INDEX.md", "RELEASE_PUBLICATION.md",
    }
    return any(path not in administrative_files and not path.startswith(administrative_prefixes)
               for path in changed_paths)
