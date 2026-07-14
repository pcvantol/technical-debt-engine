# G2-GOV-4 Historical Branch Closure

## Purpose

Classify the three historical commits left on local branches after the Engineering Method v2.2 transition, preserve traceability without rewriting history, and authorize local cleanup only when every required verification succeeds.

## Incident Summary

P1-1 PR #38 and G2-GOV-2 PR #39 were merged before later branch-only commits were created. P1-2 PR #41 subsequently delivered the reviewed Code Size persisted-evidence implementation. The historical commits must not be cherry-picked or represented as part of their earlier Pull Requests.

## Architect Decision

| Commit | Branch | Decision | Reason |
| --- | --- | --- | --- |
| `6f4d60c` | `agent/code-size-vertical-slice` | `SUPERSEDED_BY_P1_2_PR_41` | PR #41 contains the reviewed, merged implementation of automatic evidence persistence and persisted-evidence consumption. No merge candidate remains. |
| `d1aa3eb` | `agent/code-size-vertical-slice` | `REJECTED_AS_INVALID_HISTORICAL_FINALIZATION` | It amended historical P1-1 status after PR #38 and incorrectly attributed implementation and validation to that PR. History must not be rewritten. |
| `da548a8` | `agent/prompt-finalization-freeze` | `DEFERRED_GOVERNANCE_EVIDENCE` | It records the Prompt Freeze incident after PR #39. The incident is preserved by this new record, not by modifying historical prompt execution. |

## Current Main State

`origin/main` is `a8b867a` (`feat: complete persisted Code Size evidence flow (#41)`). PR #41 is merged and is the accepted implementation for the superseded Code Size functionality.

## Repository Cleanup Verification

| Required verification | `agent/code-size-vertical-slice` | `agent/prompt-finalization-freeze` | Result |
| --- | --- | --- | --- |
| Previous Pull Request merged | PR #38 merged at `b95e5b1` | PR #39 merged at `9f89404` | Pass |
| Remote branch absent | `origin/agent/code-size-vertical-slice` exists at `d1aa3eb` | `origin/agent/prompt-finalization-freeze` exists at `da548a8` | **Fail** |
| No open Pull Request references branch | None | None | Pass |
| Current main contains accepted implementation | PR #41 merged at `a8b867a` | Governance v2.2 records the incident | Pass |
| No remaining merge candidate | `6f4d60c` superseded; `d1aa3eb` rejected | `da548a8` deferred evidence only | Pass |

Cleanup authorization is **not granted**. The required remote-branch-absent condition is false. Neither local branch may be deleted by this prompt.

## Lessons Learned

- A merged Pull Request and a branch tip are distinct facts; branch-only commits require explicit classification.
- Squash merges do not make original branch commits Git ancestors of `main`; Pull Request evidence is required for closure decisions.
- The reviewable-state Freeze Point prevents late implementation from being silently treated as reviewed work.

## Engineering Method Implications

The Engineering Method v2.2 remains unchanged. This record applies it: no immutable history is edited, no superseded code is cherry-picked, and blocked cleanup is reported rather than inferred as safe.

## Required Follow-Up

An authorized governance prompt must first remove the two remote historical branches, re-run all cleanup verification, and only then delete the matching local branches.
