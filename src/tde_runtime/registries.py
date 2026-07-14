"""Registry boundaries. Entries arrive only in later capability/adapter increments."""

from __future__ import annotations


class CapabilityRegistry:
    def discover(self) -> tuple[object, ...]:
        return ({"id": "code_size", "version": "0.1.0", "status": "VALIDATED"},{"id":"complexity","version":"0.1.0","status":"VALIDATED"},{"id":"maintainability","version":"0.1.0","status":"VALIDATED"},{"id":"dependency_health","version":"0.1.0","status":"VALIDATED"})


class AdapterRegistry:
    def discover(self) -> tuple[object, ...]:
        return ({"id": "code_size.cloc", "version": "0.1.0", "analyzer": "cloc"},{"id":"complexity.radon","version":"0.1.0","analyzer":"radon"})
