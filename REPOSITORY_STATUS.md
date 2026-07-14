# Repository status

| Field | Value |
| --- | --- |
| Generation | 2 |
| Status | TDE_PRODUCT_PARTIALLY_OPERATIONAL (audited on current main) |
| Canonical CLI | `tde` |
| Runtime | Public Code Size CLI path executes through Runtime with truthful execution evidence; broader recovery remains pending |
| Analyzers | Not implemented |
| Releases | None |
| Mandatory workflow | One prompt → one objective → one engineering increment → one reviewable pull request; reviewable state is the Prompt Freeze Point |
| Repository hygiene | Canonical `.gitignore` and `REPOSITORY_HYGIENE.md`; no tracked or untracked operating-system artifacts |
| Primary engineering handoff | `ENGINEERING_STATUS.md` — fully replaced by each prompt |
| Prompt history | Immutable, prospective archives under `docs/history/prompts/` |
| Engineering method | Established by Prompt 2 |
| Runtime architecture | Established by Prompt 3; not implemented |
| Canonical schemas | Established by Prompt 4; runtime contracts only |
| Capability contracts | Established by Prompt 5; no capabilities implemented |
| Adapter SDK | Established by Prompt 6; no adapters implemented |
| Runtime foundation | Implemented by Prompt 7; no CLI or capabilities |
| CLI foundation | Implemented by Prompt 8; no capability or adapter behavior |
| Code Size | Public `tde assess --capability code-size` validated through an installed wheel with host `cloc 2.10` |
| Complexity | Direct adapter implementation only; isolated package lacks Radon and public CLI execution blocked |
| Maintainability | Derived implementation exists; no validated public CLI evidence |
| Dependency Health | Declarative Python/npm implementation exists; no validated public CLI evidence |
| Policy Engine | Operational with versioned, dynamically discovered policy files and evidence |
| Baseline & Comparison | Operational immutable baseline persistence and canonical-evidence comparison |
| Trend Engine | Operational normalized baseline-history aggregation and CLI reporting |
| Query Engine | Code Size Query consumes only integrity-verified persisted Evidence Store records |
| Evidence Store | Operational immutable filesystem persistence, retrieval, identity and integrity verification |
| Execution Engine | Registry-backed planning and truthful planned/executed adapter and capability evidence for the recovered Code Size flow |
| Runtime Qualification | Fail-closed for missing execution, capability and adapter evidence; empty execution is blocked |
| Platform Qualification | Partially qualified for continued internal engineering; no release created |
| Platform Certification | Not certified; explicit foundation gaps remain and no release exists |
| Platform Release Engineering | Release Runtime architecture established; no package or release created |
| Software Assurance | Operational with explicit dependency, workflow and artifact limitations |
| Trusted Delivery | Operational immutable-candidate validation with explicit workflow and artifact limitations |
| Release Qualification | Candidate manifest established; publication blocked by objective gaps |
| Release Certification | Release process not certified; no publication exists |
| Operational Release Dry Run | Local wheel/checksum created; dry run blocked by workflow and reproducibility gaps |
| Internal Release 0.1.0 | INTERNAL_RELEASE_0_1_0_NOT_EXECUTED: local wheel only; no tag, publication or approved release evidence |
| Operational Burn-In | Local deterministic runs completed; operational readiness remains blocked |
| DJConnect Reference Consumer | Blocked: no released TDE CLI and no selected DJConnect repository |
| Generation 2 Strategy | Established with Core Runtime, Platform Evolution and Innovation Lab programs |

Prompt 9 implements the first Code Size vertical slice through Runtime, registry, `code_size.cloc`, normalization, canonical evidence, and CLI assess routing. The slice is validated on macOS with explicitly installed cloc 2.10 but is not cross-platform qualified. Other capabilities remain unimplemented; no release exists.

Prompt 10 adds validated Python Complexity through `complexity.radon` and preserves registry architecture for other native analyzers. Cross-platform and multi-language qualification remain pending.

Prompt 13 operationalizes qualification policy. The Runtime now invokes the standalone Policy Engine after normalization, records policy identity, decision, triggered rules, and inputs in evidence, and projects only that output into Qualification. Default and repository/workspace policies are dynamically discovered; custom/organization/cloud policies remain future work.

Prompt 14 adds immutable baseline persistence and canonical-evidence comparison. It reports metric/finding/capability transitions and sends regression evidence to the Policy Engine without embedding qualification decisions in the Comparison Engine.

Prompt 15 adds a read-only Trend Engine. It aggregates baseline history and current evidence into repository, capability, metric, finding, and qualification trends, then exposes that evidence to Policy without making a policy decision.

Prompt 32 is the current-state correction. Its evidence-based Operational Reality Audit classifies TDE as `TDE_PRODUCT_PARTIALLY_OPERATIONAL`: local installation, console help/version, direct Runtime Code Size execution, filesystem baseline/store, and unit tests exist; the public CLI capability flow emits empty execution evidence, persisted query is absent, empty evidence is over-qualified, and no release exists. Historical prompt records are retained as history; [OPERATIONAL_REALITY_AUDIT.md](OPERATIONAL_REALITY_AUDIT.md) is canonical for current product truth.

Recovery Prompt P0-1 repairs the audited Code Size public execution path. An installed wheel now executes `tde assess --capability code-size`, emits one planned and executed capability/adapter work item with canonical measurements, and qualifies that evidence. Empty or missing execution, capability, or adapter evidence now blocks Runtime Qualification. Product and release status remain partially operational and unreleased.

G2-GOV-1 establishes Engineering Method V2 repository governance. Current `main` and operational reality are authoritative; `ENGINEERING_STATUS.md` is the primary handoff, and prompt archives are immutable prospective repository memory. No product implementation, Runtime Architecture, schema, capability contract, or Adapter SDK was changed.

P1-1 completes the macOS Code Size vertical slice: `.tde.yml` discovery and CLI override, analyzer availability/version checks, repository/language/file evidence, retained raw analyzer output/hash, and JSON/Markdown report rendering.

P1-2 completes the remaining persisted-evidence flow for Code Size. An installed CLI assessment automatically persists validated canonical evidence; persisted record identity and integrity are verified before Query or report consumption; Query and Code Size report no longer execute Runtime or consume Runtime memory. The vertical slice is operational on the macOS audit host. Cross-platform analyzer qualification and release evidence remain separate blockers.

G2-GOV-2 establishes the first Prompt Freeze Point rule in current `main`, but its required immutable execution report and final status handoff were not included before PR #39 merged. That historical finalization gap is explicitly deferred to `G2-GOV-4`; it is not repaired retrospectively in this increment.

G2-GOV-3 establishes Engineering Method v2.2. Every prompt owns exactly one objective, one engineering increment, and one reviewable Pull Request. The increment ends when that Pull Request becomes reviewable; merge remains separate. A draft Pull Request may prepare finalization records in the same PR but does not freeze engineering. Repository hygiene is canonical: operating-system artifacts are ignored and removed when safe, while engineering evidence, release evidence, and fixtures remain protected.

G2-GOV-4 classifies the three historical branch-only commits without rewriting history: `6f4d60c` is superseded by P1-2 / PR #41, `d1aa3eb` is rejected as invalid historical finalization, and `da548a8` is deferred governance evidence. Local historical branch deletion is blocked because the required remote branches still exist; no branch was deleted by this increment.
