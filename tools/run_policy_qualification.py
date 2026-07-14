"""Installed-wheel policy qualification and dogfood check for GitHub Actions."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


def run(*arguments: str) -> tuple[int, dict[str, object]]:
    completed = subprocess.run([sys.executable, "-c", "from tde_cli.main import console_main; console_main()", *arguments], text=True, capture_output=True, check=False)
    if not completed.stdout:
        raise RuntimeError(completed.stderr)
    return completed.returncode, json.loads(completed.stdout)


def main() -> None:
    with TemporaryDirectory(prefix="tde-policy-") as temporary:
        location = Path(temporary)
        config = location / "policy-config.json"
        config.write_text(json.dumps({"capabilities": {"code_size": {"enabled": True}, "complexity": {"enabled": True}}}), encoding="utf-8")
        store = location / "evidence"
        code, assessment = run("--format", "json", "--config", str(config), "--store-location", str(store),
                               "--policy-override", 'code_size.repository_lines={"warning":0,"blocking":100000}',
                               "--policy-override", 'complexity.maximum={"warning":0,"blocking":100000}',
                               "--policy-override", 'critical.finding={"enabled":false}',
                               "assess", str(ROOT), "--capability", "code-size")
        if code != 1 or assessment["evidence"]["policyEvidence"]["decision"] != "PASS_WITH_WARNINGS":
            raise RuntimeError("real combined policy warning qualification did not succeed")
        capabilities = {item["capabilityId"] for item in assessment["evidence"]["capabilityResults"]}
        if capabilities != {"code_size", "complexity"}:
            raise RuntimeError(f"expected real Code Size and Complexity evidence, got {capabilities}")
        code, query = run("--format", "json", "--store-location", str(store), "query", str(ROOT), "--resource", "policies")
        if code or query["results"][0]["decision"] != "PASS_WITH_WARNINGS":
            raise RuntimeError("persisted policy evidence query failed")
        print(json.dumps({"policyDecision": assessment["evidence"]["policyEvidence"]["decision"],
                          "evidenceId": assessment["evidenceId"], "queryResults": query["results"]}, sort_keys=True))


if __name__ == "__main__":
    main()
