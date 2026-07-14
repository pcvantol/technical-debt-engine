"""Runtime-owned value objects. No capability or adapter behavior belongs here."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any


class StageStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class RuntimeQualification(StrEnum):
    READY = "RUNTIME_READY"
    FAILED = "RUNTIME_FAILED"


@dataclass(frozen=True)
class RuntimeContext:
    repository_root: Path
    repository_id: str
    candidate: dict[str, str]
    configuration: dict[str, Any]
    runtime_version: str
    schema_version: str
    execution_id: str
    working_directory: Path
    temporary_directory: Path
    execution_options: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StageResult:
    identifier: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    status: StageStatus
    result: str
    started_at: str
    finished_at: str

    @property
    def duration_ms(self) -> int:
        start = datetime.fromisoformat(self.started_at)
        finish = datetime.fromisoformat(self.finished_at)
        return int((finish - start).total_seconds() * 1000)


@dataclass(frozen=True)
class RuntimeResult:
    context: RuntimeContext
    stages: tuple[StageResult, ...]
    evidence: dict[str, Any]
    validation: dict[str, Any]
    qualification: RuntimeQualification
    report: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def serialise_context(context: RuntimeContext) -> dict[str, Any]:
    data = asdict(context)
    return {key: str(value) if isinstance(value, Path) else value for key, value in data.items()}
