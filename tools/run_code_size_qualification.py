#!/usr/bin/env python3
"""Run the installed-wheel Code Size qualification on one CI matrix target."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from typing import Any

from code_size_projection import analytical_projection


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "code-size-cross-platform"
OUTPUT = ROOT / "qualification"


def run(command: list[str], *, expected: set[int] = {0}, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(command, text=True, capture_output=True, encoding="utf-8", env=env)
    if completed.returncode not in expected:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")
    return {"invocation": command, "exitCode": completed.returncode,
            "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-1000:], "_raw": completed.stdout}


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    for file in sorted(item for item in path.rglob("*") if item.is_file()):
        hasher.update(file.relative_to(path).as_posix().encode())
        hasher.update(file.read_bytes().replace(b"\r\n", b"\n"))
    return "sha256:" + hasher.hexdigest()


def executable(venv: Path, name: str) -> str:
    directory = venv / ("Scripts" if os.name == "nt" else "bin")
    return str(directory / (f"{name}.exe" if os.name == "nt" else name))


def command_record(command: dict[str, Any]) -> dict[str, Any]:
    return {"invocation": [Path(str(item)).name if Path(str(item)).is_absolute() else item
                            for item in command["invocation"]],
            "exitCode": command["exitCode"],
            "outputDigest": "sha256:" + hashlib.sha256(command["_raw"].encode()).hexdigest()}


def main() -> int:
    wheel = Path(os.environ["TDE_WHEEL"]).resolve()
    tool_directory = Path(os.environ["TDE_CLOC_DIRECTORY"]).resolve()
    if not wheel.is_file() or not tool_directory.is_dir():
        raise SystemExit("TDE_WHEEL and TDE_CLOC_DIRECTORY must identify the provisioned artifacts")
    target = f"{platform.system().lower()}-py{sys.version_info.major}.{sys.version_info.minor}"
    OUTPUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tde-code-size-") as temporary:
        temporary_path = Path(temporary)
        fixture = temporary_path / "fixture"
        shutil.copytree(FIXTURE, fixture)
        venv = temporary_path / "venv"
        run([sys.executable, "-m", "venv", str(venv)])
        python, tde = executable(venv, "python"), executable(venv, "tde")
        base_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        installed_environment = {**base_environment, "PATH": str(Path(tde).parent) + os.pathsep + str(tool_directory) + os.pathsep + base_environment.get("PATH", "")}
        run([python, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", str(wheel)])
        missing_analyzer = run([tde, "--format", "json", "assess", "--capability", "code-size", str(fixture)], expected={5}, env={**base_environment, "PATH": str(Path(tde).parent)})
        fake_tools = temporary_path / "fake-cloc"
        fake_tools.mkdir()
        fake_cloc = fake_tools / ("cloc.cmd" if os.name == "nt" else "cloc")
        fake_cloc.write_text("@echo 2.09\r\n" if os.name == "nt" else "#!/bin/sh\necho 2.09\n", encoding="utf-8")
        if os.name != "nt":
            fake_cloc.chmod(0o755)
        fake_environment = {**base_environment, "PATH": str(fake_tools) + os.pathsep + str(Path(tde).parent)}
        unsupported_analyzer = run([python, "-c", "import sys; from pathlib import Path; from tde_runtime.code_size import analyze; "
                                    "result = analyze(Path(sys.argv[1])); assert result['status'] == 'ANALYZER_NOT_FOUND'; "
                                    "assert result['limitations'][0]['id'] == 'analyzer.cloc.unsupported_version'; print('blocked')", str(fixture)], env=fake_environment)
        timeout_script = """from pathlib import Path
from subprocess import TimeoutExpired
from unittest.mock import patch
from tde_runtime.code_size import analyze
with patch('tde_runtime.code_size.shutil.which', return_value='cloc'), patch('tde_runtime.code_size.subprocess.run', side_effect=TimeoutExpired(['cloc'], 1)):
    result = analyze(Path('.'), timeout=1)
