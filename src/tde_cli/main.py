"""CLI framework that consumes only the public Runtime API."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Sequence, TextIO

from tde_runtime import Runtime, RuntimeConfiguration
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
    "qualify": {"purpose": "Qualify evidence (not implemented)."},
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tde", description="Technical Debt Engine CLI foundation.")
    parser.add_argument("--version", action="store_true", help="Show CLI, runtime, schema, and generation versions.")
    _global_options(parser)
    subcommands = parser.add_subparsers(dest="command", title="commands")
    for identifier, metadata in COMMANDS.items():
        command = subcommands.add_parser(identifier, help=metadata["purpose"], description=metadata["purpose"])
        command.add_argument("target", nargs="?", default=".", help="Repository target (default: current directory).")
        command.add_argument("--capability", action="append", default=[], help="Enable a registered capability.")
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
               "execution": result.report["executionSummary"], "environment": result.report["environment"],
               "validation": result.validation, "evidenceId": result.evidence["integrity"]["contentDigest"]}
    return ExitCode.SUCCESS, payload


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
    if arguments.command in {"validate", "inspect", "assess"}:
        if arguments.command == "assess":
            if arguments.capability not in (["code-size"], ["complexity"], ["maintainability"], ["dependency-health"]):
                _render({"command": "assess", "status": "NOT_IMPLEMENTED", "reason": "Only code-size and complexity are delivered."}, arguments.format, stream)
                return ExitCode.NOT_SUPPORTED
            values = configuration.as_dict()
            key={"code-size":"code_size","dependency-health":"dependency_health"}.get(arguments.capability[0],arguments.capability[0]); values["capabilities"] = {key: {"enabled": True}}
            configuration = RuntimeConfiguration.load(values)
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
