# Mainline Internal Release Candidate Status

## Current R1-3A candidate — certified

| Field | Value |
| --- | --- |
| Candidate SHA | `3fda62e72850f1c67f1554f7612580eccf16ae34` |
| Candidate version | `0.1.0` |
| Source | synchronized `main`; PR #70 merge commit |
| Workflow run | [29451595432](https://github.com/pcvantol/technical-debt-engine/actions/runs/29451595432) |
| Artifact ID | `8357722985` (`docker-release-candidate-3fda62e72850f1c67f1554f7612580eccf16ae34`) |
| Retention | 90 days; expires 2026-10-13T21:20:53Z |
| Decision | `MAINLINE_INTERNAL_RELEASE_CANDIDATE_CERTIFIED` |
| Release Qualification | `RELEASE_QUALIFIED` / `READY` |
| Release Certification | `RELEASE_CERTIFIED` (`release-certification.sha256.0d7b4ba25494ced37ad39d114e0854f9b88d20f4050ddd9b2e19b8c3f5696b59`) |
| Bundle ID | `bundle.sha256.e0c12c31b0ecf4b0bc6a9a4054717ed4d449c70ff90af9fc917f0ac87c6deeef` |
| Bundle checksum | `sha256:a4cbaab6cf23b294d9777c1086798a2e68bb1f1d916276eaeb32627f52b68377` |
| Generation 1 Recovery | `COMPLETED` |
| Generation 1 Release Candidate | `CERTIFIED` |
| Generation 1 Internal Release | `PENDING HUMAN AUTHORIZATION` |

The preserved bundle was downloaded and verified without rebuilding. It is
complete and integrity-valid, contains the wheel, source distribution, OCI
archive, provenance, release manifest, qualification, certification, and
release evidence, and binds every item to this candidate SHA. Runtime
Qualification is `QUALIFIED`; Policy is `PASS_WITH_WARNINGS`; Software
Assurance and Trusted Delivery are `PASS`.

No Git tag, GitHub Release, PyPI publication, Docker publication, or `latest`
tag exists. This candidate is publication-ready but requires explicit human
authorization before the preserved bundle may be published.

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
