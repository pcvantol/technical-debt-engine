"""CLI framework that consumes only the public Runtime API."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Sequence, TextIO

from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.assessment import AssessmentError, AssessmentOrchestrator
from tde_runtime.baseline import BaselineError, BaselineRepository, ComparisonEngine, ComparisonRepository
from tde_runtime.policy import PolicyEngine, PolicyError
from tde_runtime.trend import TrendEngine
from tde_runtime.evidence_store import EvidenceStore
from tde_runtime.runtime_qualification import RuntimeQualificationEngine
from tde_runtime.software_assurance import SoftwareAssurance
from tde_runtime.trusted_delivery import TrustedDelivery
from tde_runtime.release_qualification import ReleaseQualification
from tde_runtime.release_certification import ReleaseCertification
from tde_runtime.runtime import EVIDENCE_SCHEMA_VERSION, RUNTIME_VERSION
from tde_runtime.schemas import SchemaRegistry
from tde_runtime.repository_qualification import (QualificationRegistry,
                                                  RepositoryDefinitionRegistry,
                                                  RepositoryQualification,
                                                  RepositoryQualificationError)
from tde_runtime.differential import AssessmentBaselineRegistry, DifferentialEngine, DifferentialError


CLI_VERSION = "1.0.4"
GENERATION = "1"


class ExitCode:
    SUCCESS = 0
    WARNING = 1
    FAILED_CLOSED = 2
    EXECUTION_ERROR = 3
    NOT_SUPPORTED = 4
    ANALYZER_NOT_FOUND = 5
    # Compatibility aliases for existing non-runtime commands.
    FAILED = FAILED_CLOSED
    BLOCKED = EXECUTION_ERROR


def _policy_exit_code(decision: str) -> int:
    """The CLI maps canonical Policy decisions; it never re-evaluates policy."""
    return {"PASS": ExitCode.SUCCESS, "PASS_WITH_WARNINGS": ExitCode.WARNING,
            "FAIL": ExitCode.FAILED, "BLOCKED": ExitCode.BLOCKED,
            "NOT_APPLICABLE": ExitCode.NOT_SUPPORTED}.get(decision, ExitCode.BLOCKED)


COMMANDS: dict[str, dict[str, str]] = {
    "help": {"purpose": "Show generated CLI help."},
    "validate": {"purpose": "Validate runtime configuration and context."},
    "inspect": {"purpose": "Inspect a target and planned Code Size execution."},
    "assess": {"purpose": "Assess a target through selected capabilities."},
    "schema": {"purpose": "List the public, versioned assessment schemas."},
    "baseline": {"purpose": "Create an immutable baseline from persisted canonical evidence."},
    "compare": {"purpose": "Persist and qualify a canonical comparison against a baseline."},
    "diff": {"purpose": "Compare a current assessment with an immutable baseline."},
    "trend": {"purpose": "Aggregate canonical evidence history into trends."},
    "query": {"purpose": "Query canonical engineering evidence."},
    "store": {"purpose": "Persist canonical Runtime evidence."},
    "history": {"purpose": "List persisted canonical evidence."},
    "run": {"purpose": "Execute registered capabilities through the Execution Engine."},
    "qualify": {"purpose": "Qualify canonical Runtime evidence."},
    "assure": {"purpose": "Assure repository and artifact integrity."},
    "trusted-delivery": {"purpose": "Validate immutable candidate and delivery evidence."},
    "release-qualify": {"purpose": "Qualify a release candidate without publication."},
    "certify": {"purpose": "Certify a qualified Internal Release candidate without publication."},
    "report": {"purpose": "Render a Code Size evidence projection."},
    "explain": {"purpose": "Explain a result (not implemented)."},
}


def _global_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--verbose", action="store_true", help="Enable INFO logging.")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error logging.")
    parser.add_argument("--config", help="Path to repository .tde.yml configuration.")
    parser.add_argument("--output", help="Output destination (reserved; console is used now).")
    parser.add_argument("--format", choices=("human", "json", "markdown"), default="human", help="Output format.")
    parser.add_argument("--log-level", choices=("ERROR", "WARNING", "INFO", "DEBUG", "TRACE"), help="Logging level.")
    parser.add_argument("--policy", metavar="FILE", help="Declarative policy configuration file.")
    parser.add_argument("--policy-override", action="append", default=[], metavar="RULE=JSON", help="Override a policy rule with a JSON object.")
    parser.add_argument("--profile", help="Declarative assessment profile for tde assess.")
    parser.add_argument("--baseline-location", help="Directory used for immutable baselines.")
    parser.add_argument("--history-depth", type=int, help="Maximum baseline history depth for trends.")
    parser.add_argument("--store-location", help="Directory used for canonical evidence storage.")
    parser.add_argument("--repository-definition", metavar="FILE", help="Declarative repository definition for tde qualify.")
    parser.add_argument("--qualification-location", help="Directory used for immutable repository qualification records.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tde", description="Technical Debt Engine CLI foundation.")
    parser.add_argument("--version", action="store_true", help="Show CLI, runtime, schema, and generation versions.")
    _global_options(parser)
    subcommands = parser.add_subparsers(dest="command", title="commands")
    for identifier, metadata in COMMANDS.items():
        command = subcommands.add_parser(identifier, help=metadata["purpose"], description=metadata["purpose"])
        command.add_argument("target", nargs="?", default=".", help="Repository target (default: current directory).")
        command.add_argument("--capability", action="append", default=[], help="Enable a registered capability.")
        if identifier == "baseline":
            command.add_argument("--name", help="Immutable baseline name.")
        if identifier in {"compare", "assess", "diff"}:
            command.add_argument("--baseline", help="Baseline name or JSON path.")
        if identifier == "query":
            command.add_argument("--resource", default="repositories", help="Evidence resource.")
            command.add_argument("--filter", action="append", default=[], metavar="KEY=VALUE")
            command.add_argument("--aggregate", choices=("count",))
        if identifier == "assure":
            command.add_argument("--artifact-directory", action="append", default=[], metavar="DIRECTORY",
                                 help="Candidate build directory; repeat for independent reproducibility verification.")
        if identifier == "trusted-delivery":
            command.add_argument("--artifact-directory", action="append", default=[], metavar="DIRECTORY",
                                 help="Candidate build directory; repeat for independent reproducibility verification.")
            command.add_argument("--manifest", metavar="PATH", help="Canonical JSON delivery manifest for this candidate.")
        if identifier == "release-qualify":
            command.add_argument("--artifact-directory", action="append", default=[], metavar="DIRECTORY")
            command.add_argument("--docker-artifact-directory", metavar="DIRECTORY")
            command.add_argument("--manifest-output", required=True, metavar="PATH")
            command.add_argument("--release-capability", action="append", default=[], metavar="CAPABILITY",
                                 help="Required release capability; repeat for every selected capability.")
        if identifier == "certify":
            command.add_argument("--qualification-evidence", required=True, metavar="PATH")
            command.add_argument("--report-output", required=True, metavar="PATH")
    return parser


def _load_configuration(path: str | None, target: str) -> RuntimeConfiguration:
    return RuntimeConfiguration.discover(target, path)


def _configure_logging(arguments: argparse.Namespace) -> None:
    level = arguments.log_level or ("INFO" if arguments.verbose else "ERROR" if arguments.quiet else "WARNING")
    logging.basicConfig(level=logging.DEBUG if level == "TRACE" else getattr(logging, level), format="%(levelname)s %(message)s")


def _render(value: dict[str, Any], output_format: str, stream: TextIO) -> None:
    if output_format == "json":
        print(json.dumps(value, sort_keys=True), file=stream)
        return
    if output_format == "markdown":
        for key, item in value.items():
            print(f"- **{key}:** `{item}`", file=stream)
        return
    for key, item in value.items():
        print(f"{key}: {item}", file=stream)


def _store_location(arguments: argparse.Namespace, target: str) -> Path:
    location = Path(arguments.store_location or ".tde/evidence")
    return location if location.is_absolute() else Path(target) / location


def _qualification_location(arguments: argparse.Namespace, target: str) -> Path:
    location = Path(arguments.qualification_location or ".tde/qualifications")
    return location if location.is_absolute() else Path(target) / location


def _runtime_result(command: str, target: str, configuration: RuntimeConfiguration,
                    store: EvidenceStore | None = None) -> tuple[int, dict[str, Any]]:
    result = Runtime().execute(target, configuration)
    payload = {"command": command, "runtime": result.report["runtimeSummary"],
               "execution": result.report["executionSummary"], "environment": result.report["environment"], "qualification": result.report["qualification"],
               "runtimeQualification": result.evidence["runtimeQualification"], "validation": result.validation,
               "evidence": result.evidence, "evidenceId": result.evidence["integrity"]["contentDigest"]}
    capability_statuses = {item.get("status") for item in result.evidence.get("capabilityResults", [])}
    if "NOT_SUPPORTED" in capability_statuses:
        return ExitCode.NOT_SUPPORTED, payload
    if "ANALYZER_NOT_FOUND" in capability_statuses:
        return ExitCode.ANALYZER_NOT_FOUND, payload
    if "FAILED_CLOSED" in capability_statuses:
        return ExitCode.FAILED_CLOSED, payload
    if store is not None:
        payload["evidenceStore"] = store.persist(result.evidence)
    if command in {"assess", "run"}:
        # Assessment exit codes describe the public execution contract. Policy
        # outcomes are preserved in canonical evidence for consumers to apply;
        # a policy threshold must not masquerade as an analyzer failure.
        if result.evidence["runtimeQualification"]["level"] != "QUALIFIED":
            return ExitCode.EXECUTION_ERROR, payload
        return _policy_exit_code(result.evidence["assessmentDecision"]["decision"]), payload
    return ExitCode.SUCCESS, payload


def _render_capability_report(evidence: dict[str, Any], capability: str, output_format: str, stream: TextIO) -> None:
    metrics = {item["metricKey"]: item["value"] for item in evidence.get("measurements", []) if item.get("scope") == "repository" and item.get("capabilityId") == capability}
    title = "Code Size" if capability == "code_size" else "Complexity"
    payload = {"schemaId": "tde.report", "schemaVersion": evidence["schemaVersion"], "evidenceId": evidence["integrity"]["contentDigest"],
               "format": output_format, "content": {"capability": capability, "metrics": metrics,
               "qualification": evidence["runtimeQualification"]["level"]}}
    if output_format == "markdown":
        print(f"# {title} Report", file=stream)
        print("", file=stream)
        for key, value in sorted(metrics.items()):
            print(f"- **{key}:** {value}", file=stream)
        print(f"- **qualification:** {payload['content']['qualification']}", file=stream)
        return
    _render(payload, output_format, stream)


def main(argv: Sequence[str] | None = None, stdout: TextIO | None = None) -> int:
    stream = stdout or sys.stdout
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.command == "schema":
        _render({"command": "schema", "schemas": list(SchemaRegistry.catalogue())}, arguments.format, stream)
        return ExitCode.SUCCESS
    prepared = _prepare_command(arguments, parser, stream)
    if isinstance(prepared, int): return prepared
    configuration = prepared
    if arguments.command in {"store", "history"}:
        store = EvidenceStore(_store_location(arguments, arguments.target))
        try:
            if arguments.command == "history":
                _render({"command": "history", "records": store.history()}, arguments.format, stream)
                return ExitCode.SUCCESS
            record = Runtime().execute(arguments.target, configuration)
            _render({"command": "store", "record": store.persist(record.evidence)}, arguments.format, stream)
            return ExitCode.SUCCESS
        except (ValueError, OSError, json.JSONDecodeError) as error:
            _render({"command": arguments.command, "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
    return _execute_command(arguments, configuration, stream)


def _prepare_command(arguments: argparse.Namespace, parser: argparse.ArgumentParser, stream: TextIO) -> RuntimeConfiguration | int:
    if arguments.version or not arguments.command or arguments.command == "help":
        if arguments.version:
            _render({"cliVersion": CLI_VERSION, "runtimeVersion": RUNTIME_VERSION, "schemaVersion": EVIDENCE_SCHEMA_VERSION, "generation": GENERATION}, arguments.format, stream)
        else:
            parser.print_help(stream)
        return ExitCode.SUCCESS
    _configure_logging(arguments)
    try:
        configuration = _apply_options(_load_configuration(arguments.config, arguments.target), arguments)
        return _apply_command_configuration(configuration, arguments)
    except (ValueError, AssessmentError) as error:
        _render({"command": arguments.command, "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
        return ExitCode.BLOCKED


def _apply_options(configuration: RuntimeConfiguration, arguments: argparse.Namespace) -> RuntimeConfiguration:
    if arguments.policy or arguments.policy_override:
        values = configuration.as_dict(); policy = dict(values["executionOptions"].get("policy", {})); policy.update({"file": arguments.policy} if arguments.policy else {})
        overrides = dict(policy.get("overrides", {}))
        for item in arguments.policy_override:
            rule, raw_value = item.split("=", 1); overrides[rule] = json.loads(raw_value)
            if not isinstance(overrides[rule], dict): raise ValueError("invalid policy override: override must be a JSON object")
        policy["overrides"] = overrides; values["policy"] = policy; values["executionOptions"].pop("policy", None); configuration = RuntimeConfiguration.load(values)
    if arguments.baseline_location:
        values = configuration.as_dict(); values["baseline"] = {"location": arguments.baseline_location}; values["executionOptions"].pop("baseline", None); configuration = RuntimeConfiguration.load(values)
    if arguments.history_depth is not None:
        if arguments.history_depth < 0: raise ValueError("history depth must not be negative")
        values = configuration.as_dict(); values["trend"] = {"historyDepth": arguments.history_depth}; values["executionOptions"].pop("trend", None); configuration = RuntimeConfiguration.load(values)
    return configuration


def _apply_command_configuration(configuration: RuntimeConfiguration, arguments: argparse.Namespace) -> RuntimeConfiguration:
    if arguments.command in {"assess", "baseline", "compare", "run", "store", "inspect", "validate", "qualify", "report"}:
        for capability in arguments.capability: configuration = configuration.with_capability(capability.replace("-", "_"))
    if arguments.command == "assess":
        return AssessmentOrchestrator().configure(configuration, profile=arguments.profile, capabilities=tuple(item.replace("-", "_") for item in arguments.capability))
    if arguments.command == "release-qualify":
        supported = {"code-size": "code_size", "complexity": "complexity", "coverage": "coverage",
                     "dependency-health": "dependency_health"}
        if not arguments.release_capability or any(item not in supported for item in arguments.release_capability): raise ValueError("release-qualify requires one or more supported --release-capability values")
        for capability in sorted(set(arguments.release_capability)): configuration = configuration.with_capability(supported[capability])
    return configuration


def _execute_command(arguments: argparse.Namespace, configuration: RuntimeConfiguration, stream: TextIO) -> int:
    if arguments.command in {"diff"} or (arguments.command == "assess" and arguments.baseline):
        return _differential_command(arguments, configuration, stream)
    if arguments.command in {"baseline", "compare"}:
        return _baseline_command(arguments, configuration, stream)
    if arguments.command == "trend":
        return _trend_command(arguments, configuration, stream)
    if arguments.command == "query":
        return _query_command(arguments, configuration, stream)
    if arguments.command == "qualify":
        return _qualification_command(arguments, configuration, stream)
    if arguments.command == "report":
        return _report_command(arguments, stream)
    if arguments.command == "assure":
        evidence=SoftwareAssurance().assure(arguments.target,arguments.artifact_directory)
        _render({"command":"assure","assuranceEvidence":evidence},arguments.format,stream)
        return _policy_exit_code(evidence["decision"])
    if arguments.command == "trusted-delivery":
        result=Runtime().execute(arguments.target,configuration)
        assurance=SoftwareAssurance().assure(arguments.target,arguments.artifact_directory)
        evidence=TrustedDelivery().validate(arguments.target,result.evidence,assurance,arguments.manifest)
        _render({"command":"trusted-delivery","trustedDeliveryEvidence":evidence,"softwareAssurance":assurance},arguments.format,stream)
        return _policy_exit_code(evidence["qualification"])
    if arguments.command == "release-qualify":
        result=Runtime().execute(arguments.target,configuration)
        evidence=ReleaseQualification().qualify(arguments.target,result.evidence,arguments.artifact_directory,arguments.manifest_output,
                                                 [item.replace("-", "_") for item in arguments.release_capability], arguments.docker_artifact_directory)
        _render({"command":"release-qualify","releaseQualificationEvidence":evidence},arguments.format,stream)
        return ExitCode.SUCCESS if evidence["decision"] == "RELEASE_QUALIFIED" else ExitCode.FAILED
    if arguments.command == "certify":
        evidence = ReleaseCertification().certify(arguments.qualification_evidence, arguments.report_output)
        _render({"command": "certify", "releaseCertificationEvidence": evidence}, arguments.format, stream)
        return ExitCode.SUCCESS if evidence["decision"] == "RELEASE_CERTIFIED" else ExitCode.BLOCKED
    if arguments.command in {"validate", "inspect", "assess", "run"}:
        if arguments.command in {"assess", "run"}:
            if arguments.command == "run" and not arguments.capability:
                _render({"command": "assess", "status": "NOT_SUPPORTED", "reason": "assess requires an explicit capability."}, arguments.format, stream)
                return ExitCode.NOT_SUPPORTED
        try:
            store = EvidenceStore(_store_location(arguments, arguments.target)) if arguments.command in {"assess", "run"} else None
            code, payload = _runtime_result(arguments.command, arguments.target, configuration, store)
        except (PolicyError, ValueError, OSError, json.JSONDecodeError) as error:
            _render({"status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
        _render(payload, arguments.format, stream)
        return code
    _render({"command": arguments.command, "status": "NOT_IMPLEMENTED",
             "reason": "This command framework is present; its capability behavior is not delivered."}, arguments.format, stream)
    return ExitCode.NOT_SUPPORTED


def _differential_command(arguments, configuration, stream):
    location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
    registry = AssessmentBaselineRegistry(Path(arguments.target) / location if not Path(location).is_absolute() else location)
    store = EvidenceStore(_store_location(arguments, arguments.target))
    try:
        if not arguments.baseline:
            raise DifferentialError("diff requires --baseline")
        current = Runtime().execute(arguments.target, configuration)
        current_record = store.persist(current.evidence)
        baseline = registry.load(arguments.baseline)
        previous = store.retrieve(baseline["assessmentEvidenceId"].removeprefix("sha256:"))["evidence"]
        differential = DifferentialEngine().compare(current.evidence, baseline, previous)
        _render({"command": "diff", "baseline": baseline, "assessmentEvidenceStore": current_record,
                 "assessmentEvidence": current.evidence, "differentialEvidence": differential}, arguments.format, stream)
        return _policy_exit_code(current.evidence["assessmentDecision"]["decision"])
    except (DifferentialError, ValueError, OSError, json.JSONDecodeError) as error:
        _render({"command": "diff", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
        return ExitCode.BLOCKED


def _qualification_command(arguments: argparse.Namespace, configuration: RuntimeConfiguration, stream: TextIO) -> int:
    """Run a profile-driven assessment and register its separate qualification result."""
    try:
        definition = RepositoryDefinitionRegistry().resolve(arguments.target, arguments.repository_definition)
        profile = arguments.profile or definition["defaultAssessmentProfile"]
        configuration = AssessmentOrchestrator().configure(
            configuration, profile=profile,
            capabilities=tuple(item.replace("-", "_") for item in arguments.capability),
        )
        target = str(definition["repositoryRoot"])
        result = Runtime().execute(target, configuration)
        qualification = RepositoryQualification.create(definition, result.evidence)
        assessment_record = EvidenceStore(_store_location(arguments, target)).persist(result.evidence)
        registry_record = QualificationRegistry(_qualification_location(arguments, target)).persist(qualification)
        payload = {"command": "qualify", "repositoryQualification": qualification,
                   "qualificationRegistry": registry_record, "assessmentEvidence": result.evidence,
                   "assessmentEvidenceStore": assessment_record}
        statuses = {item.get("status") for item in result.evidence.get("capabilityResults", [])}
        if "NOT_SUPPORTED" in statuses:
            code = ExitCode.NOT_SUPPORTED
        elif "ANALYZER_NOT_FOUND" in statuses:
            code = ExitCode.ANALYZER_NOT_FOUND
        elif "FAILED_CLOSED" in statuses:
            code = ExitCode.FAILED_CLOSED
        elif qualification["qualificationStatus"] == "BLOCKED":
            code = ExitCode.EXECUTION_ERROR
        else:
            code = _policy_exit_code(qualification["assessmentDecision"])
        _render(payload, arguments.format, stream)
        return code
    except (RepositoryQualificationError, PolicyError, ValueError, OSError, json.JSONDecodeError) as error:
        _render({"command": "qualify", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
        return ExitCode.BLOCKED


def _baseline_command(arguments: argparse.Namespace, configuration: RuntimeConfiguration, stream: TextIO) -> int:
    location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
    repository = BaselineRepository(Path(arguments.target) / location if not Path(location).is_absolute() else location)
    evidence_store = EvidenceStore(_store_location(arguments, arguments.target))
    try:
        current = Runtime().execute(arguments.target, configuration)
        persisted = evidence_store.persist(current.evidence)
        evidence = evidence_store.retrieve(persisted["id"])["evidence"]
        if arguments.command == "baseline": return _create_baseline(arguments, repository, evidence, persisted, stream)
        return _compare_baseline(arguments, repository, current, evidence, persisted, stream)
    except (BaselineError, PolicyError, ValueError) as error:
        _render({"command": arguments.command, "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
        return ExitCode.BLOCKED


def _create_baseline(arguments, repository, evidence, persisted, stream):
    baseline = AssessmentBaselineRegistry(repository.location).create(evidence, arguments.name)
    _render({"command": "baseline", "status": "VALID", "evidenceStore": persisted, "baseline": baseline}, arguments.format, stream)
    return ExitCode.SUCCESS


def _compare_baseline(arguments, repository, current, evidence, persisted, stream):
    if not arguments.baseline: raise BaselineError("compare requires --baseline")
    baseline = repository.load(arguments.baseline)
    if "evidence" not in baseline:
        baseline = {**baseline, "evidence": EvidenceStore(_store_location(arguments, arguments.target)).retrieve(
            baseline["assessmentEvidenceId"].removeprefix("sha256:"))["evidence"]}
    comparison = ComparisonEngine().compare(evidence, baseline)
    policy = PolicyEngine().load(current.context.configuration, current.context.repository_root, current.context.runtime_version, current.context.schema_version)
    normalized = {"measurements": evidence["measurements"], "findings": evidence["findings"], "capabilityResults": evidence["capabilityResults"], "comparison": comparison}
    policy_evidence = PolicyEngine().evaluate(policy, normalized, current.context.configuration)
    persisted_comparison = ComparisonRepository(repository.location.parent / "comparisons").persist(comparison, policy_evidence, baseline)
    _render({"command": "compare", "evidenceStore": persisted, "comparison": comparison, "comparisonStore": persisted_comparison, "policyEvidence": policy_evidence, "qualificationDelta": persisted_comparison["qualificationDelta"]}, arguments.format, stream)
    return ExitCode.BLOCKED if policy_evidence["decision"] == "BLOCKED" else ExitCode.SUCCESS


def _trend_command(arguments, configuration, stream):
    location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
    location = Path(arguments.target) / location if not Path(location).is_absolute() else Path(location)
    try:
        current = Runtime().execute(arguments.target, configuration)
        trend = TrendEngine().build(current.evidence, location, configuration.execution_options.get("trend", {}).get("historyDepth"))
        policy = PolicyEngine().load(current.context.configuration, current.context.repository_root, current.context.runtime_version, current.context.schema_version)
        inputs = {"measurements": current.evidence["measurements"], "findings": current.evidence["findings"], "capabilityResults": current.evidence["capabilityResults"], "trend": trend}
        evidence = PolicyEngine().evaluate(policy, inputs, current.context.configuration)
        _render({"command": "trend", "trendEvidence": trend, "policyEvidence": evidence}, arguments.format, stream)
        return ExitCode.BLOCKED if evidence["decision"] == "BLOCKED" else ExitCode.SUCCESS
    except (ValueError, PolicyError) as error:
        _render({"command": "trend", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream); return ExitCode.BLOCKED


def _query_command(arguments, configuration, stream):
    try:
        filters = dict(item.split("=", 1) for item in arguments.filter)
        records = EvidenceStore(_store_location(arguments, arguments.target)).history()
        if not records: raise ValueError("no persisted evidence is available; run assess first")
        evidence = records[-1]["evidence"]
        location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
        baseline_path = Path(arguments.target) / location if not Path(location).is_absolute() else Path(location)
        comparisons = ComparisonRepository(baseline_path.parent / "comparisons").history()
        baselines = [BaselineRepository(baseline_path).load(path) for path in sorted(baseline_path.glob("*.json"))] if baseline_path.is_dir() else []
        response = Runtime().query(evidence, {"resource": arguments.resource, "filter": filters, "aggregate": arguments.aggregate, "baselines": baselines, "comparisons": comparisons})
        _render({"command": "query", "evidenceId": evidence["integrity"]["contentDigest"], **response}, arguments.format, stream); return ExitCode.SUCCESS
    except (ValueError, PolicyError) as error:
        _render({"command": "query", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream); return ExitCode.BLOCKED


def _report_command(arguments, stream):
    supported = {"code-size": "code_size", "complexity": "complexity"}
    if len(arguments.capability) != 1 or arguments.capability[0] not in supported:
        _render({"command": "report", "status": "NOT_SUPPORTED", "reason": "report requires --capability code-size or --capability complexity"}, arguments.format, stream); return ExitCode.NOT_SUPPORTED
    try:
        capability = supported[arguments.capability[0]]
        records = EvidenceStore(_store_location(arguments, arguments.target)).history()
        evidence = next((record["evidence"] for record in reversed(records) if any(item.get("capabilityId") == capability for item in record["evidence"].get("capabilityResults", []))), None)
        if evidence is None: raise ValueError("no persisted evidence is available for this capability; run assess first")
    except ValueError as error:
        _render({"command": "report", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream); return ExitCode.BLOCKED
    if evidence["runtimeQualification"]["level"] != "QUALIFIED":
        _render({"command": "report", "status": "BLOCKED", "reason": "capability evidence is not qualified"}, arguments.format, stream); return ExitCode.BLOCKED
    _render_capability_report(evidence, capability, arguments.format, stream); return ExitCode.SUCCESS


def console_main() -> None:
    raise SystemExit(main())
