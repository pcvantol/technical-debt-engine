#!/usr/bin/env python3
"""Run the installed-wheel Complexity qualification on one CI matrix target."""
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


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "complexity-cross-platform"
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
        hasher.update(file.read_bytes())
    return "sha256:" + hasher.hexdigest()


def executable(venv: Path, name: str) -> str:
    directory = venv / ("Scripts" if os.name == "nt" else "bin")
    return str(directory / (f"{name}.exe" if os.name == "nt" else name))


def command_record(command: dict[str, Any]) -> dict[str, Any]:
    """Keep reproducible command evidence without host paths or source text."""
    return {"invocation": [Path(str(item)).name if Path(str(item)).is_absolute() else item
                            for item in command["invocation"]],
            "exitCode": command["exitCode"],
            "outputDigest": "sha256:" + hashlib.sha256(command["_raw"].encode()).hexdigest()}


def main() -> int:
    wheel = Path(os.environ["TDE_WHEEL"]).resolve()
    if not wheel.is_file():
        raise SystemExit(f"TDE_WHEEL does not exist: {wheel}")
    target = f"{platform.system().lower()}-py{sys.version_info.major}.{sys.version_info.minor}"
    OUTPUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tde-complexity-") as temporary:
        temporary_path = Path(temporary)
        fixture = temporary_path / "fixture"
        shutil.copytree(FIXTURE, fixture)
        venv = temporary_path / "venv"
        run([sys.executable, "-m", "venv", str(venv)])
        python, tde = executable(venv, "python"), executable(venv, "tde")
        run([python, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", str(wheel)])
        missing_analyzer = run([tde, "--format", "json", "assess", "--capability", "complexity", str(fixture)], expected={3}, env={**os.environ, "PATH": str(Path(tde).parent)})
        run([python, "-m", "pip", "install", "--disable-pip-version-check", "radon==6.0.1"])
        commands = {
            "version": run([tde, "--format", "json", "--version"]),
            "inspect": run([tde, "--format", "json", "inspect", str(fixture)], expected={0, 3}),
            # A blocking policy result is expected: it proves the analyzer ran
            # and found the fixture's critical symbol.
            "assess": run([tde, "--format", "json", "assess", "--capability", "complexity", str(fixture)], expected={3}),
            "validate": run([tde, "--format", "json", "validate", str(fixture)], expected={0, 3}),
            "query": run([tde, "--format", "json", "query", str(fixture), "--resource", "findings"]),
            "report": run([tde, "--format", "markdown", "report", "--capability", "complexity", str(fixture)]),
        }
        dogfood = temporary_path / "technical-debt-engine"
        shutil.copytree(ROOT, dogfood, ignore=shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__", ".tde", "qualification"))
        dogfood_assessment = run([tde, "--format", "json", "assess", "--capability", "complexity", str(dogfood)], expected={0, 3})
        assessment = json.loads(commands["assess"]["_raw"])
        evidence_id = assessment["evidenceId"].removeprefix("sha256:")
        evidence_path = fixture / ".tde" / "evidence" / "evidence" / f"{evidence_id}.json"
        record = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence = record["evidence"]
        # EvidenceStore validation is the supported persisted-evidence
        # validation path; `validate` validates a target configuration/runtime.
        validation = run([python, "-c", "from tde_runtime.evidence_store import EvidenceStore; "
                          f"EvidenceStore({str(fixture / '.tde' / 'evidence')!r}).retrieve({evidence_id!r}); print('valid')"])
        tampered = json.loads(evidence_path.read_text(encoding="utf-8"))
        tampered["evidence"]["measurements"][0]["value"] = -999
        evidence_path.write_text(json.dumps(tampered), encoding="utf-8")
        tamper = run([python, "-c", "from tde_runtime.evidence_store import EvidenceStore; "
                      f"EvidenceStore({str(fixture / '.tde' / 'evidence')!r}).retrieve({evidence_id!r})"], expected={1})
        evidence_path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        analyzer = evidence["adapterResults"][0]["analyzer"]
        result = {
            "schemaVersion": "1.0.0", "repository": "pcvantol/technical-debt-engine",
            "candidateSha": os.environ.get("GITHUB_SHA", "local"), "workflow": os.environ.get("GITHUB_WORKFLOW", "local"),
            "workflowRun": os.environ.get("GITHUB_RUN_ID"), "operatingSystem": platform.platform(),
            "pythonVersion": platform.python_version(), "packageVersion": json.loads(commands["version"]["_raw"])["cliVersion"],
            "wheelChecksum": digest(wheel), "capability": {"id": "complexity", "version": "0.1.0"},
            "adapter": {"id": "complexity.radon", "version": "0.1.0"}, "analyzer": analyzer,
            "fixture": {"path": "fixtures/complexity-cross-platform", "digest": tree_digest(FIXTURE)},
            "configurationDigest": evidence["configurationDigest"], "evidenceId": assessment["evidenceId"],
            "commands": {name: command_record(command) for name, command in commands.items()},
            "dogfooding": {"target": "technical-debt-engine", "assessment": command_record(dogfood_assessment),
                            "note": "A policy-blocking exit is product debt, not analyzer qualification failure."},
            "persistence": {"result": "PASS", "evidencePath": ".tde/evidence/evidence/<digest>.json"},
            "missingAnalyzer": {"result": "PASS", "command": command_record(missing_analyzer)},
            "persistedEvidenceValidation": command_record(validation),
            "tamperDetection": {"result": "PASS", "command": command_record(tamper)},
            "analyticalProjection": {
                "capabilityResults": evidence["capabilityResults"], "adapter": {key: value for key, value in evidence["adapterResults"][0].items() if key not in {"rawOutput", "executionTiming"}},
                "measurements": evidence["measurements"], "findings": evidence["findings"],
                "runtimeQualification": evidence["runtimeQualification"], "limitations": evidence.get("limitations", []),
            },
            "qualification": {"technicalExecution": "PASS", "policyAssessmentExit": 3, "decision": "PENDING_MATRIX_COMPARISON"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "limitations": ["Policy-blocking fixture findings are expected and are distinct from technical analyzer qualification."],
        }
    path = OUTPUT / f"complexity-{target}.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / f"complexity-{target}.md").write_text(
        f"# Complexity cross-platform qualification — {target}\n\n"
        f"- Wheel: `{result['wheelChecksum']}`\n- Radon: `{analyzer['version']}`\n"
        f"- Technical execution: PASS\n- Policy assessment exit: `3` (expected fixture finding)\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
