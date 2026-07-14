# Dashboard Architecture

## Purpose and boundaries

The Dashboard is TDE's read-only presentation layer for canonical engineering evidence. It visualizes Query Engine results; it never executes analyzers, invokes Runtime, modifies evidence, or becomes an engineering source of truth.

```text
Browser → Dashboard Server → Query Engine → Evidence Store → Canonical Evidence
```

The Dashboard Server hosts static assets, exposes a Query-facing API, and serves presentation state. It is stateless and performs no engineering analysis. The browser is responsive, evidence-driven, presentation-only, and frontend-technology-independent.

## Generation model

| Generation | Product scope |
| --- | --- |
| Generation 1 | Local Dashboard and localhost-only server; filesystem Evidence Store; Query Engine; single user; no authentication. SQLite is a future implementation detail. |
| Generation 2 | Self-hosted and Docker deployment; multiple repositories; repository, trend, qualification and evidence exploration; optional authentication. |
| Generation 3 | Cloud and organization dashboards, multi-user/RBAC, notifications and portfolio analytics are evaluation only. |

## Query and persistence

Dashboard consumers access persisted evidence only through Query Engine results. There is no direct filesystem, SQLite, PostgreSQL, cloud-backend, Runtime, adapter, or analyzer access. Persistence follows [Persistence Architecture](PERSISTENCE_ARCHITECTURE.md): filesystem JSON is authoritative; SQLite and future backends are derived or optional storage concerns.

## Views

Initial views are Repository Overview, Capability Overview, Repository Details, Code Size, Complexity, Maintainability, Dependency Health, Findings, Qualification, Evidence, Trend, Baseline, and Comparison. Generation 2 may add Portfolio, Organization, Repository Health, Engineering Health, Architecture Health, and Documentation Health.

## Deployment and CLI integration

Generation 1 targets are a local executable and local CLI interaction. Future CLI commands such as `tde dashboard` and `tde dashboard serve` only start the separate presentation layer; they do not make Dashboard part of Runtime. Generation 2 adds Docker/self-hosting; Generation 3 evaluates cloud deployment. These are product targets only, not implementations.

## Consumers and API

Individual developers, CI investigators, teams, and future organization users consume read-only presentation. The Dashboard API is a Query-facing projection; a future REST API may provide the same stable boundary. Dashboard must not expose engineering implementation details.
