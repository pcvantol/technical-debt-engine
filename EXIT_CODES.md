# Exit codes

| Code | Name | Meaning |
| --- | --- | --- |
| 0 | `SUCCESS` | Policy decision `PASS`, or a generic operation completed. |
| 1 | `WARNING` | Policy decision `PASS_WITH_WARNINGS`. |
| 2 | `FAILED` | Policy decision `FAIL`. |
| 3 | `BLOCKED` | Policy decision `BLOCKED`, or safe execution is prevented. |
| 4 | `NOT_SUPPORTED` | Policy decision `NOT_APPLICABLE`, or behavior is unsupported. |

`assess` and `run` map only the Policy Engine decision to these policy exits; they do not duplicate threshold logic.
