# Capability qualification

Capability qualification consumes validated canonical evidence only. Its allowed outcomes are `PASS`, `PASS_WITH_WARNINGS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`.

Qualification binds policy, capability version, evidence identity, baseline/comparison where used, reasons, regressions, suppressions, and limitations. Execution status is not a qualification outcome: for example, a valid execution may fail policy, while an unavailable adapter may block qualification. See [QUALIFICATION_RESULT_SCHEMA.md](QUALIFICATION_RESULT_SCHEMA.md).
