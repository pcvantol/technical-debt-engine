#!/usr/bin/env python3
"""Create deterministic Python distributions and checksum-bound provenance."""

from __future__ import annotations

import argparse
from io import BytesIO
import gzip
from hashlib import sha256
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory
from typing import Any
import zipfile


PROVENANCE_SCHEMA_VERSION = "1.0.0"


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return "sha256:" + hasher.hexdigest()


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], check=True, text=True,
                          capture_output=True).stdout.strip()


def source_date_epoch(root: Path) -> int:
    supplied = __import__("os").environ.get("SOURCE_DATE_EPOCH")
    return int(supplied) if supplied else int(git(root, "log", "-1", "--format=%ct"))


def zip_timestamp(epoch: int) -> tuple[int, int, int, int, int, int]:
    # ZIP cannot represent dates before 1980 and stores two-second precision.
    import datetime
    return datetime.datetime.fromtimestamp(max(epoch, 315532800), datetime.timezone.utc).timetuple()[:6]


def normalize_wheel(path: Path, epoch: int) -> None:
    """Repack ZIP metadata without changing any wheel member content."""
    with TemporaryDirectory(prefix="tde-wheel-") as temporary:
        target = Path(temporary) / path.name
        with zipfile.ZipFile(path) as source, zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED,
                                                               compresslevel=9) as output:
            for member in sorted(source.infolist(), key=lambda item: item.filename):
                info = zipfile.ZipInfo(member.filename, date_time=zip_timestamp(epoch))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = member.external_attr
                info.create_system = 3
                output.writestr(info, source.read(member.filename), compress_type=zipfile.ZIP_DEFLATED,
                                compresslevel=9)
        shutil.copyfile(target, path)


def normalize_sdist(path: Path, epoch: int) -> None:
    """Write a canonical gzip/tar container with stable metadata and ordering."""
    with TemporaryDirectory(prefix="tde-sdist-") as temporary:
        target = Path(temporary) / path.name
        with tarfile.open(path, "r:gz") as source, target.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch, compresslevel=9) as compressed:
                with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as output:
                    for member in sorted(source.getmembers(), key=lambda item: item.name):
                        info = member.replace(uid=0, gid=0, uname="root", gname="root", mtime=epoch)
                        info.pax_headers = {}
                        content = source.extractfile(member) if member.isfile() else None
                        output.addfile(info, content)
                        if content:
                            content.close()
        shutil.copyfile(target, path)


def tool_versions() -> dict[str, str]:
    from importlib.metadata import version
    return {name: version(name) for name in ("build", "packaging", "pyproject_hooks", "setuptools", "wheel")}


def build(root: Path, output: Path) -> dict[str, Any]:
    root, output = root.resolve(), output.resolve()
    if git(root, "status", "--porcelain"):
        raise ValueError("candidate repository must be clean before a provenance-bearing build")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    epoch = source_date_epoch(root)
    environment = dict(__import__("os").environ, SOURCE_DATE_EPOCH=str(epoch), PYTHONHASHSEED="0")
    # Setuptools regenerates egg-info manifests.  Build an exact archive of the
    # committed candidate instead of the checkout so independent builds cannot
    # contaminate one another or the provenance-bearing source candidate.
    candidate_sha = git(root, "rev-parse", "HEAD")
    archive = subprocess.run(["git", "-C", str(root), "archive", "--format=tar", candidate_sha], check=True,
                             capture_output=True).stdout
    with TemporaryDirectory(prefix="tde-candidate-") as temporary:
        candidate_root = Path(temporary)
        with tarfile.open(fileobj=BytesIO(archive), mode="r:") as source:
            source.extractall(candidate_root, filter="data")
        subprocess.run([sys.executable, "-m", "build", "--no-isolation", "--outdir", str(output), str(candidate_root)],
                       check=True, env=environment)
    artifacts = sorted([*output.glob("*.whl"), *output.glob("*.tar.gz")])
    if len(artifacts) != 2 or not any(item.suffix == ".whl" for item in artifacts) or not any(item.name.endswith(".tar.gz") for item in artifacts):
        raise RuntimeError("builder did not create exactly one wheel and one source distribution")
    for artifact in artifacts:
        normalize_wheel(artifact, epoch) if artifact.suffix == ".whl" else normalize_sdist(artifact, epoch)
    versions = tool_versions()
    build_inputs = {"candidateSha": candidate_sha, "schemaVersion": PROVENANCE_SCHEMA_VERSION,
                    "sourceDateEpoch": epoch, "tools": versions}
    build_id = "build.sha256." + sha256(canonical_json(build_inputs)).hexdigest()
    artifact_records = [{"artifactIdentity": "artifact." + digest(item), "digest": digest(item),
                         "filename": item.name, "kind": "wheel" if item.suffix == ".whl" else "source_distribution"}
                        for item in artifacts]
    provenance = {"schemaVersion": PROVENANCE_SCHEMA_VERSION,
                  "repository": git(root, "config", "--get", "remote.origin.url") or "local",
                  "candidateIdentity": "candidate.git." + candidate_sha,
                  "candidateSha": candidate_sha, "branch": git(root, "branch", "--show-current"),
                  "buildIdentity": build_id, "sourceDateEpoch": epoch,
                  "runtime": {"packageVersion": "0.1.0", "pythonVersion": platform.python_version()},
                  "buildPlatform": {"system": platform.system(), "machine": platform.machine()},
                  "tools": versions, "artifacts": artifact_records}
    (output / "build-provenance.json").write_bytes(canonical_json(provenance))
    checksums = "".join(f"{record['digest'].removeprefix('sha256:')}  {record['filename']}\n" for record in artifact_records)
    (output / "SHA256SUMS").write_text(checksums, encoding="utf-8")
    return provenance


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    print(json.dumps(build(arguments.root, arguments.output), sort_keys=True))


if __name__ == "__main__":
    main()
