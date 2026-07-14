# Prompt Lifecycle

```text
Draft → Active → Reviewable → Merged → Archived
                         ↘ Superseded (optional)
```

| State | Meaning |
| --- | --- |
| Draft | Proposed, not yet the active engineering increment. |
| Active | The single current prompt being executed. |
| Reviewable | A focused branch and exactly one reviewable pull request exist. |
| Merged | The pull request has been merged by explicit human decision. |
| Archived | The immutable prompt history record is retained for context. |
| Superseded | An optional terminal state for a prompt replaced before merge. |

Only one prompt may be Active. Lifecycle state is not a substitute for product implementation, validation, qualification, release, or operational state.
