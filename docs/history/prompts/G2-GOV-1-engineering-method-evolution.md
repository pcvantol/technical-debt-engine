# G2-GOV-1 — Engineering Method Evolution: Repository Governance Alignment

| Metadata | Value |
| --- | --- |
| Prompt ID | `G2-GOV-1` |
| Prompt Title | Engineering Method Evolution: Repository Governance Alignment |
| Generation | 2 |
| Engineering Program | Platform Evolution |
| Branch | [`agent/engineering-method-v2`](https://github.com/pcvantol/technical-debt-engine/tree/agent/engineering-method-v2) |
| Commit | [`afae54f5f05be85148179cfb3a551c0e18f35c71`](https://github.com/pcvantol/technical-debt-engine/commit/afae54f5f05be85148179cfb3a551c0e18f35c71) |
| Pull Request | [#37](https://github.com/pcvantol/technical-debt-engine/pull/37) |
| Decision | `ENGINEERING_METHOD_V2_ESTABLISHED` |
| Execution Date | 2026-07-14 |
| Created | 2026-07-14 |
| Updated | 2026-07-14 |

## Summary

Established the Generation 2 AI-native repository governance model. Current `main` and operational reality are authoritative; `ENGINEERING_STATUS.md` is the primary handoff; prompt history is immutable and consulted only when historical context is needed. The canonical lifecycle is Draft → Active → Reviewable → Merged → Archived, with optional Superseded.

## Validation

- Governance-only diff reviewed; no `src/`, schema, capability-contract, or Adapter SDK implementation files changed.
- `git diff --check` passed before finalization.
- Bootstrap, Engineering Method, workflow, session initialization, prompt governance, lifecycle, finalization, current status, navigation, and archive records were updated or created.

## Known Limitations

- Prompt archives are required prospectively from `G2-GOV-1`; historical prompt records remain represented by the pre-V2 index and repository history.
- This governance increment does not resolve product recovery, release, or consumer-integration blockers.

## Next Prompt

P1: define and validate explicit Code Size analyzer provisioning and cross-platform qualification for the installed CLI.

This archive is immutable. Any correction is recorded by a subsequent prompt archive.
