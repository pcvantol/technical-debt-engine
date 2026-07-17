# Internal Release 0.1.0 Report

## Decision

**INTERNAL_RELEASE_COMPLETED**

Release `0.1.0` is complete for the certified candidate
`223ccfe4b3646f1907ee7e2d7a8c07e8989badd7`. Publication used the preserved
certified bundle `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836`
with checksum `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752`.
No candidate was rebuilt or requalified.

## Published targets

| Target | Immutable identity | Verification |
| --- | --- | --- |
| Git tag | `0.1.0` -> `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` | Preserved by PyPI-only completion run |
| GitHub Release | [`0.1.0`](https://github.com/pcvantol/technical-debt-engine/releases/tag/0.1.0) | Preserved by PyPI-only completion run |
| Docker Hub | `docker.io/pcvantol/technical-debt-engine:0.1.0` | OCI index `sha256:aa648019045a442a0dbce029ee11ecb15c7755d845205fa8f07467e0faf18679` |
| PyPI | [`technical-debt-engine-runtime` `0.1.0`](https://pypi.org/project/technical-debt-engine-runtime/0.1.0/) | Trusted Publishing, run `29581079651` |

No `latest` Docker tag was created.

## PyPI completion evidence

After the PyPI Trusted Publisher was configured for
`technical-debt-engine-runtime`, GitHub Actions run
[`29581079651`](https://github.com/pcvantol/technical-debt-engine/actions/runs/29581079651)
verified the existing candidate, authorization, tag, GitHub Release, and Docker
identity; it skipped the already-completed immutable targets and published only
the preserved wheel and source distribution. Protected environment
`internal-release` approved the publish job.

The downloaded PyPI artifacts match the certified bundle exactly:

| Distribution | SHA-256 |
| --- | --- |
| `technical_debt_engine_runtime-0.1.0-py3-none-any.whl` | `ae53b589492f2a379302c960c3f7827c9e515e9ff0d00726ddbb5ca9d7c5c4e0` |
| `technical_debt_engine_runtime-0.1.0.tar.gz` | `8aac975b9cf293cb31d3e24a66c0f0c27c9f169e8af447006906f43a2aa7272f` |

An isolated PyPI installation of `technical-debt-engine-runtime==0.1.0`
succeeded. `tde --version` reported CLI/runtime `0.1.0`, schema `1.0.0`, and
Generation `1`; `tde --help` succeeded. Publication evidence artifact
`8407067905` (`internal-release-publication-evidence-223ccfe4b3646f1907ee7e2d7a8c07e8989badd7`)
was downloaded and inspected.

## Release boundary

This is a release-completion record, not a claim that every planned product
capability is operational. The Operational Reality Audit and its recovery plan
remain applicable to runtime capability claims.
