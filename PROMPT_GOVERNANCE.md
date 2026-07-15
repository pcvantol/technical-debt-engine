# Prompt Governance

## Canonical rule

```text
One Prompt = One Engineering Increment = One Reviewable Pull Request
```

Merge remains an explicit human engineering decision. A prompt is scoped from
verified current `main` and current operational reality; historical prompt
order is informational, not an implementation queue.

## Mandatory initialization

Repository Synchronization and objective previous-PR verification begin every engineering prompt:

```text
Repository Synchronization → Current Main Verification → Objective Previous Pull Request Verification → Post-Merge State Classification → Rolling Status Reconciliation → Canonical Repository Read → Implementation Reality Check → Engineering Planning
```

Execute `git switch main` and then `git pull --ff-only`. Do not continue if
either command fails. Immediately verify the checked-out branch, `HEAD`,
repository and working-tree cleanliness, tracking branch, and fast-forward
status; any verification failure stops engineering. Then verify the preceding
pull request through GitHub, its accepted merge commit in current `main`, and
its immutable Prompt History. A merged PR with only stale rolling status is
`MERGED_UNRECONCILED`, an expected transition that must be reconciled before
planning. An unmerged/unverifiable PR, stale main, missing history,
uncommitted work, or absent accepted implementation is material and stops
engineering. Read the canonical sources
in [BOOTSTRAP.md](BOOTSTRAP.md) only after that gate succeeds. Planning must
derive the increment, program, repository truth, backlog, and deferred work
from current repository contents—not from prompt text, conversation history,
historical prompts, or AI memory.

## Sources of current work

The canonical handoff order is:

```text
Current main → Repository Status → ENGINEERING_STATUS → Recovery Plan → Next Engineering Increment
```

`ENGINEERING_STATUS.md` is the primary current handoff and contains no historical narrative. Every completed prompt replaces it completely. The repository must remain self-describing and preserve engineering memory without requiring chat history.

Immutable Prompt History records only the preceding Freeze Point and is never
edited after merge. `ENGINEERING_STATUS.md`, `REPOSITORY_STATUS.md`,
`MANAGEMENT_SUMMARY.md`, and `PROMPT_INDEX.md` are rolling documents: after
objective merge verification, they reflect `MERGED_RECONCILED` state. Future
substantive prompts may make this administrative reconciliation first in their
own PR; it is not a second engineering objective.

## Prompt index and history

[PROMPT_INDEX.md](PROMPT_INDEX.md) is navigation only. It links each prompt to its immutable archive, branch, pull request, commit, and lifecycle status. Immutable prompt archives live in [docs/history/prompts](docs/history/prompts); corrections are new prompts, never edits to an archive.
