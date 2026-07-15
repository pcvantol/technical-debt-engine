"""Canonical, fail-closed operational Software Assurance evidence."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable

from .configuration import RuntimeConfiguration

ASSURANCE_SCHEMA_VERSION = "1.0.0"
_ACTION_SHA = re.compile(r"^\s*-\s*uses:\s*[^@\s]+@[0-9a-f]{40}(?:\s+#.*)?\s*$")


def _canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def _digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return "sha256:" + hasher.hexdigest()


def _git(root: Path, *arguments: str) -> tuple[bool, str]:
    completed = subprocess.run(["git", "-C", str(root), *arguments], text=True, capture_output=True, check=False)
    return completed.returncode == 0, completed.stdout.strip()


class SoftwareAssurance:
    """Evaluate repository and candidate artifacts without delivery or release behavior."""

    def assure(self, root: str | Path, artifact_directories: Iterable[str | Path] = ()) -> dict[str, Any]:
        root = Path(root).resolve(); limitations: list[str] = []
        repository = self._repository(root, limitations); dependencies = self._dependencies(root, limitations)
        workflows = self._workflows(root, limitations); configuration = self._configuration(root, limitations)
        documentation = self._documentation(root, limitations)
        artifacts = self._artifacts(tuple(Path(item).resolve() for item in artifact_directories), limitations)
        checks = {"repositoryIntegrity": repository["integrity"], "dependencyIntegrity": dependencies["integrity"],
                  "artifactIntegrity": artifacts["integrity"], "workflowIntegrity": workflows["integrity"],
                  "configurationIntegrity": configuration["integrity"], "documentationIntegrity": documentation["integrity"],
                  "buildProvenanceVerification": artifacts["provenanceVerified"]}
        required = ("repositoryIntegrity", "dependencyIntegrity", "workflowIntegrity", "configurationIntegrity", "documentationIntegrity")
        failed = not all(checks[name] for name in required) or (bool(artifacts["directories"]) and not checks["artifactIntegrity"])
        decision = "FAIL" if failed else "PASS_WITH_WARNINGS" if limitations else "PASS"
        evidence = {"schemaId": "tde.software-assurance", "schemaVersion": ASSURANCE_SCHEMA_VERSION,
                    "repository": repository, "dependencies": dependencies, "artifacts": artifacts, "workflows": workflows,
                    "configuration": configuration, "documentation": documentation, "checks": checks,
                    "limitations": limitations, "decision": decision}
        evidence["assuranceId"] = "assurance.sha256." + sha256(_canonical(evidence)).hexdigest()
        evidence["qualification"] = decision
        return evidence

    @staticmethod
    def _repository(root: Path, limitations: list[str]) -> dict[str, Any]:
        valid, candidate = _git(root, "rev-parse", "HEAD"); _, branch = _git(root, "branch", "--show-current")
        _, remote = _git(root, "config", "--get", "remote.origin.url"); status_ok, dirty = _git(root, "status", "--porcelain")
        integrity = valid and status_ok and not dirty and bool(branch)
        if not valid: limitations.append("repository identity is unavailable")
        if not branch: limitations.append("candidate is detached from a branch")
        if dirty: limitations.append("working tree is not clean")
        return {"identity": remote or "local", "candidateIdentity": "candidate.git." + candidate if candidate else None,
                "branch": branch or None, "workingTreeClean": not bool(dirty), "integrity": integrity}

    @staticmethod
    def _dependencies(root: Path, limitations: list[str]) -> dict[str, Any]:
        project = root / "pyproject.toml"; build_tools = root / "requirements" / "build-tools.txt"; pinned = hashes = False
        if project.is_file():
            match = re.search(r"requires\s*=\s*\[([^]]*)\]", project.read_text(encoding="utf-8"), re.DOTALL)
            pinned = bool(match and re.findall(r'"[^"\n]+==[^"\n]+"', match.group(1)))
        if build_tools.is_file():
            content = build_tools.read_text(encoding="utf-8"); hashes = "--hash=sha256:" in content and "Generated with:" in content
        integrity = project.is_file() and pinned and build_tools.is_file() and hashes
        if not integrity: limitations.append("dependency declarations, exact versions, and hash-locked build provenance are incomplete")
        return {"declaration": str(project.relative_to(root)), "buildTools": str(build_tools.relative_to(root)),
                "exactVersions": pinned, "reproducible": hashes, "provenance": hashes, "integrity": integrity}

    @staticmethod
    def _workflows(root: Path, limitations: list[str]) -> dict[str, Any]:
        directory = root / ".github" / "workflows"; files = sorted(directory.glob("*.y*ml")) if directory.is_dir() else []
        contents = [item.read_text(encoding="utf-8") for item in files]
        action_lines = [line for content in contents for line in content.splitlines() if "uses:" in line]
        immutable = bool(action_lines) and all(_ACTION_SHA.match(line) for line in action_lines)
        least_privilege = any(re.search(r"^permissions:\s*\n\s+contents:\s+read\s*$", content, re.MULTILINE) for content in contents)
        package_build = any(item.name == "package-build.yml" and "tools/package_build.py" in content and "--require-hashes" in content for item, content in zip(files, contents))
        integrity = bool(files) and immutable and least_privilege and package_build
        if not integrity: limitations.append("workflow immutability, least privilege, or reproducible-build coverage is incomplete")
        return {"workflowCount": len(files), "immutableActions": immutable, "leastPrivilege": least_privilege,
                "buildReproducibility": package_build, "integrity": integrity}

    @staticmethod
    def _configuration(root: Path, limitations: list[str]) -> dict[str, Any]:
        schema = root / "schemas" / "configuration.schema.json"; project = root / "pyproject.toml"; config = root / ".tde.yml"
        compatible = False; provenance = None
        try:
            compatible = schema.is_file() and json.loads(schema.read_text(encoding="utf-8"))["properties"]["schemaVersion"]["const"] == "1.0.0"
            if config.is_file(): provenance = RuntimeConfiguration.discover(root).digest()
        except (KeyError, ValueError, json.JSONDecodeError): pass
        integrity = schema.is_file() and project.is_file() and compatible
        if not integrity: limitations.append("configuration schema compatibility or provenance is unavailable")
        return {"schema": str(schema.relative_to(root)), "schemaCompatible": compatible, "configurationDigest": provenance, "integrity": integrity}

    @staticmethod
    def _documentation(root: Path, limitations: list[str]) -> dict[str, Any]:
        required = ("README.md", "ENGINEERING_METHOD.md", "RUNTIME_ARCHITECTURE.md", "INTEGRATION_MODEL.md", "PACKAGING.md")
        missing = [item for item in required if not (root / item).is_file()]
        if missing: limitations.append("canonical documentation is missing: " + ", ".join(missing))
        return {"required": list(required), "missing": missing, "architectureConsistent": not missing,
                "governanceConsistent": not missing, "integrity": not missing}

    @staticmethod
    def _artifacts(directories: tuple[Path, ...], limitations: list[str]) -> dict[str, Any]:
        if not directories:
            limitations.append("no candidate artifact directory was supplied; artifact integrity and reproducibility were not evaluated")
            return {"directories": [], "records": [], "checksumsVerified": False, "identityVerified": False,
                    "reproducible": False, "provenanceVerified": False, "integrity": False}
        records: list[dict[str, Any]] = []; valid = True; identities: list[list[tuple[str, str]]] = []
        for directory in directories:
            manifest = directory / "SHA256SUMS"; provenance = directory / "build-provenance.json"
            artifacts = sorted([*directory.glob("*.whl"), *directory.glob("*.tar.gz")]) if directory.is_dir() else []
            try:
                expected = {line.split(maxsplit=1)[1]: "sha256:" + line.split(maxsplit=1)[0] for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()}
                source = json.loads(provenance.read_text(encoding="utf-8")); recorded = {item["filename"]: item["digest"] for item in source["artifacts"]}
                current = {item.name: _digest(item) for item in artifacts}; directory_valid = len(artifacts) == 2 and current == expected == recorded and bool(source.get("candidateSha"))
            except (OSError, ValueError, KeyError, IndexError, json.JSONDecodeError): directory_valid = False; current = {}
            valid = valid and directory_valid; identities.append(sorted(current.items()))
            records.append({"directory": str(directory), "artifactCount": len(artifacts), "verified": directory_valid,
                            "artifacts": [{"filename": name, "digest": digest} for name, digest in sorted(current.items())]})
        reproducible = valid and len(identities) > 1 and all(identity == identities[0] for identity in identities[1:])
        if not valid: limitations.append("candidate artifact checksums, identities, or build provenance are invalid")
        if len(directories) == 1: limitations.append("one candidate artifact directory was supplied; reproducibility requires an independent second candidate")
        elif not reproducible: limitations.append("candidate artifacts are not byte-identical across independent builds")
        return {"directories": [str(item) for item in directories], "records": records, "checksumsVerified": valid,
                "identityVerified": valid, "reproducible": reproducible, "provenanceVerified": valid, "integrity": valid and reproducible}
