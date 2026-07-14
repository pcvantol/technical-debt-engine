# Prompt Index

This is navigation only. Current engineering state is in [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md); immutable archives are in [docs/history/prompts](docs/history/prompts). Prompt archives apply prospectively from `G2-GOV-1`; earlier rows remain preserved historical navigation until separately archived.

| Prompt | Scope | Status |
| --- | --- | --- |
| 0 | Remote repository initialization and GitHub configuration | Complete |
| 1 | Generation 1 product bootstrap and documentation foundation | Complete |
| 1.5 | Engineering Workflow Alignment | Complete |
| 2 | AI-Native Engineering Method | Complete |
| 3 | Canonical Runtime Architecture | Complete |
| 4 | Canonical Domain and Evidence Schemas | Complete |
| 5 | Capability Contracts and Qualification Policy | Complete |
| 6 | Adapter SDK | Complete |
| 7 | Runtime Foundation | Complete |
| 8 | Canonical CLI Foundation | Complete |
| 9 | Code Size Capability | Complete |
| 10 | Complexity Capability | Complete |
| 11 | Maintainability Capability | Complete |
| 12 | Dependency Health Capability | Complete |
| 13 | Policy Engine Qualification Operationalization | Complete |
| 14 | Baseline & Comparison Engine | Complete |
| 15 | Trend Engine | Complete |
| 16 | Query Engine | Complete |
| 17 | Canonical Evidence Store | Complete |
| 18 | Capability Execution Engine | Complete |
| 19 | Runtime Qualification Engine | Complete |
| 20 | Platform Qualification | Complete |
| 21 | Platform Certification | Complete |
| 22 | Platform Release Engineering | Complete |
| 23 | Software Assurance | Complete |
| 24 | Trusted Delivery | Complete |
| 25 | Release Qualification | Complete |
| 26 | Release Certification | Complete |
| 27 | Operational Release Dry Run | Complete |
| 28 | Internal Release 0.1.0 | Complete |
| 29 | Operational Burn-In | Complete |
| 30 | DJConnect Reference Consumer Integration | Blocked |
| 31 | Generation 2 Strategy Refresh | Complete |
| 32 | Operational Reality Audit | Complete |
| P0-1 | Public CLI Execution and Truthful Runtime Qualification | Complete |
| [G2-GOV-1](docs/history/prompts/G2-GOV-1-engineering-method-evolution.md) | Engineering Method Evolution: Repository Governance Alignment | [Reviewable — #37](https://github.com/pcvantol/technical-debt-engine/pull/37) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/agent/engineering-method-v2) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/afae54f5f05be85148179cfb3a551c0e18f35c71) |
| [P1-1](docs/history/prompts/P1-1-complete-code-size-vertical-slice.md) | Complete Code Size Vertical Slice | [Reviewable — #38](https://github.com/pcvantol/technical-debt-engine/pull/38) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/agent/code-size-vertical-slice) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/964ff2aea582c1751485cb050cc4868d51d49f56) |
| G2-GOV-2 | Engineering Method Evolution: Prompt Finalization Freeze | [Merged — #39](https://github.com/pcvantol/technical-debt-engine/pull/39); immutable finalization record deferred to `G2-GOV-4` |
| [G2-GOV-3](docs/history/prompts/G2-GOV-3-prompt-ownership-hygiene.md) | Engineering Method Evolution: Prompt Ownership, Freeze Boundary, Repository Hygiene | [Reviewable — #40](https://github.com/pcvantol/technical-debt-engine/pull/40) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/agent/prompt-ownership-hygiene) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/d9e6634e6ed797f84525ee029747f749a8ef9a58) |
| [P1-2](docs/history/prompts/P1-2-code-size-persisted-evidence-flow.md) | Complete Code Size Vertical Slice: Persisted Evidence Flow | [Reviewable — #41](https://github.com/pcvantol/technical-debt-engine/pull/41) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/agent/code-size-evidence-store) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/8fc34936139473d1a0303c0242c9b80381e9b175) |
| [G2-GOV-4](docs/history/prompts/G2-GOV-4-historical-branch-closure.md) | Historical Branch Closure and Superseded Commit Registration | [Reviewable — #42](https://github.com/pcvantol/technical-debt-engine/pull/42) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/agent/historical-branch-closure) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/5a37d97b91072af61ceadfbe7780575886f9b91f) |
| [P1-2 Complexity](docs/history/prompts/P1-2-complete-complexity-vertical-slice.md) | Complete Complexity Vertical Slice | [Reviewable — #43](https://github.com/pcvantol/technical-debt-engine/pull/43) · [branch](https://github.com/pcvantol/technical-debt-engine/tree/codex/p1-2-complexity-vertical-slice) · [commit](https://github.com/pcvantol/technical-debt-engine/commit/7fe339f63b8e3abb9c99cbba91ecbe212b7e5a59) |

Prompt lifecycle is **Draft → Active → Reviewable → Merged → Archived**, with optional **Superseded**. Generation 2 consists of exactly Core Runtime, Platform Evolution and Innovation Lab. Future prompts must preserve the frozen Generation 1 foundations, follow the mandatory [engineering workflow](ENGINEERING_WORKFLOW.md), and update this index as navigation only.

Prompt 32 is an evidence-only audit, not a Generation 2 implementation increment. It establishes `TDE_PRODUCT_PARTIALLY_OPERATIONAL` as the current product state and records the implementation recovery sequence in [IMPLEMENTATION_RECOVERY_PLAN.md](IMPLEMENTATION_RECOVERY_PLAN.md).

Recovery Prompt P0-1 implements only the first P0 recovery slice: installed CLI Code Size execution through the canonical Runtime and fail-closed Runtime Qualification. It does not create a release or advance other recovery milestones.

`G2-GOV-1` establishes repository-native engineering continuity and the prospective immutable archive requirement. It is governance-only and does not alter Runtime, Schema, Capability, or Adapter SDK architecture.

`G2-GOV-2` introduced the initial freeze rule, but PR #39 merged before its finalization record entered the PR. Its missing historical handoff is Deferred Work owned by `G2-GOV-4`.

`G2-GOV-3` establishes prompt ownership, the reviewable-state Freeze Point, Deferred Work fields, and canonical repository hygiene. It is governance-only and does not alter Runtime, implementation, capabilities, schemas, contracts, or the Adapter SDK.

`P1-2` completes the Code Size persisted-evidence flow: installed CLI assessment persists evidence automatically and integrity-verified persisted evidence is the only source for Code Size Query and report. It is operational on the macOS audit host; cross-platform analyzer qualification is deferred to `P1-3`.

`G2-GOV-4` records the historical local-branch incident without changing prior prompt archives. It classifies the three commits and blocks local branch deletion because the mandatory remote-branch-absent verification failed. `G2-GOV-5` owns any authorized remote-branch removal and renewed local closure.
