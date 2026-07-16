# R1-4F — Human Release Authorization

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4F |
| Title | Human Release Authorization |
| Branch | `codex/r1-4f-human-release-authorization` |
| Implementation commit | `336e5fda90bb881d0c6d9781f9c78182c3040731` |
| Pull Request | Draft [#81](https://github.com/pcvantol/technical-debt-engine/pull/81) |
| Decision | `CURRENT_MAINLINE_RELEASE_AUTHORIZATION_RECORDED` |
| Candidate SHA | `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Release version | `0.1.0` |
| Bundle identity | `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836` |
| Bundle checksum | `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752` |
| Authorization record | `release/authorizations/internal-release-0.1.0-223ccfe4.json` / `authorization.sha256.09973d239287053808740f38bb83b102146cc5a3ae943c5b1148f571ef2e4631` |
| Created and updated | 2026-07-16 |
| Freeze reached | No — this immutable record is committed while PR #81 is draft. |

## Authorization evidence

The record binds sole-maintainer approver `pcvantol`, timestamp, the exact
candidate/version/bundle, Actions artifact `8387371267`, protected Environment
`internal-release`, and `.github/workflows/internal-release-publish.yml`.
It independently approves the immutable Git tag, GitHub Release, PyPI, and
Docker Hub targets. `publicationExecuted` is false.

GitHub confirms `pcvantol` is the Environment's required reviewer and
self-review is permitted under the R1-GOV-5 verified single-maintainer policy.

## Validation

- Authorization validation returned `HUMAN_RELEASE_AUTHORIZATION_RECORDED` with no errors.
- Retrieved-bundle preflight returned `PUBLICATION_PREFLIGHT_READY`: integrity, completeness, candidate identity, and authorization structure are valid.
- PR #80 merged at `2c3d6f9`; its repaired workflow and immutable archive are present in main.
- `git diff --check` passed. No publication workflow dispatch, Git tag, GitHub Release, PyPI upload, or Docker publication occurred.

## Known limitations

The authorization does not publish. A separately protected manual workflow
must retrieve and re-verify this exact preserved bundle before publication.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Execute the protected manual publication workflow from the authorized preserved bundle only. | Publication is explicitly excluded from authorization. | R1-4G — Internal Release Publication | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
