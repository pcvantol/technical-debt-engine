# Platform strategy

## Mission and positioning

TDE is an independent capability-based engineering platform for measuring, normalizing, qualifying, and reporting technical debt across projects and languages. It is a reusable product, not a consumer subsystem or plugin.

## Scope and non-goals

The product owns the `tde` CLI, configuration contracts, adapters, canonical model, evidence, qualification, reporting, and releases. It does not own consumer runtime internals, prescribe a CI vendor, or become a project-specific dashboard or bespoke integration layer.

## Generation 2 strategy

Generation 1 is complete and frozen: the Engineering Method, Runtime Architecture, Schema Architecture, Capability Contracts, and Adapter SDK remain canonical foundations. Generation 2 extends them without redesign.

Generation 2 has exactly three engineering programs:

1. **Core Runtime** — independently delivered capabilities and their evidence/qualification contracts.
2. **Platform Evolution** — additive platform surfaces such as storage, query, execution, distribution, and IDE integration.
3. **Innovation Lab** — research-only engineering intelligence hypotheses that require promotion before product delivery.

Evolution favors independent capabilities, stable evidence, explicit policy, and additive compatibility. Releases progress according to [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md); no Generation 2 roadmap entry is a release commitment.

The canonical product deployment model, including Generation 1 targets and future distribution evaluation, is [Deployment Strategy](docs/product/DEPLOYMENT_STRATEGY.md). It remains independent from Runtime Architecture and release execution.

The canonical persistence model is [Persistence Architecture](docs/product/PERSISTENCE_ARCHITECTURE.md). It keeps JSON evidence authoritative while allowing additive local indexing and future optional backends.

The canonical presentation model is [Dashboard Architecture](docs/product/DASHBOARD_ARCHITECTURE.md); it consumes Query results without coupling presentation to Runtime.

## Governance and long-term vision

The product roadmap is owned by TDE governance and prioritized for reusable value, contract integrity, evidence quality, and long-term maintainability. The long-term direction is a trusted technical-debt platform with portable contracts, release gates, IDE support, and optional cloud delivery without vendor lock-in.
