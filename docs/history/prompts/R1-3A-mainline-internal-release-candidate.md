# R1-3A — Create and Certify Mainline Internal Release Candidate

| Field | Value |
| --- | --- |
| Prompt ID | `R1-3A` |
| Version | `1` |
| Branch | `codex/r1-3a-mainline-internal-release-candidate` |
| Candidate SHA | `a507838482a80b3eced48bfc6a157c11bb1f2ee7` |
| Release version | `0.1.0` |
| Workflow run | [29450643140](https://github.com/pcvantol/technical-debt-engine/actions/runs/29450643140) |
| Decision | `MAINLINE_INTERNAL_RELEASE_CANDIDATE_BLOCKED` |
| Release Qualification | `RELEASE_BLOCKED` / `NOT_READY` |
| Release Certification | Not started |
| Bundle identity/checksum | Not created |
| Pull Request | Recorded by the reviewable pull request for this branch. |
| Freeze | Immediately when the sole pull request becomes reviewable. |

## Validation and blocker

- `a507838` is the synchronized main merge of PR #67 and passes the required
  mainline ancestry check.
- Workflow run 29450643140 verified the exact SHA, built reproducible package
  artifacts, and built the non-published multi-platform OCI archive.
- Runtime Qualification, Policy (`PASS_WITH_WARNINGS`), Software Assurance,
  and Docker artifact verification passed within Release Qualification.
- Trusted Delivery failed because the release-qualification candidate branch is
  empty in the detached exact-SHA checkout, while Trusted Delivery and Software
  Assurance consume `TDE_CANDIDATE_SOURCE_BRANCH=main`. The manifest identity
  mismatch correctly resulted in `RELEASE_BLOCKED`.
- Release Certification, bundle assembly, artifact upload, and bundle retrieval
  were skipped. No final tag or external publication occurred.

## Deferred Work

Exactly one recommended next prompt: **R1-GOV-3 — Canonical Candidate
Source-Branch Identity Correction**. It must unify candidate source-branch
identity in all release-chain evidence before a fresh R1-3A attempt.
