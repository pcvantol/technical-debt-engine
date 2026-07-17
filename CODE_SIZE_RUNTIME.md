# Code Size Runtime Contract

`code_size` is the first public Runtime capability. Invoke it only through the
public CLI:

```text
tde assess --capability code_size <repository>
```

The CLI forwards the request to the Runtime. The Runtime planner resolves
`code_size`, selects `code_size.cloc`, discovers `cloc` on `PATH`, executes it,
normalizes its JSON output, writes canonical evidence, and derives Runtime
Qualification. Consumers must not invoke `cloc` or import Runtime modules.

## Analyzer requirement

`cloc` 2.10 or later must be installed and available on `PATH`. TDE never
downloads or installs it at execution time. The official Docker image provides
the checksum-verified 2.10 executable; wheel users provision it themselves.

If discovery fails or the version is unsupported, the command exits `5`
(`ANALYZER_NOT_FOUND`). Execution and parsing failures exit `2`
(`FAILED_CLOSED`). No metrics are fabricated or silently skipped.

## Canonical evidence

Successful evidence includes the execution ID, timestamps, Runtime version,
repository identity, capability result, analyzer identity/version, qualification
and normalized measurements. The repository-level measurements are:

- `code_size.file_count`
- `code_size.code_lines`
- `code_size.comment_lines`
- `code_size.blank_lines`
- `code_size.source_lines`
- `code_size.test_lines`
- `code_size.generated_lines`
- `code_size.vendor_lines`
- `code_size.documentation_lines`
- `code_size.test_to_source_ratio`

Language and file measurements use the same canonical model. Raw `cloc` JSON
is adapter provenance, not a public consumer contract.