assert result['status'] == 'FAILED_CLOSED'
assert result['limitations'][0]['id'] == 'analyzer.cloc.failed'
print('blocked')
"""
        timeout_behavior = run([python, "-c", timeout_script], env=installed_environment)
        shutil.rmtree(fixture / ".tde", ignore_errors=True)
        commands = {
            "version": run([tde, "--format", "json", "--version"], env=installed_environment),
            "inspect": run([tde, "--format", "json", "inspect", str(fixture)], expected={0, 3}, env=installed_environment),
            "assess": run([tde, "--format", "json", "assess", "--capability", "code-size", str(fixture)], env=installed_environment),
            "validate": run([tde, "--format", "json", "validate", str(fixture)], expected={0, 3}, env=installed_environment),
            "query": run([tde, "--format", "json", "query", str(fixture), "--resource", "metrics"], env=installed_environment),
            "report": run([tde, "--format", "markdown", "report", "--capability", "code-size", str(fixture)], env=installed_environment),
        }
        dogfood = temporary_path / "technical-debt-engine"
        shutil.copytree(ROOT, dogfood, ignore=shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__", ".tde", "qualification"))
        dogfood_assessment = run([tde, "--format", "json", "assess", "--capability", "code-size", str(dogfood)], env=installed_environment)
        assessment = json.loads(commands["assess"]["_raw"])
        evidence_id = assessment["evidenceId"].removeprefix("sha256:")
        evidence_path = fixture / ".tde" / "evidence" / "evidence" / f"{evidence_id}.json"
        record = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence = record["evidence"]
        validation = run([python, "-c", "from tde_runtime.evidence_store import EvidenceStore; "
                          f"EvidenceStore({str(fixture / '.tde' / 'evidence')!r}).retrieve({evidence_id!r}); print('valid')"])
        tampered = json.loads(evidence_path.read_text(encoding="utf-8"))
        tampered["evidence"]["measurements"][0]["value"] = -999
        evidence_path.write_text(json.dumps(tampered), encoding="utf-8")
        tamper = run([python, "-c", "from tde_runtime.evidence_store import EvidenceStore; "
                      f"EvidenceStore({str(fixture / '.tde' / 'evidence')!r}).retrieve({evidence_id!r})"], expected={1})
        analyzer = evidence["adapterResults"][0]["analyzer"]
        result = {
            "schemaVersion": "1.0.0", "repository": "pcvantol/technical-debt-engine",
            "candidateSha": os.environ.get("GITHUB_SHA", "local"), "workflow": os.environ.get("GITHUB_WORKFLOW", "local"),
            "workflowRun": os.environ.get("GITHUB_RUN_ID"), "operatingSystem": platform.platform(),
            "pythonVersion": platform.python_version(), "packageVersion": json.loads(commands["version"]["_raw"])["cliVersion"],
            "wheelChecksum": digest(wheel), "capability": {"id": "code_size", "version": "0.1.0"},
            "adapter": {"id": "code_size.cloc", "version": "0.1.0"}, "analyzer": analyzer,
            "fixture": {"path": "fixtures/code-size-cross-platform", "digest": tree_digest(FIXTURE)},
            "configurationDigest": evidence["configurationDigest"], "evidenceId": assessment["evidenceId"],
            "commands": {name: command_record(command) for name, command in commands.items()},
            "dogfooding": {"target": "technical-debt-engine", "assessment": command_record(dogfood_assessment)},
            "persistence": {"result": "PASS", "evidencePath": ".tde/evidence/evidence/<digest>.json"},
            "missingAnalyzer": {"result": "PASS", "command": command_record(missing_analyzer)},
            "unsupportedAnalyzer": {"result": "PASS", "command": command_record(unsupported_analyzer)},
            "timeoutBehavior": {"result": "PASS", "command": command_record(timeout_behavior)},
            "persistedEvidenceValidation": command_record(validation),
            "tamperDetection": {"result": "PASS", "command": command_record(tamper)},
            "analyticalProjection": analytical_projection(evidence),
            "qualification": {"technicalExecution": "PASS", "policyAssessmentExit": 0, "decision": "PENDING_MATRIX_COMPARISON"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "limitations": ["The fixture contains only deterministic text inputs; raw native output and execution metadata are excluded from comparison."],
        }
    path = OUTPUT / f"code-size-{target}.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / f"code-size-{target}.md").write_text(
        f"# Code Size cross-platform qualification — {target}\n\n"
        f"- Wheel: `{result['wheelChecksum']}`\n- cloc: `{analyzer['version']}`\n"
        "- Technical execution: PASS\n- Persisted query/report: PASS\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
