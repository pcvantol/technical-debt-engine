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
| Code Size | Installed `tde assess --capability code-size` cross-platform qualified on Ubuntu, macOS and Windows for Python 3.11/3.13 with checksum-verified `cloc 2.10`; persistence, Query and report verified |
| Complexity | Public `tde assess --capability complexity` validated through an installed wheel with host Radon 6.0.1; repository/language/file/symbol evidence, immutable persistence, Query and report are operational on the macOS audit host |
| Maintainability | Derived implementation exists; no validated public CLI evidence |
| Dependency Health | Declarative Python/npm implementation exists; no validated public CLI evidence |
| Policy Engine | Operational and qualified on real persisted Code Size and Complexity evidence; deterministic policy decision-to-CLI-exit mapping verified |
| Baseline & Comparison | Operational immutable baseline persistence and canonical-evidence comparison |
| Trend Engine | Operational normalized baseline-history aggregation and CLI reporting |
| Query Engine | Code Size Query consumes only integrity-verified persisted Evidence Store records |
| Evidence Store | Operational immutable filesystem persistence, retrieval, identity and integrity verification |
| Execution Engine | Registry-backed planning and truthful planned/executed adapter and capability evidence for the recovered Code Size flow |
| Runtime Qualification | Fail-closed for missing execution, capability and adapter evidence; empty execution is blocked |
| Platform Qualification | Partially qualified for continued internal engineering; no release created |
| Platform Certification | Not certified; explicit foundation gaps remain and no release exists |
| Platform Release Engineering | Release Runtime architecture established; no package or release created |
| Build Reproducibility | Local deterministic wheel and source-distribution build foundation with hash-locked tooling, SHA-256 evidence, provenance and isolated installed-artifact qualification; hosted workflow run `29367776918` is blocked by a tracked egg-info mutation between independent builds |
| Software Assurance | Operational with explicit dependency, workflow and artifact limitations |
| Trusted Delivery | Operational canonical candidate, manifest, artifact, workflow, and Software Assurance evidence validation; real release-candidate inputs remain a separate Release Qualification concern |
| Release Qualification | Candidate manifest established; publication blocked by objective gaps |
| Release Certification | Release process not certified; no publication exists |
| Operational Release Dry Run | Local wheel/checksum created; dry run blocked by workflow and reproducibility gaps |
| Internal Release 0.1.0 | INTERNAL_RELEASE_0_1_0_NOT_EXECUTED: local wheel only; no tag, publication or approved release evidence |
| Operational Burn-In | Local deterministic runs completed; operational readiness remains blocked |
| DJConnect Reference Consumer | Blocked: no released TDE CLI and no selected DJConnect repository |
| Generation 2 Strategy | Established with Core Runtime, Platform Evolution and Innovation Lab programs |
| Deployment Strategy | Canonical target, distribution, consumer and lifecycle model defined; no deployment implementation or release created |
| Persistence Architecture | Canonical JSON-authoritative, local-first storage/index/consumer model defined; no SQLite, cloud, migration or retention implementation created |
| Dashboard Architecture | Canonical Query-only, read-only presentation model defined; no dashboard implementation created |
| Product Strategy Alignment | Product Vision, Strategy, Definitions, Roadmap and backlogs have canonical navigation; no implementation changed |

Prompt 9 implements the first Code Size vertical slice through Runtime, registry, `code_size.cloc`, normalization, canonical evidence, and CLI assess routing. The slice is validated on macOS with explicitly installed cloc 2.10 but is not cross-platform qualified. Other capabilities remain unimplemented; no release exists.

Prompt 10 adds validated Python Complexity through `complexity.radon` and preserves registry architecture for other native analyzers. Cross-platform and multi-language qualification remain pending.

Recovery P1-2 completes the public Complexity vertical slice: the installed CLI executes validated Radon 6.0+, normalizes deterministic repository/language/file/symbol evidence and threshold findings, persists verified evidence and serves Query and report only from the Evidence Store. Python/macOS is currently qualified; other languages remain explicit analyzer limitations. P1-3 adds the pending GitHub-hosted installed-wheel qualification matrix for Linux, macOS and Windows; cross-platform qualification is not claimed until that matrix succeeds.

Prompt 13 operationalizes qualification policy. The Runtime now invokes the standalone Policy Engine after normalization, records policy identity, decision, triggered rules, and inputs in evidence, and projects only that output into Qualification. Default and repository/workspace policies are dynamically discovered; custom/organization/cloud policies remain future work.

Prompt 14 adds immutable baseline persistence and canonical-evidence comparison. It reports metric/finding/capability transitions and sends regression evidence to the Policy Engine without embedding qualification decisions in the Comparison Engine.

Prompt 15 adds a read-only Trend Engine. It aggregates baseline history and current evidence into repository, capability, metric, finding, and qualification trends, then exposes that evidence to Policy without making a policy decision.

Prompt 32 is the current-state correction. Its evidence-based Operational Reality Audit classifies TDE as `TDE_PRODUCT_PARTIALLY_OPERATIONAL`: local installation, console help/version, direct Runtime Code Size execution, filesystem baseline/store, and unit tests exist; the public CLI capability flow emits empty execution evidence, persisted query is absent, empty evidence is over-qualified, and no release exists. Historical prompt records are retained as history; [OPERATIONAL_REALITY_AUDIT.md](OPERATIONAL_REALITY_AUDIT.md) is canonical for current product truth.

