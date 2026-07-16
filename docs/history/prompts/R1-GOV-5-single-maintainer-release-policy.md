# R1-GOV-5 — Single Maintainer Internal Release Authorization Policy

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-GOV-5 |
| Title | Single Maintainer Internal Release Authorization Policy |
| Branch | `codex/r1-gov-5-single-maintainer-policy` |
| Implementation commit | `1fbfaf2b6b60c1e343dc5bd7d379047d94b73f8b` |
| Pull Request | Draft [#76](https://github.com/pcvantol/technical-debt-engine/pull/76) |
| Decision | `SINGLE_MAINTAINER_RELEASE_POLICY_OPERATIONAL` |
| Created and updated | 2026-07-16 |
| Freeze reached | No — this immutable record is committed while PR #76 is draft. |

## Canonical policy

GitHub identifies `pcvantol` as the repository owner and only direct
collaborator. In this objectively verified single-maintainer operating model,
the `internal-release` protected Environment may require that sole maintainer
and permit self-review. Self-approval is valid only together with an explicit
immutable authorization record that binds approver identity and timestamp, the
candidate SHA, bundle identity/checksum, approved targets, and publication
workflow. Bundle retrieval/verification, candidate verification, and
publication evidence remain mandatory.

If multiple maintainers exist, independent approval and self-review prevention
become mandatory before publication. The policy does not permit a historical
single-maintainer authorization to bypass the future team model.

## Protected Environment and validation

GitHub reports Environment `internal-release` with required reviewer
`pcvantol` and `prevent_self_review: false`, consistent with this policy. The
existing historical authorization record validates fail-closed and confirms all
required binding fields; it remains bound to its prior candidate and does not
authorize the current preserved bundle. `git diff --check` passed and the
working tree was clean before finalization. No tag, GitHub Release, PyPI upload,
Docker push, candidate regeneration, qualification, certification, or
publication occurred.

## Known limitations

GitHub collaborator and Environment state are external configuration and must
be re-verified at each authorization. A maintainer-model change requires the
multi-maintainer branch of this policy before authorization.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Create and approve a fresh authorization record for the current certified bundle. | Policy is operational but does not itself authorize or publish. | R1-4B — Human Release Authorization | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
