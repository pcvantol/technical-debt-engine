# CI-1 — GitHub CI Tooling Refresh

| Field | Value |
| --- | --- |
| Prompt ID | `CI-1` |
| Branch | `codex/ci-tooling-refresh` |
| Decision | `CI_TOOLING_REFRESH_IMPLEMENTED` |
| Pull Request | Recorded by the reviewable pull request for this branch. |
| Freeze | Immediately when the sole pull request becomes reviewable. |

## Changes

- Added `requirements/ci-bootstrap.txt`: `pip==26.1.2` with the published
  wheel SHA-256 hash.
- Every GitHub workflow that invokes pip installs that bootstrap first using
  `--require-hashes`.
- Updated immutable references to `actions/setup-python` v6.3.0 and Docker
  QEMU/Buildx setup actions v4.2.0.

## Validation

- PyPI index confirmed `pip 26.1.2` is current.
- A clean temporary virtual environment installed the pinned pip through the
  hash-checked bootstrap and reported `pip 26.1.2`.
- Every workflow YAML file parsed successfully; `git diff --check` passed.

## Deferred Work

The hash-locked `build` and `setuptools` toolchain is intentionally unchanged:
changing it affects reproducible release artifacts and needs its own review.

Exactly one recommended next prompt: **R1-GOV-3 — Canonical Candidate
Source-Branch Identity Correction**.
