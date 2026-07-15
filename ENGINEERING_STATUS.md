# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current prompt | CI-1 GitHub CI Tooling Refresh |
| Lifecycle state | Active CI-maintenance increment; PR #68 is merged and reconciled. |
| Current branch | `codex/ci-tooling-refresh` |
| Current pull request | To be created after workflow validation. |
| Current decision | `CI_TOOLING_REFRESH_IN_PROGRESS` |
| Current repository truth | PR #68 is `MERGED_RECONCILED` at `03ae48b`. The R1-3A candidate remains blocked before certification; this increment updates only the CI bootstrap and immutable action references. |
| Next recommended prompt | R1-GOV-3 — Canonical Candidate Source-Branch Identity Correction. |

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- |
| Correct candidate source-branch identity across Release Qualification and Trusted Delivery. | R1-3A's exact-SHA detached checkout fails closed on divergent branch evidence. | R1-GOV-3 — Canonical Candidate Source-Branch Identity Correction | `P0` |
| Review hash-pinned build-toolchain upgrades separately. | `build` and `setuptools` updates alter release-producing inputs and require explicit reproducibility/release review. | Build Toolchain Refresh | `P1` |
| Create and certify a fresh mainline candidate. | R1-3A did not reach certification or bundle preservation. | R1-3A retry after R1-GOV-3 merges | `P1` |
| Human release approval and publication. | It requires a certified preserved bundle after a successful future candidate. | Human Release Authorization & Internal Publication | `P1` |
| Reduce remaining Complexity policy warnings (maximum 23; warning threshold 15). | Certification permits warnings; no blocking threshold is reached. | Complexity Quality Improvement | `P2` |
