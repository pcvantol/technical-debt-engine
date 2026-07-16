# R1-4B — Human Release Authorization

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4B |
| Title | Human Release Authorization |
| Branch | `codex/r1-4b-human-release-authorization` |
| Implementation commit | `0eada9508ceebb74eff66411d942d8636773f91e` |
| Pull Request | Draft [#77](https://github.com/pcvantol/technical-debt-engine/pull/77) |
| Decision | `HUMAN_RELEASE_AUTHORIZATION_RECORDED` |
| Candidate SHA | `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` |
| Release version | `0.1.0` |
| Bundle identity | `bundle.sha256.fe7a81f7daa9fafbf40a031c7988ad3e7b1b00dda94e4e91facc4e30352b4ec1` |
| Bundle checksum | `sha256:2c0a36cca64c632c58b7b9e7a4fc57b1af9804595da0bed4c6c822e1a91b4a11` |
| Authorization record | `release/authorizations/internal-release-0.1.0-04b39c51.json` / `authorization.sha256.73d47d6991e39983669fe77468feb919107658978d881aa3c941d5780aa334bc` |
| Created and updated | 2026-07-16 |
| Freeze reached | No — this immutable record is committed while PR #77 is draft. |

## Authorization evidence

The record explicitly approves the immutable Git tag, GitHub Release, PyPI,
and Docker Hub targets for this candidate/version/bundle only. It records sole
maintainer `pcvantol`, authorization timestamp, Actions run `29483960813`,
artifact `8369651393`, retention expiry, `internal-release`, and
`.github/workflows/internal-release-publish.yml`. It records
`publicationExecuted: false`.

GitHub confirms that `pcvantol` is repository owner and sole direct
collaborator; the required reviewer of `internal-release` is also `pcvantol`
and self-review is permitted by the R1-GOV-5 single-maintainer policy.

## Validation

- Authorization-record validation returned `HUMAN_RELEASE_AUTHORIZATION_RECORDED` with no errors.
- Retrieved certified-bundle validation returned `PUBLICATION_PREFLIGHT_READY`; integrity, completeness, candidate identity, and authorization structure are valid.
- `git diff --check` passed and the working tree was clean before finalization.
- No Git tag, GitHub Release, PyPI upload, Docker Hub publication, or workflow dispatch occurred.

## Known limitations

Authorization does not publish artifacts. The protected publication workflow
must retrieve and re-verify the preserved bundle; repository collaborator and
Environment state must be re-verified before dispatch.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Execute the protected manual publication workflow using the authorized preserved bundle only. | Publication is explicitly excluded from this authorization increment. | R1-4C — Internal Release Publication | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
