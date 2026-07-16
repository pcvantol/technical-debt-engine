# Release Artifacts

Generation 1 defines package-independent artifact contracts for Python wheels, source archives, standalone executables, Docker images, documentation bundles, and evidence bundles. Each artifact has a logical ID, type, version, checksum, provenance, and qualification state.

Every future release artifact is bound to the exact mainline candidate SHA
defined in [RELEASE_ARCHITECTURE.md](RELEASE_ARCHITECTURE.md). The preserved
bundle additionally records its workflow artifact ID, run ID, retention expiry,
access control, checksum, and retrieval procedure; publication retrieves those
files and never regenerates them.

## Current certified mainline candidate

Candidate `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` produced the certified
internal version `0.1.0` bundle in Actions [run 29483960813](https://github.com/pcvantol/technical-debt-engine/actions/runs/29483960813), artifact
`8369651393`, retained through 2026-10-14. Bundle ID:
`bundle.sha256.fe7a81f7daa9fafbf40a031c7988ad3e7b1b00dda94e4e91facc4e30352b4ec1`;
checksum: `sha256:2c0a36cca64c632c58b7b9e7a4fc57b1af9804595da0bed4c6c822e1a91b4a11`.
It contains checksum-bound wheel, source distribution, multi-platform OCI
archive/provenance, and release-chain evidence. It was retrieved and verified
without rebuilding; it is not published.

## Current Docker-integrated candidate

Candidate `2d6132061807a433178a1ababc1709340cb937de` produced a non-published
OCI archive for `linux/amd64` and `linux/arm64`, bound to the exact wheel and
source archive. Its verified certified bundle is GitHub Actions artifact
`docker-release-candidate-2d6132061807a433178a1ababc1709340cb937de` from
[run 29446629544](https://github.com/pcvantol/technical-debt-engine/actions/runs/29446629544), retained until 2026-10-13. Bundle ID:
`bundle.sha256.139c9262145431fbfe52d827a081a50fdd04b9d19c564e3c8ffb34dc9b750cb0`.
It has not been published to Docker Hub or any registry.
