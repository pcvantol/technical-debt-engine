# Repository status

| Field | Value |
| --- | --- |
| Generation | 1 |
| Status | CODE_SIZE_CAPABILITY_VALIDATED |
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
| Code Size | Validated by Prompt 9 with cloc 2.10; cross-platform qualification pending |
| Complexity | Validated by Prompt 10 with Radon 6.0.1 for Python; multi-language pending |

Prompt 9 implements the first Code Size vertical slice through Runtime, registry, `code_size.cloc`, normalization, canonical evidence, and CLI assess routing. The slice is validated on macOS with explicitly installed cloc 2.10 but is not cross-platform qualified. Other capabilities remain unimplemented; no release exists.

Prompt 10 adds validated Python Complexity through `complexity.radon` and preserves registry architecture for other native analyzers. Cross-platform and multi-language qualification remain pending.
