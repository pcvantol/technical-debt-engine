# Product backlog

## Current

- P0: make `tde assess --capability code-size` execute a real analyzer and produce truthful canonical evidence.
- P0: fail Runtime Qualification closed for missing selected/required capability evidence.
- P1: make persisted Evidence Store records queryable and prove baseline/compare on real capability evidence, following [Persistence Architecture](docs/product/PERSISTENCE_ARCHITECTURE.md).
- P1: establish repeatable package dependencies, provenance and an approved release workflow before any release claim, following the canonical [Deployment Strategy](docs/product/DEPLOYMENT_STRATEGY.md).
- P1: after R1-GOV-2 merges, create and certify a mainline-snapshot Internal Release Candidate; do not promote the superseded R1-2B sibling candidate.

## Completed

- P1: qualify Policy Engine evaluation and CLI decision exits using persisted Code Size and Complexity evidence.

## Planned

- Add Complexity only after isolated package execution is proven.
- Extend capability ecosystems only after the minimal Code Size CLI vertical slice is stable.
- Complete reporting from Query results only after persisted-query integration.

## Future

- Architecture Health and Documentation Health capabilities.
- Release gates, IDE integration, and a cloud dashboard.

## Research

- Cross-language normalization methods.
- Evidence retention and provenance models.
- Reliable trend analysis across schema and adapter versions.
