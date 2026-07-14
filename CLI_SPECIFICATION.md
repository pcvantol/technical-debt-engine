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

All commands will accept explicit configuration and emit documented exit codes. This specification creates no command implementation.
