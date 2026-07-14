#!/usr/bin/env python3
"""Fail closed unless all matrix records have equivalent analytical output."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "qualification").glob("complexity-*.json"))]
    operating_systems = {record["operatingSystem"].split("-")[0].lower() for record in records}
    if len(records) < 6 or not {"linux", "darwin", "windows"}.issubset(operating_systems):
        raise SystemExit("qualification matrix is incomplete")
    baseline = records[0]["analyticalProjection"]
    differences = [record["operatingSystem"] for record in records if record["analyticalProjection"] != baseline]
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
