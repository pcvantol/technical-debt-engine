# Capability dependencies

Capabilities declare directed dependencies in the registry:

- **Hard dependency:** must be available, enabled, and valid before execution.
- **Soft dependency:** improves behavior when available; absence produces an explicit limitation.
- **Optional capability:** may participate but never blocks the dependent capability.

The runtime validates the complete dependency graph before execution. Cycles, unknown references, incompatible versions, missing hard dependencies, and ambiguous ordering fail closed. A capability may depend on canonical evidence or another capability result, but never communicate directly with an adapter.
