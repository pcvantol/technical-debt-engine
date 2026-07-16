# R1-4A — Create and Certify Current Mainline Release Candidate

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-4A |
| Title | Create and Certify Current Mainline Release Candidate |
| Version | 2 |
| Branch | `codex/r1-4a-mainline-release-candidate` |
| Implementation commit | `c217ee3230001c44e8ec6dc23af3daa3bbbfbcd8` |
| Pull Request | Draft [#75](https://github.com/pcvantol/technical-debt-engine/pull/75) |
| Decision | `CURRENT_MAINLINE_RELEASE_CANDIDATE_PARTIALLY_CERTIFIED` |
| Candidate SHA | `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` |
| Release version | `0.1.0` |
| Workflow run | [29483960813](https://github.com/pcvantol/technical-debt-engine/actions/runs/29483960813) |
| Bundle identity | `bundle.sha256.fe7a81f7daa9fafbf40a031c7988ad3e7b1b00dda94e4e91facc4e30352b4ec1` |
| Bundle checksum | `sha256:2c0a36cca64c632c58b7b9e7a4fc57b1af9804595da0bed4c6c822e1a91b4a11` |
| Bundle preservation | Actions artifact `8369651393`, expires 2026-10-14T08:34:55Z; retrieved and verified without rebuilding. |
| Runtime Qualification | `QUALIFIED` |
| Policy | `PASS_WITH_WARNINGS` |
| Software Assurance | `PASS` (`assurance.sha256.195634ce56b9c0c01f1d460386a9639715edfc67399e1f546ddb719540506da3`) |
| Trusted Delivery | `PASS` (`trusted-delivery.sha256.039235a25ad2204c8979978d1a51f992b8d14a0d2f025f8cfa1725741a839162`) |
| Release Qualification | `RELEASE_QUALIFIED` / `READY` |
| Release Certification | `RELEASE_CERTIFIED` (`release-certification.sha256.0a165bf4491ed5609801f02cc142f6303c0f4205041a099d08586f17a4f18514`) |
| Created and updated | 2026-07-16 |
| Freeze reached | No — finalization record is committed while the PR is draft. |

## Candidate and artifact evidence

The workflow verified that the candidate is the synchronized `main` snapshot
and an ancestor of `origin/main`. It built two byte-identical wheel/source
distribution sets, then bound the exact wheel and source distribution to a
non-published OCI archive. The OCI archive records index
`sha256:12f5ea8ba192528e6063a9109405e7ab64ee8dbd97ea7f363925bff5aa0064f1`,
`linux/amd64` digest `sha256:5994cd0b08caf7b652eea3f1185954c454519a57b7dd32a3bdb5950a3cf26356`,
and `linux/arm64` digest `sha256:14349342e2c826016abb78a7e5579ebcdf6037da42fc0a268ac6dcdfbcbdef91`.

Bundle verification returned `integrity=true` and `complete=true`. Retrieval
used the retained artifact and did not rebuild any artifact. No Git tag,
GitHub Release, PyPI upload, Docker push, or `latest` tag was created.

## Publication readiness and decision

The candidate is technically certified, but publication readiness is incomplete.
The `internal-release` Environment exists, while GitHub reports only one
reviewer and `prevent_self_review: false`; this fails the repository's
documented independent-reviewer and self-review-prevention contract. Therefore
the decision is partial rather than a publication-ready certification claim.

## Known limitations

OCI provenance records platform-qualified images but does not claim byte-for-byte
OCI reproducibility because BuildKit timestamps and metadata need separate
platform-equivalence analysis. This does not alter the passing candidate-bound
Docker artifact qualification.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Complete Environment protection and perform human release authorization against the preserved bundle. | Publication is excluded, and current Environment settings do not meet the canonical contract. | R1-4B — Human Release Authorization | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
