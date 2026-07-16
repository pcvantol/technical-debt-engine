# R1-4D — Internal Release Publication

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4D |
| Title | Internal Release Publication |
| Branch | `codex/r1-4d-internal-release-publication` |
| Implementation commit | `d70231cf09b59b71cbe40934efe88a52b7daaf81` |
| Pull Request | Draft [#78](https://github.com/pcvantol/technical-debt-engine/pull/78) |
| Decision | `INTERNAL_RELEASE_BLOCKED` |
| Candidate SHA | `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` |
| Release version | `0.1.0` |
| Bundle identity | `bundle.sha256.fe7a81f7daa9fafbf40a031c7988ad3e7b1b00dda94e4e91facc4e30352b4ec1` |
| Bundle checksum | `sha256:2c0a36cca64c632c58b7b9e7a4fc57b1af9804595da0bed4c6c822e1a91b4a11` |
| Authorization record | `release/authorizations/internal-release-0.1.0-04b39c51.json` / `authorization.sha256.73d47d6991e39983669fe77468feb919107658978d881aa3c941d5780aa334bc` |
| Publication workflow run | [29526820939](https://github.com/pcvantol/technical-debt-engine/actions/runs/29526820939) |
| Created and updated | 2026-07-16 |
| Freeze reached | No — this immutable record is committed while PR #78 is draft. |

## Publication eligibility and validation

The candidate is an ancestor of current main. All commits between the candidate
and current main were classified as administrative status, governance, prompt
history, release documentation, or authorization records. No Runtime,
dependency, build, Docker, artifact, workflow, qualification, or certification
change was present before the authorized workflow dispatch.

The workflow passed authorization validation, preserved-bundle preflight, and
immediate bundle re-verification. The protected `internal-release` Environment
approval and the R1-GOV-5 single-maintainer policy were verified.

The workflow then failed at `Create immutable Git tag and GitHub Release from
the certified bundle`: the runner did not have a Git committer identity for the
annotated tag. The failure occurred before creation of the tag or any release.

## No-side-effect verification

- No immutable Git tag was created.
- No GitHub Release was created.
- PyPI returned no `0.1.0` release.
- Docker Hub returned no `0.1.0` tag.
- No published digest or publication evidence exists.

## Known limitations

The publication workflow needs a deterministic Git `user.name` and `user.email`
before it can create the required annotated tag. Repairing that workflow is a
forbidden candidate-to-main workflow change, so this candidate cannot be
retried: a fresh current-main candidate must be created, qualified, certified,
bundled, authorized, and then published.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Repair deterministic Git identity in the publication workflow and establish a fresh current-main candidate through certification and authorization. | The failure blocks publication before tag creation; workflow repair invalidates the current candidate's administrative boundary. | Release Publication Workflow Identity Repair and Current Mainline Candidate Refresh | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
