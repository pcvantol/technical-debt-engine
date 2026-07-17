# R1-4I — Resumable PyPI Publication and Release Completion

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4I |
| Title | Resumable PyPI Publication and Release Completion |
| Branch | `codex/r1-4i-release-publication-completion` |
| Decision | `INTERNAL_RELEASE_COMPLETED` |
| Candidate SHA | `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Release version | `0.1.0` |
| Bundle identity / checksum | `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836` / `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752` |
| Authorization | `authorization.sha256.09973d239287053808740f38bb83b102146cc5a3ae943c5b1148f571ef2e4631` |
| Completion run | [29581079651](https://github.com/pcvantol/technical-debt-engine/actions/runs/29581079651) |
| Publication-evidence artifact | `8407067905` / `internal-release-publication-evidence-223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Generation 1 lifecycle | `RELEASED` |

## Outcome

The protected `internal-release` environment approved the resumable publication
run after PyPI Trusted Publishing was configured for
`technical-debt-engine-runtime`. The run verified the existing certified bundle
and authorization, verified the already-published tag, GitHub Release, and
Docker image, skipped those completed targets, and published only the preserved
wheel and source distribution to PyPI.

The tag remains `0.1.0` at the certified candidate SHA. The GitHub Release and
Docker OCI index remain unchanged; no `latest` Docker tag was created. No
candidate, package, OCI archive, qualification, certification, or authorization
record was rebuilt or changed.

## Verification

- Workflow run `29581079651`: success; preflight and publish jobs passed.
- PyPI artifact checksums exactly match the certified bundle:
  - wheel: `ae53b589492f2a379302c960c3f7827c9e515e9ff0d00726ddbb5ca9d7c5c4e0`
  - source distribution: `8aac975b9cf293cb31d3e24a66c0f0c27c9f169e8af447006906f43a2aa7272f`
- A clean PyPI installation of `technical-debt-engine-runtime==0.1.0` passed.
- Installed `tde --version` reports CLI/runtime `0.1.0`, schema `1.0.0`, and
  Generation `1`; installed `tde --help` passed.
- The publication-evidence artifact was downloaded and inspected. It records
  the certified candidate, GitHub Release, Docker digest, and Trusted
  Publishing mode.

## Archive and boundary

Generation 1 release lifecycle is `RELEASED`. This archive finalizes the R1-4I
release-completion prompt history. It does not supersede the Operational Reality
Audit: any remaining runtime recovery work is product work, not release repair.

This archive is immutable. Any correction requires a later prompt archive.
