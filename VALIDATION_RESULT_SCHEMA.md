# Validation result schema

Validation is independent of technical-debt qualification. Its top-level outcomes are `VALID`, `INVALID`, `INCOMPLETE`, and `UNSUPPORTED`; it records schema, candidate identity, repository identity, adapter, analyzer, completeness, integrity, warnings, errors, and limitations.

Validation is fail-closed. A record cannot qualify until its canonical evidence and required identities are valid. See [`schemas/validation.schema.json`](schemas/validation.schema.json).
