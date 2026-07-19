"""Consumer-driven dependency-health normalization for DJConnect repositories."""

from __future__ import annotations

import fnmatch
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tomllib
from typing import Any
import xml.etree.ElementTree as ET


ADAPTER_ID = "dependency_health.platform"
ADAPTER_VERSION = "1.0.0"
CAPABILITY_ID = "dependency_health"
CAPABILITY_VERSION = "1.0.0"


def analyze(root: Path, timeout: int) -> dict[str, Any]:
    """Normalize only package ecosystems actually present in a repository."""
    records = []
    if (root / "package.json").is_file(): records.append(_npm(root, timeout))
    python = _python(root, timeout)
    if python is not None: records.append(python)
    nuget = _nuget(root, timeout)
    if nuget is not None: records.append(nuget)
    if (root / "platformio.ini").is_file(): records.append(_platformio(root, timeout))
    if (root / "Package.swift").is_file(): records.append(_swift(root, timeout))
    if not records:
        return _unavailable("no supported dependency manifest was found")
    limitations = [item for record in records for item in record["limitations"]]
    if any(item["blocking"] for item in limitations):
        return {"status": "BLOCKED", "limitations": limitations}
    raw = "\n".join(item["rawOutput"] for item in records)
    return {"status": "VALID", "ecosystems": records, "rawOutput": raw,
            "rawOutputHash": "sha256:" + sha256(raw.encode()).hexdigest(),
            "limitations": limitations}


def _npm(root: Path, timeout: int) -> dict[str, Any]:
    package, lock = root / "package.json", root / "package-lock.json"
    try:
        manifest = json.loads(package.read_text(encoding="utf-8"))
        lock_data = json.loads(lock.read_text(encoding="utf-8")) if lock.is_file() else {}
    except (OSError, json.JSONDecodeError) as error:
        return _blocked("npm", "npm", str(error))
    direct = _npm_direct(manifest); packages = lock_data.get("packages", {})
    if not isinstance(packages, dict): packages = {}
    resolved = sorted(path.removeprefix("node_modules/") for path in packages if path.startswith("node_modules/"))
    unknown = sorted(name for name in direct if lock.is_file() and f"node_modules/{name}" not in packages)
    outdated, analyzer, raw, limitations = _outdated_command("npm", ["npm", "outdated", "--json", "--package-lock-only"], root, timeout)
    return _record("npm", "npm", direct, [name for name in resolved if name not in direct], unknown, outdated, analyzer, raw, limitations)


def _python(root: Path, timeout: int) -> dict[str, Any] | None:
    requirements = _manifest_files(root, "requirements*.txt")
    pyproject = root / "pyproject.toml"
    if not requirements and not pyproject.is_file(): return None
    direct: dict[str, str] = {}
    for path in requirements:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*([A-Za-z0-9_.-]+)\s*(.*)$", line)
            if match and not line.lstrip().startswith(("#", "-")): direct[match.group(1)] = match.group(2).strip()
    if pyproject.is_file():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            for requirement in data.get("project", {}).get("dependencies", []):
                match = re.match(r"^\s*([A-Za-z0-9_.-]+)\s*(.*)$", requirement)
                if match: direct[match.group(1)] = match.group(2).strip()
        except (OSError, tomllib.TOMLDecodeError) as error: return _blocked("PyPI", "pip", str(error))
    pip = shutil.which("pip") or shutil.which("pip3")
    if not pip: return _record("PyPI", "pip", sorted(direct), None, None, None, {"id": "pip", "version": "UNAVAILABLE"}, "", [_limitation("dependency_health.pip.unavailable", "pip was not found on PATH")])
    version = _version(pip, root, timeout); outdated, raw, limitations = [], [], []
    for name, constraint in sorted(direct.items()):
        if not constraint.startswith("=="):
            outdated = None; limitations.append(_limitation("dependency_health.python.outdated.unavailable", f"{name} is not pinned")); continue
        try:
            completed = subprocess.run([pip, "index", "versions", name], cwd=root, capture_output=True, text=True, timeout=timeout, check=True)
            raw.append(completed.stdout); latest = re.search(r"Available versions:\s*([^,\s]+)", completed.stdout)
            if latest and latest.group(1) != constraint[2:]: outdated.append(name)
        except (OSError, subprocess.SubprocessError) as error:
            outdated = None; limitations.append(_limitation("dependency_health.python.outdated.unavailable", str(error)))
    return _record("PyPI", "pip", sorted(direct), None, None, outdated, {"id": "pip", "version": version}, "".join(raw), limitations)


