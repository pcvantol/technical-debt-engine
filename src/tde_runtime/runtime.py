"""Generic orchestration pipeline for the Technical Debt Engine runtime foundation."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4
from typing import Any, Callable

from .configuration import RuntimeConfiguration
from .models import RuntimeContext, RuntimeQualification, RuntimeResult, StageResult, StageStatus, utc_now
from .registries import AdapterRegistry, CapabilityRegistry, PolicyRegistry
from .policy import PolicyEngine, PolicyError
from .query import QueryEngine
from .execution import CapabilityExecutionEngine
from .runtime_qualification import RuntimeQualificationEngine

RUNTIME_VERSION = "0.1.0"
EVIDENCE_SCHEMA_VERSION = "1.0.0"


class Runtime:
    """Stable public API. A future CLI is a consumer of this class, not its owner."""

    _stage_names = (
        "repository-discovery", "repository-inspection", "language-detection",
        "capability-planning", "adapter-planning", "execution-planning",
        "execution-context", "pipeline-execution", "normalization", "validation",
        "policy-evaluation", "qualification", "evidence", "reporting",
    )

    def __init__(self, capability_registry: CapabilityRegistry | None = None,
                 adapter_registry: AdapterRegistry | None = None,
                 policy_engine: PolicyEngine | None = None) -> None:
        self._capability_registry = capability_registry or CapabilityRegistry()
        self._adapter_registry = adapter_registry or AdapterRegistry()
        self._policy_engine = policy_engine or PolicyEngine()
        self._execution_engine = CapabilityExecutionEngine(self._capability_registry, self._adapter_registry)

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
            qualification = RuntimeQualification.READY if values["qualification"]["status"] != "BLOCKED" else RuntimeQualification.FAILED
            return RuntimeResult(context, tuple(stages), evidence, validation, qualification, report)

    def query(self, evidence: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
        """Public read-only canonical-evidence query entrypoint."""
        return QueryEngine().execute(evidence, query)

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
            "execution-planning": lambda: self._execution_engine.plan(context),
            "execution-context": lambda: {"executionId": context.execution_id},
            "pipeline-execution": lambda: self._execution_engine.execute(context),
            "normalization": lambda: values.get("pipeline-execution", {"measurements": [], "findings": []}),
            "validation": lambda: self._validation(context, values.get("pipeline-execution", {})),
            "policy-evaluation": lambda: self._policy(context, values.get("normalization", {})),
            "qualification": lambda: self._qualification(values.get("policy-evaluation", {})),
            "evidence": lambda: self._evidence(context, values.get("validation", self._validation(context, values.get("pipeline-execution", {}))), values.get("normalization", {}), values.get("policy-evaluation", {})),
            "reporting": lambda: self._report(context, values),
        }
        outputs = handlers[identifier]()
        return StageResult(identifier, {"executionId": context.execution_id}, outputs,
                           StageStatus.SUCCESS, "completed", started, utc_now())

    def _policy(self, context: RuntimeContext, normalized: dict[str, Any]) -> dict[str, Any]:
        try:
            policy = self._policy_engine.load(context.configuration, context.repository_root,
                                              context.runtime_version, context.schema_version)
            return self._policy_engine.evaluate(policy, normalized, context.configuration)
        except PolicyError as error:
            return {"policy": None, "decision": "BLOCKED", "triggeredRules": [{"ruleId": "policy.validation", "outcome": "BLOCKING", "reason": str(error)}], "qualificationInputs": {}}

    @staticmethod
    def _qualification(policy_evidence: dict[str, Any]) -> dict[str, Any]:
        """Qualification is deliberately a projection of Policy Engine output only."""
        decision = policy_evidence.get("decision", "BLOCKED")
        return {"status": decision, "policyDecision": decision, "policy": policy_evidence.get("policy"),
                "triggeredRules": policy_evidence.get("triggeredRules", [])}

    @staticmethod
    def _validation(context: RuntimeContext, execution: dict[str, Any]) -> dict[str, Any]:
        execution_evidence = execution.get("executionEvidence", {})
        executed = execution_evidence.get("executedCapabilities", [])
        return {"status": "VALID", "schema": "VALID", "candidateIdentity": "VALID",
                "repositoryIdentity": "VALID", "adapter": "VALID", "analyzer": "VALID",
                "completeness": "COMPLETE" if executed else "INCOMPLETE", "integrity": "VALID",
                "warnings": [] if executed else ["no capability was executed"], "errors": []}

    @staticmethod
    def _evidence(context: RuntimeContext, validation: dict[str, Any], normalized: dict[str, Any], policy_evidence: dict[str, Any]) -> dict[str, Any]:
        generated_at = utc_now()
        seed = f"{context.repository_id}:{context.candidate['id']}:{context.execution_id}"
        return {"schemaId": "tde.evidence", "schemaVersion": context.schema_version,
                "runtime": {"id": "tde", "version": context.runtime_version},
                "executionId": context.execution_id,
                "repository": {"id": context.repository_id, "displayName": "local-repository"},
                "candidate": context.candidate,
                "configurationDigest": RuntimeConfiguration.load(context.configuration).digest(),
                "capabilityResults": normalized.get("capabilityResults", []), "measurements": normalized.get("measurements", []), "findings": normalized.get("findings", []), "executionEvidence": normalized.get("executionEvidence", {}), "validation": validation, "policyEvidence": policy_evidence, "runtimeQualification": RuntimeQualificationEngine().qualify({"validation":validation,"capabilityResults":normalized.get("capabilityResults",[]),"executionEvidence":normalized.get("executionEvidence",{}),"executionId":context.execution_id,"policyEvidence":policy_evidence,"integrity":{"contentDigest":seed}}),
                "timestamps": {"executedAt": generated_at, "generatedAt": generated_at},
                "integrity": {"algorithm": "sha-256", "contentDigest": f"sha256:{sha256(seed.encode()).hexdigest()}"}}

    @staticmethod
    def _report(context: RuntimeContext, values: dict[str, Any]) -> dict[str, Any]:
        execution = values.get("pipeline-execution", {}).get("executionEvidence", {})
        return {"runtimeSummary": {"status": "RUNTIME_READY", "runtimeVersion": context.runtime_version},
                "executionSummary": {"executionId": context.execution_id, "workItems": len(execution.get("workItems", [])),
                                     "plannedCapabilities": execution.get("plannedCapabilities", []),
                                     "executedCapabilities": execution.get("executedCapabilities", []),
                                     "plannedAdapters": execution.get("plannedAdapters", []),
                                     "executedAdapters": execution.get("executedAdapters", [])},
                "qualification": values.get("qualification", {}),
                "environment": {"schemaVersion": context.schema_version, "capabilities": len(execution.get("plannedCapabilities", [])), "adapters": len(execution.get("plannedAdapters", [])),
                                "policies": len(PolicyRegistry().discover())}}
