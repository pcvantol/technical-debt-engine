# R1-3A — Create and Certify Mainline Internal Release Candidate (retry)

| Field | Value |
| --- | --- |
| Prompt ID | `R1-3A` (retry after R1-GOV-3) |
| Version | `1` |
| Branch | `codex/r1-3a-mainline-candidate-retry` |
| Candidate SHA | `3fda62e72850f1c67f1554f7612580eccf16ae34` |
| Release version | `0.1.0` |
| Workflow run | [29451595432](https://github.com/pcvantol/technical-debt-engine/actions/runs/29451595432) |
| Artifact ID | `8357722985` |
| Bundle ID | `bundle.sha256.e0c12c31b0ecf4b0bc6a9a4054717ed4d449c70ff90af9fc917f0ac87c6deeef` |
| Bundle checksum | `sha256:a4cbaab6cf23b294d9777c1086798a2e68bb1f1d916276eaeb32627f52b68377` |
| Decision | `MAINLINE_INTERNAL_RELEASE_CANDIDATE_CERTIFIED` |
| Pull Request | [#71](https://github.com/pcvantol/technical-debt-engine/pull/71) |
| Implementation commit | `7c404b41198bb0b57221d33ae1772237fcfb2fbd` |
| Freeze | Immediately when the sole pull request becomes reviewable. |

## Evidence

- Candidate is the exact synchronized mainline SHA and passed the ancestry gate.
- The manual, non-publishing workflow produced reproducible wheel and source
  distribution artifacts plus a verified multi-platform OCI archive.
- Runtime Qualification is `QUALIFIED`; Policy is `PASS_WITH_WARNINGS`;
  Software Assurance and Trusted Delivery are `PASS`; Release Qualification is
  `RELEASE_QUALIFIED` / `READY`; Release Certification is `RELEASE_CERTIFIED`.
- The complete bundle was retained for 90 days, downloaded, and verified as
  complete and integrity-valid without rebuilding.

## Scope boundary

No Git tag, GitHub Release, PyPI publication, Docker Hub publication, or
`latest` tag was created.

## Deferred Work

Exactly one recommended next prompt: **R1-3B — Human Release Authorization &
Internal Publication**.
