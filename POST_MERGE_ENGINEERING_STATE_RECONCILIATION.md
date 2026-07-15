# Post-Merge Engineering State Reconciliation

## Canonical rule

A reviewable pull request cannot truthfully record its own future human merge.
The next engineering session therefore verifies objective GitHub merge state
before substantive planning, confirms current `main` contains the accepted
change and the immutable Prompt History exists, then reconciles rolling
current-state documents when necessary.

## Lifecycle classification

| State | Meaning |
| --- | --- |
| `REVIEWABLE_FROZEN` | A ready pull request exists and its implementation scope is frozen. |
| `MERGED_UNRECONCILED` | GitHub proves merge into `main`; only rolling status documents still truthfully show the prior Freeze Point. |
| `MERGED_RECONCILED` | Objective merge state is reflected in rolling status; the next increment may proceed. |

These are engineering-governance lifecycle states, not product, qualification,
or release states.

## Responsibilities and fail-closed boundary

Immutable Prompt History records the preceding Freeze Point and is never
changed after merge. `ENGINEERING_STATUS.md` records current engineering truth;
`REPOSITORY_STATUS.md` records repository truth; `MANAGEMENT_SUMMARY.md`
records executive state; and `PROMPT_INDEX.md` records lifecycle traceability.

Only stale rolling status after a verified merge is an expected transition. Stop
for an unmerged or unverifiable PR, stale main, uncommitted work, missing
history, unresolved candidate, repository identity mismatch, or a status claim
whose implementation is absent from main. Future substantive prompts perform
the permitted rolling-status reconciliation in their own single PR; a separate
governance increment is needed only when the lifecycle method or historical
evidence itself is disputed.
