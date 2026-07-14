# Exit status model

The runtime emits one canonical execution state:

| State | Meaning |
| --- | --- |
| `SUCCESS` | Requested work completed with no warning-level or failure-level outcome. |
| `WARNING` | Execution completed with explicit non-fatal limitations or warning qualification. |
| `FAILED` | Execution completed and produced a failing qualification or execution result. |
| `BLOCKED` | The runtime cannot safely continue because required identity, validation, configuration, policy, or evidence is missing or incompatible. |
| `NOT_SUPPORTED` | The requested target, capability, adapter, or format is unsupported. |

Policy decisions now map deterministically to CLI exits: `PASS` → 0, `PASS_WITH_WARNINGS` → 1, `FAIL` → 2, `BLOCKED` → 3 and `NOT_APPLICABLE` → 4. Unknown states fail closed as `BLOCKED`.
