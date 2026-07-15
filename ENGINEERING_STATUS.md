# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current prompt | R1-3B Establish Internal Release Publication Infrastructure |
| Lifecycle state | `ACTIVE`; one reviewable PR is pending. |
| Current branch | `codex/r1-3b-publication-infrastructure` |
| Current pull request | Not yet created. |
| Current decision | `PUBLICATION_INFRASTRUCTURE_OPERATIONAL` pending review validation. |
| Current repository truth | Candidate `3fda62e72850f1c67f1554f7612580eccf16ae34` remains certified. R1-3B adds a checksum-, evidence-, candidate-, and authorization-structure preflight against its retained Actions bundle without rebuilding or publishing. |
| Next recommended prompt | R1-3C — Human Release Authorization. |

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- |
| Human release authorization and protected non-dry-run dispatch. | R1-3B establishes the workflow and Environment contract but cannot supply reviewer approval or Environment configuration. | R1-3C — Human Release Authorization | `P0` |
| Review hash-pinned build-toolchain upgrades separately. | `build` and `setuptools` updates alter release-producing inputs and require explicit reproducibility/release review. | Build Toolchain Refresh | `P1` |
| Create and certify a fresh mainline candidate. | R1-3A did not reach certification or bundle preservation. | R1-3A retry after R1-GOV-3 merges | `P1` |
| Human release approval and publication. | It requires a certified preserved bundle after a successful future candidate. | Human Release Authorization & Internal Publication | `P1` |
| Reduce remaining Complexity policy warnings (maximum 23; warning threshold 15). | Certification permits warnings; no blocking threshold is reached. | Complexity Quality Improvement | `P2` |
