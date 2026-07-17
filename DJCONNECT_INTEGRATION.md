# DJConnect Consumer Integration

## Generation 2 decision

DJConnect is the primary product; TDE is the supporting pipeline tool. A
consumer must use only a released, exact-pinned TDE version or immutable
artifact and the public `tde` CLI, configuration, schemas, evidence, and exit
codes. It must not import runtime modules, adapters, or capability logic, and
must not duplicate analyzer or policy logic.

The concrete pilot set is deliberately not selected by this repository. Before
G2-D, repository research selects a small representative set using active
development, real pipeline risk, supported analyzer/language, existing coverage
or dependency artifacts, reasonable execution time, clear ownership, and no
duplicate required checks.

Each selected pipeline progresses from read-only observation to warning and
soft-fail. A required check is allowed only after a documented stable-evidence
period. CI retains the canonical assessment evidence as an artifact. The
integration is preferably one thin pinned GitHub Actions integration or
reusable workflow.
