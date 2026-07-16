# Mainline Internal Release Candidate Status

## Current R1-4A candidate — certified and human-authorized, pending publication

| Field | Value |
| --- | --- |
| Candidate SHA | `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` |
| Candidate version | `0.1.0` |
| Source | synchronized `main`; PR #74 merge commit |
| Workflow run | [29483960813](https://github.com/pcvantol/technical-debt-engine/actions/runs/29483960813) |
| Artifact ID | `8369651393` (`docker-release-candidate-04b39c51e2e36a5ac70059f2c030e7cadd37dbe0`) |
| Retention | 90 days; expires 2026-10-14T08:34:55Z |
| Decision | `HUMAN_RELEASE_AUTHORIZATION_RECORDED`; publication pending R1-4C |
| Release Qualification | `RELEASE_QUALIFIED` / `READY` |
| Release Certification | `RELEASE_CERTIFIED` (`release-certification.sha256.0a165bf4491ed5609801f02cc142f6303c0f4205041a099d08586f17a4f18514`) |
| Bundle ID | `bundle.sha256.fe7a81f7daa9fafbf40a031c7988ad3e7b1b00dda94e4e91facc4e30352b4ec1` |
| Bundle checksum | `sha256:2c0a36cca64c632c58b7b9e7a4fc57b1af9804595da0bed4c6c822e1a91b4a11` |
| Generation 1 Recovery | Authorization policy and current-bundle authorization established; publication pending |
| Generation 1 Release Candidate | `CERTIFIED` |
| Generation 1 Internal Release | `PENDING HUMAN AUTHORIZATION` |

The preserved bundle was downloaded and verified without rebuilding. It is
complete and integrity-valid, contains the wheel, source distribution, OCI
archive, provenance, release manifest, qualification, certification, and
release evidence, and binds every item to this candidate SHA. Runtime
Qualification is `QUALIFIED`; Policy is `PASS_WITH_WARNINGS`; Software
Assurance and Trusted Delivery are `PASS`. The OCI archive contains qualified
`linux/amd64` and `linux/arm64` images and remains unpublished.

No Git tag, GitHub Release, PyPI publication, Docker publication, or `latest`
tag exists. R1-GOV-5 establishes that the Environment's sole reviewer and
self-review setting are valid for the current single-maintainer model. R1-4B
records the fresh candidate-bound authorization; publication remains a separate
protected operation.

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
