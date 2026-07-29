# ADR-0065: Cross-language complexity policy parity

## Status

Accepted for the TDE 1.1 implementation increment.

## Context

TDE 1.0.5 publishes one canonical `complexity` capability, but its only
adapter is Radon and therefore only Python product source receives meaningful
complexity evidence. The seven selected DJConnect source consumers use Python,
TypeScript/JavaScript, Swift, C/C++, and C#. Auxiliary Python files must not
substitute for a repository's primary product language.

The existing policy already evaluates the normalized product metric
`complexity.cyclomatic.product.maximum` with warning `15` and blocking `30`.
Those thresholds remain unchanged.

## Decision

TDE 1.1 retains the single `complexity` capability, policy route, assessment
profile and qualification route. It adds registered language adapters, not
language-specific capabilities or policies.

| Product language | Adapter | Analyzer and pin | Platforms | Native output |
| --- | --- | --- | --- | --- |
| Python | `complexity.radon` | `radon==6.0.1` | Linux, macOS, Windows | JSON |
| TypeScript / JavaScript | `complexity.lizard` | `lizard==1.23.0` | Linux, macOS, Windows | CSV |
| Swift | `complexity.lizard` | `lizard==1.23.0` | macOS (also portable Python environments) | CSV |
| C / C++ | `complexity.lizard` | `lizard==1.23.0` | Linux, macOS, Windows | CSV |
| C# | `complexity.lizard` | `lizard==1.23.0` | Linux, macOS, Windows | CSV |

Both analyzers are public Python packages and are exact runtime dependencies.
Radon is retained for Python because its structured Python analysis is the
existing public contract. Lizard is MIT licensed, publicly installable,
version-pinnable and documents function-level CCN, locations, deterministic
single-thread CLI operation, and support for all four added language families.

The adapters normalize every emitted symbol to the existing canonical shape:
repository-relative path, language, symbol name and kind, location, CCN,
product-source classification, adapter and analyzer provenance. Raw analyzer
formats never reach policy evaluation. Each adapter result records executable,
package identity, analyzer version, language, host platform and a stable raw
output digest.

`primaryLanguage` is discovered generically from canonical product-source
files: the recognised language with the highest nonblank source-line count.
Ties are retained as multiple primary languages. The product policy summary is
computed from symbols in those primary languages only. Non-primary symbols
remain symbol-, file-, language- and repository-level evidence, but cannot
satisfy a missing primary-language measurement. This prevents a Windows Python
helper from qualifying C# complexity, without repository-name logic.

One shared source-classification model identifies product, test, fixture,
mock, generated, dependency/vendor, build/cache, verification and coverage
artifact paths. Generated coverage XML/JSON/HTML/intermediates are excluded
from both Code Size discovery and Complexity adapter input while remaining
available to the Coverage capability's configured artifact reader.

Availability is explicit. No applicable product source is valid evidence with
no numeric product metric; unavailable analyzers, unsupported versions,
execution failures, malformed output, empty output for applicable source,
missing locations, partial language analysis, and duplicate symbols are
fail-closed structured limitations. They never become a zero metric or an
implicit PASS.

## Rejected alternatives

- **A new capability per language:** would fork policy, qualification and
  evidence semantics, contrary to the public TDE contract.
- **Consumer-local analyzers or policies:** would make evidence nonportable and
  let consumers bypass the exact public runtime.
- **SwiftLint plus language-specific tools:** SwiftLint's cyclomatic rule is a
  lint violation mechanism rather than a complete, stable symbol metric feed;
  separate toolchains also multiply release and platform qualifications.
- **A TDE parser/CCN algorithm:** forbidden without a separate architectural
  decision; public analyzers already meet the required capability.
- **Let any supported-language result qualify a repository:** auxiliary scripts
  could hide missing primary product coverage.

## Consequences

Raw CCN values remain analyzer-dependent and should not be interpreted as
mathematically interchangeable across languages. They are intentionally
evaluated through one transparent product policy after canonical normalization.
Existing Python/Radon evidence remains valid: TDE 1.1 adds optional provenance
and language summaries without changing the established metric keys or policy
thresholds. Consumers continue to use only the published `tde` CLI and remain
Observe-only.
