"""Fail-closed validation for a preserved candidate-bound OCI archive."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


def digest(path: str | Path) -> str:
    value = Path(path)
    hasher = sha256()
    with value.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def canonical(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def validate(directory: str | Path, candidate_sha: str) -> dict[str, Any]:
    """Return a Docker artifact record only when archive and provenance bind."""
    root = Path(directory).resolve()
    archive = root / "tde-oci.tar"
    provenance_path = root / "docker-provenance.json"
    try:
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        archive_digest = digest(archive)
        platforms = provenance["platforms"]
        valid = (
            provenance.get("schemaId") == "tde.docker-provenance"
            and provenance.get("schemaVersion") == "1.0.0"
            and provenance.get("candidateSha") == candidate_sha
            and provenance.get("ociArchive", {}).get("digest") == archive_digest
            and provenance.get("baseImage", {}).get("digest", "").startswith("sha256:")
            and provenance.get("wheel", {}).get("digest", "").startswith("sha256:")
            and provenance.get("dockerfile", {}).get("digest", "").startswith("sha256:")
            and isinstance(platforms, list) and {item.get("platform") for item in platforms} >= {"linux/amd64", "linux/arm64"}
            and all(str(item.get("digest", "")).startswith("sha256:") for item in platforms)
            and str(provenance.get("ociIndex", {}).get("digest", "")).startswith("sha256:")
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        provenance, archive_digest, valid = {}, None, False
    return {"filename": archive.name, "digest": archive_digest, "kind": "oci_archive",
            "candidateSha": candidate_sha, "provenance": provenance, "verified": valid}
