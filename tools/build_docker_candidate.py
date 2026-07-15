#!/usr/bin/env python3
"""Build a non-published multi-platform OCI archive from one exact wheel."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile


BASE_IMAGE = "python:3.11-slim-bookworm@sha256:b18992999dbe963a45a8a4da40ac2b1975be1a776d939d098c647482bcad5cba"
PLATFORMS = ("linux/amd64", "linux/arm64")
CLOC_SHA256 = "bf59272455172108072a0a106379f7509fd4349bdcfd85203bac038ccd286d83"


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], check=True, text=True, capture_output=True).stdout.strip()


def _index(archive: Path) -> tuple[str, list[dict[str, str]]]:
    with tarfile.open(archive, "r:") as source:
        member = source.extractfile("index.json")
        if member is None:
            raise RuntimeError("OCI archive has no index.json")
        outer = json.load(member)
        descriptors = outer.get("manifests", [])
        if len(descriptors) != 1 or not descriptors[0].get("digest", "").startswith("sha256:"):
            raise RuntimeError("OCI archive has no single index descriptor")
        index_digest = descriptors[0]["digest"]
        blob = source.extractfile("blobs/sha256/" + index_digest.removeprefix("sha256:"))
        if blob is None:
            raise RuntimeError("OCI archive has no platform index blob")
        index = json.load(blob)
    platforms = []
    for item in index.get("manifests", []):
        platform = item.get("platform", {})
        if platform.get("os") == "linux" and platform.get("architecture") in {"amd64", "arm64"}:
            platforms.append({"platform": f"{platform['os']}/{platform['architecture']}", "digest": item["digest"]})
    if {item["platform"] for item in platforms} != set(PLATFORMS):
        raise RuntimeError("OCI archive does not contain required linux/amd64 and linux/arm64 manifests")
    return index_digest, sorted(platforms, key=lambda item: item["platform"])


def build(root: Path, wheel: Path, sdist: Path, output: Path) -> dict:
    root, wheel, sdist, output = root.resolve(), wheel.resolve(), sdist.resolve(), output.resolve()
    if git(root, "status", "--porcelain"):
        raise ValueError("candidate repository must be clean before Docker provenance generation")
    candidate, epoch = git(root, "rev-parse", "HEAD"), git(root, "log", "-1", "--format=%ct")
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError(f"output directory must be empty: {output}")
    with tempfile.TemporaryDirectory(prefix="tde-docker-context-") as temporary:
        context = Path(temporary)
        shutil.copy2(root / "Dockerfile", context / "Dockerfile")
        (context / "wheel").mkdir(); shutil.copy2(wheel, context / "wheel" / wheel.name)
        created = subprocess.run(["python", "-c", f"import datetime; print(datetime.datetime.fromtimestamp({epoch}, datetime.timezone.utc).isoformat().replace('+00:00','Z'))"], check=True, text=True, capture_output=True).stdout.strip()
        command = ["docker", "buildx", "build", "--platform", ",".join(PLATFORMS), "--provenance=false", "--sbom=false", "--output", f"type=oci,dest={output / 'tde-oci.tar'}",
                   "--build-arg", f"CANDIDATE_SHA={candidate}", "--build-arg", "TDE_VERSION=0.1.0", "--build-arg", f"WHEEL_FILE={wheel.name}",
                   "--build-arg", f"WHEEL_SHA256={digest(wheel).removeprefix('sha256:')}", "--build-arg", f"SOURCE_DATE_EPOCH={epoch}", "--build-arg", f"CREATED={created}", str(context)]
        subprocess.run(command, check=True)
    archive = output / "tde-oci.tar"
    index_digest, platforms = _index(archive)
    dockerfile = root / "Dockerfile"
    result = {"schemaId": "tde.docker-provenance", "schemaVersion": "1.0.0", "candidateSha": candidate,
              "repository": git(root, "config", "--get", "remote.origin.url") or "local", "target": "docker.io/pcvantol/technical-debt-engine", "publicationState": "NOT_PUBLISHED",
              "baseImage": {"reference": BASE_IMAGE, "digest": "sha256:b18992999dbe963a45a8a4da40ac2b1975be1a776d939d098c647482bcad5cba"},
              "wheel": {"filename": wheel.name, "digest": digest(wheel)}, "sourceDistribution": {"filename": sdist.name, "digest": digest(sdist)},
              "dockerfile": {"path": "Dockerfile", "digest": digest(dockerfile)}, "analyzers": {"cloc": {"version": "2.10", "sha256": CLOC_SHA256}, "radon": {"version": "6.0.1"}},
              "platforms": platforms, "ociIndex": {"digest": index_digest}, "ociArchive": {"filename": archive.name, "digest": digest(archive)},
              "reproducibility": {"claimedByteIdentical": False, "reason": "OCI timestamps and BuildKit metadata require platform-specific equivalence analysis."}}
    (output / "docker-provenance.json").write_bytes(canonical(result))
    (output / "SHA256SUMS").write_text(f"{digest(archive).removeprefix('sha256:')}  {archive.name}\n{digest(output / 'docker-provenance.json').removeprefix('sha256:')}  docker-provenance.json\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True); parser.add_argument("--sdist", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True); parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args(); print(json.dumps(build(arguments.root, arguments.wheel, arguments.sdist, arguments.output), sort_keys=True))


if __name__ == "__main__":
    main()
