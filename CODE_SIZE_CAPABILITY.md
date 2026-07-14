# Code Size capability

Code Size `0.1.0` is TDE's first validated vertical slice. It uses the registered `code_size.cloc` adapter (`0.1.0`) and explicitly installed `cloc 2.10` from PATH; no analyzer is downloaded at runtime.

Run `tde assess --capability code-size --format json .`. The adapter uses safe argument-array process invocation, a timeout, no project-script execution, no repository mutation, deterministic relative paths, and raw-output hashing. Analyzer absence or malformed output returns structured blocked evidence rather than zero metrics.

Status: **VALIDATED**, not qualified. Automated and dogfooding checks passed on macOS; Linux and Windows analyzer packaging/execution remains to be qualified.
