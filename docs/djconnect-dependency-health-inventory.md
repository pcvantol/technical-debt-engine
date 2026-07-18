# DJConnect dependency-health inventory

## Platform consumer set

Dependency Health is a DJConnect-platform capability. It executes in every
active DJConnect repository pipeline; it does not select a single consumer.
Each assessment remains repository-scoped, and G2-D will retain the resulting
canonical evidence from every repository for platform-level consumption.

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
per ecosystem rather than guessed. CVE data, licenses, SBOMs, supply-chain
governance, and automatic remediation remain post-1.0.