def _nuget(root: Path, timeout: int) -> dict[str, Any] | None:
    projects = _manifest_files(root, "*.csproj")
    if not projects: return None
    direct = []
    for project in projects:
        try: direct.extend(item.attrib["Include"] for item in ET.parse(project).iter() if item.tag.endswith("PackageReference") and "Include" in item.attrib)
        except (ET.ParseError, OSError) as error: return _blocked("NuGet", "dotnet", str(error))
    dotnet = shutil.which("dotnet")
    if not dotnet: return _record("NuGet", "dotnet", sorted(set(direct)), None, None, None, {"id": "dotnet", "version": "UNAVAILABLE"}, "", [_limitation("dependency_health.dotnet.unavailable", "dotnet was not found on PATH")])
    raw, outdated, transitive, limitations = [], [], [], []
    for project in projects:
        try:
            completed = subprocess.run([dotnet, "package", "list", "--project", str(project), "--outdated", "--include-transitive", "--format", "json"], cwd=root, capture_output=True, text=True, timeout=timeout, check=False)
            raw.append(completed.stdout); payload = json.loads(completed.stdout or "{}")
            problems = payload.get("problems", [])
            errors = [item.get("text", "NuGet analysis failed") for item in problems if item.get("level") == "error"]
            if completed.returncode != 0 or errors:
                detail = "; ".join(errors) or completed.stderr.strip() or f"dotnet exited with status {completed.returncode}"
                return _analysis_failed("NuGet", "dotnet", f"{project}: {detail}")
            for project_data in payload.get("projects", []):
                for framework in project_data.get("frameworks", []):
                    outdated.extend(item["id"] for item in framework.get("topLevelPackages", []) if item.get("latestVersion"))
                    outdated.extend(item["id"] for item in framework.get("transitivePackages", []) if item.get("latestVersion"))
                    transitive.extend(item["id"] for item in framework.get("transitivePackages", []) if item.get("id"))
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
            outdated = None; transitive = None; limitations.append(_limitation("dependency_health.nuget.outdated.unavailable", str(error)))
    return _record("NuGet", "dotnet", sorted(set(direct)), None if transitive is None else sorted(set(transitive) - set(direct)), None, None if outdated is None else sorted(set(outdated)), {"id": "dotnet", "version": _version(dotnet, root, timeout)}, "".join(raw), limitations)


def _platformio(root: Path, timeout: int) -> dict[str, Any]:
    direct = []
    lines = (root / "platformio.ini").read_text(encoding="utf-8").splitlines(); in_deps = False
    for line in lines:
        if line.strip().startswith("lib_deps"): in_deps = True; continue
        if in_deps and line and not line[0].isspace(): in_deps = False
        if in_deps and line.strip(): direct.append(line.strip().split("@")[0])
    pio = shutil.which("pio")
    if not pio: return _record("PlatformIO", "PlatformIO", direct, None, None, None, {"id": "pio", "version": "UNAVAILABLE"}, "", [_limitation("dependency_health.platformio.unavailable", "pio was not found on PATH")])
    try:
        completed = subprocess.run([pio, "pkg", "outdated", "-d", str(root)], cwd=root, capture_output=True, text=True, timeout=timeout, check=False)
        raw = completed.stdout + completed.stderr
        outdated = [line.split()[0] for line in raw.splitlines() if re.match(r"^[A-Za-z0-9_.-]+\s+\d", line) and len(line.split()) >= 4 and line.split()[1] != line.split()[3]]
        return _record("PlatformIO", "PlatformIO", sorted(direct), None, None, sorted(set(outdated)), {"id": "pio", "version": _version(pio, root, timeout)}, raw, [])
    except (OSError, subprocess.SubprocessError) as error: return _record("PlatformIO", "PlatformIO", sorted(direct), None, None, None, {"id": "pio", "version": "UNAVAILABLE"}, "", [_limitation("dependency_health.platformio.outdated.unavailable", str(error))])


