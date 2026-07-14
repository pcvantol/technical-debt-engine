# Evidence runtime

Evidence publication creates immutable, versioned results after validation and qualification. JSON is canonical; Markdown and SARIF are derived views. OpenTelemetry is a future projection and does not alter the canonical record.

Every evidence record includes runtime and schema identity, repository and candidate identity, capabilities, adapters, native tool versions, normalized metrics and findings, qualification, limitations, and timestamps. Provenance binds each record to the execution context that produced it.

Evidence is never mutated after publication. Corrections, retries, and comparisons create new evidence records that reference prior evidence where applicable.
