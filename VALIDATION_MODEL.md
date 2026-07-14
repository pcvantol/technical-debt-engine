# Validation model

Validation is a runtime-owned, fail-closed gate between normalization and qualification. It verifies:

- schema and schema version;
- runtime version;
- adapter identity;
- native tool identity;
- repository identity;
- candidate identity; and
- measurement completeness.

Validation rejects malformed, incomplete, unsupported, or incompatible normalized records. It does not repair data, infer missing identity, or treat a partial result as complete. A rejection produces explicit limitations and a blocked execution path rather than qualification or reporting based on untrusted data.
