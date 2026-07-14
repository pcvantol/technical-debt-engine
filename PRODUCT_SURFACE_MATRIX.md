# Product Surface Matrix

| Surface | Actual implementation | Evidence | Truth state | Primary gap |
| --- | --- | --- | --- | --- |
| Install method | Local `pip install --no-deps .` and local wheel install | Isolated venv install succeeded | VALIDATED | No supported published distribution or dependency declaration |
| CLI entry point | setuptools `tde` script | `tde --help`, `tde --version` exit 0 | VALIDATED | Version is duplicated; no release binding |
| CLI command tree | argparse commands in `src/tde_cli/main.py` | Help exposes 16 commands | VALIDATED | Several commands are stubs or return empty evidence |
| Runtime API | `tde_runtime.Runtime` | Direct Code Size execution executed one work item | VALIDATED | Stage reporting and validation overstate empty runs |
| Configuration | Explicit JSON passed to `RuntimeConfiguration.load` | Unit tests and direct API use | VALIDATED | No `.tde.yml` discovery; CLI help is misleading |
| Schemas | JSON Schema files under `schemas/` | Schema validation tests | VALIDATED | Runtime validation is hard-coded, not demonstrated against all runtime outputs |
| Evidence | In-memory evidence; filesystem store | Store/history commands persisted and read empty evidence | VALIDATED | Identity includes random execution ID; persisted evidence cannot be queried by Query Engine |
| Platforms | Python/macOS audit host | Local execution only | IMPLEMENTED | No cross-platform qualification |
| Release artifacts | Two tracked local wheels and manifests | Files exist, no tag/release/workflow | BLOCKED | No publication, provenance or reproducibility |
