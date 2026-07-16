# Operational Release Qualification

`tde release-qualify` creates canonical, evidence-only release qualification.
It requires an explicit release-capability selection, executes that selection
through Runtime, and persists an integrity-bound Release Evidence record. It
consumes independently built artifact directories, Software Assurance, and
Trusted Delivery; it never tags, publishes, or creates a release.

```sh
tde --format json release-qualify . \
  --release-capability code-size \
  --release-capability complexity \
  --artifact-directory /path/to/build-one \
  --artifact-directory /path/to/build-two \
  --manifest-output /path/to/release-manifest.json
```

The output binds Git candidate identity, the selected capabilities, runtime
qualification (including execution, confidence, and limitations), policy
decision, artifacts/checksums/provenance, Software Assurance, Trusted Delivery,
and Release Qualification. The adjacent `*.release-evidence.json` record is
immutable: its digest and content-derived identity are referenced by the
manifest and then validated by Release Certification. Missing selection,
Runtime evidence, policy evidence, or an unexecuted required capability causes
`RELEASE_BLOCKED`.

## Current Internal Release Candidate (R1-1)

The refreshed candidate is current main
`5932411201556be628fb5ca93912a26f95b9d424`, with Code Size and Complexity
selected. Two independent local builds produced byte-identical wheel and sdist
checksums. Fresh Runtime Qualification was `QUALIFIED`, Policy was
`PASS_WITH_WARNINGS`, Software Assurance and Trusted Delivery were `PASS`, and
Release Qualification was `RELEASE_QUALIFIED` / `READY`. The immutable
candidate, manifest, artifact, provenance, and qualification identities are
recorded in `release/current-candidate-r1-1.json`. This is evidence only; it
does not authorize or publish a release.

## Publication boundary

Qualification binds an immutable candidate, not a moving `main` reference.
Later administrative merges do not rerun or invalidate this qualification.
Before publication, classify every intervening commit according to
[RELEASE_PUBLICATION.md](RELEASE_PUBLICATION.md); any non-administrative change
requires a new candidate and fresh qualification.

## Current Docker-integrated candidate (R1-2B)

Hosted run `29446629544` qualified candidate
`2d6132061807a433178a1ababc1709340cb937de` as `RELEASE_QUALIFIED` with the
non-published multi-architecture OCI archive included as a checksum-verified
artifact. The certified bundle is the retained Actions artifact documented in
[RELEASE_ARTIFACTS.md](RELEASE_ARTIFACTS.md); downloading it, rather than
rebuilding it, is the retrieval path.

This evidence is historical only. R1-GOV-2 classifies its candidate as a
non-mainline sibling and therefore not publishable; future qualification starts
from an exact mainline snapshot as defined in [RELEASE_ARCHITECTURE.md](RELEASE_ARCHITECTURE.md).

## Current mainline candidate (R1-3A)

Run `29451595432` qualified mainline candidate
`3fda62e72850f1c67f1554f7612580eccf16ae34` as `RELEASE_QUALIFIED` / `READY`.
Runtime Qualification is `QUALIFIED`, Policy is `PASS_WITH_WARNINGS`, and
Software Assurance and Trusted Delivery are `PASS`. Its immutable manifest
digest is `sha256:38074717a76e056faff176fa37fa0981b3b12a8c11de63bc5fa8428a052d1670`.

## Current mainline candidate (R1-4A)

Run `29483960813` qualified current-main candidate
`04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` as `RELEASE_QUALIFIED` / `READY`.
Runtime Qualification is `QUALIFIED`, Policy is `PASS_WITH_WARNINGS`, and
Software Assurance and Trusted Delivery are `PASS`. All candidate-bound
qualification checks, including reproducible package artifacts and the
non-published Docker archive, passed. Its Release Evidence identity is
`release-evidence.sha256.61276073a2154c28e2a46692d9ba0a43d47cd354c3b248d92abd3e1772e1d1d7`.
