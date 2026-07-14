# Command reference

| Command | Current behavior | Output | Exit status |
| --- | --- | --- | --- |
| `tde help` / `tde --help` | Generated argparse help. | Console help. | `SUCCESS` |
| `tde --version` | Shows CLI/runtime/schema/generation versions. | Human or JSON. | `SUCCESS` |
| `tde validate [target]` | Invokes Runtime Foundation validation. | Runtime summary. | Runtime exit. |
| `tde inspect [target]` | Invokes Runtime Foundation inspection. | Runtime summary. | Runtime exit. |
| `tde assess [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |
| `tde baseline [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |
| `tde compare [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |
| `tde qualify [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |
| `tde report [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |
| `tde explain [target]` | Framework route only. | `NOT_IMPLEMENTED`. | `NOT_SUPPORTED` |

All command-specific `--help` text is generated from command metadata. Target defaults to the current directory.
