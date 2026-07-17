"""npm dependency-health adapter; it normalizes native npm evidence only."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any


ADAPTER_ID = "dependency_health.npm"
ADAPTER_VERSION = "1.0.0"
CAPABILITY_ID = "dependency_health"
CAPABILITY_VERSION = "1.0.0"


def analyze(root: Path, timeout: int) -> dict[str, Any]:
    """Read an npm project and normalize lockfile plus `npm outdated` evidence.

    npm remains responsible for registry lookups. A missing registry result is
    explicit unavailable evidence, not a substituted dependency calculation.
    """
    package = root / "package.json"
    lock = root / "package-lock.json"
    if not package.is_file() or not lock.is_file():
        return _unavailable("npm project with package-lock.json was not found")
    try:
        manifest = json.loads(package.read_text(encoding="utf-8"))
        lock_data = json.loads(lock.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {"status": "BLOCKED", "limitations": [_limitation("dependency_health.manifest.invalid", str(error), True)]}
    if not isinstance(manifest, dict) or not isinstance(lock_data, dict):
        return {"status": "BLOCKED", "limitations": [_limitation("dependency_health.manifest.invalid", "package metadata must be objects", True)]}

    direct = _direct_dependencies(manifest)
    packages = lock_data.get("packages", {})
    if not isinstance(packages, dict):
        return {"status": "BLOCKED", "limitations": [_limitation("dependency_health.lock.unsupported", "package-lock packages table is unavailable", True)]}
    resolved = _resolved_packages(packages)
    unknown = sorted(name for name in direct if f"node_modules/{name}" not in packages)
    transitive = sorted(name for name in resolved if name not in direct)
    npm = shutil.which("npm")
    if npm is None:
        outdated, analyzer, limitations = None, {"id": "npm", "version": "UNAVAILABLE"}, [_limitation("dependency_health.npm.unavailable", "npm was not found on PATH", False)]
        raw = ""
    else:
        try:
            version = subprocess.run([npm, "--version"], cwd=root, capture_output=True, text=True, timeout=timeout, check=True).stdout.strip()
            completed = subprocess.run([npm, "outdated", "--json", "--package-lock-only"], cwd=root, capture_output=True, text=True, timeout=timeout, check=False)
            raw = completed.stdout or "{}"
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise ValueError("npm outdated did not return an object")
            outdated, analyzer, limitations = sorted(parsed), {"id": "npm", "version": version}, []
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError) as error:
            outdated, analyzer, limitations = None, {"id": "npm", "version": "UNAVAILABLE"}, [_limitation("dependency_health.outdated.unavailable", str(error), False)]
            raw = ""
    return {
        "status": "VALID", "ecosystem": "npm", "packageManager": "npm", "directDependencies": direct,
        "transitiveDependencies": transitive, "unknownDependencies": unknown, "outdatedDependencies": outdated,
        "analyzer": analyzer, "rawOutput": raw, "rawOutputHash": "sha256:" + sha256(raw.encode()).hexdigest(),
        "limitations": limitations,
    }


def _direct_dependencies(manifest: dict[str, Any]) -> list[str]:
    names: set[str] = set()
    for key in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        section = manifest.get(key, {})
        if isinstance(section, dict): names.update(name for name in section if isinstance(name, str))
    return sorted(names)


def _resolved_packages(packages: dict[str, Any]) -> list[str]:
    return sorted(path.removeprefix("node_modules/") for path, value in packages.items()
                  if isinstance(path, str) and path.startswith("node_modules/") and isinstance(value, dict))


def _unavailable(reason: str) -> dict[str, Any]:
    return {"status": "VALID", "ecosystem": "npm", "packageManager": "npm", "directDependencies": [],
            "transitiveDependencies": [], "unknownDependencies": [], "outdatedDependencies": None,
            "analyzer": {"id": "npm", "version": "UNAVAILABLE"}, "rawOutput": "", "rawOutputHash": "sha256:" + sha256(b"").hexdigest(),
            "limitations": [_limitation("dependency_health.ecosystem.unavailable", reason, False)], "available": False}


def _limitation(identifier: str, description: str, blocking: bool) -> dict[str, Any]:
    return {"id": identifier, "description": description, "cause": "dependency health", "blocking": blocking}
