# DJConnect Consumer Integration

## Generation 2 decision

DJConnect is the primary product; TDE is the supporting pipeline tool. A
consumer must use only a released, exact-pinned TDE version or immutable
artifact and the public `tde` CLI, configuration, schemas, evidence, and exit
codes. It must not import runtime modules, adapters, or capability logic, and
must not duplicate analyzer or policy logic.

The first selected G2-D consumer is `djconnect-pi`, a bounded Python/pip
observe pilot. Its selection, public-CLI contract, retained evidence, and
observed limitations are recorded in
[the Phase 1 Observe record](docs/djconnect-observe-pilot.md). A non-Python
consumer is not yet selected; this is not a platform-wide rollout.

G2-B established the platform-wide dependency-health baseline. The G2-D pilot
selects only `djconnect-pi` and does not claim that every repository runs TDE
as a required check.

Each selected pipeline progresses from read-only observation to warning and
soft-fail. A required check is allowed only after a documented stable-evidence
period. CI retains the canonical assessment evidence as an artifact. The
integration is preferably one thin pinned GitHub Actions integration or
reusable workflow.