Recovery Prompt P0-1 repairs the audited Code Size public execution path. An installed wheel now executes `tde assess --capability code-size`, emits one planned and executed capability/adapter work item with canonical measurements, and qualifies that evidence. Empty or missing execution, capability, or adapter evidence now blocks Runtime Qualification. Product and release status remain partially operational and unreleased.

G2-GOV-1 establishes Engineering Method V2 repository governance. Current `main` and operational reality are authoritative; `ENGINEERING_STATUS.md` is the primary handoff, and prompt archives are immutable prospective repository memory. No product implementation, Runtime Architecture, schema, capability contract, or Adapter SDK was changed.

P1-1 completes the macOS Code Size vertical slice: `.tde.yml` discovery and CLI override, analyzer availability/version checks, repository/language/file evidence, retained raw analyzer output/hash, and JSON/Markdown report rendering.

P1-2 completes the remaining persisted-evidence flow for Code Size. An installed CLI assessment automatically persists validated canonical evidence; persisted record identity and integrity are verified before Query or report consumption; Query and Code Size report no longer execute Runtime or consume Runtime memory. The vertical slice is operational on the macOS audit host. Cross-platform analyzer qualification and release evidence remain separate blockers.

P1-4 qualifies the existing Code Size vertical slice on GitHub-hosted Ubuntu, macOS and Windows runners for Python 3.11 and 3.13. Each matrix target installs one candidate wheel into an isolated environment, provisions checksum-verified `cloc 2.10`, executes assessment, persists evidence, reads persisted Query and report output, verifies store integrity and tamper detection, and dogfoods TDE. The six normalized records are analytically equivalent; missing, unsupported and timed-out analyzers fail closed. No release is created.

P1-5 qualifies the Policy Engine against real persisted Code Size and Complexity evidence. Policies use canonical decisions (`PASS`, `PASS_WITH_WARNINGS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`), workspace/repository precedence, explicit provenance, deterministic threshold evidence, persisted Query retrieval, and CLI exits derived only from policy output. Invalid and missing policy inputs fail closed. No release is created.

P1-7 establishes the Build Reproducibility Foundation. Exact SHA-256-hash-locked build tooling and an exact setuptools backend create a wheel and source distribution from a clean candidate. The canonical builder derives a stable source epoch, normalizes wheel and tar/gzip metadata, emits artifact/build/candidate identities, `SHA256SUMS`, and versioned provenance. Local independent artifacts are byte-equivalent and isolated wheel/sdist installations dogfood the installed CLI, Runtime, Code Size, Complexity, Policy, baseline, comparison, Query, and report. GitHub-hosted workflow run `29367776918` failed because its first build rewrote a tracked egg-info manifest before the clean-candidate guard started build two; this repair is deferred. No release or publication is created.

P1-9 operationalizes Trusted Delivery. `tde trusted-delivery` validates a clean candidate SHA, repository and branch; consumes canonical Software Assurance without repeating its assurance rules; verifies a versioned JSON manifest against candidate and artifact checksums; validates assurance-backed reproducibility/provenance; and records SHA-256 workflow-source provenance with immutable-action and least-privilege checks. It creates no release, certification, tag, or publication. Dogfooding TDE's clean committed candidate returned `PASS_WITH_WARNINGS` only because this non-release increment intentionally supplied no external manifest or independent artifact directories.

PD-1 establishes the canonical Deployment Strategy. Generation 1 product targets are PyPI, GitHub Releases, Homebrew, Docker, GitHub Action and the Python Runtime API; distribution execution remains unimplemented and no target is currently published. Generation 2 package-manager and IDE targets are planned; Generation 3 service targets remain research. Runtime Architecture and implementation are unchanged.

PD-2 establishes the canonical Persistence Architecture. Generation 1 uses immutable canonical JSON with filesystem persistence and persisted Query; Generation 2 SQLite is derived local indexing only; Generation 3 PostgreSQL/object/distributed/cloud persistence is future evaluation. Canonical Evidence remains authoritative and consumers read only through Query. Runtime and implementation are unchanged.

G2-GOV-2 establishes the first Prompt Freeze Point rule in current `main`, but its required immutable execution report and final status handoff were not included before PR #39 merged. That historical finalization gap is explicitly deferred to `G2-GOV-4`; it is not repaired retrospectively in this increment.

G2-GOV-3 establishes Engineering Method v2.2. Every prompt owns exactly one objective, one engineering increment, and one reviewable Pull Request. The increment ends when that Pull Request becomes reviewable; merge remains separate. A draft Pull Request may prepare finalization records in the same PR but does not freeze engineering. Repository hygiene is canonical: operating-system artifacts are ignored and removed when safe, while engineering evidence, release evidence, and fixtures remain protected.

G2-GOV-4 classifies the three historical branch-only commits without rewriting history: `6f4d60c` is superseded by P1-2 / PR #41, `d1aa3eb` is rejected as invalid historical finalization, and `da548a8` is deferred governance evidence. Local historical branch deletion is blocked because the required remote branches still exist; no branch was deleted by this increment.
