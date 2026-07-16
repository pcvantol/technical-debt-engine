# R1-4H — Release Publication Completion: PyPI Publication Repair

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4H |
| Title | Release Publication Completion — PyPI Publication Repair |
| Branch | `codex/r1-4h-pypi-publication-repair` |
| Implementation commit | `7185edb50c8b703ae6782420d29a76067e2221c3` |
| Pull Request | Draft [#84](https://github.com/pcvantol/technical-debt-engine/pull/84) |
| Decision | `PYPI_PUBLICATION_BLOCKED` |
| Candidate SHA | `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Release version | `0.1.0` |
| Bundle identity / checksum | `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836` / `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752` |
| Original partial publication run | [29529932503](https://github.com/pcvantol/technical-debt-engine/actions/runs/29529932503) |
| Completion verification run | [29531471511](https://github.com/pcvantol/technical-debt-engine/actions/runs/29531471511) |
| Repaired PyPI Action | `pypa/gh-action-pypi-publish@cef221092ed1bacb1cc03d23a2d87d1d172e277b` |

## Validation

The original pinned PyPI Action container was unavailable from GHCR. R1-4H
updated only that immutable dependency to the current PyPA `release/v1` commit;
its container manifest exists and the publication contract tests pass.

Completion run `29531471511` passed preserved-bundle and authorization
verification. It stopped before PyPI after the all-target workflow created a
local tag and the remote correctly rejected push of existing immutable tag
`0.1.0`. Tag, GitHub Release, Docker index, candidate, bundle, and all
qualification/certification evidence remained unchanged. PyPI `0.1.0` remains
absent.

## Known limitations

The current workflow always executes tag/release/Docker stages before PyPI. It
cannot resume an already partially completed release without encountering the
immutable tag conflict.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Add a protected resumable completion workflow that verifies existing published identities, skips completed targets, publishes only preserved Python distributions through Trusted Publishing, and creates completion evidence. | The existing all-target workflow cannot reach PyPI after the immutable tag exists. | Resumable PyPI Publication Workflow and Completion Evidence | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
