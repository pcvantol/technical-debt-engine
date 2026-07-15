# R1-1 — Release Candidate Refresh & Re-Certification

| Field | Value |
| --- | --- |
| Prompt ID | `R1-1` |
| Branch | `codex/r1-1-release-candidate-refresh` |
| Candidate SHA | `5932411201556be628fb5ca93912a26f95b9d424` |
| Decision | `CURRENT_RELEASE_CANDIDATE_CERTIFIED` |
| Freeze | Immediately when the sole pull request becomes reviewable |

## Objective evidence

- Current `main` was synchronized and clean at the candidate SHA.
- Two independent deterministic builds produced byte-identical wheel and source
  distribution artifacts. Their SHA-256 identities, checksums, and provenance
  are recorded in `release/current-candidate-r1-1.json`.
- Installed wheel and source-distribution dogfooding passed.
- Fresh selected-capability Runtime Qualification was `QUALIFIED`; Policy was
  `PASS_WITH_WARNINGS`; Software Assurance and Trusted Delivery were `PASS`.
- Fresh Release Qualification was `RELEASE_QUALIFIED` / `READY`, with manifest
  digest `sha256:ae27eff699a244860c1980e0caa8c1302fae5183aa38104e4bbd8aae6b579a19`
  and Release Evidence ID
  `release-evidence.sha256.c04883536aabb8f721d959704d40ceed85b50254cfb8148ed51552cd71309dfc`.
- Fresh Release Certification was `RELEASE_CERTIFIED` with ID
  `release-certification.sha256.1faddeb93d49956055e59449bd70d2f897493650ad7b9d2362cb81c4e7996a2d`.

## Scope boundary

No Git tag, GitHub Release, Docker image publication, package publication, or
human release authorization occurred.

## Deferred Work

Human authorization and any release publication are intentionally deferred to
`R1-2 — Human Release Authorization & Publication`.
