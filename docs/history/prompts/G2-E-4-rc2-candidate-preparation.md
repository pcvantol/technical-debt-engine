# G2-E-4 — RC2 Candidate Preparation

| Field | Record |
| --- | --- |
| Prompt ID | `G2-E-4` |
| Program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Branch | `codex/rc2-candidate-preparation` |
| Implementation commit | `6392654ba950963a718491c634274d269ae10644` |
| Pull Request | [#131](https://github.com/pcvantol/technical-debt-engine/pull/131) |
| Decision | `TDE_1_0_0_RC2_CANDIDATE_PREPARATION_READY` |
| Created / updated | 2026-07-27 / 2026-07-27 |
| Freeze reached | Yes — when PR #131 is made reviewable. |
| Prompt completed | Yes — candidate execution begins only from merged `main`. |
| Pull Request created | Yes — draft #131 was created before this record. |
| Engineering stopped | Yes — no candidate, consumer, or publication action occurred in this preparation increment. |

## Scope and rationale

RC1 is immutable NO-GO evidence: its build-tool and release-capability
selection gates failed in separate non-publishing runs. PR #130 repaired the
selection gate and merged at `9446cc191643e71738d959bd6428e50ee0bc99d6` with
all CI checks passing. RC2 is a new candidate identity, not a mutation or
republish of RC1.

The package, Runtime, CLI, and bundled-policy compatibility declarations now
identify `1.0.0rc2`. Existing tests were aligned with the current four-item
standard profile, current Runtime evidence shape, and candidate package
version. No capability, analyzer, policy rule, schema, workflow, consumer, or
publication behavior changed.

## Validation summary

- Full suite: 144 passed; one Docker integration test remained intentionally
  skipped unless its explicit environment flag is set.
- Two independent candidate builds produced identical package checksums.
- Installed wheel and source distribution verification passed.
- `git diff --check` passed.

## Known limitations and deferred work

- RC2 does not exist until PR #131 merges and the candidate workflow runs on
  its exact merged mainline SHA.
- No public RC distribution exists, so `djconnect-pi` remains on public `0.2.0`
  in non-blocking OBSERVE.
- Public RC distribution, selected-consumer qualification, and final `1.0.0`
  publication require separate evidence and explicit authority.

## Recommended next prompt

After PR #131 merges, dispatch the existing non-publishing Docker release
candidate workflow using the merged SHA and `1.0.0rc2`, verify the retained
bundle and all four selected capabilities, and record its GO/PARTIAL/NO-GO
result. Do not publish the final `1.0.0` release.
