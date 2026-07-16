# R1-4E — Release Publication Workflow Identity Repair and Current Mainline Candidate Refresh

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4E |
| Branch | `codex/r1-4e-publication-identity-repair` |
| Final release-evidence commit | `3ab346d78115242d77ff5385acf7f25f85b77764` |
| Pull Request | Draft [#80](https://github.com/pcvantol/technical-debt-engine/pull/80) |
| Decision | `PUBLICATION_WORKFLOW_IDENTITY_REPAIRED_AND_CANDIDATE_CERTIFIED` |
| Failed publication run | [29526820939](https://github.com/pcvantol/technical-debt-engine/actions/runs/29526820939) |
| Tagger identity | `Technical Debt Engine Release Automation <technical-debt-engine-release[bot]@users.noreply.github.com>` |
| Superseded candidate | `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` |
| Fresh candidate | `223ccfe4b3646f1907ee7e2d7a8c07e8989badd7` |
| Release version | `0.1.0` |
| Candidate workflow run / artifact | `29527704042` / `8387371267` |
| Retention expiry | `2026-10-14T19:21:58Z` |
| Bundle identity / checksum | `bundle.sha256.f80926d7d5fb978c9da4f997230e76f9833f2d607a258553d92a807db22a2836` / `sha256:605fea97fde0e92ec15d5b1d3b836c16dc41bd6a70809996f04ccd323889d752` |
| Wheel / source checksum | `sha256:ae53b589492f2a379302c960c3f7827c9e515e9ff0d00726ddbb5ca9d7c5c4e0` / `sha256:8aac975b9cf293cb31d3e24a66c0f0c27c9f169e8af447006906f43a2aa7272f` |
| OCI archive / index | `sha256:11b666aacfe1f73ecb0894c08c4e426a960294ee6f0380087968dff13d11c0ab` / `sha256:aa648019045a442a0dbce029ee11ecb15c7755d845205fa8f07467e0faf18679` |
| Runtime / Policy | `QUALIFIED` / `PASS_WITH_WARNINGS` |
| Software Assurance / Trusted Delivery | `PASS` / `PASS` |
| Release Qualification / Certification | `RELEASE_QUALIFIED` / `RELEASE_CERTIFIED` |

## Validation

Run `29526820939` failed at annotated-tag creation with `Committer identity
unknown`, before tag, release, PyPI, or Docker steps. PR #78 merged at
`b3a552b`; PR #79 merged the repair at `223ccfe`.

The workflow configures and verifies the explicit repository-local identity and
retains tagger identity evidence. Isolated tests prove missing identity fails
before tag creation and approved identity tags the selected SHA. Dry-run
`29527658608` passed and skipped the publish job.

Fresh candidate run `29527704042` passed deterministic package builds,
multi-platform OCI construction, qualification, certification, and artifact
upload. Its bundle was retrieved and all `SHA256SUMS` entries verified without
rebuilding.

## Known limitations

Policy remains `PASS_WITH_WARNINGS` for known complexity findings. The fresh
candidate has no authorization; the previous authorization is not transferable.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Record explicit human authorization for the fresh candidate and preserved bundle. | Authorization is candidate-bound and publication remains excluded. | R1-4F — Human Release Authorization | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
