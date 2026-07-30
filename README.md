# Technical Debt Engine

Technical Debt Engine (TDE) is an operational engineering-quality platform.
It observes engineering quality through capability-based, evidence-first
analysis and produces canonical assessment and qualification evidence for
repository-independent consumers.

The current public runtime is `1.1.1`. Generation 2 delivery is complete; TDE
now follows a maintenance-first model for bug fixes, analyzer and dependency
updates, compatibility work, documentation, governance, and public-runtime
maintenance.

## Operating philosophy

TDE intentionally remains:

- Observe-only and non-blocking
- Public: consumers use only the published runtime and public `tde` CLI
- Capability-driven and evidence-first
- Repository-independent

Consumer workflows do not use required checks, merge blocking, soft-fails,
suppressions, internal imports, or repository-specific policy forks.

## Capability model

The public runtime provides four canonical capabilities:

| Capability | Engineering evidence |
| --- | --- |
| `code_size` | Classified repository source-size evidence |
| `complexity` | Primary-product-language cyclomatic-complexity evidence |
| `coverage` | Canonical consumer CI coverage-artifact evidence |
| `dependency_health` | Package-manager-native outdated-dependency evidence |

Python uses Radon for complexity; JavaScript/TypeScript, Swift, C/C++, and C#
use Lizard. All five languages normalize to
`complexity.cyclomatic.product.maximum` and the same policy and qualification
route. See the [capability support matrix](CAPABILITY_SUPPORT_MATRIX.md).

## Public integration contract

Consumers integrate only through the public `tde` CLI, declared
configuration, versioned Evidence Schema, documented exit codes, and released
immutable contracts or artifacts. They must not depend on runtime internals,
private adapter APIs, repository layout, or unreleased behaviour. See
[INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

## Capability governance

New capabilities are not roadmap-driven. An approved architectural assessment
must first prove that a required engineering decision cannot be made using the
existing capability model. The delivery path is architectural assessment,
capability decision, implementation, qualification, public runtime, and then
consumer adoption.

Routine product-quality findings remain owned by consumer repositories.

## Documentation

- [Product roadmap](PRODUCT_ROADMAP.md) and [operational backlog](PRODUCT_BACKLOG.md)
- [Current engineering status](ENGINEERING_STATUS.md)
- [Integration model](INTEGRATION_MODEL.md)
- [Capability support matrix](CAPABILITY_SUPPORT_MATRIX.md)
- [Complexity support detail](docs/complexity-support-matrix.md)
- [Security gap assessment](SECURITY_GAP_ASSESSMENT.md)
- [Evidence schema](EVIDENCE_SCHEMA.md) and [qualification model](QUALIFICATION_MODEL.md)
- [Release architecture](RELEASE_ARCHITECTURE.md) and [release qualification](RELEASE_QUALIFICATION.md)
