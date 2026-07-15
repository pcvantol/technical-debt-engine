# Mainline Internal Release Candidate Status

## R1-3A attempt — blocked

| Field | Value |
| --- | --- |
| Candidate SHA | `a507838482a80b3eced48bfc6a157c11bb1f2ee7` |
| Candidate version | `0.1.0` |
| Source | synchronized `main`; PR #67 merge commit |
| Workflow run | [29450643140](https://github.com/pcvantol/technical-debt-engine/actions/runs/29450643140) |
| Decision | `MAINLINE_INTERNAL_RELEASE_CANDIDATE_BLOCKED` |
| Release Qualification | `RELEASE_BLOCKED` / `NOT_READY` |
| Release Certification | Not started |
| Bundle | Not created or retained |

The exact-SHA ancestry gate, deterministic package builds, and non-published
multi-platform OCI archive succeeded. Release Qualification failed closed
because its candidate record read an empty detached-checkout branch while
Software Assurance and Trusted Delivery correctly used the validated
`TDE_CANDIDATE_SOURCE_BRANCH=main` value. The resulting delivery manifest did
not match Trusted Delivery's candidate identity.

No Git tag, GitHub Release, PyPI package, Docker publication, or bundle
artifact was created. This failed attempt is evidence only and is not a
certified candidate. A dedicated release-governance correction must make all
candidate-bound evidence consume one canonical source-branch identity before a
fresh mainline candidate attempt.
