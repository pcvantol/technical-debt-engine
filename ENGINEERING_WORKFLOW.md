# Engineering workflow

Generation 1 uses one mandatory, incremental engineering workflow. It applies to every future canonical prompt.

```text
Prompt
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
Commit(s)
  ↓
Exactly One Reviewable Pull Request
  ↓
STOP
```

## Rules

1. One prompt equals one engineering increment.
2. One engineering increment equals one pull request.
3. A pull request has one coherent objective.
4. A pull request is independently reviewable.
5. The next canonical prompt begins only after the prior prompt has produced a reviewable pull request.
6. Merge is always a separate, explicit engineering decision.
7. Every pull request leaves the repository in a valid state.

Engineering increments are intentionally small. Prompt numbering provides architectural traceability. A canonical prompt terminates with one reviewable pull request; it does not merge that pull request automatically.