def _swift(root: Path, timeout: int) -> dict[str, Any]:
    contents = (root / "Package.swift").read_text(encoding="utf-8")
    direct = re.findall(r"\.package\([^\n]*?(?:url|path):\s*\"([^\"]+)", contents)
    analyzer = {"id": "swift", "version": "NOT_REQUIRED"}
    limitations = [] if not direct else [_limitation("dependency_health.swift.outdated.unavailable", "SwiftPM has no non-mutating outdated command")]
    return _record("SwiftPM", "SwiftPM", sorted(direct), None, None, [] if not direct else None, analyzer, "", limitations)


def _record(ecosystem: str, manager: str, direct: list[str], transitive: list[str] | None, unknown: list[str] | None, outdated: list[str] | None, analyzer: dict[str, str], raw: str, limitations: list[dict[str, Any]]) -> dict[str, Any]:
    return {"ecosystem": ecosystem, "packageManager": manager, "directDependencies": direct, "transitiveDependencies": transitive, "unknownDependencies": unknown, "outdatedDependencies": outdated, "analyzer": analyzer, "rawOutput": raw, "limitations": limitations}


def _blocked(ecosystem: str, manager: str, reason: str) -> dict[str, Any]: return _record(ecosystem, manager, [], None, None, None, {"id": manager, "version": "UNAVAILABLE"}, "", [_limitation("dependency_health.manifest.invalid", reason, True)])
def _analysis_failed(ecosystem: str, manager: str, reason: str) -> dict[str, Any]: return _record(ecosystem, manager, [], None, None, None, {"id": manager, "version": "UNAVAILABLE"}, "", [_limitation(f"dependency_health.{manager}.analysis.failed", reason, True)])
def _unavailable(reason: str) -> dict[str, Any]: return {"status": "VALID", "ecosystems": [], "rawOutput": "", "rawOutputHash": "sha256:" + sha256(b"").hexdigest(), "limitations": [_limitation("dependency_health.ecosystem.unavailable", reason)] , "available": False}
def _limitation(identifier: str, description: str, blocking: bool = False) -> dict[str, Any]: return {"id": identifier, "description": description, "cause": "dependency health", "blocking": blocking}
def _version(executable: str, root: Path, timeout: int) -> str:
    try: return subprocess.run([executable, "--version"], cwd=root, capture_output=True, text=True, timeout=timeout, check=True).stdout.strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError): return "UNAVAILABLE"
def _npm_direct(manifest: dict[str, Any]) -> list[str]: return sorted({name for key in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies") for name in manifest.get(key, {}) if isinstance(manifest.get(key), dict)})
def _outdated_command(name: str, command: list[str], root: Path, timeout: int) -> tuple[list[str] | None, dict[str, str], str, list[dict[str, Any]]]:
    executable = shutil.which(name)
    if not executable: return None, {"id": name, "version": "UNAVAILABLE"}, "", [_limitation(f"dependency_health.{name}.unavailable", f"{name} was not found on PATH")]
    try:
        completed = subprocess.run([executable, *command[1:]], cwd=root, capture_output=True, text=True, timeout=timeout, check=False); raw = completed.stdout or "{}"; parsed = json.loads(raw)
        return sorted(parsed) if isinstance(parsed, dict) else None, {"id": name, "version": _version(executable, root, timeout)}, raw, []
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as error: return None, {"id": name, "version": "UNAVAILABLE"}, "", [_limitation(f"dependency_health.{name}.outdated.unavailable", str(error))]
def _manifest_files(root: Path, pattern: str) -> list[Path]:
    manifests = []
    for directory, names, files in os.walk(root):
        names[:] = [name for name in names if not _ignored_directory(name)]
        manifests.extend(Path(directory, name) for name in files if fnmatch.fnmatch(name, pattern))
    return sorted(manifests)


def _ignored_directory(name: str) -> bool:
    return name in {".git", "node_modules", "dist", "build", ".venv", "venv", ".build", ".swiftpm", ".pio", ".release", ".public-release"} or name.startswith(".xcode-derived")
