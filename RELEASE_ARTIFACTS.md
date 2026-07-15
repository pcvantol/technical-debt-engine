# Release Artifacts

Generation 1 defines package-independent artifact contracts for Python wheels, source archives, standalone executables, Docker images, documentation bundles, and evidence bundles. Each artifact has a logical ID, type, version, checksum, provenance, and qualification state.

Every future release artifact is bound to the exact mainline candidate SHA
defined in [RELEASE_ARCHITECTURE.md](RELEASE_ARCHITECTURE.md). The preserved
bundle additionally records its workflow artifact ID, run ID, retention expiry,
access control, checksum, and retrieval procedure; publication retrieves those
files and never regenerates them.

## Current Docker-integrated candidate

Candidate `2d6132061807a433178a1ababc1709340cb937de` produced a non-published
OCI archive for `linux/amd64` and `linux/arm64`, bound to the exact wheel and
source archive. Its verified certified bundle is GitHub Actions artifact
`docker-release-candidate-2d6132061807a433178a1ababc1709340cb937de` from
[run 29446629544](https://github.com/pcvantol/technical-debt-engine/actions/runs/29446629544), retained until 2026-10-13. Bundle ID:
`bundle.sha256.139c9262145431fbfe52d827a081a50fdd04b9d19c564e3c8ffb34dc9b750cb0`.
It has not been published to Docker Hub or any registry.
