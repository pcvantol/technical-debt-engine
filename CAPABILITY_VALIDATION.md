# Capability validation

Capability validation is an evidence-facing, fail-closed check of supported language, resolved configuration, required adapters, required analyzer versions, and measurement completeness. It emits canonical validation status and structured limitations; it does not silently substitute an unsupported adapter or incomplete measurement.

The validation result remains separate from execution status and qualification decision. A capability with insufficient valid evidence is `BLOCKED`, `PARTIAL`, or `NOT_SUPPORTED` as appropriate, and cannot claim a successful qualification.
