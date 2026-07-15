# Prompt Lifecycle

```text
Draft → Active → REVIEWABLE_FROZEN → MERGED_UNRECONCILED → MERGED_RECONCILED → Archived
                                      ↘ Superseded (optional)
```

| State | Meaning |
| --- | --- |
| Draft | Proposed, not yet the active engineering increment. |
| Active | The single current prompt being executed. |
| REVIEWABLE_FROZEN | A focused branch and ready pull request exist; scope and implementation are frozen pending human review. |
| MERGED_UNRECONCILED | GitHub proves the pull request is merged into current `main`, but rolling status documents still describe the legitimate pre-merge Freeze Point. This expected transition does not alone block future work. |
| MERGED_RECONCILED | Objective merge evidence is represented in rolling status documents; the next increment may proceed. |
| Archived | The immutable prompt history record is retained for context. |
| Superseded | An optional terminal state for a prompt replaced before merge. |

Only one prompt may be Active. Lifecycle state is not a substitute for product implementation, validation, qualification, release, or operational state.

The immutable Prompt History records the preceding increment's actual Freeze
Point and is never amended to claim a future merge. The next session verifies
the PR and current `main`, preserves that history, and reconciles only rolling
status documents. An unmerged or unverifiable PR, stale main, missing history,
uncommitted work, or implementation absent from main is material and stops
engineering.
