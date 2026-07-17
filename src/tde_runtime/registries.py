"""Registry boundaries. Entries arrive only in later capability/adapter increments."""

from __future__ import annotations


class CapabilityRegistry:
    def discover(self) -> tuple[object, ...]:
        return (
            {"id": "code_size", "version": "0.1.0", "description": "Canonical physical code-size metrics", "outputContract": "tde.code_size.v1", "analyzerSelection": "highest_priority", "qualificationRules": "complete_adapter_evidence", "supportedAnalyzers": ("code_size.cloc",)},
            {"id": "complexity", "version": "0.1.0", "description": "Canonical cyclomatic-complexity metrics", "outputContract": "tde.complexity.v1", "analyzerSelection": "highest_priority", "qualificationRules": "complete_adapter_evidence", "supportedAnalyzers": ("complexity.radon",)},
            {"id":"maintainability","version":"0.1.0","status":"VALIDATED"},{"id":"dependency_health","version":"0.1.0","status":"VALIDATED"},
        )


class AdapterRegistry:
    def discover(self) -> tuple[object, ...]:
        return (
            {"id": "code_size.cloc", "version": "0.1.0", "analyzer": "cloc", "capabilities": ("code_size",), "minimumVersion": "2.10", "platforms": ("any",), "priority": 100},
            {"id":"complexity.radon","version":"0.1.0","analyzer":"radon", "capabilities": ("complexity",), "minimumVersion": "6.0", "platforms": ("any",), "priority": 100},
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
