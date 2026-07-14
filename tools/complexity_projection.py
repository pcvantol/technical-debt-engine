"""Stable projection used to compare cross-platform Complexity evidence."""
from __future__ import annotations

from typing import Any, Mapping


def analytical_projection(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Exclude only execution envelope fields that are intentionally variable."""
    return {
        "capabilityResults": evidence.get("capabilityResults", []),
        "adapterResults": [
            {key: value for key, value in result.items()
             if key not in {"executionTiming", "rawOutput"}}
            for result in evidence.get("adapterResults", [])
        ],
        "measurements": evidence.get("measurements", []),
        "findings": evidence.get("findings", []),
        "runtimeQualification": {
            key: value for key, value in evidence.get("runtimeQualification", {}).items()
            if key not in {"evaluatedAt", "executionDurationMs"}
        },
        "limitations": evidence.get("limitations", []),
    }
