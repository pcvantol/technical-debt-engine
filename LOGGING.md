# Logging

The CLI owns presentation logging and remains Runtime-independent. Supported levels are `ERROR`, `WARNING`, `INFO`, `DEBUG`, and `TRACE`; `TRACE` maps to Python debug output in the foundation. `--verbose` selects `INFO`, `--quiet` selects `ERROR`, and `--log-level` is explicit.

Logs do not alter runtime evidence, qualification, or exit-code semantics.
