# Repository status

| Field | Value |
| --- | --- |
| Generation | 1 |
| Status | CLI_FOUNDATION |
| Canonical CLI | `tde` |
| Runtime | Foundation implemented; no capability-specific logic |
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

Product Bootstrap, Engineering Workflow Alignment, the AI-Native Engineering Method, Canonical Runtime Architecture, Canonical Domain and Evidence Schemas, Capability Contracts, Adapter SDK, and Runtime Foundation are complete. Prompt 8 implements the thin Canonical CLI Foundation over the Runtime public API, with framework command routing, help, version, logging, configuration loading, output, and canonical exit codes. Adapters, analyzers, and capabilities are not implemented; no release exists. Prompt 8's focused reviewable pull request is required before a subsequent canonical prompt begins. Merge remains a separate decision.
