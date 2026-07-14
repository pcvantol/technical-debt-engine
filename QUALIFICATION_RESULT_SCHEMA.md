# Qualification result schema

Qualification consumes only validated canonical evidence. It records policy ID/version, baseline and comparison identity, evaluated capabilities and rules, threshold and regression results, waivers, decision, reasons, limitations, and timestamps.

Allowed decisions are `PASS`, `PASS_WITH_WARNINGS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`. Execution status and qualification decision are separate. See [`schemas/qualification.schema.json`](schemas/qualification.schema.json).
