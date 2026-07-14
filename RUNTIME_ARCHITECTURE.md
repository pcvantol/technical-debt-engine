# Runtime architecture

The TDE runtime is the canonical execution model for every future capability. It is capability-based, evidence-driven, qualification-based, adapter-based, project-independent, platform-independent, language-independent, vendor-neutral, CLI-first, configuration-driven, extensible, incremental, and fail-closed.

The runtime owns orchestration, identity, planning, dispatch, normalization, validation, qualification, evidence, reporting, and exit status. Adapters own measurement only. Adapters never communicate directly; the runtime coordinates all execution through canonical contracts.

Runtime configuration declares enabled capabilities, adapter selection, thresholds, exclusions, report formats, and qualification policy; see [CONFIGURATION_RUNTIME.md](CONFIGURATION_RUNTIME.md). It contains no project-specific runtime code.

Native analyzers remain authoritative for native analysis. TDE invokes, ingests, normalizes, qualifies, and reports their results; it does not duplicate analyzer logic. Examples include Radon, Lizard, Roslyn, Swift tooling, and ESLint.

The canonical model is a single versioned schema. All capabilities and adapters map into it before downstream validation, qualification, or reporting. Future parallel, incremental, distributed, cached, and cloud execution may extend orchestration without redesigning these boundaries.
