"""Registry boundaries. Entries arrive only in later capability/adapter increments."""

from __future__ import annotations


class CapabilityRegistry:
    def discover(self) -> tuple[object, ...]:
        return ()


class AdapterRegistry:
    def discover(self) -> tuple[object, ...]:
        return ()
