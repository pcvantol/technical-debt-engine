# CLI specification

The canonical executable name is `tde`. Commands are stable contracts for people and automation; they do not expose runtime internals.

| Command | Intent |
| --- | --- |
| `tde inspect` | Discover a target and describe applicable adapters. |
| `tde assess` | Collect and normalize capability observations. |
| `tde baseline` | Create a compatible immutable reference evidence set. |
| `tde compare` | Compare compatible evidence sets. |
| `tde qualify` | Apply an explicit policy and severity model. |
| `tde report` | Render evidence and qualification results. |
| `tde explain` | Explain a metric, result, policy decision, or exit code. |
| `tde validate` | Validate configuration, evidence, and contract compatibility. |

## Implemented runtime contract

The currently implemented public capability is `code_size`:

```text
tde assess --capability code_size <repository>
```

The CLI only parses and forwards the requested capability. Capability and
adapter resolution, `cloc` execution, normalization, evidence production, and
qualification are Runtime responsibilities. The command persists immutable
canonical evidence by default under `<repository>/.tde/evidence`.

| Exit code | Name | Meaning |
| --- | --- | --- |
| 0 | `SUCCESS` | The requested capability was executed and qualified. |
| 2 | `FAILED_CLOSED` | Runtime execution failed without producing analysis metrics. |
| 3 | `EXECUTION_ERROR` | The public command could not complete its execution contract. |
| 4 | `NOT_SUPPORTED` | The Runtime does not register the requested capability. |
| 5 | `ANALYZER_NOT_FOUND` | `cloc` is absent or does not meet the required version. |
