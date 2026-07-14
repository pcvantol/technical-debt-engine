# Capability registry

The registry is the sole canonical source for capability discovery. The runtime discovers capabilities only through registry entries; it must not infer capabilities from adapters, consumers, or configuration keys.

## Registration and ownership

Registration requires the complete [capability contract](CAPABILITY_CONTRACT.md), an owner, independent version/status, supported languages, required adapters, metrics, reports, dependency declarations, qualification support, and compatibility statement. TDE capability governance owns registry acceptance; the named owner stewards the entry.

## Generation 1 registry

| ID | Version | Status | Category | Required adapters | Languages | Metrics / reports | Qualification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `code_size` | 0.1.0 | VALIDATED | Measurement | `code_size.cloc` | cloc-supported languages | `code_size.*`; summary | Observational PASS |
| `complexity` | 0.1.0 | VALIDATED | Measurement | `complexity.radon` | Python implemented; others planned | `complexity.cyclomatic.*`; findings | Observational PASS |
| `maintainability` | 0.1.0 | VALIDATED | Measurement | Derived canonical evidence | Code Size + Complexity | `maintainability.index`; summary | Observational PASS |
| `duplication` | 0.x | PLANNED | Measurement | TBD | Adapter-defined | `duplication.*`; findings | Supported when implemented |
| `dependency_health` | 0.x | PLANNED | Measurement | TBD | Adapter-defined | `dependency.*`; findings | Supported when implemented |
| `test_health` | 0.x | PLANNED | Measurement | TBD | Adapter-defined | `test.*`; summary | Supported when implemented |
| `qualification` | 0.x | PLANNED | Qualification | Canonical evidence | All compatible evidence | decision; qualification report | Core |
| `evidence` | 0.x | PLANNED | Infrastructure | Canonical evidence | All | evidence envelope | Not applicable |
| `reporting` | 0.x | PLANNED | Infrastructure | Canonical evidence | All | JSON, Markdown, SARIF | Not applicable |

`TBD` does not indicate an available adapter. No registry entry is implementation scope.
