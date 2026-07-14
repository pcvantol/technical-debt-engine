# Implementation Inventory

## Executable modules

- `src/tde_cli/main.py`: argparse CLI, console rendering and command dispatch.
- `src/tde_runtime/runtime.py`: stage loop, context and evidence construction; repository inspection and language detection are minimal/no-op (`languages: []`).
- `execution.py`, `code_size.py`, `complexity.py`, `maintainability.py`, `dependency_health.py`: capability execution paths. Code Size shells out to `cloc`; Complexity shells out to `python -m radon`; dependency discovery reads only three manifest forms.
- `policy.py`, `baseline.py`, `trend.py`, `query.py`, `evidence_store.py`, `runtime_qualification.py`: local engines described in the capability matrix.

## Registry reality

`CapabilityRegistry.discover()` and `AdapterRegistry.discover()` return fixed tuples. They list four capabilities and two adapters, but contain no dynamic discovery, lifecycle validation, supported-language declaration or adapter loading. Runtime planning calls them, while reporting hard-codes `capabilities: 0` and `adapters: 0`. Registry presence is therefore not proof of operational capability.

## Adapter and analyzer reality

- `code_size.cloc` invokes executable `cloc`; observed host version: 2.10.
- `complexity.radon` invokes the active interpreter's `radon` module; observed host version: 6.0.1, but missing in the isolated installed environment.
- Maintainability has no adapter; it computes `max(0, min(100, 100 - complexity_average * 3 - code_lines / 1000))` from supplied metrics.
- Dependency Health has a filesystem adapter only, no package-manager execution or network lookup.

## Explicit no-op or misleading behavior

- Language detection always returns an empty list.
- Validation returns `VALID` unconditionally and does not validate analyzer execution for an empty run.
- Evidence identity is seeded with a random execution ID, so identical content is not reproducibly identified.
- Runtime Qualification marks zero capability results as `QUALIFIED`.
- `assess` and `run` accept capability flags but manual installed invocations produced no executed work items.
- `report` and `explain` return `NOT_IMPLEMENTED`; `assess` without a capability is likewise not supported.
