"""Declarative repository qualification, independent from capabilities and analyzers."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from .registries import AssessmentProfileRegistry
from .schemas import SchemaRegistry
from .models import utc_now


class RepositoryQualificationError(ValueError):
    """Raised when a repository definition or qualification record is invalid."""


class RepositoryDefinitionRegistry:
    """Loads public repository definitions without embedding repository knowledge."""

    required = {"identifier", "name", "repositoryRoot", "repositoryType", "primaryLanguage", "defaultAssessmentProfile", "metadata"}

    def resolve(self, repository_root: str | Path, definition_file: str | Path | None = None) -> dict[str, Any]:
        path = Path(definition_file) if definition_file else None
        if path is None:
            root = Path(repository_root).resolve()
            definition = {"identifier": f"repository.local.{sha256(str(root).encode()).hexdigest()[:16]}",
                          "name": root.name or "repository", "repositoryRoot": str(root), "repositoryType": "source",
                          "primaryLanguage": "unknown", "defaultAssessmentProfile": "standard",
                          "metadata": {"source": "runtime-generated"}}
        else:
            try:
                definition = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise RepositoryQualificationError(f"invalid repository definition {path}: {error}") from error
            if not isinstance(definition, dict):
                raise RepositoryQualificationError("repository definition must be an object")
            definition = dict(definition)
            root_value = definition.get("repositoryRoot")
            if isinstance(root_value, str) and not Path(root_value).is_absolute():
                definition["repositoryRoot"] = str((path.parent / root_value).resolve())
        self._validate(definition)
        return definition

    @classmethod
    def _validate(cls, definition: Mapping[str, Any]) -> None:
        missing = sorted(cls.required - set(definition))
        if missing:
            raise RepositoryQualificationError(f"repository definition is missing required fields: {missing}")
        if not all(isinstance(definition[key], str) and definition[key].strip()
                   for key in ("identifier", "name", "repositoryRoot", "repositoryType", "primaryLanguage", "defaultAssessmentProfile")):
            raise RepositoryQualificationError("repository definition identity fields must be non-empty strings")
        if not isinstance(definition["metadata"], dict):
            raise RepositoryQualificationError("repository definition metadata must be an object")
        if not Path(definition["repositoryRoot"]).is_dir():
            raise RepositoryQualificationError("repository definition root must be an existing directory")
        if AssessmentProfileRegistry().resolve(definition["defaultAssessmentProfile"]) is None:
            raise RepositoryQualificationError("repository definition references an unknown assessment profile")


class QualificationRegistry:
    """Immutable registry of independently reproducible repository qualifications."""

    def __init__(self, location: str | Path) -> None:
        self.location = Path(location)

    def persist(self, qualification: Mapping[str, Any]) -> dict[str, Any]:
        SchemaRegistry.validate_qualification(qualification)
        identifier = qualification["qualificationId"]
        path = self.location / f"{identifier}.json"
        if path.is_file():
            return {"id": identifier, "path": str(path), "immutable": True, "existing": True}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(qualification, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return {"id": identifier, "path": str(path), "immutable": True, "existing": False}

    def history(self) -> list[dict[str, Any]]:
        records = []
        for path in sorted(self.location.glob("*.json")) if self.location.is_dir() else []:
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                SchemaRegistry.validate_qualification(value)
                records.append(value)
            except (OSError, json.JSONDecodeError, ValueError) as error:
                raise RepositoryQualificationError(f"invalid qualification registry record {path}: {error}") from error
        return sorted(records, key=lambda item: item["timestamp"])


class RepositoryQualification:
    """Projects canonical assessment evidence into a separately registered result."""

    @staticmethod
    def create(definition: Mapping[str, Any], assessment_evidence: Mapping[str, Any]) -> dict[str, Any]:
        SchemaRegistry.validate_assessment(assessment_evidence)
        assessment = assessment_evidence["assessment"]
        runtime_qualification = assessment_evidence["runtimeQualification"]
        decision = assessment_evidence["assessmentDecision"]["decision"]
        if runtime_qualification["level"] != "QUALIFIED":
            status = "BLOCKED"
        elif decision in {"PASS", "PASS_WITH_WARNINGS", "NOT_APPLICABLE"}:
            status = "QUALIFIED"
        else:
            status = "FAILED"
        definition_identity = json.dumps(dict(definition), sort_keys=True, separators=(",", ":"))
        qualification_id = "repository-qualification." + sha256(
            f"{assessment_evidence['integrity']['contentDigest']}:{definition_identity}".encode()).hexdigest()[:24]
        version = str(assessment["schema"]["assessmentVersion"])
        result = {"schema": SchemaRegistry.identity("repository-qualification-evidence", assessment_evidence["runtime"]["version"], version),
                  "qualificationId": qualification_id,
                  "repository": {key: definition[key] for key in ("identifier", "name", "repositoryRoot", "repositoryType", "primaryLanguage", "metadata")},
                  "assessmentProfile": {"identifier": assessment["profile"], "version": assessment["profileVersion"], "hash": assessment["profileHash"]},
                  "runtimeVersion": assessment_evidence["runtime"]["version"], "schemaVersion": assessment_evidence["schemaVersion"],
                  "assessmentDecision": decision, "qualificationStatus": status,
                  "executionDurationMs": assessment["durationMs"], "timestamp": utc_now(),
                  "assessmentEvidenceId": assessment_evidence["integrity"]["contentDigest"],
                  "assessmentExecutionId": assessment_evidence["executionId"]}
        SchemaRegistry.validate_qualification(result)
        return result
