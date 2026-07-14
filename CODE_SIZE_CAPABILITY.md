# Code Size Capability

## Operational path

`tde assess --capability code-size <repository>` executes the Code Size capability through the public CLI, Runtime, Execution Engine, capability registry, `code_size.cloc` adapter, `cloc`, normalization, validation, Policy Engine, Runtime Qualification, and Evidence Store.

The assessment persists validated canonical evidence automatically. `tde query` and `tde report --capability code-size` read the most recent persisted record; they do not execute Runtime or consume Runtime memory.

## Analyzer

The canonical analyzer is `cloc` version 2.10 or later, available on `PATH`. The adapter invokes `cloc --version` before a deterministic `cloc --json --by-file --quiet <repository>` execution. Native output is retained in adapter evidence with a SHA-256 hash.

## Measurements and classification

Evidence contains repository, language, and file measurements for physical, code, comment, and blank lines, plus file counts and test-to-source ratio. File classification is deterministic: source, test, documentation, generated, vendor, and configuration paths are distinguished without repository-specific rules.

`cloc` does not provide logical-line counts. The capability records that as a structured limitation rather than fabricating a value.

## Limitations

- The supported execution proof is host-specific until cross-platform qualification is completed.
- `cloc` must be installed separately; a missing or unsupported analyzer blocks assessment without measurements.
- The current YAML reader accepts the canonical mapping-only `.tde.yml` subset.
