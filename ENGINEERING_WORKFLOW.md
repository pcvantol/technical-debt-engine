# Engineering workflow

The mandatory, incremental engineering workflow applies to every future canonical prompt.

```text
Prompt
  ↓
Repository Synchronization
  ↓
Current Main Verification
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
3. Read the canonical repository state before the implementation reality check or engineering planning.
4. One prompt equals one engineering increment.
5. One engineering increment equals one pull request.
6. A pull request has one coherent objective.
7. A pull request is independently reviewable.
8. The next canonical prompt begins only after the prior prompt has produced a reviewable pull request.
9. Merge is always a separate, explicit engineering decision.
10. Every pull request leaves the repository in a valid state.
11. Every prompt completely replaces `ENGINEERING_STATUS.md` with current state and creates exactly one immutable prompt archive.
12. Current `main` and operational reality determine the next increment; prompt order is historical context only.

Engineering increments are intentionally small. Prompt numbering provides architectural traceability. A canonical prompt terminates with one reviewable pull request; it does not merge that pull request automatically.
