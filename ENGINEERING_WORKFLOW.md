# Engineering workflow

The mandatory, incremental engineering workflow applies to every future canonical prompt.

```text
Prompt
  ↓
Repository Synchronization
  ↓
Current Main Verification
  ↓
Objective Previous Pull Request Verification
  ↓
Post-Merge State Classification
  ↓
Rolling Status Reconciliation
  ↓
Canonical Repository Read
  ↓
Implementation Reality Check
  ↓
Engineering Planning
  ↓
Dedicated Branch
  ↓
Focused Implementation
  ↓
Validation
  ↓
Documentation Update
  ↓
Repository Status Update
  ↓
Management Summary Update
  ↓
Prompt Index Update
  ↓
Current Engineering Status Replacement
  ↓
Immutable Prompt Archive
  ↓
Commit(s)
  ↓
Exactly One Reviewable Pull Request
  ↓
STOP
```

## Rules

1. Every prompt begins with `git switch main` and `git pull --ff-only`. If either fails, stop.
2. After synchronization, verify the current branch, `HEAD`, repository and working-tree cleanliness, tracking branch, and fast-forward status. If verification fails, stop.
3. Verify the previous PR objectively through GitHub, its accepted merge commit in current `main`, and its immutable Prompt History. Reconcile a `MERGED_UNRECONCILED` rolling-status transition before planning; material inconsistency stops engineering.
4. Read the canonical repository state before the implementation reality check or engineering planning.
5. One prompt equals one engineering increment.
6. One engineering increment equals one pull request.
7. A pull request has one coherent objective.
8. A pull request is independently reviewable.
9. The next canonical prompt begins only after the prior prompt has produced a reviewable pull request.
10. Merge is always a separate, explicit engineering decision.
11. Every pull request leaves the repository in a valid state.
12. Every prompt completely replaces `ENGINEERING_STATUS.md` with current state and creates exactly one immutable prompt archive.
13. Current `main` and operational reality determine the next increment; prompt order is historical context only.

Engineering increments are intentionally small. Prompt numbering provides architectural traceability. A canonical prompt terminates with one reviewable pull request; it does not merge that pull request automatically.
