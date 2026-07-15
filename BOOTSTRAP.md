# Bootstrap

This is the mandatory entry point for every human or AI engineering session.
Before reading this file, interpreting repository work, or making changes,
synchronize with current `main` and verify that synchronization.

## Repository synchronization

Every engineering prompt must execute:

```sh
git switch main
git pull --ff-only
```

If either command fails, stop. Do not begin engineering.

Immediately after synchronization, verify the checked-out branch, current
`HEAD` commit, repository and working-tree cleanliness, tracking branch, and
fast-forward status. If any verification fails, stop.

## Canonical reading order

After successful synchronization and verification, objectively verify the
immediately preceding pull request, its merged commit in current `main`, and
its immutable Prompt History. Classify a merge with only stale rolling status
as `MERGED_UNRECONCILED`, reconcile the rolling status before planning, and
stop for material inconsistency. Only then read:

1. [BOOTSTRAP.md](BOOTSTRAP.md)
2. [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md)
3. [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md)
4. [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md)
5. [ROADMAP_INDEX.md](ROADMAP_INDEX.md)
6. The current active roadmap and backlog named by that index
7. [PROMPT_INDEX.md](PROMPT_INDEX.md)
8. Current engineering work: the active prompt, its recovery-plan position, and applicable canonical documents
9. [ENGINEERING_METHOD.md](ENGINEERING_METHOD.md), [PROMPT_FINALIZATION.md](PROMPT_FINALIZATION.md), [REPOSITORY_HYGIENE.md](REPOSITORY_HYGIENE.md), [PLATFORM_VISION.md](PLATFORM_VISION.md), [PLATFORM_STRATEGY.md](PLATFORM_STRATEGY.md), [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md), and [CANONICAL_SOURCE_HIERARCHY.md](CANONICAL_SOURCE_HIERARCHY.md)
10. Applicable ADRs in [architecture/adr](architecture/adr), then relevant product architecture and capability documents

Perform the implementation reality check only after this canonical read, then
plan engineering from current repository contents. Consult
[docs/history/prompts](docs/history/prompts) only when historical context is
required. The repository must remain self-describing: chat history is never
required for engineering continuity. If sources conflict, use the canonical
hierarchy; current `main` overrides conversation history, historical prompts,
prompt examples, and AI memory. Do not infer a replacement architecture. One
prompt owns one objective, one increment, and one reviewable Pull Request. A
draft Pull Request is not frozen; `REVIEWABLE_FROZEN` begins when it becomes
reviewable. After human merge, `MERGED_UNRECONCILED` is permitted only while
rolling status awaits objective reconciliation; `MERGED_RECONCILED` permits the
next increment. Do not continue engineering or add implementation after the
Freeze Point; record any late discovery as Deferred Work for the next prompt. Confirm
repository hygiene with `git status --short` before completion.
