# Capability Support Matrix

## Current public baseline

| Field | Supported contract |
| --- | --- |
| Runtime | Public `technical-debt-engine-runtime==1.1.1` |
| Consumer entrypoint | Public `tde` CLI only |
| Execution posture | Observe-only, non-blocking, evidence-first |
| Policy parity | One canonical policy and qualification route; no consumer policy forks |
| Distribution | Published public runtime, exactly pinned by consumers |

## Supported capabilities

| Capability | Canonical analyzer or source | Supported evidence |
| --- | --- | --- |
| `code_size` | `cloc` through `code_size.cloc` | Classified source, test, documentation, comment, blank-line, file, and language measurements |
| `complexity` | Radon or Lizard, selected from canonical primary-product language | `complexity.cyclomatic.product.maximum` and symbol evidence through one policy route |
| `coverage` | Consumer-produced canonical CI coverage artifact | Repository line and branch coverage evidence; TDE does not execute consumer tests |
| `dependency_health` | Native package-manager inventory | Direct, transitive where available, outdated, and unknown-dependency evidence |

## Cross-language complexity parity

| Language | Adapter | Analyzer | Support |
| --- | --- | --- | --- |
| Python | `complexity.radon` | Radon `6.0.1` | Canonical and qualified |
| JavaScript / TypeScript | `complexity.lizard` | Lizard `1.23.0` | Canonical and qualified |
| Swift | `complexity.lizard` | Lizard `1.23.0` | Canonical and qualified |
| C / C++ | `complexity.lizard` | Lizard `1.23.0` | Canonical and qualified |
| C# | `complexity.lizard` | Lizard `1.23.0` | Canonical and qualified |

Complexity evaluates only classified primary-product source. Tests, fixtures,
mocks, generated code, dependencies, build output, coverage output, and
verification harnesses are excluded or separately classified and do not
inflate the primary-product result.

Future capability support requires the architectural-assessment gate described
in [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md) and
[ROADMAP_GOVERNANCE.md](ROADMAP_GOVERNANCE.md).
