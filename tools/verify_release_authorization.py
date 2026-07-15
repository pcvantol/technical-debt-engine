#!/usr/bin/env python3
"""Validate a persisted Internal Release authorization record without publishing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tde_runtime.release_publication import canonical, validate_authorization_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--release-version", required=True)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--bundle-checksum", required=True)
    arguments = parser.parse_args()
    record = json.loads(arguments.record.read_text(encoding="utf-8"))
    errors = validate_authorization_record(record, arguments.candidate_sha, arguments.release_version,
                                           arguments.bundle_id, arguments.bundle_checksum)
    result = {"schemaId": "tde.internal-release-authorization-validation", "schemaVersion": "1.0.0",
              "authorizationId": record.get("authorizationId"), "valid": not errors, "errors": errors,
              "decision": "HUMAN_RELEASE_AUTHORIZATION_RECORDED" if not errors else "HUMAN_RELEASE_AUTHORIZATION_BLOCKED"}
    print(canonical(result).decode(), end="")
    if errors: raise SystemExit(1)


if __name__ == "__main__": main()
