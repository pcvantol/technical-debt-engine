# Code Size adapter

`code_size.cloc` wraps `cloc 2.10+` from PATH with `--json --by-file --quiet`. It verifies analyzer availability and minimum version before execution, uses deterministic argument-array invocation, retains native JSON output with a SHA-256 hash in adapter evidence, and reports structured limitations for unavailable, unsupported or failed analyzers. The adapter is local-only until cross-platform behavior is qualified.
