# DJConnect dependency-health inventory

## Platform consumer set

Dependency Health is a DJConnect-platform capability. The validated platform
baseline assesses every active DJConnect repository; it does not select a
single consumer. Each assessment remains repository-scoped. G2-D will select
the small set of pipelines that retain canonical evidence in normal CI.

| Repository | Ecosystem / package manager | Dependency source | Native outdated evidence |
| --- | --- | --- | --- |
| `djconnect` | Python / pip | `requirements-dev.txt`, verification requirements | `pip index versions` for pinned requirements |
| `djconnect-pi` | Python / pip | `pyproject.toml` | Explicit unavailable when requirements are not pinned |
| `djconnect-api` | npm | `package.json`, `package-lock.json` | `npm outdated --json --package-lock-only` |
| `djconnect-website` | npm | `package.json`, `package-lock.json` | `npm outdated --json --package-lock-only` |
| `djconnect-windows` | NuGet / dotnet | `*.csproj` | `dotnet package list --outdated --include-transitive --format json` |
| `djconnect-app` | SwiftPM | `Package.swift` | No external dependencies currently; zero dependencies is explicit evidence |
| `djconnect-esp32` | PlatformIO | `platformio.ini` | `pio pkg outdated` |
| `djconnect-firmware` | none | release artifacts only | Explicit unavailable/no manifest evidence |

## Boundary

The capability normalizes package-manager output; it does not install, update,
publish, resolve, or rewrite dependencies. Unavailable native data is retained
per ecosystem rather than guessed. A failed native analysis, including a NuGet
restore failure, blocks the capability rather than reporting healthy zero
metrics. SwiftPM projects without external dependencies do not invoke Swift;
their zero-dependency evidence is derived from the manifest. For NuGet, outdated
evidence includes direct and transitive packages when the native output supplies
a newer version. CVE data, licenses, SBOMs, supply-chain governance, and
automatic remediation remain post-1.0.

Generated dependency artifacts, including SwiftPM, Xcode-derived, PlatformIO,
and release-output directories, are excluded before manifest discovery and
candidate hashing. They cannot change dependency evidence or make a repository
scan scale with local build output.

## G2-B closure baseline — 2026-07-19

The public CLI assessed all repositories above after the bounded ecosystem,
native-error handling, NuGet-transitive-outdated, and generated-artifact
exclusion fixes. Each dependency-health capability result was `VALID` and the
runtime qualification was `QUALIFIED`.

| Repository | Direct | Transitive | Outdated | Recorded condition |
| --- | ---: | ---: | ---: | --- |
| `djconnect` | 3 | unavailable | 3 | Pinned PyPI requirements. |
| `djconnect-pi` | 4 | unavailable | unavailable | Direct requirements are unpinned, so pip outdated evidence is explicitly unavailable. |
| `djconnect-api` | 6 | 208 | 4 | npm lockfile assessment. |
| `djconnect-website` | 2 | 87 | 1 | npm lockfile assessment. |
| `djconnect-windows` | 6 | 15 | 15 | NuGet evidence after the repository's restore repair and package servicing. |
| `djconnect-app` | 0 | unavailable | 0 | SwiftPM manifest has no external dependencies. |
| `djconnect-esp32` | 7 | unavailable | 1 | PlatformIO package assessment. |
| `djconnect-firmware` | unavailable | unavailable | unavailable | No supported dependency manifest. |

This is a platform discovery and capability-qualification baseline, not proof
that every repository already has a required CI check. Pilot selection and the
observe → warn → soft-fail → required progression remain G2-D work.
