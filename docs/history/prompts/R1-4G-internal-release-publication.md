# R1-4G — Internal Release Publication

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4G |
| Title | Internal Release Publication |
| Branch | `codex/r1-4g-internal-release-publication` |
| Implementation commit | `3f141aac8922ec251513e8518e67ed71af317e6a` |
| Pull Request | Draft [#82](https://github.com/pcvantol/technical-debt-engine/pull/82) |
| Decision | `INTERNAL_RELEASE_PARTIALLY_COMPLETED` |
| Candidate SHA | `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Release version | `0.1.0` |
| Bundle identity | `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836` |
| Bundle checksum | `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752` |
| Authorization | `authorization.sha256.09973d239287053808740f38bb83b102146cc5a3ae943c5b1148f571ef2e4631` |
| Publication run | [29529932503](https://github.com/pcvantol/technical-debt-engine/actions/runs/29529932503) |
| Git tag | `0.1.0` → `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Docker OCI index | `sha256:aa648019045a442a0dbce029ee11ecb15c7755d845205fa8f07467e0faf18679` |

## Completed publication targets

The workflow re-verified the preserved bundle and authorization, configured the
approved deterministic tagger identity, created immutable tag `0.1.0`, created
the GitHub Release, and published the preserved OCI artifact to Docker Hub.
Docker Hub confirms `linux/amd64` digest
`sha256:8042fb9e9d89d35e85d0350ef98569c5ba4c41c3e8d6bc1484ec4e668f8dee37`
and `linux/arm64` digest
`sha256:64d0208459b395f84af74e416cff5efb78b12e0475a73c0efc6832a54ff53f09`.
No `latest` tag was published.

## Blocking result

PyPI was not published. The pinned
`pypa/gh-action-pypi-publish@6733eb7d741f0b11ec6a39b58540dab7590f9b7d`
container failed to pull from GHCR with `manifest unknown`. The workflow stopped
before publication evidence creation. No artifact was rebuilt.

## Validation

- Candidate ancestry and administrative-only boundary passed before dispatch.
- Bundle preflight and immediate pre-publication verification passed.
- Git tag, GitHub Release target SHA, and Docker OCI index/platform digests were verified after the run.
- PyPI endpoint for `0.1.0` returned 404.
- `git diff --check` passed.

## Known limitations

The GitHub Release currently has only the workflow's existing checksum and
bundle-manifest attachments because the failure occurred before later evidence
processing. PyPI and workflow publication evidence remain incomplete.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Restore availability of the immutable PyPI publishing action container, publish only the preserved wheel and source distribution, and create completion evidence without rebuilding. | The pinned action container is unavailable from GHCR; tag, GitHub Release, and Docker are already immutable published state. | Release Publication Completion and PyPI Action Availability Repair | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
