# Operational Release Certification

## Decision

`tde certify` consumes the canonical JSON produced by `tde release-qualify` and
creates a deterministic certification report. It does not rebuild, tag,
publish, or otherwise release a package.

```sh
tde --format json certify . \
  --qualification-evidence /path/to/release-qualification.json \
  --report-output /path/to/release-certification.json
```

It validates candidate and artifact identities, checksums, reproducibility and
provenance, persisted Release Evidence identity and digest, Runtime
Qualification and policy evidence, Software Assurance, Trusted Delivery,
Release Qualification, workflow integrity, and the canonical evidence envelope.
It consumes that evidence and does not repeat Runtime or Policy evaluation. The only decisions are `RELEASE_CERTIFIED` and
`RELEASE_NOT_CERTIFIED`.

## Current Internal Release Candidate (R1-1)

Fresh R1-1 certification is `RELEASE_CERTIFIED` for current main
`5932411201556be628fb5ca93912a26f95b9d424`. Its certification identity is
`release-certification.sha256.1faddeb93d49956055e59449bd70d2f897493650ad7b9d2362cb81c4e7996a2d`.
All candidate, artifact, reproducibility, provenance, manifest, Runtime,
Policy, Software Assurance, Trusted Delivery, Release Qualification, and
Release Evidence checks passed. The evidence example is
`release/current-candidate-r1-1.json`. Certification is not human release
authorization and no publication occurred.

## Publication boundary

Certification attests to the immutable candidate and its evidence. It remains
valid across later administrative merges, but not across a non-administrative
change to the release-producing repository state. Publication verifies the
commit classification and uses the certified candidate SHA, as defined in
[RELEASE_PUBLICATION.md](RELEASE_PUBLICATION.md); it does not require current
`main` to equal the candidate.

## Current Docker-integrated candidate (R1-2B)

Hosted run `29446629544` certified candidate
`2d6132061807a433178a1ababc1709340cb937de` as `RELEASE_CERTIFIED`. Its
verified bundle checksum is
`sha256:9fecca747da109ecdc8f9b60c453885b5446359577ba5459cd0e24e1179f7d8b`.
Certification is evidence only: no Docker Hub login, registry push, tag, or
release was performed.

## Historical Baseline

**RELEASE_NOT_CERTIFIED**

The release process has a coherent architecture and an immutable candidate manifest, but it cannot be certified as a trustworthy release system. This review creates no release, package, binary, or publication.

## Objective evidence

- Candidate manifest binds commit `f0baf98c72ba2c3ed6e10f34f4c6670e32fe6469`, runtime/CLI `0.1.0`, schema `1.0.0`, capabilities, adapters and policy.
- 41 unit tests and local schema validation passed during this certification review.
- Software Assurance and Trusted Delivery are operational but return `PASS_WITH_WARNINGS` for a clean candidate.
- Release Qualification is `RELEASE_BLOCKED`; Platform Certification is `PLATFORM_NOT_CERTIFIED`.

The missing immutable workflow, dependency provenance/lock, artifacts/checksums and platform certification make release-process trust insufficient.
