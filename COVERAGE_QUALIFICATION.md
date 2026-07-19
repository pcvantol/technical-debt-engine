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

## Post-merge completion proof — 2026-07-19

The branch-collection changes were subsequently merged in the two Python
consumer repositories and their fresh post-merge artifacts were assessed with
the public CLI:

| Repository | Source CI artifact | Canonical result |
| --- | --- | --- |
| `djconnect` | Run `29683579286`, `ha-cobertura-coverage`, main `b2681ad` | 37,275 / 42,486 lines (87.73%) and 6,566 / 9,528 branches (68.91%); `VALID` / `QUALIFIED`. |
| `djconnect-pi` | Run `29683630590`, `pi-cobertura-coverage`, main `55a2f34` | 4,201 / 5,594 lines (75.10%) and 1,063 / 1,704 branches (62.38%); `VALID` / `QUALIFIED`. |

This completes the live-artifact proof for the read-only Coverage capability.
It does not activate a required TDE CI check; that phased consumer rollout is
still G2-D work.

## Platform coverage snapshot — 2026-07-19

The read-only platform scan consumes the latest non-expired coverage artifact
from each repository. Values below are repository-provided coverage, not a
cross-repository quality score.

| Repository | Artifact format | Line coverage | Branch coverage | TDE result |
| --- | --- | ---: | ---: | --- |
| `djconnect` | coverage.py XML | 37,275 / 42,486 (87.73%) | 6,566 / 9,528 (68.91%) | `VALID` / `QUALIFIED` |
| `djconnect-pi` | coverage.py XML | 4,201 / 5,594 (75.10%) | 1,063 / 1,704 (62.38%) | `VALID` / `QUALIFIED` |
| `djconnect-api` | Cobertura XML | 509 / 571 (89.14%) | 354 / 459 (77.12%) | `VALID` / `QUALIFIED` |
| `djconnect-website` | Cobertura XML | 198 / 205 (96.59%) | 29 / 35 (82.86%) | `VALID` / `QUALIFIED` |
| `djconnect-windows` | coverage.py XML | 4,348 / 5,031 (86.42%) | 1,324 / 2,138 (61.93%) | `VALID` / `QUALIFIED` |
| `djconnect-app` | xccov JSON | 27,492 / 72,210 (38.07%) | unavailable | `VALID` / `QUALIFIED` |
| `djconnect-esp32` | Cobertura XML | 628 / 707 (88.83%) | 980 / 1,619 (60.53%) | `VALID` / `QUALIFIED` |
| `djconnect-firmware` | no artifact | unavailable | unavailable | explicit unavailable evidence when assessed without an artifact |

## Supported artifact boundary

Cobertura-compatible XML, including coverage.py XML, LCOV, and the JSON summary
emitted by `xcrun xccov view --json` are supported.
Cobertura method-level line entries are excluded from repository totals because
they duplicate their owning class lines. A `0/0` XML branch summary without
branch records is represented as unavailable rather than 100% coverage.
Unsupported report formats, test execution, coverage generation, test-health
analysis, and consumer CI installation remain outside this capability. The
latter is G2-D work.
