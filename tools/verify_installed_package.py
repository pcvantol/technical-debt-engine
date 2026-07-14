#!/usr/bin/env python3
"""Verify wheel and source-distribution installations using only ``tde``."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


def executable(environment: Path, name: str) -> Path:
    directory = environment / ("Scripts" if os.name == "nt" else "bin")
    return directory / (f"{name}.exe" if os.name == "nt" else name)


def run(command: list[str], environment: dict[str, str], accepted: set[int] = {0}) -> dict[str, object]:
    completed = subprocess.run(command, text=True, capture_output=True, check=False, env=environment)
    if completed.returncode not in accepted:
        raise RuntimeError(f"{' '.join(command)} exited {completed.returncode}: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


def qualify(distribution: Path, build_tools: Path) -> None:
    with TemporaryDirectory(prefix="tde-installed-") as temporary:
        root = Path(temporary)
        environment = root / "venv"
        child_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, env=child_environment)
        pip, tde = executable(environment, "pip"), executable(environment, "tde")
        subprocess.run([str(pip), "install", "--require-hashes", "--no-deps", "-r", str(build_tools)], check=True,
                       env=child_environment, capture_output=True, text=True)
        subprocess.run([str(pip), "install", "--no-deps", "--no-build-isolation", str(distribution)], check=True,
                       env=child_environment, capture_output=True, text=True)
        target, store = root / "target", root / "evidence"
        target.mkdir(); (target / "sample.py").write_text("def value():\n    return 1\n", encoding="utf-8")
        config = target / "tde.json"
        config.write_text(json.dumps({"capabilities": {"code_size": {"enabled": True}, "complexity": {"enabled": True}}}),
                          encoding="utf-8")
        common = [str(tde), "--format", "json", "--config", str(config), "--store-location", str(store),
                  "--policy-override", 'code_size.repository_lines={"warning":0,"blocking":100000}',
                  "--policy-override", 'complexity.maximum={"warning":0,"blocking":100000}',
                  "--policy-override", 'critical.finding={"enabled":false}']
        run([str(tde), "--format", "json", "--version"], child_environment)
        run(common + ["validate", str(target)], child_environment)
        run(common + ["inspect", str(target)], child_environment)
        run(common + ["assess", "--capability", "code-size", str(target)], child_environment, {0, 1})
        run(common + ["baseline", "--name", "initial", "--capability", "code-size", str(target)], child_environment, {0, 1})
        (target / "sample.py").write_text("def value():\n    return 2\n\ndef second():\n    return 3\n", encoding="utf-8")
        run(common + ["compare", "--baseline", "initial", "--capability", "code-size", str(target)], child_environment, {0, 1})
        run(common + ["query", str(target), "--resource", "comparisons"], child_environment)
        report = run(common + ["report", "--capability", "code-size", str(target)], child_environment)
        if report.get("schemaId") != "tde.report" or report.get("content", {}).get("capability") != "code_size":
            raise RuntimeError("installed package did not render a Code Size report")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--sdist", type=Path, required=True)
    parser.add_argument("--build-tools", type=Path, default=Path("requirements/build-tools.txt"))
    arguments = parser.parse_args()
    for distribution in (arguments.wheel, arguments.sdist):
        qualify(distribution.resolve(), arguments.build_tools.resolve())
    print(json.dumps({"installedDistributions": [arguments.wheel.name, arguments.sdist.name], "status": "VALID"}, sort_keys=True))


if __name__ == "__main__":
    main()
