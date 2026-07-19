# Coverage qualification

Coverage is qualified when TDE reads a pre-existing coverage artifact into
schema-conform canonical evidence through the public CLI. TDE never runs tests,
generates a report, or modifies the consumer repository. A missing artifact is
explicit unavailable evidence; a malformed or internally inconsistent artifact
fails closed.

## G2-A completion baseline — 2026-07-19

The following immutable GitHub Actions artifacts were downloaded read-only and
assessed with the public CLI. They establish the representative qualification
set, not a G2-D consumer-CI rollout.

| Repository | Source CI artifact | Evidence result |
| --- | --- | --- |
| `djconnect` | Run `29681771467`, `ha-cobertura-coverage` | coverage.py XML: 42,454 total lines, 37,242 covered (87.72%); branch coverage unavailable because the artifact reports no branch collection. |
| `djconnect-website` | Run `29448604029`, `website-cobertura-coverage` | Cobertura XML: 96.59% line coverage and 82.86% branch coverage. |
| `djconnect-esp32` | Run `29452119930`, `esp32-native-cobertura-coverage` | Cobertura XML: 88.83% line coverage and 60.53% branch coverage. |

Every record produced `VALID` coverage evidence and `QUALIFIED` runtime
qualification. The website artifact also produced a public-CLI baseline and
differential whose sole capability delta is `coverage`, plus a repository
qualification of `QUALIFIED` with assessment decision `PASS`.

## Supported artifact boundary

Cobertura-compatible XML, including coverage.py XML, and LCOV are supported.
Cobertura method-level line entries are excluded from repository totals because
they duplicate their owning class lines. A `0/0` XML branch summary without
branch records is represented as unavailable rather than 100% coverage.
Unsupported report formats, test execution, coverage generation, test-health
analysis, and consumer CI installation remain outside this capability. The
latter is G2-D work.
