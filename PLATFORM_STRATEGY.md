# Platform strategy

## Mission and positioning

TDE is an independent capability-based engineering platform for measuring, normalizing, qualifying, and reporting technical debt across projects and languages. It is a reusable product, not a consumer subsystem or plugin.

## Scope and non-goals

The product owns the `tde` CLI, configuration contracts, adapters, canonical model, evidence, qualification, reporting, and releases. It does not own consumer runtime internals, prescribe a CI vendor, or become a project-specific dashboard or bespoke integration layer.

## Evolution and releases

Generation 1 establishes contracts and the first runtime capabilities. Evolution favors independent capabilities, stable evidence, explicit policy, and additive compatibility. Releases progress from bootstrap through alpha, beta, and stable according to [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md); stable public releases begin at `1.0.0`.

## Governance and long-term vision

The product roadmap is owned by TDE governance and prioritized for reusable value, contract integrity, evidence quality, and long-term maintainability. The long-term direction is a trusted technical-debt platform with portable contracts, release gates, IDE support, and optional cloud delivery without vendor lock-in.
