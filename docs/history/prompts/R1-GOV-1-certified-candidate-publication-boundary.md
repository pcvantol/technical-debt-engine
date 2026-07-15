# R1-GOV-1 — Certified Candidate Publication Boundary

| Field | Value |
| --- | --- |
| Prompt ID | `R1-GOV-1` |
| Branch | `codex/r1-gov-1-certified-candidate-boundary` |
| Certified candidate | `5932411201556be628fb5ca93912a26f95b9d424` |
| Administrative merge | `df8a36bc1b553c85e6a4e81abfdc20eaee2c2b08` |
| Decision | `CERTIFIED_CANDIDATE_PUBLICATION_BOUNDARY_ESTABLISHED` |
| Freeze | Immediately when the sole pull request becomes reviewable |

## Objective evidence

- The R1-1 candidate record reports `RELEASE_CERTIFIED` and binds the candidate
  to its qualified artifacts, checksums, provenance, manifest, and evidence.
- `git rev-list 5932411..df8a36b` identifies only `df8a36b` after the
  candidate. Its changed paths are rolling status, release governance/evidence,
  and prompt-history documentation; no Runtime, capability, dependency, build,
  package, artifact, Docker, or workflow path changed.
- The merge is therefore classified `ADMINISTRATIVE`.
- [RELEASE_PUBLICATION.md](../../../RELEASE_PUBLICATION.md) now requires
  publication to use the immutable certified candidate and fail closed on any
  non-administrative intervening commit. It removes current-main SHA equality
  as a publication precondition.

## Scope boundary

No Runtime, capability, Release Qualification, Release Certification, policy,
artifact, tag, or publication changed.

## Deferred Work

Human release authorization and the actual internal publication remain owned
by `R1-2 — Human Release Authorization & Internal Publication`.
