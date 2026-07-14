# CLI user guide

The first executable `tde` CLI is a thin, Python 3.11+ presentation layer over the public Runtime API. Install it as a project script or invoke it in development with `PYTHONPATH=src python3 -c 'from tde_cli.main import console_main; console_main()'`.

Examples:

```text
tde --help
tde --version
tde --format json validate .
tde --format json inspect .
```

`validate` and `inspect` invoke the generic Runtime Foundation. `assess`, `baseline`, `compare`, `qualify`, `report`, and `explain` are routed command frameworks and return `NOT_IMPLEMENTED` with the canonical `NOT_SUPPORTED` exit code until their capability behavior is delivered.

Configuration defaults to the runtime default. `--config` accepts a JSON-compatible `.tde.yml` document during this foundation phase; JSON is a YAML subset and avoids adding a parser dependency. Configuration ownership remains in the Runtime.
