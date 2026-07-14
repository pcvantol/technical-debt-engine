# Repository status

| Field | Value |
| --- | --- |
| Generation | 1 |
| Status | BASELINE_AND_COMPARISON_ENGINE_OPERATIONAL |
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

Prompt 9 implements the first Code Size vertical slice through Runtime, registry, `code_size.cloc`, normalization, canonical evidence, and CLI assess routing. The slice is validated on macOS with explicitly installed cloc 2.10 but is not cross-platform qualified. Other capabilities remain unimplemented; no release exists.

Prompt 10 adds validated Python Complexity through `complexity.radon` and preserves registry architecture for other native analyzers. Cross-platform and multi-language qualification remain pending.

Prompt 13 operationalizes qualification policy. The Runtime now invokes the standalone Policy Engine after normalization, records policy identity, decision, triggered rules, and inputs in evidence, and projects only that output into Qualification. Default and repository/workspace policies are dynamically discovered; custom/organization/cloud policies remain future work.

Prompt 14 adds immutable baseline persistence and canonical-evidence comparison. It reports metric/finding/capability transitions and sends regression evidence to the Policy Engine without embedding qualification decisions in the Comparison Engine.
