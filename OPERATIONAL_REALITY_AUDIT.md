# Operational Reality Audit

## Decision

**TDE_PRODUCT_PARTIALLY_OPERATIONAL**

For the Platform Architect's complete review route, start at [PLATFORM_ARCHITECT_AUDIT_ENTRYPOINT.md](PLATFORM_ARCHITECT_AUDIT_ENTRYPOINT.md).

Current `main` contains executable Python code, a buildable local wheel and a working `tde` console entry point. The public core analysis flow is not operational: manual `tde assess --capability ...` and `tde run --capability ...` invocations returned successful, empty runtime evidence (`workItems: 0`, no capabilities or adapters). The Runtime API can execute Code Size directly when `cloc` is available. No approved or published release exists.

## Evidence collected on 2026-07-14

- Source: `2228b69ae86fe3640f17c06b004ebea994e8570f` (`main` at audit start).
- Local isolated install: `python3 -m venv /tmp/tde-audit-venv` then `pip install --no-deps .` installed `technical-debt-engine-runtime 0.1.0`; `/tmp/tde-audit-venv/bin/tde --help` and `--version` exited 0.
- Wheel build: `pip wheel --no-deps --wheel-dir /tmp/tde-audit-wheel .` produced `technical_debt_engine_runtime-0.1.0-py3-none-any.whl`. It is a local build, not a release artifact.
- Tools on the audit host: `cloc 2.10`; `radon 6.0.1` only on the host Python path, not in the isolated TDE environment.
- Tests: `PYTHONPATH=src python -m unittest discover -s tests -v`: **41 passed, 0 failed, 0 skipped**.
- There are no `.github/workflows` files, Git tags, or GitHub Releases. Existing wheels under `internal-release-artifacts/` and `dry-run-artifacts/` are repository files, not published releases.

## What exists

The implementation language is Python 3.11+. Packaging is setuptools (`pyproject.toml`); the package name is `technical-debt-engine-runtime`, version `0.1.0`, and its console entry point is `tde = tde_cli.main:console_main`. The public library API is principally `tde_runtime.Runtime`, `RuntimeConfiguration`, and the independently importable engine modules. Configuration is JSON-compatible only despite the CLI help mentioning `.tde.yml`; no automatic configuration-file discovery exists.

Schemas are versioned JSON files under `schemas/`; the runtime embeds evidence schema version `1.0.0`. The version source is duplicated constants in `pyproject.toml`, `tde_cli.main`, and `tde_runtime.runtime`, not a single release-derived source. Supported execution platforms are not qualified; only macOS host execution was observed.

## Command observations

| Command | Exit | Observed result | State |
| --- | ---: | --- | --- |
| `tde --help` | 0 | Command tree is rendered. | VALIDATED |
| `tde --version` | 0 | Reports CLI/runtime `0.1.0`, schema `1.0.0`, Generation 1. | VALIDATED |
| `tde inspect .` | 0 | Produces structurally valid but empty-capability evidence. | VALIDATED |
| `tde assess --help` | 0 | Help is present. | SCAFFOLDED |
| `tde assess --capability code-size .` | 0 | Empty execution; does not expose Code Size measurements. | BLOCKED |
| `tde baseline --help`, `compare --help`, `qualify --help`, `query --help`, `trend --help` | 0 | Help is present. | VALIDATED |
| `tde baseline`, `compare`, `trend`, `store`, `history` | 0 | Execute against empty evidence when global options precede the subcommand. | VALIDATED |
| `tde query` | 0 | Queries only the current in-memory runtime evidence; persisted store records are not consumed. | BLOCKED |
| `tde qualify --capability code-size .` | 0 | Returns `NOT_SUPPORTED` because CLI evidence is empty. | BLOCKED |
| `tde assure .`, `tde trusted-delivery .` | 2 | Fail on missing workflow, clean-tree, provenance and release-artifact evidence. | BLOCKED |

Argparse requires global options before the subcommand; putting `--baseline-location` or `--store-location` after it exits 2. This is an observable CLI constraint, not a documented installation flow.

## Dogfooding

Direct Runtime execution on this repository with `RuntimeConfiguration.load({"capabilities": {"code_size": {"enabled": true}}})` invoked `cloc` and produced 307 files, 3,570 code lines, a `code_size.cloc` capability result and execution evidence with one work item. The CLI route intended to make the same configuration emitted no capability result. Therefore dogfooding proves a local API vertical slice, not a usable public CLI assessment flow.

## Release and consumer reality

`gh release list --limit 20` returned no releases; `git tag -l` returned no tags. The local candidate wheels have different checksums and no published GitHub Release, source archive, release workflow, provenance or reproducibility evidence. **INTERNAL_RELEASE_0_1_0_NOT_EXECUTED** is the current product truth.

DJConnect integration cannot be proven from this repository and remains blocked: no released TDE version can be pinned and no DJConnect repository has been selected. No cross-repository invocation, evidence ingestion or release gate exists here.

See [IMPLEMENTATION_INVENTORY.md](IMPLEMENTATION_INVENTORY.md), [PRODUCT_SURFACE_MATRIX.md](PRODUCT_SURFACE_MATRIX.md), [CAPABILITY_REALITY_MATRIX.md](CAPABILITY_REALITY_MATRIX.md), [TEST_REALITY_REPORT.md](TEST_REALITY_REPORT.md), [RELEASE_REALITY_REPORT.md](RELEASE_REALITY_REPORT.md), [DOCUMENTATION_IMPLEMENTATION_GAP.md](DOCUMENTATION_IMPLEMENTATION_GAP.md), and [IMPLEMENTATION_RECOVERY_PLAN.md](IMPLEMENTATION_RECOVERY_PLAN.md).
