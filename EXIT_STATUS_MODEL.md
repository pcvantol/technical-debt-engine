# Exit status model

The runtime emits one canonical execution state:

| State | Meaning |
| --- | --- |
| `SUCCESS` | Requested work completed with no warning-level or failure-level outcome. |
| `WARNING` | Execution completed with explicit non-fatal limitations or warning qualification. |
| `FAILED` | Execution completed and produced a failing qualification or execution result. |
| `BLOCKED` | The runtime cannot safely continue because required identity, validation, configuration, policy, or evidence is missing or incompatible. |
| `NOT_SUPPORTED` | The requested target, capability, adapter, or format is unsupported. |

Future policy may map these states to CI exit codes. Until then, the states are semantic contracts rather than numeric implementation choices. Unknown states fail closed as `BLOCKED`.
