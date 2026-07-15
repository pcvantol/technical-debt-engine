# R1-GOV-2 — Mainline Snapshot Release Candidate Model

| Field | Value |
| --- | --- |
| Prompt ID | `R1-GOV-2` |
| Branch | `codex/r1-gov-2-mainline-snapshot-model` |
| Decision | `MAINLINE_SNAPSHOT_RELEASE_MODEL_ESTABLISHED` |
| Obsolete candidate | `2d6132061807a433178a1ababc1709340cb937de` |
| Reconciled main | `0d7fea6961b1ad495525427fb473c0629b3eb53b` |
| Shared parent | `a07271b9643961ab6f3b75672513a9fa253c6b92` |
| Pull Request | Recorded by the reviewable pull request for this branch. |
| Freeze | Immediately when the sole pull request becomes reviewable. |

## Incident and decision

The obsolete candidate and reconciled main are sibling commits. The candidate
is not an ancestor of main; main contains the intended Runtime, Docker,
workflow, tooling, and test changes. The prior publication stop was correct.
The evidence remains immutable but the candidate is
`SUPERSEDED_NON_MAINLINE_CANDIDATE` and must never be published.

R1-GOV-2 establishes an exact-mainline-SHA candidate snapshot, an ancestry
gate, manual exact-SHA candidate workflow checkout, candidate-bound artifact
and bundle evidence, supersession rules, retained-bundle retrieval, a separate
human authorization boundary, and a no-rebuild protected publication contract.

## Validation

- PR #66 is objectively merged at `0d7fea6` and rolling draft status is
  reconciled.
- Deterministic tests accept a mainline ancestor and reject a sibling/unmerged
  candidate; they also classify administrative versus product supersession.
- The candidate workflow is manual only and takes explicit SHA, version, and
  internal-profile inputs; it cannot run from a pull request.
- No candidate, final tag, GitHub Release, PyPI publication, or Docker Hub
  publication was created.

## Known limitations and Deferred Work

The replacement candidate must be created only after this governance change is
merged and main is synchronized. Protected publication credentials and approval
are intentionally not exercised by this increment.

Exactly one recommended next prompt: **R1-3A — Create and Certify Mainline
Internal Release Candidate**.
