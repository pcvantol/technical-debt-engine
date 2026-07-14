#!/usr/bin/env python3
"""Fail closed unless Code Size matrix records have equivalent output."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize(value: object) -> object:
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()
                if key not in {"executionTiming", "executionId", "qualificationId", "evaluatedAt", "executionDurationMs"}}
    return value


def operating_system(record: dict[str, object]) -> str:
    value = str(record["operatingSystem"]).lower()
    if value.startswith(("macos", "darwin")):
        return "macos"
    if value.startswith("windows"):
        return "windows"
    if value.startswith("linux"):
        return "linux"
    return value.split("-")[0]


def main() -> int:
    records = [json.loads(path.read_text(encoding="utf-8"))
               for path in sorted((ROOT / "qualification").glob("code-size-*.json"))]
    systems = {operating_system(record) for record in records}
    if len(records) < 6 or not {"linux", "macos", "windows"}.issubset(systems):
        raise SystemExit("qualification matrix is incomplete")
    baseline = normalize(records[0]["analyticalProjection"])
    differences = [record["operatingSystem"] for record in records
                   if normalize(record["analyticalProjection"]) != baseline]
    if differences:
        raise SystemExit(f"analytical output differs: {differences}")
    versions = {record["analyzer"]["version"] for record in records}
    if versions != {"2.10"}:
        raise SystemExit(f"unsupported or inconsistent cloc versions: {sorted(versions)}")
    result = {
        "decision": "CODE_SIZE_CROSS_PLATFORM_QUALIFIED",
        "records": len(records),
        "wheelChecksums": sorted({record["wheelChecksum"] for record in records}),
        "clocVersions": sorted(versions),
        "analyticalComparison": "EQUIVALENT",
    }
    (ROOT / "qualification" / "code-size-cross-platform-summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
