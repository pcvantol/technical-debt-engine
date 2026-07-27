# G2-E-3 — RC1 Release-Capability Selection Repair

| Field | Record |
| --- | --- |
| Prompt ID | `G2-E-3` |
| Program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Branch | `codex/rc1-release-capability-aliases` |
| Implementation commit | `1d425792dbf3364ce30747ac1723a82cbe7cc99b` |
| Pull Request | [#130](https://github.com/pcvantol/technical-debt-engine/pull/130) |
| Decision | `NO_GO_TDE_1_0_0_RC1_RELEASE_CAPABILITY_REPAIR_PREPARED` |
| Created / updated | 2026-07-27 / 2026-07-27 |
| Freeze reached | Yes — when PR #130 is made reviewable. |
| Prompt completed | Yes — a new candidate begins only from merged `main`. |
| Pull Request created | Yes — draft #130 was created before this record. |
| Engineering stopped | Yes — no candidate, consumer, or publication action occurred in this repair increment. |

## Failing gate and root cause

Non-publishing candidate run
[30278550321](https://github.com/pcvantol/technical-debt-engine/actions/runs/30278550321)
failed at **Qualify and certify the complete candidate without publication**.
Its existing workflow selected `code-size`, `complexity`, `coverage`, and
`dependency-health`, but `release-qualify` only accepted the first two names.
The candidate therefore failed closed before Runtime, artifact, release, or
certification qualification could complete.

## Bounded repair

The existing `release-qualify` capability-alias map now also accepts
`coverage` and `dependency-health`, mapping them to the existing canonical
capability identifiers. A regression test verifies the complete four-item
selection. This introduces no capability, analyzer, policy, schema, consumer,
workflow, publication, or final release.

## Validation summary

- The targeted `tests.test_release_qualification` suite passed (5 tests).
- `git diff --check` passed.
- The full suite ran: 138 passed and 1 was skipped. Six failures/errors are
  pre-existing RC-preparation drift outside this repair: release-bundle and
  publication fixtures still assert package version `0.2.0`; one profile test
  expects `1.0.0` rather than `1.2.0`; and two Runtime tests assert the former
  stage/evidence shape. The new release-capability test passed.

## Known limitations

- RC1 cannot be repaired or republished: it remains immutable NO-GO evidence.
- No public RC distribution exists. `djconnect-pi` remains pinned to `0.2.0`
  in non-blocking OBSERVE until an exact public RC is explicitly authorized.
- The candidate workflow must be rerun only after this repair merges, using a
  new exact mainline SHA and a new RC version.

## Deferred work

| Work | Reason for deferral | Priority |
| --- | --- | --- |
| New immutable RC2 and hosted non-publishing qualification | Requires the exact merged mainline SHA. | Next increment |
| Public RC distribution and `djconnect-pi` qualification | Requires a qualified RC2 and explicit publication authorization. | Next increment |
| Final `1.0.0` publication and broader consumer rollout | Outside this repair and requires all candidate evidence. | Post-candidate / post-1.0 |

## Recommended next prompt

After PR #130 merges, create one immutable `1.0.0rc2` candidate from the exact
merged `main` SHA, run the existing non-publishing candidate workflow with all
four capabilities, and retain its evidence. Do not publish the final `1.0.0`
release.
