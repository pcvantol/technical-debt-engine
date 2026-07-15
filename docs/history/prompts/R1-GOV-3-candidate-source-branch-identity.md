# R1-GOV-3 — Canonical Candidate Source-Branch Identity Correction

| Field | Value |
| --- | --- |
| Prompt ID | `R1-GOV-3` |
| Branch | `codex/r1-gov-3-candidate-source-branch-identity` |
| Decision | `CANDIDATE_SOURCE_BRANCH_IDENTITY_CORRECTED` |
| Incident | R1-3A workflow run `29450643140` |
| Pull Request | Recorded by the reviewable pull request for this branch. |
| Freeze | Immediately when the sole pull request becomes reviewable. |

## Correction

Exact-SHA candidate checkouts are detached. R1-3A failed because Release
Qualification recorded Git's empty detached branch while Software Assurance and
Trusted Delivery correctly consumed the workflow-validated `main` branch.
Release Qualification now uses the same `TDE_CANDIDATE_SOURCE_BRANCH` fallback,
so its delivery manifest and all candidate-bound evidence share one branch
identity.

## Validation

- New deterministic regression test creates a detached Git checkout and proves
  the validated source branch is recorded.
- Focused release-chain tests pass.
- Full suite: 91 tests passed; `git diff --check` passed.
- No candidate, certification, bundle, tag, GitHub Release, PyPI package, or
  Docker publication was created.

## Deferred Work

Exactly one recommended next prompt: **R1-3A — Create and Certify Mainline
Internal Release Candidate**.
