# Complexity support matrix

TDE 1.1 exposes one public `complexity` capability. Adapter selection is
repository-discovery-driven; consumers never invoke an adapter themselves.

| Language | Adapter | Analyzer | Pin | CI support | Evidence |
| --- | --- | --- | --- | --- | --- |
| Python | `complexity.radon` | Radon | `6.0.1` | Linux, macOS, Windows | canonical, qualified |
| JavaScript | `complexity.lizard` | Lizard | `1.23.0` | Linux, macOS, Windows | canonical, qualified |
| TypeScript | `complexity.lizard` | Lizard | `1.23.0` | Linux, macOS, Windows | canonical, qualified |
| Swift | `complexity.lizard` | Lizard | `1.23.0` | macOS | canonical, qualified |
| C / C++ | `complexity.lizard` | Lizard | `1.23.0` | Linux, macOS, Windows | canonical, qualified |
| C# | `complexity.lizard` | Lizard | `1.23.0` | Linux, macOS, Windows | canonical, qualified |

Lizard is selected because its public CLI emits deterministic CSV with
function-level CCN and source locations, and supports every non-Python language
in the selected DJConnect set. TDE invokes it single-threaded against an
explicit, classified source list. Radon remains the Python adapter.

The shared policy evaluates only primary product languages through
`complexity.cyclomatic.product.maximum` (warning `15`, blocking `30`). Test,
fixture, mock, generated, dependency, build, coverage and verification symbols
remain either excluded from discovery or separately classified; they cannot
inflate the primary product result.

The adapter evidence includes analyzer executable, installed package identity,
version, adapter identity/version, language, platform, raw-output hash and
run-local timestamp through the enclosing assessment. Analyzer unavailability
and invalid evidence are structured fail-closed results, never zeroes.
