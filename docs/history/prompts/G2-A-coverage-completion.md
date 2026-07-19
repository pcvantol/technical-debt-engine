# G2-A — Coverage Completion

| Field | Value |
| --- | --- |
| Prompt ID | `G2-A` |
| Program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Decision | `G2_A_COVERAGE_COMPLETION_CLOSED` |
| Created | 2026-07-19 |
| Freeze point | This immutable record is included before the reviewable transition. |

## Objective

Complete the existing read-only Coverage capability through public CLI,
evidence, policy, baseline/differential, and qualification proof against real
DJConnect CI artifacts. This work does not make TDE generate coverage, run
tests, or install consumer CI integration.

## Repository evidence

- Read-only GitHub Actions artifacts from `djconnect`, `djconnect-website`,
  and `djconnect-esp32` were assessed with the public CLI.
- Each produced `VALID` capability evidence and `QUALIFIED` runtime
  qualification. The detailed metrics and artifact runs are canonical in
  [Coverage Qualification](../../../COVERAGE_QUALIFICATION.md).
- A public-CLI baseline and differential for `djconnect-website` contained the
  `coverage` capability delta. Its explicit repository qualification was
  `QUALIFIED` with assessment decision `PASS`.
- Real Cobertura artifacts exposed duplicated method-line entries and zero/zero
  branch summaries. The existing normalizer now counts only class-owned source
  lines and represents the latter as unavailable, preserving fail-closed
  handling for malformed or inconsistent artifacts.

## Closure and limits

G2-A moves from the active backlog to completed work. Supported artifacts are
Cobertura-compatible XML (including coverage.py XML) and LCOV. JaCoCo and
other report formats are not added speculatively. Test execution, coverage
generation, test-health analysis, and consumer CI installation remain out of
scope; consumer rollout remains G2-D.

## Next bounded work

Select the small G2-D CI pilot set and perform the G2-C GitHub-native
security-tooling gap analysis before proposing any security analyzer work. No
architecture decision record is required: this increment corrects an existing
artifact normalizer and closes its existing capability workstream.
