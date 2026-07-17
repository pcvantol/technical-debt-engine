"""Public, versioned assessment-evidence schemas and their runtime validator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "1.0.0"
SCHEMA_COMPATIBILITY_VERSION = "1"


class SchemaValidationError(ValueError):
    """Raised when canonical evidence does not satisfy its public contract."""


class SchemaRegistry:
    """Owns the Runtime's public schema catalogue and fail-closed validation."""

    _files = {
        "capability-evidence": "capability-evidence.json",
        "policy-evidence": "policy-evidence.json",
        "assessment-decision-evidence": "assessment-decision-evidence.json",
        "assessment-evidence": "assessment-evidence.json",
    }

    @classmethod
    def identity(cls, name: str, runtime_version: str, assessment_version: str) -> dict[str, str]:
        if name not in cls._files:
            raise SchemaValidationError(f"unknown public schema: {name}")
        return {"name": f"tde.{name}", "version": SCHEMA_VERSION,
                "compatibilityVersion": SCHEMA_COMPATIBILITY_VERSION,
                "runtimeVersion": runtime_version, "assessmentVersion": assessment_version}

    @classmethod
    def catalogue(cls) -> tuple[dict[str, str], ...]:
        directory = Path(__file__).parent
        return tuple({"name": f"tde.{name}", "version": SCHEMA_VERSION,
                      "compatibilityVersion": SCHEMA_COMPATIBILITY_VERSION,
                      "location": str(directory / filename)}
                     for name, filename in cls._files.items())

    @classmethod
    def validate(cls, name: str, value: Mapping[str, Any]) -> None:
        if not isinstance(value, Mapping):
            raise SchemaValidationError(f"{name} evidence must be an object")
        identity = value.get("schema")
        expected = f"tde.{name}"
        if not isinstance(identity, Mapping) or identity.get("name") != expected:
            raise SchemaValidationError(f"{name} evidence has an incompatible schema identifier")
        if identity.get("version") != SCHEMA_VERSION or identity.get("compatibilityVersion") != SCHEMA_COMPATIBILITY_VERSION:
            raise SchemaValidationError(f"{name} evidence has an incompatible schema version")
        if not isinstance(identity.get("runtimeVersion"), str) or not identity["runtimeVersion"]:
            raise SchemaValidationError(f"{name} evidence is missing runtime version")
        if not isinstance(identity.get("assessmentVersion"), str) or not identity["assessmentVersion"]:
            raise SchemaValidationError(f"{name} evidence is missing assessment version")
        definition = cls.document(name)
        required = tuple(definition["required"])
        missing = [key for key in required if key not in value]
        if missing:
            raise SchemaValidationError(f"{name} evidence is missing required fields: {missing}")
        type_checks = {"string": str, "object": Mapping, "array": list}
        for field, definition in definition.get("properties", {}).items():
            expected_type = definition.get("type")
            if expected_type and field in value and not isinstance(value[field], type_checks[expected_type]):
                raise SchemaValidationError(f"{name} evidence field {field} has an invalid type")

    @classmethod
    def validate_assessment(cls, evidence: Mapping[str, Any]) -> None:
        cls.validate("assessment-evidence", evidence.get("assessment", {}))
        cls.validate("policy-evidence", evidence.get("policyEvidence", {}))
        cls.validate("assessment-decision-evidence", evidence.get("assessmentDecision", {}))
        for item in evidence.get("assessment", {}).get("capabilityExecutions", []):
            cls.validate("capability-evidence", item)

    @classmethod
    def document(cls, name: str) -> dict[str, Any]:
        filename = cls._files.get(name.removeprefix("tde."))
        if filename is None:
            raise SchemaValidationError(f"unknown public schema: {name}")
        return json.loads((Path(__file__).parent / filename).read_text(encoding="utf-8"))
