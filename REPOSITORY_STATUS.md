# Repository status

| Field | Value |
| --- | --- |
| Generation | 1 |
| Status | RELEASE_DRY_RUN_BLOCKED |
| Canonical CLI | `tde` |
| Runtime | Foundation implemented; Policy Engine is the qualification decision layer |
| Analyzers | Not implemented |
| Releases | None |
| Mandatory workflow | One prompt → one reviewable pull request |
| Engineering method | Established by Prompt 2 |
| Runtime architecture | Established by Prompt 3; not implemented |
| Canonical schemas | Established by Prompt 4; runtime contracts only |
| Capability contracts | Established by Prompt 5; no capabilities implemented |
| Adapter SDK | Established by Prompt 6; no adapters implemented |
| Runtime foundation | Implemented by Prompt 7; no CLI or capabilities |
| CLI foundation | Implemented by Prompt 8; no capability or adapter behavior |
| Code Size | Validated by Prompt 9 with cloc 2.10; cross-platform qualification pending |
| Complexity | Validated by Prompt 10 with Radon 6.0.1 for Python; multi-language pending |
| Maintainability | Validated derived capability from Code Size and Complexity evidence |
| Dependency Health | Validated declarative dependency discovery |
| Policy Engine | Operational with versioned, dynamically discovered policy files and evidence |
| Baseline & Comparison | Operational immutable baseline persistence and canonical-evidence comparison |
| Trend Engine | Operational normalized baseline-history aggregation and CLI reporting |
| Query Engine | Operational versioned, read-only canonical-evidence query layer |
| Evidence Store | Operational immutable filesystem persistence and history listing |
| Execution Engine | Operational dependency-ordered capability execution and evidence |
| Runtime Qualification | Operational evidence-only trustworthiness and confidence assessment |
| Platform Qualification | Partially qualified for continued internal engineering; no release created |
| Platform Certification | Not certified; explicit foundation gaps remain and no release exists |
| Platform Release Engineering | Release Runtime architecture established; no package or release created |
| Software Assurance | Operational with explicit dependency, workflow and artifact limitations |
| Trusted Delivery | Operational immutable-candidate validation with explicit workflow and artifact limitations |
| Release Qualification | Candidate manifest established; publication blocked by objective gaps |
| Release Certification | Release process not certified; no publication exists |
| Operational Release Dry Run | Local wheel/checksum created; dry run blocked by workflow and reproducibility gaps |

Prompt 9 implements the first Code Size vertical slice through Runtime, registry, `code_size.cloc`, normalization, canonical evidence, and CLI assess routing. The slice is validated on macOS with explicitly installed cloc 2.10 but is not cross-platform qualified. Other capabilities remain unimplemented; no release exists.

Prompt 10 adds validated Python Complexity through `complexity.radon` and preserves registry architecture for other native analyzers. Cross-platform and multi-language qualification remain pending.

Prompt 13 operationalizes qualification policy. The Runtime now invokes the standalone Policy Engine after normalization, records policy identity, decision, triggered rules, and inputs in evidence, and projects only that output into Qualification. Default and repository/workspace policies are dynamically discovered; custom/organization/cloud policies remain future work.

Prompt 14 adds immutable baseline persistence and canonical-evidence comparison. It reports metric/finding/capability transitions and sends regression evidence to the Policy Engine without embedding qualification decisions in the Comparison Engine.

Prompt 15 adds a read-only Trend Engine. It aggregates baseline history and current evidence into repository, capability, metric, finding, and qualification trends, then exposes that evidence to Policy without making a policy decision.
