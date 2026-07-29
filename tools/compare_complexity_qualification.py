#!/usr/bin/env python3
"""Fail closed unless all matrix records have equivalent analytical output."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize(value: object) -> object:
    """Remove the documented non-deterministic execution envelope only.

    Analyzer provenance intentionally records the runner platform and absolute
    executable path. Both remain in each qualification record for audit, but
    neither is an analytical result and therefore cannot participate in a
    cross-platform equivalence comparison.
    """
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        excluded_keys = {
            "executionTiming", "executionId", "qualificationId", "evaluatedAt", "executionDurationMs",
            "targetEntityId", "measurementId", "qualificationReference", "executable", "platform",
        }
        return {key: normalize(item) for key, item in value.items() if key not in excluded_keys}
    return value


def main() -> int:
    records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "qualification").glob("complexity-*.json"))]
    def operating_system(record: dict[str, object]) -> str:
        value = str(record["operatingSystem"]).lower()
        if value.startswith("macos") or value.startswith("darwin"):
            return "macos"
        if value.startswith("windows"):
            return "windows"
        if value.startswith("linux"):
            return "linux"
        return value.split("-")[0]

    operating_systems = {operating_system(record) for record in records}
    if len(records) < 6 or not {"linux", "macos", "windows"}.issubset(operating_systems):
        raise SystemExit("qualification matrix is incomplete")
    baseline = normalize(records[0]["analyticalProjection"])
    differences = [record["operatingSystem"] for record in records if normalize(record["analyticalProjection"]) != baseline]
    if differences:
        raise SystemExit(f"analytical output differs: {differences}")
    result = {"decision": "COMPLEXITY_CROSS_PLATFORM_QUALIFIED", "records": len(records),
              "wheelChecksums": sorted({record["wheelChecksum"] for record in records}),
              "radonVersions": sorted({record["analyzer"]["version"] for record in records}),
              "analyticalComparison": "EQUIVALENT"}
    (ROOT / "qualification" / "cross-platform-summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
