#!/usr/bin/env python3
"""Validate and emit a non-mutating mainline candidate snapshot record."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tde_runtime.release_candidate import validate_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--main-ref", default="origin/main")
    arguments = parser.parse_args()
    print(json.dumps(validate_snapshot(arguments.repository, arguments.candidate_sha,
                                      arguments.version, arguments.profile, arguments.main_ref), sort_keys=True))


if __name__ == "__main__":
    main()
