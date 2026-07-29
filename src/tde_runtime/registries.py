"""Registry boundaries. Entries arrive only in later capability/adapter increments."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


class CapabilityRegistry:
    def discover(self) -> tuple[object, ...]:
        return (
            {"id": "code_size", "version": "0.1.0", "description": "Canonical physical code-size metrics", "outputContract": "tde.code_size.v1", "analyzerSelection": "highest_priority", "qualificationRules": "complete_adapter_evidence", "supportedAnalyzers": ("code_size.cloc",)},
            {"id": "complexity", "version": "1.1.1", "description": "Canonical cross-language cyclomatic-complexity metrics", "outputContract": "tde.complexity.v1", "analyzerSelection": "repository_primary_language", "qualificationRules": "complete_adapter_evidence", "supportedAnalyzers": ("complexity.radon", "complexity.lizard")},
            {"id": "coverage", "version": "0.1.0", "description": "Canonical test coverage metrics from existing artifacts", "outputContract": "tde.coverage.v1", "analyzerSelection": "highest_priority", "qualificationRules": "complete_adapter_evidence", "supportedAnalyzers": ("coverage.artifact",)},
            {"id":"maintainability","version":"0.1.0","status":"VALIDATED"},
            {"id":"dependency_health","version":"1.0.0","description":"Canonical DJConnect dependency-health evidence", "outputContract":"tde.dependency_health.v1", "analyzerSelection":"highest_priority", "qualificationRules":"complete_adapter_evidence", "supportedAnalyzers":("dependency_health.platform",)},
        )


class AdapterRegistry:
    def discover(self) -> tuple[object, ...]:
        return (
            {"id": "code_size.cloc", "version": "0.1.0", "analyzer": "cloc", "capabilities": ("code_size",), "minimumVersion": "2.10", "platforms": ("any",), "priority": 100},
            {"id":"complexity.radon","version":"1.1.1","analyzer":"radon", "capabilities": ("complexity",), "minimumVersion": "6.0", "platforms": ("any",), "languages": ("Python",), "priority": 100},
            {"id":"complexity.lizard","version":"1.1.1","analyzer":"lizard", "capabilities": ("complexity",), "minimumVersion": "1.23", "platforms": ("any",), "languages": ("JavaScript", "TypeScript", "Swift", "C", "C++", "C#"), "priority": 90},
            {"id":"coverage.artifact","version":"0.1.0","analyzer":"coverage-artifact", "capabilities": ("coverage",), "minimumVersion": "1.0", "platforms": ("any",), "priority": 100},
            {"id":"dependency_health.platform","version":"1.0.0","analyzer":"consumer-native", "capabilities": ("dependency_health",), "minimumVersion": "1.0", "platforms": ("any",), "priority": 100},
        )

    def select(self, capability: dict[str, object]) -> dict[str, object] | None:
        supported = set(capability.get("supportedAnalyzers", ()))
        candidates = [item for item in self.discover() if item["id"] in supported and capability["id"] in item.get("capabilities", ())]
        return sorted(candidates, key=lambda item: (-int(item.get("priority", 0)), str(item["id"])))[0] if candidates else None


class PolicyRegistry:
    """Discovery boundary for configuration-driven policy files."""

    def discover(self) -> tuple[object, ...]:
        from .policy import PolicyEngine
        return PolicyEngine().discover()


class AssessmentProfileRegistry:
    """Loads public, declarative assessment profiles."""

    def discover(self) -> tuple[object, ...]:
        directory = Path(__file__).with_name("profiles")
        return tuple(self._read(path) for path in sorted(directory.glob("*.json")))

    def resolve(self, identifier: str | None = None) -> dict[str, object] | None:
        if identifier is not None:
            candidate = Path(identifier)
            if candidate.suffix == ".json" or candidate.exists():
                if not candidate.is_file():
                    raise ValueError(f"assessment profile file does not exist: {candidate}")
                return self._read(candidate)
        profiles = tuple(self.discover())
        if identifier is None:
            defaults = [profile for profile in profiles if profile["metadata"].get("default")]
            return defaults[0] if len(defaults) == 1 else None
        return next((profile for profile in profiles if profile["identifier"] == identifier), None)

    @staticmethod
    def _read(path: Path) -> dict[str, object]:
        try:
            profile = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid assessment profile {path}: {error}") from error
        if not isinstance(profile, dict):
            raise ValueError(f"assessment profile {path} must be an object")
        AssessmentProfileRegistry._validate(profile, path)
        resolved = deepcopy(profile)
        canonical = json.dumps(profile, sort_keys=True, separators=(",", ":"))
        resolved["identity"] = {"identifier": profile["identifier"], "version": profile["version"],
                                "hash": f"sha256:{sha256(canonical.encode()).hexdigest()}", "source": path.name}
        resolved["policyFile"] = str((path.parent / profile["policy"]["file"]).resolve())
        return resolved

    @staticmethod
    def _validate(profile: dict[str, object], path: Path) -> None:
        required = {"identifier", "version", "description", "capabilities", "policy", "metadata"}
        missing = required - set(profile)
        if missing:
            raise ValueError(f"assessment profile {path} is missing required fields: {sorted(missing)}")
        if not all(isinstance(profile[key], str) and profile[key] for key in ("identifier", "version", "description")):
            raise ValueError(f"assessment profile {path} identity fields must be non-empty strings")
        if not isinstance(profile["metadata"], dict) or not isinstance(profile["metadata"].get("default"), bool):
            raise ValueError(f"assessment profile {path} metadata.default must be boolean")
        if not isinstance(profile["policy"], dict) or not isinstance(profile["policy"].get("file"), str):
            raise ValueError(f"assessment profile {path} policy.file must be a string")
        if not (path.parent / profile["policy"]["file"]).is_file():
            raise ValueError(f"assessment profile {path} policy file does not exist")
        capabilities = profile["capabilities"]
        if not isinstance(capabilities, list) or not capabilities:
            raise ValueError(f"assessment profile {path} capabilities must be a non-empty array")
        available = {item["id"] for item in CapabilityRegistry().discover()}
        identifiers: set[str] = set()
        for capability in capabilities:
            if not isinstance(capability, dict) or not isinstance(capability.get("identifier"), str):
                raise ValueError(f"assessment profile {path} capabilities require an identifier")
            identifier = capability["identifier"]
            if identifier not in available:
                raise ValueError(f"assessment profile {path} references unknown capability: {identifier}")
            if identifier in identifiers:
                raise ValueError(f"assessment profile {path} contains duplicate capability: {identifier}")
            if not isinstance(capability.get("required"), bool) or not isinstance(capability.get("optional"), bool) or capability["required"] == capability["optional"]:
                raise ValueError(f"assessment profile {path} capability {identifier} must select exactly one of required or optional")
            identifiers.add(identifier)
