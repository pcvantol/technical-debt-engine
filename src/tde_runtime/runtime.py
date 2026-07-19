"""Generic orchestration pipeline for the Technical Debt Engine runtime foundation."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from uuid import uuid4
from typing import Any, Callable

from .configuration import RuntimeConfiguration
from .models import RuntimeContext, RuntimeQualification, RuntimeResult, StageResult, StageStatus, utc_now
from .registries import AdapterRegistry, CapabilityRegistry, PolicyRegistry
from .policy import PolicyEngine
from .query import QueryEngine
from .execution import CapabilityExecutionEngine
from .runtime_qualification import RuntimeQualificationEngine
from .schemas import SchemaRegistry

RUNTIME_VERSION = "0.2.0"
EVIDENCE_SCHEMA_VERSION = "1.0.0"


class Runtime:
    """Stable public API. A future CLI is a consumer of this class, not its owner."""

    _stage_names = (
        "repository-discovery", "repository-inspection", "language-detection",
        "capability-planning", "adapter-planning", "execution-planning",
        "execution-context", "pipeline-execution", "normalization", "validation",
        "policy-evaluation", "qualification", "evidence", "schema-validation", "reporting",
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
            assessment_started_at = utc_now()
            # Policy is configuration, not a post-execution best effort.  Resolve
            # and validate it before planners or analyzers receive any work.
            resolved_policy = self._policy_engine.load(context.configuration, context.repository_root,
                                                       context.runtime_version, context.schema_version)
            stages: list[StageResult] = []
            values: dict[str, Any] = {"capabilities": (), "adapters": (), "resolved-policy": resolved_policy,
                                      "assessment-started-at": assessment_started_at}
            for identifier in self._stage_names:
                result = self._run_stage(identifier, context, values)
                stages.append(result)
                values[identifier] = result.outputs
            validation = values["validation"]
            evidence = values["evidence"]
            validation["schema"] = values["schema-validation"]["status"]
            report = values["reporting"]
            qualification = RuntimeQualification.READY if evidence["runtimeQualification"]["level"] == "QUALIFIED" else RuntimeQualification.FAILED
            return RuntimeResult(context, tuple(stages), evidence, validation, qualification, report)

    def query(self, evidence: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
        """Public read-only canonical-evidence query entrypoint."""
        return QueryEngine().execute(evidence, query)

    def _context(self, root: Path, config: RuntimeConfiguration, temporary: Path) -> RuntimeContext:
        root_digest = self._repository_digest(root)
        return RuntimeContext(
            # Repository identity identifies the checkout; candidate identity identifies
            # its source content.  Conflating the two makes every source revision an
            # incompatible baseline and prevents repository-evolution comparisons.
            repository_root=root, repository_id=self._repository_identity(root),
            candidate={"id": f"candidate.content.{root_digest}", "identityType": "content_digest",
                       "value": f"sha256:{root_digest}", "validationStatus": "VALID"},
            configuration=config.as_dict(), runtime_version=RUNTIME_VERSION,
            schema_version=EVIDENCE_SCHEMA_VERSION, execution_id=f"execution.{uuid4().hex}",
            working_directory=root, temporary_directory=temporary,
            execution_options=config.execution_options or {},
        )

    @staticmethod
    def _repository_digest(root: Path) -> str:
        """Identify source content independently of an absolute checkout path."""
        digest = sha256()
        excluded = {".git", ".tde", "__pycache__", ".venv", "venv", "build", "dist", ".build", ".swiftpm", ".pio", ".release", ".public-release"}
        def included_directory(name: str) -> bool:
            return name not in excluded and not name.startswith(".xcode-derived")
        files = []
        for directory, names, filenames in os.walk(root):
            names[:] = [name for name in names if included_directory(name)]
            files.extend(Path(directory, name) for name in filenames)
        for path in sorted(files):
            relative = path.relative_to(root).as_posix()
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            # Git may materialize text files with CRLF on Windows.  Candidate
            # identity represents source content, not checkout line endings.
            digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
            digest.update(b"\0")
        return digest.hexdigest()[:16]

    @staticmethod
    def _repository_identity(root: Path) -> str:
        """Use the Git origin when available; absolute paths are only a local fallback."""
        try:
            origin = subprocess.run(
                ["git", "-C", str(root), "config", "--get", "remote.origin.url"],
                capture_output=True, text=True, timeout=2, check=False,
            ).stdout.strip().removesuffix(".git").lower()
        except (OSError, subprocess.SubprocessError):
            origin = ""
        value = origin or str(root)
        kind = "git" if origin else "local"
        return f"repository.{kind}.{sha256(value.encode()).hexdigest()[:16]}"

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
            "policy-evaluation": lambda: self._policy(context, values.get("normalization", {}), values["resolved-policy"]),
            "qualification": lambda: self._qualification(values.get("policy-evaluation", {})),
            "evidence": lambda: self._evidence(context, values.get("validation", self._validation(context, values.get("pipeline-execution", {}))), values.get("normalization", {}), values.get("policy-evaluation", {}), values["assessment-started-at"]),
            "schema-validation": lambda: self._schema_validation(values["evidence"]),
            "reporting": lambda: self._report(context, values),
        }
        outputs = handlers[identifier]()
        status = self._stage_status(identifier, outputs)
        return StageResult(identifier, {"executionId": context.execution_id}, outputs,
                           status, "completed" if status == StageStatus.SUCCESS else "blocked", started, utc_now())

    @staticmethod
    def _schema_validation(evidence: dict[str, Any]) -> dict[str, Any]:
        """Validate emitted public evidence before it reaches any consumer."""
        SchemaRegistry.validate_assessment(evidence)
        return {"status": "VALID", "schemas": [item["name"] for item in SchemaRegistry.catalogue()]}

    @staticmethod
    def _stage_status(identifier: str, outputs: dict[str, Any]) -> StageStatus:
        if identifier == "pipeline-execution":
            return StageStatus.SUCCESS if outputs.get("executionEvidence", {}).get("state") == "COMPLETED" else StageStatus.BLOCKED
        if identifier == "validation":
            return StageStatus.SUCCESS if outputs.get("status") == "VALID" and outputs.get("completeness") == "COMPLETE" else StageStatus.BLOCKED
        return StageStatus.SUCCESS

    def _policy(self, context: RuntimeContext, normalized: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
        return self._policy_engine.evaluate(policy, normalized, context.configuration)

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
        selected = bool(execution_evidence.get("plannedCapabilities") or execution_evidence.get("unsupportedCapabilities"))
        complete = bool(executed) and not execution_evidence.get("blockedCapabilities")
        valid = complete or not selected
        return {"status": "VALID" if valid else "BLOCKED", "schema": "VALID", "candidateIdentity": "VALID",
                "repositoryIdentity": "VALID", "adapter": "VALID" if complete else "NOT_APPLICABLE", "analyzer": "VALID" if complete else "NOT_APPLICABLE",
                "completeness": "COMPLETE" if executed else "INCOMPLETE", "integrity": "VALID",
                "warnings": [] if valid else ["selected capability execution is incomplete"],
                "errors": [] if valid else ["required selected capability evidence is missing"]}

    @staticmethod
    def _evidence(context: RuntimeContext, validation: dict[str, Any], normalized: dict[str, Any], policy_evidence: dict[str, Any], assessment_started_at: str) -> dict[str, Any]:
        generated_at = utc_now()
        profile = context.execution_options.get("assessment", {})
        assessment_version = str(profile.get("profileIdentity", {}).get("version") or "1.0.0")
        policy_evidence = dict(policy_evidence)
        policy_evidence["schema"] = SchemaRegistry.identity("policy-evidence", context.runtime_version, assessment_version)
        stable_results = [{key: value for key, value in result.items() if key != "executionTiming"}
                          for result in normalized.get("capabilityResults", [])]
        decision = policy_evidence.get("decision", "BLOCKED")
        decision_evidence = {"schema": SchemaRegistry.identity("assessment-decision-evidence", context.runtime_version, assessment_version),
                             "assessmentId": f"assessment.{context.execution_id.removeprefix('execution.')}",
                             "runtimeVersion": context.runtime_version, "policies": [policy_evidence.get("policy")],
                             "policyConfiguration": policy_evidence.get("policyConfiguration"),
                             "policyResults": policy_evidence.get("triggeredRules", []), "decision": decision,
                             "capabilityEvidenceReference": context.execution_id, "timestamp": generated_at}
        execution = normalized.get("executionEvidence", {})
        adapter_results = {item.get("adapter", {}).get("id"): item for item in normalized.get("adapterResults", [])}
        capability_executions = []
        for result in normalized.get("capabilityResults", []):
            capability_id = result.get("capabilityId")
            adapter_id = next(iter(result.get("adapterIds", [])), None)
            adapter = adapter_results.get(adapter_id, {})
            reference_seed = json.dumps({"candidate": context.candidate["id"], "capability": capability_id,
                                         "result": {key: value for key, value in result.items() if key != "executionTiming"}},
                                        sort_keys=True, separators=(",", ":"), default=str)
            capability_executions.append({"schema": SchemaRegistry.identity("capability-evidence", context.runtime_version, assessment_version),
                                          "capability": capability_id,
                                          "capabilityEvidenceId": f"sha256:{sha256(reference_seed.encode()).hexdigest()}",
                                          "analyzer": adapter.get("analyzer", {}).get("id"),
                                          "analyzerVersion": adapter.get("analyzer", {}).get("version"),
                                          "executionStatus": result.get("status"),
                                          "qualification": "QUALIFIED" if result.get("status") == "VALID" else "BLOCKED",
                                          "durationMs": result.get("executionTiming", {}).get("durationMs", 0)})
        assessment = {"schema": SchemaRegistry.identity("assessment-evidence", context.runtime_version, assessment_version),
                      "assessmentId": decision_evidence["assessmentId"], "runtimeVersion": context.runtime_version,
                      "repository": context.repository_id,
                      "profile": profile.get("profile", "explicit"),
                      "profileVersion": profile.get("profileIdentity", {}).get("version") or assessment_version,
                      "profileHash": profile.get("profileIdentity", {}).get("hash"),
                      "startedAt": assessment_started_at, "completedAt": generated_at,
                      "executionStatus": execution.get("state", "BLOCKED"),
                      "executionPlan": {key: execution.get(key, []) for key in ("plannedCapabilities", "plannedAdapters", "analyzerBindings")},
                      "executedCapabilities": execution.get("executedCapabilities", []),
                      "skippedCapabilities": execution.get("skippedCapabilities", []),
                      "capabilityExecutions": capability_executions, "durationMs": execution.get("durationMs", 0),
                      "assessmentDecision": decision, "policyConfiguration": policy_evidence.get("policyConfiguration")}
        stable_assessment = {key: value for key, value in assessment.items()
                             if key not in {"assessmentId", "startedAt", "completedAt", "durationMs"}}
        stable_assessment["capabilityExecutions"] = [{key: value for key, value in item.items() if key != "durationMs"}
                                                      for item in capability_executions]
        seed = json.dumps({"repository": context.repository_id, "candidate": context.candidate,
                           "configuration": RuntimeConfiguration.load(context.configuration).digest(),
                           "capabilityResults": stable_results,
                           "measurements": normalized.get("measurements", []), "findings": normalized.get("findings", []),
                           "policy": policy_evidence, "assessment": stable_assessment},
                          sort_keys=True, separators=(",", ":"), default=str)
        return {"schemaId": "tde.evidence", "schemaVersion": context.schema_version,
                "schema": SchemaRegistry.identity("assessment-evidence", context.runtime_version, assessment_version),
                "assessmentVersion": assessment_version,
                "runtime": {"id": "tde", "version": context.runtime_version},
                "executionId": context.execution_id,
                "repository": {"id": context.repository_id, "displayName": "local-repository"},
                "candidate": context.candidate,
                "configurationDigest": RuntimeConfiguration.load(context.configuration).digest(),
                "capabilityResults": normalized.get("capabilityResults", []), "adapterResults": normalized.get("adapterResults", []), "measurements": normalized.get("measurements", []), "findings": normalized.get("findings", []), "executionEvidence": normalized.get("executionEvidence", {}), "assessment": assessment, "validation": validation, "policyEvidence": policy_evidence, "assessmentDecision": decision_evidence, "runtimeQualification": RuntimeQualificationEngine().qualify({"validation":validation,"capabilityResults":normalized.get("capabilityResults",[]),"executionEvidence":normalized.get("executionEvidence",{}),"executionId":context.execution_id,"policyEvidence":policy_evidence,"integrity":{"contentDigest":seed}}),
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
