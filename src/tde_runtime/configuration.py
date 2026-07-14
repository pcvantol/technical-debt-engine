"""Configuration loading for the empty-registry runtime foundation."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class RuntimeConfiguration:
    schema_version: str = "1.0.0"
    execution_options: dict[str, Any] | None = None

    @classmethod
    def load(cls, values: Mapping[str, Any] | None = None) -> "RuntimeConfiguration":
        values = {} if values is None else dict(values)
        allowed = {"schemaVersion", "executionOptions", "capabilities", "policy", "baseline", "trend"}
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"unsupported runtime configuration: {sorted(unknown)}")
        schema_version = values.get("schemaVersion", "1.0.0")
        if schema_version != "1.0.0":
            raise ValueError("unsupported configuration schema version")
        options = values.get("executionOptions", {})
        if not isinstance(options, dict):
            raise ValueError("executionOptions must be an object")
        capabilities = values.get("capabilities", {})
        if not isinstance(capabilities, dict):
            raise ValueError("capabilities must be an object")
        policy = values.get("policy", {})
        if not isinstance(policy, dict):
            raise ValueError("policy must be an object")
        baseline = values.get("baseline", {})
        if not isinstance(baseline, dict):
            raise ValueError("baseline must be an object")
        trend = values.get("trend", {})
        if not isinstance(trend, dict):
            raise ValueError("trend must be an object")
        return cls(schema_version=schema_version, execution_options={**options, "capabilities": capabilities, "policy": policy, "baseline": baseline, "trend": trend})

    def as_dict(self) -> dict[str, Any]:
        return {"schemaVersion": self.schema_version, "executionOptions": self.execution_options or {}}

    def digest(self) -> str:
        canonical = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))
        return f"sha256:{sha256(canonical.encode()).hexdigest()}"
