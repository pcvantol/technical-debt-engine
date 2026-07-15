# AI session initialization

Every AI-assisted engineering session begins with repository synchronization. It
must not interpret the prompt, inspect implementation, or plan engineering work
until every synchronization and verification step succeeds.

```text
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
Implement focused increment
  ↓
Validate
  ↓
Update documentation
  ↓
Replace ENGINEERING_STATUS and archive the prompt
  ↓
Produce reviewable Pull Request
```

## Repository synchronization

Every engineering prompt begins by executing:

```sh
git switch main
git pull --ff-only
```

If either command fails, stop. Do not begin engineering.

## Current main verification

Immediately after synchronization, verify the checked-out branch, `HEAD`
commit, repository and working-tree cleanliness, tracking branch, and
fast-forward status. If any verification fails, stop. Current `main` is the
only repository state from which engineering may be planned.

## Post-merge verification and reconciliation

Before the canonical read, verify the immediately preceding pull request with
GitHub, confirm its merge commit is in current `main`, and confirm its immutable
Prompt History exists. `REVIEWABLE_FROZEN`, `MERGED_UNRECONCILED`, and
`MERGED_RECONCILED` are engineering lifecycle states only. A merged PR whose
rolling status still records its real Freeze Point is an expected
`MERGED_UNRECONCILED` transition: reconcile rolling status documents before
planning, without editing immutable history. Stop for material inconsistencies
such as unmerged/unverifiable PRs, stale main, missing history, uncommitted
work, or implementation absent from main.

## Canonical repository read

Only after synchronization and verification, read the canonical sources in
this order:

1. [BOOTSTRAP.md](BOOTSTRAP.md)
2. [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md)
3. [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md)
4. [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md)
5. [ROADMAP_INDEX.md](ROADMAP_INDEX.md)
6. The current active roadmap
7. The current active backlog
8. [PROMPT_INDEX.md](PROMPT_INDEX.md)
9. Prompt History only when historical context is required

Perform the implementation reality check only after this read. Engineering
planning then determines the current engineering increment, program,
repository truth, backlog, and deferred work from repository contents. Prompt
text, conversation history, historical prompts, and prior AI assumptions do
not determine current repository state.

The session must distinguish, in its working record and final report, between:

- **Repository facts:** directly observable current state.
- **Architectural decisions:** approved canonical choices, normally backed by an ADR.
- **Recommendations:** non-binding proposed actions.
- **Assumptions:** provisional statements that need validation.
- **Unresolved questions:** decisions or facts that prevent safe inference.

AI consumes canonical documentation, follows established architecture, respects source authority, avoids duplicate or competing documents, and updates documentation when an architectural change is approved. AI must not infer architecture where canonical documents exist, create competing roadmaps, modify governance implicitly, or change engineering principles outside a dedicated Engineering Governance prompt. Current `main` is the source of truth; repository status and operational evidence override historical prompt order. The repository, not chat history, preserves engineering continuity.
