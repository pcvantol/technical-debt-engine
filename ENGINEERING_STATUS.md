# Current Engineering Status

| Field | Current state |
| --- | --- |
| Generation 2 | `COMPLETE` |
| Operational mode | `MAINTENANCE` |
| Current branch | `main` |
| Current runtime | Public `1.1.x` baseline; `1.1.1` is the current published runtime. |
| Current mission | Operational engineering quality platform: observe engineering quality through capability-based, evidence-first analysis. |
| Public contract | Public `tde` CLI, declared configuration, versioned evidence schema, documented exit codes, canonical evidence, and qualification. |
| Capabilities | `code_size`, `complexity`, `coverage`, and `dependency_health`. |
| Consumer posture | Observe-only, non-blocking, public-runtime-only, capability-driven, and repository-independent. |
| Consumer baseline | Seven selected DJConnect consumers execute all four capabilities on `main`, publish evidence artifacts, and are `PASS_WITH_WARNINGS` / `QUALIFIED`. |
| Policy posture | No required checks, merge blocking, soft-fails, suppressions, or repository-specific policy forks. |
| Dependency-health baseline | Latest qualified `main` evidence reports zero outdated dependencies for all seven selected consumers. |
| Next public release | None scheduled. A maintenance release requires a demonstrated operational or consumer need and qualification evidence. |
| Capability governance | A new capability requires an approved architectural assessment showing that an engineering decision cannot be made with the existing capability model. |

## Normal responsibilities

- Bug fixes and public runtime maintenance
- Analyzer and dependency updates
- Compatibility work
- Documentation and governance
- Evidence and qualification compatibility

Routine product findings are handled by consumer repositories. TDE changes are
made only when the platform itself has a demonstrated maintenance need or an
approved capability decision.

Generation 2 history remains preserved in the completed milestones, ADRs,
release records, and `docs/history/prompts/`.
