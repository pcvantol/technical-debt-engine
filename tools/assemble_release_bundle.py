#!/usr/bin/env python3
"""Assemble a non-published, checksum-bound certified release bundle."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tomllib

from tde_runtime.release_bundle import canonical, digest, verify


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-sha", required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-version", required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--wheel", type=Path, required=True); parser.add_argument("--sdist", type=Path, required=True)
    parser.add_argument("--oci-archive", type=Path, required=True); parser.add_argument("--docker-provenance", type=Path, required=True)
    parser.add_argument("--release-manifest", type=Path, required=True); parser.add_argument("--release-qualification", type=Path, required=True)
    parser.add_argument("--release-certification", type=Path, required=True); parser.add_argument("--release-evidence", type=Path, required=True)
    arguments = parser.parse_args(); output = arguments.output.resolve()
    with (arguments.repository / "pyproject.toml").open("rb") as configuration:
        package_version = tomllib.load(configuration).get("project", {}).get("version")
    if arguments.release_version != package_version:
        raise ValueError("release version must match the certified candidate package version")
    if output.exists() and any(output.iterdir()): raise ValueError(f"bundle output must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    sources = [("wheel", arguments.wheel), ("source_distribution", arguments.sdist), ("oci_archive", arguments.oci_archive),
               ("docker_provenance", arguments.docker_provenance), ("release_manifest", arguments.release_manifest),
               ("release_qualification", arguments.release_qualification), ("release_certification", arguments.release_certification),
               ("release_evidence", arguments.release_evidence)]
    contents = []
    for kind, source in sources:
        source = source.resolve(); target = output / source.name; shutil.copy2(source, target)
        contents.append({"kind": kind, "filename": target.name, "digest": digest(target)})
    sums = "".join(f"{item['digest'].removeprefix('sha256:')}  {item['filename']}\n" for item in sorted(contents, key=lambda item: item["filename"])).encode()
    (output / "SHA256SUMS").write_bytes(sums)
    manifest = {"schemaId": "tde.certified-release-bundle", "schemaVersion": "1.0.0", "candidateSha": arguments.candidate_sha,
                "bundleVersion": arguments.release_version, "contents": contents, "bundleChecksum": "sha256:" + sha256(sums).hexdigest(),
                "retention": {"mechanism": "GitHub Actions artifact", "retentionDays": 90, "retrieval": "Download docker-release-candidate-<candidate-sha> from the qualifying workflow run; no rebuild is permitted."}}
    manifest["bundleId"] = "bundle.sha256." + sha256(canonical(manifest)).hexdigest()
    (output / "bundle-manifest.json").write_bytes(canonical(manifest))
    result = verify(output)
    if not result["integrity"]: raise RuntimeError("assembled bundle failed integrity verification")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__": main()
