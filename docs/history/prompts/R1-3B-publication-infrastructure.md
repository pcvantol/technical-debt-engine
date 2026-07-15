# R1-3B — Establish Internal Release Publication Infrastructure

| Field | Value |
| --- | --- |
| Prompt ID | `R1-3B` |
| Branch | `codex/r1-3b-publication-infrastructure` |
| Candidate | `3fda62e72850f1c67f1554f7612580eccf16ae34` / version `0.1.0` |
| Source bundle | Actions run `29451595432`, artifact `8357722985` |
| Decision | `PUBLICATION_INFRASTRUCTURE_OPERATIONAL` pending review validation |

R1-3B adds the canonical manual-only internal-release workflow and its read-only preflight verifier. It retrieves the retained certified bundle rather than rebuilding, validates checksums, candidate identity, all bundle artifact identities, release qualification/certification, and an authorization assertion's structural binding. Its dry run emits publication preflight evidence and has no external publication side effect.

The protected `internal-release` Environment contract is documented in `RELEASE_PUBLICATION.md`. The guarded non-dry-run job defines the future GitHub Release, PyPI Trusted Publishing, and Docker Hub version-tag path; it has not been dispatched. No tag, release, PyPI package, Docker image, or `latest` tag was created by this increment.

Exactly one recommended next prompt: **R1-3C — Human Release Authorization**.
