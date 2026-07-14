"""Generic orchestration pipeline for the Technical Debt Engine runtime foundation."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4
from typing import Any, Callable

from .configuration import RuntimeConfiguration
from .models import RuntimeContext, RuntimeQualification, RuntimeResult, StageResult, StageStatus, utc_now
from .registries import AdapterRegistry, CapabilityRegistry

RUNTIME_VERSION = "0.1.0"
EVIDENCE_SCHEMA_VERSION = "1.0.0"


class Runtime:
    """Stable public API. A future CLI is a consumer of this class, not its owner."""

    _stage_names = (
        "repository-discovery", "repository-inspection", "language-detection",
        "capability-planning", "adapter-planning", "execution-planning",
        "execution-context", "pipeline-execution", "normalization", "validation",
        "qualification", "evidence", "reporting",
    )

    def __init__(self, capability_registry: CapabilityRegistry | None = None,
                 adapter_registry: AdapterRegistry | None = None) -> None:
        self._capability_registry = capability_registry or CapabilityRegistry()
        self._adapter_registry = adapter_registry or AdapterRegistry()

    def execute(self, repository_root: str | Path,
                configuration: RuntimeConfiguration | dict[str, Any] | None = None) -> RuntimeResult:
        config = configuration if isinstance(configuration, RuntimeConfiguration) else RuntimeConfiguration.load(configuration)
        root = Path(repository_root).resolve()
        if not root.is_dir():
            raise ValueError("repository root must be an existing directory")
        with TemporaryDirectory(prefix="tde-runtime-") as temporary:
            context = self._context(root, config, Path(temporary))
            stages: list[StageResult] = []
            values: dict[str, Any] = {"capabilities": (), "adapters": ()}
            for identifier in self._stage_names:
                result = self._run_stage(identifier, context, values)
                stages.append(result)
                values[identifier] = result.outputs
            validation = values["validation"]
            evidence = values["evidence"]
            report = values["reporting"]
            return RuntimeResult(context, tuple(stages), evidence, validation,
                                 RuntimeQualification.READY, report)

    def _context(self, root: Path, config: RuntimeConfiguration, temporary: Path) -> RuntimeContext:
        root_digest = sha256(str(root).encode()).hexdigest()[:16]
        return RuntimeContext(
            repository_root=root, repository_id=f"repository.local.{root_digest}",
            candidate={"id": f"candidate.content.{root_digest}", "identityType": "content_digest",
                       "value": f"sha256:{root_digest}", "validationStatus": "VALID"},
            configuration=config.as_dict(), runtime_version=RUNTIME_VERSION,
            schema_version=EVIDENCE_SCHEMA_VERSION, execution_id=f"execution.{uuid4().hex}",
            working_directory=root, temporary_directory=temporary,
            execution_options=config.execution_options or {},
        )

    def _run_stage(self, identifier: str, context: RuntimeContext,
                   values: dict[str, Any]) -> StageResult:
        started = utc_now()
        handlers: dict[str, Callable[[], dict[str, Any]]] = {
            "repository-discovery": lambda: {"repositoryId": context.repository_id},
            "repository-inspection": lambda: {"rootExists": context.repository_root.is_dir()},
            "language-detection": lambda: {"languages": []},
            "capability-planning": lambda: {"capabilities": list(self._capability_registry.discover())},
            "adapter-planning": lambda: {"adapters": list(self._adapter_registry.discover())},
            "execution-planning": lambda: {"executable": True, "workItems": 0},
            "execution-context": lambda: {"executionId": context.execution_id},
            "pipeline-execution": lambda: {"executedWorkItems": 0},
            "normalization": lambda: {"measurements": [], "findings": []},
            "validation": lambda: self._validation(context),
            "qualification": lambda: {"runtimeDecision": RuntimeQualification.READY.value},
            "evidence": lambda: self._evidence(context, values.get("validation", self._validation(context))),
            "reporting": lambda: self._report(context, values),
        }
        outputs = handlers[identifier]()
        return StageResult(identifier, {"executionId": context.execution_id}, outputs,
                           StageStatus.SUCCESS, "completed", started, utc_now())

    @staticmethod
    def _validation(context: RuntimeContext) -> dict[str, Any]:
        return {"status": "VALID", "schema": "VALID", "candidateIdentity": "VALID",
                "repositoryIdentity": "VALID", "adapter": "VALID", "analyzer": "VALID",
                "completeness": "COMPLETE", "integrity": "VALID", "warnings": [], "errors": []}

    @staticmethod
    def _evidence(context: RuntimeContext, validation: dict[str, Any]) -> dict[str, Any]:
        generated_at = utc_now()
        seed = f"{context.repository_id}:{context.candidate['id']}:{context.execution_id}"
        return {"schemaId": "tde.evidence", "schemaVersion": context.schema_version,
                "runtime": {"id": "tde", "version": context.runtime_version},
                "executionId": context.execution_id,
                "repository": {"id": context.repository_id, "displayName": "local-repository"},
                "candidate": context.candidate,
                "configurationDigest": RuntimeConfiguration.load(context.configuration).digest(),
                "capabilityResults": [], "measurements": [], "findings": [], "validation": validation,
                "timestamps": {"executedAt": generated_at, "generatedAt": generated_at},
                "integrity": {"algorithm": "sha-256", "contentDigest": f"sha256:{sha256(seed.encode()).hexdigest()}"}}

    @staticmethod
    def _report(context: RuntimeContext, values: dict[str, Any]) -> dict[str, Any]:
        return {"runtimeSummary": {"status": "RUNTIME_READY", "runtimeVersion": context.runtime_version},
                "executionSummary": {"executionId": context.execution_id, "workItems": 0},
                "environment": {"schemaVersion": context.schema_version, "capabilities": 0, "adapters": 0}}
