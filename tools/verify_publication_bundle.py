#!/usr/bin/env python3
"""Verify a retrieved certified bundle without rebuilding or publishing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tde_runtime.release_publication import canonical, verify_publication_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-directory", type=Path, required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--release-version", required=True)
    parser.add_argument("--authorization-json", required=True)
    parser.add_argument("--evidence-output", type=Path)
    arguments = parser.parse_args()
    try:
        authorization = json.loads(arguments.authorization_json)
    except json.JSONDecodeError as error:
        raise SystemExit(f"authorization JSON is invalid: {error}") from error
    result = verify_publication_bundle(arguments.bundle_directory, arguments.candidate_sha,
                                       arguments.release_version, authorization)
    if arguments.evidence_output:
        arguments.evidence_output.parent.mkdir(parents=True, exist_ok=True)
        arguments.evidence_output.write_bytes(canonical(result))
    print(json.dumps(result, sort_keys=True))
    if result["decision"] != "PUBLICATION_PREFLIGHT_READY": raise SystemExit(1)


if __name__ == "__main__": main()
