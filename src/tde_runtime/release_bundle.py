"""Immutable manifest and integrity checks for a certified release bundle."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def canonical(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def verify(root: str | Path) -> dict[str, Any]:
    directory = Path(root)
    try:
        manifest = json.loads((directory / "bundle-manifest.json").read_text(encoding="utf-8"))
        sums = (directory / "SHA256SUMS").read_bytes()
        expected = {line.split(maxsplit=1)[1]: "sha256:" + line.split(maxsplit=1)[0] for line in sums.decode().splitlines() if line}
        valid_files = bool(expected) and all((directory / name).is_file() and digest(directory / name) == value for name, value in expected.items())
        complete = {"wheel", "source_distribution", "oci_archive", "release_manifest", "release_qualification", "release_certification", "docker_provenance"}.issubset({item["kind"] for item in manifest["contents"]})
        valid = (manifest.get("schemaId") == "tde.certified-release-bundle" and valid_files and complete
                 and manifest.get("bundleChecksum") == "sha256:" + sha256(sums).hexdigest())
    except (OSError, ValueError, KeyError, IndexError, json.JSONDecodeError):
        manifest, valid, complete = {}, False, False
    return {"bundle": manifest, "integrity": valid, "complete": complete}
