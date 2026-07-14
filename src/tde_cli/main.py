"""CLI framework that consumes only the public Runtime API."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Sequence, TextIO

from tde_runtime import Runtime, RuntimeConfiguration
from tde_runtime.baseline import BaselineError, BaselineRepository, ComparisonEngine
from tde_runtime.policy import PolicyEngine, PolicyError
from tde_runtime.trend import TrendEngine
from tde_runtime.evidence_store import EvidenceStore
from tde_runtime.runtime_qualification import RuntimeQualificationEngine
from tde_runtime.software_assurance import SoftwareAssurance
from tde_runtime.trusted_delivery import TrustedDelivery
from tde_runtime.runtime import EVIDENCE_SCHEMA_VERSION, RUNTIME_VERSION


CLI_VERSION = "0.1.0"
GENERATION = "1"


class ExitCode:
    SUCCESS = 0
    WARNING = 1
    FAILED = 2
    BLOCKED = 3
    NOT_SUPPORTED = 4


COMMANDS: dict[str, dict[str, str]] = {
    "help": {"purpose": "Show generated CLI help."},
    "validate": {"purpose": "Validate runtime configuration and context."},
    "inspect": {"purpose": "Inspect a target through the Runtime foundation."},
    "assess": {"purpose": "Assess technical debt (not implemented)."},
    "baseline": {"purpose": "Create a baseline (not implemented)."},
    "compare": {"purpose": "Compare evidence (not implemented)."},
    "trend": {"purpose": "Aggregate canonical evidence history into trends."},
    "query": {"purpose": "Query canonical engineering evidence."},
    "store": {"purpose": "Persist canonical Runtime evidence."},
    "history": {"purpose": "List persisted canonical evidence."},
    "run": {"purpose": "Execute registered capabilities through the Execution Engine."},
    "qualify": {"purpose": "Qualify canonical Runtime evidence."},
    "assure": {"purpose": "Assure repository and artifact integrity."},
    "trusted-delivery": {"purpose": "Validate immutable candidate and delivery evidence."},
    "report": {"purpose": "Render reports (not implemented)."},
    "explain": {"purpose": "Explain a result (not implemented)."},
}


def _global_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--verbose", action="store_true", help="Enable INFO logging.")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error logging.")
    parser.add_argument("--config", help="Path to JSON-compatible .tde.yml configuration.")
    parser.add_argument("--output", help="Output destination (reserved; console is used now).")
    parser.add_argument("--format", choices=("human", "json"), default="human", help="Output format.")
    parser.add_argument("--log-level", choices=("ERROR", "WARNING", "INFO", "DEBUG", "TRACE"), help="Logging level.")
    parser.add_argument("--policy", help="Repository or workspace policy directory.")
    parser.add_argument("--policy-override", action="append", default=[], metavar="RULE=JSON", help="Override a policy rule with a JSON object.")
    parser.add_argument("--baseline-location", help="Directory used for immutable baselines.")
    parser.add_argument("--history-depth", type=int, help="Maximum baseline history depth for trends.")
    parser.add_argument("--store-location", help="Directory used for canonical evidence storage.")


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
        if identifier == "compare":
            command.add_argument("--baseline", help="Baseline name or JSON path.")
        if identifier == "query":
            command.add_argument("--resource", default="repositories", help="Evidence resource.")
            command.add_argument("--filter", action="append", default=[], metavar="KEY=VALUE")
            command.add_argument("--aggregate", choices=("count",))
    return parser


def _load_configuration(path: str | None) -> RuntimeConfiguration:
    if path is None:
        return RuntimeConfiguration.load()
    try:
        contents = Path(path).read_text(encoding="utf-8")
        return RuntimeConfiguration.load(json.loads(contents))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid configuration: {error}") from error


def _configure_logging(arguments: argparse.Namespace) -> None:
    level = arguments.log_level or ("INFO" if arguments.verbose else "ERROR" if arguments.quiet else "WARNING")
    logging.basicConfig(level=logging.DEBUG if level == "TRACE" else getattr(logging, level), format="%(levelname)s %(message)s")


def _render(value: dict[str, Any], output_format: str, stream: TextIO) -> None:
    if output_format == "json":
        print(json.dumps(value, sort_keys=True), file=stream)
        return
    for key, item in value.items():
        print(f"{key}: {item}", file=stream)


def _runtime_result(command: str, target: str, configuration: RuntimeConfiguration) -> tuple[int, dict[str, Any]]:
    result = Runtime().execute(target, configuration)
    payload = {"command": command, "runtime": result.report["runtimeSummary"],
               "execution": result.report["executionSummary"], "environment": result.report["environment"], "qualification": result.report["qualification"],
               "runtimeQualification": result.evidence["runtimeQualification"], "validation": result.validation,
               "evidence": result.evidence, "evidenceId": result.evidence["integrity"]["contentDigest"]}
    blocked = result.report["qualification"]["status"] == "BLOCKED" or (
        command in {"assess", "run"} and result.evidence["runtimeQualification"]["level"] != "QUALIFIED"
    )
    return (ExitCode.BLOCKED if blocked else ExitCode.SUCCESS), payload


def main(argv: Sequence[str] | None = None, stdout: TextIO | None = None) -> int:
    stream = stdout or sys.stdout
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.version:
        _render({"cliVersion": CLI_VERSION, "runtimeVersion": RUNTIME_VERSION,
                 "schemaVersion": EVIDENCE_SCHEMA_VERSION, "generation": GENERATION}, arguments.format, stream)
        return ExitCode.SUCCESS
    if not arguments.command:
        parser.print_help(stream)
        return ExitCode.SUCCESS
    if arguments.command == "help":
        parser.print_help(stream)
        return ExitCode.SUCCESS
    _configure_logging(arguments)
    try:
        configuration = _load_configuration(arguments.config)
    except ValueError as error:
        _render({"status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
        return ExitCode.BLOCKED
    if arguments.policy or arguments.policy_override:
        values = configuration.as_dict()
        policy = dict(values["executionOptions"].get("policy", {}))
        if arguments.policy:
            policy["repository"] = arguments.policy
        overrides = dict(policy.get("overrides", {}))
        try:
            for item in arguments.policy_override:
                rule, raw_value = item.split("=", 1)
                overrides[rule] = json.loads(raw_value)
                if not isinstance(overrides[rule], dict):
                    raise ValueError("override must be a JSON object")
        except (ValueError, json.JSONDecodeError) as error:
            _render({"status": "BLOCKED", "reason": f"invalid policy override: {error}"}, arguments.format, stream)
            return ExitCode.BLOCKED
        policy["overrides"] = overrides
        values["policy"] = policy
        values["executionOptions"].pop("policy", None)
        configuration = RuntimeConfiguration.load(values)
    if arguments.baseline_location:
        values = configuration.as_dict()
        values["baseline"] = {"location": arguments.baseline_location}
        values["executionOptions"].pop("baseline", None)
        configuration = RuntimeConfiguration.load(values)
    if arguments.history_depth is not None:
        if arguments.history_depth < 0:
            _render({"status": "BLOCKED", "reason": "history depth must not be negative"}, arguments.format, stream)
            return ExitCode.BLOCKED
        values = configuration.as_dict()
        values["trend"] = {"historyDepth": arguments.history_depth}
        values["executionOptions"].pop("trend", None)
        configuration = RuntimeConfiguration.load(values)
    if arguments.command in {"store", "history"}:
        location = Path(arguments.store_location or ".tde/evidence")
        location = Path(arguments.target) / location if not location.is_absolute() else location
        store = EvidenceStore(location)
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
    if arguments.command in {"assess", "baseline", "compare", "run"} and arguments.capability:
        if arguments.capability not in (["code-size"], ["complexity"], ["maintainability"], ["dependency-health"]):
            _render({"command": arguments.command, "status": "NOT_IMPLEMENTED", "reason": "Only validated Generation 1 capabilities are available."}, arguments.format, stream)
            return ExitCode.NOT_SUPPORTED
        values = configuration.as_dict()
        key = {"code-size": "code_size", "dependency-health": "dependency_health"}.get(arguments.capability[0], arguments.capability[0])
        values["capabilities"] = {key: {"enabled": True}}
        values["executionOptions"].pop("capabilities", None)
        configuration = RuntimeConfiguration.load(values)
    if arguments.command in {"baseline", "compare"}:
        location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
        repository = BaselineRepository(Path(arguments.target) / location if not Path(location).is_absolute() else location)
        try:
            current = Runtime().execute(arguments.target, configuration)
            if arguments.command == "baseline":
                baseline = repository.create(current.evidence, arguments.name)
                _render({"command": "baseline", "status": "VALID", "baseline": baseline}, arguments.format, stream)
                return ExitCode.SUCCESS
            if not arguments.baseline:
                raise BaselineError("compare requires --baseline")
            baseline = repository.load(arguments.baseline)
            comparison = ComparisonEngine().compare(current.evidence, baseline)
            policy = PolicyEngine().load(current.context.configuration, current.context.repository_root,
                                         current.context.runtime_version, current.context.schema_version)
            normalized = {"measurements": current.evidence["measurements"], "findings": current.evidence["findings"],
                          "capabilityResults": current.evidence["capabilityResults"], "comparison": comparison}
            policy_evidence = PolicyEngine().evaluate(policy, normalized, current.context.configuration)
            status = ExitCode.BLOCKED if policy_evidence["decision"] == "BLOCKED" else ExitCode.SUCCESS
            _render({"command": "compare", "comparison": comparison, "policyEvidence": policy_evidence}, arguments.format, stream)
            return status
        except (BaselineError, PolicyError, ValueError) as error:
            _render({"command": arguments.command, "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
    if arguments.command == "trend":
        location = configuration.execution_options.get("baseline", {}).get("location", ".tde/baselines")
        location = Path(arguments.target) / location if not Path(location).is_absolute() else Path(location)
        try:
            current = Runtime().execute(arguments.target, configuration)
            trend = TrendEngine().build(current.evidence, location, configuration.execution_options.get("trend", {}).get("historyDepth"))
            policy = PolicyEngine().load(current.context.configuration, current.context.repository_root, current.context.runtime_version, current.context.schema_version)
            policy_evidence = PolicyEngine().evaluate(policy, {"measurements": current.evidence["measurements"], "findings": current.evidence["findings"], "capabilityResults": current.evidence["capabilityResults"], "trend": trend}, current.context.configuration)
            _render({"command": "trend", "trendEvidence": trend, "policyEvidence": policy_evidence}, arguments.format, stream)
            return ExitCode.SUCCESS
        except (ValueError, PolicyError) as error:
            _render({"command": "trend", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
    if arguments.command == "query":
        try:
            filters = dict(item.split("=", 1) for item in arguments.filter)
            result = Runtime().execute(arguments.target, configuration)
            response = Runtime().query(result.evidence, {"resource": arguments.resource, "filter": filters, "aggregate": arguments.aggregate})
            _render({"command": "query", **response}, arguments.format, stream)
            return ExitCode.SUCCESS
        except (ValueError, PolicyError) as error:
            _render({"command": "query", "status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
    if arguments.command == "qualify":
        try:
            result=Runtime().execute(arguments.target,configuration)
            capability=arguments.capability[0].replace("-","_") if arguments.capability else None
            qualification=RuntimeQualificationEngine().qualify(result.evidence,capability)
            _render({"command":"qualify","runtimeQualification":qualification},arguments.format,stream)
            return ExitCode.SUCCESS if qualification["level"]!="BLOCKED" else ExitCode.BLOCKED
        except ValueError as error:
            _render({"command":"qualify","status":"BLOCKED","reason":str(error)},arguments.format,stream); return ExitCode.BLOCKED
    if arguments.command == "assure":
        evidence=SoftwareAssurance().assure(arguments.target)
        _render({"command":"assure","assuranceEvidence":evidence},arguments.format,stream)
        return ExitCode.FAILED if evidence["qualification"] in {"FAIL","BLOCKED"} else ExitCode.WARNING if evidence["qualification"]=="PASS_WITH_WARNINGS" else ExitCode.SUCCESS
    if arguments.command == "trusted-delivery":
        result=Runtime().execute(arguments.target,configuration)
        evidence=TrustedDelivery().validate(arguments.target,result.evidence)
        _render({"command":"trusted-delivery","trustedDeliveryEvidence":evidence,"softwareAssurance":SoftwareAssurance().assure(arguments.target)},arguments.format,stream)
        return ExitCode.FAILED if evidence["qualification"] in {"FAIL","BLOCKED"} else ExitCode.WARNING if evidence["qualification"]=="PASS_WITH_WARNINGS" else ExitCode.SUCCESS
    if arguments.command in {"validate", "inspect", "assess", "run"}:
        if arguments.command in {"assess", "run"}:
            if not arguments.capability:
                _render({"command": "assess", "status": "NOT_IMPLEMENTED", "reason": "Only code-size and complexity are delivered."}, arguments.format, stream)
                return ExitCode.NOT_SUPPORTED
        try:
            code, payload = _runtime_result(arguments.command, arguments.target, configuration)
        except ValueError as error:
            _render({"status": "BLOCKED", "reason": str(error)}, arguments.format, stream)
            return ExitCode.BLOCKED
        _render(payload, arguments.format, stream)
        return code
    _render({"command": arguments.command, "status": "NOT_IMPLEMENTED",
             "reason": "This command framework is present; its capability behavior is not delivered."}, arguments.format, stream)
    return ExitCode.NOT_SUPPORTED


def console_main() -> None:
    raise SystemExit(main())
