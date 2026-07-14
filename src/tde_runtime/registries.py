"""Registry boundaries. Entries arrive only in later capability/adapter increments."""

from __future__ import annotations


class CapabilityRegistry:
    def discover(self) -> tuple[object, ...]:
        return ({"id": "code_size", "version": "0.1.0", "status": "QUALIFIED"},)


class AdapterRegistry:
    def discover(self) -> tuple[object, ...]:
        return ({"id": "code_size.cloc", "version": "0.1.0", "analyzer": "cloc"},)
