# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current prompt | R1-GOV-3 Canonical Candidate Source-Branch Identity Correction |
| Lifecycle state | `REVIEWABLE_FROZEN`; PR #70 contains the completed candidate source-branch identity correction. |
| Current branch | `codex/r1-gov-3-candidate-source-branch-identity` |
| Current pull request | Reviewable [#70](https://github.com/pcvantol/technical-debt-engine/pull/70). |
| Current decision | `CANDIDATE_SOURCE_BRANCH_IDENTITY_CORRECTED` |
| Current repository truth | PR #69 is `MERGED_RECONCILED` at `933849f`. R1-3A remains blocked historically; the detached-SHA source-branch mismatch is corrected for a future fresh candidate attempt. |
| Next recommended prompt | R1-3A — Create and Certify Mainline Internal Release Candidate. |

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- |
| Create and certify a fresh mainline candidate after R1-GOV-3 merges. | The previous R1-3A candidate remains blocked and cannot be retried from a branch. | R1-3A — Create and Certify Mainline Internal Release Candidate | `P0` |
| Review hash-pinned build-toolchain upgrades separately. | `build` and `setuptools` updates alter release-producing inputs and require explicit reproducibility/release review. | Build Toolchain Refresh | `P1` |
| Create and certify a fresh mainline candidate. | R1-3A did not reach certification or bundle preservation. | R1-3A retry after R1-GOV-3 merges | `P1` |
| Human release approval and publication. | It requires a certified preserved bundle after a successful future candidate. | Human Release Authorization & Internal Publication | `P1` |
| Reduce remaining Complexity policy warnings (maximum 23; warning threshold 15). | Certification permits warnings; no blocking threshold is reached. | Complexity Quality Improvement | `P2` |
