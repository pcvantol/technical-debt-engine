# G2-E-1 — TDE 1.0.0rc1 Candidate Preparation

| Field | Record |
| --- | --- |
| Prompt ID | `G2-E-1` |
| Program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Branch | `agent/tde-1-0-rc1-qualification` |
| Implementation commit | `f84a9dd3f06385ca38ab6c87ffecdad39dffede0` |
| Pull Request | [#127](https://github.com/pcvantol/technical-debt-engine/pull/127) |
| Decision | `TDE_1_0_RC1_CANDIDATE_PREPARATION_READY` |
| Created / updated | 2026-07-27 / 2026-07-27 |
| Freeze reached | Yes — when PR #127 is made reviewable. |
| Prompt completed | Yes — candidate execution begins only from merged `main`. |
| Pull Request created | Yes — draft #127 was created before this record. |
| Engineering stopped | Yes — no candidate, publication, or consumer execution occurred in this increment. |

## Objective

Prepare the exact existing TDE 1.0 capability set for an immutable
`1.0.0rc1` candidate. This increment does not add a capability, analyzer,
schema, policy rule, ecosystem, or Runtime behavior.

## Implementation

- Align package metadata, Runtime identity, and public CLI identity on
  `1.0.0rc1`.
- Extend the existing policy compatibility declaration to list Coverage and
  `1.0.0rc1`; no rule or decision threshold changed.
- Make the existing release-candidate workflow select exactly `code_size`,
  `complexity`, `coverage`, and `dependency_health`.

## Validation summary

- `PYTHONPATH=src python -m unittest discover -s tests -v` passed.
- Two independent wheel/sdist builds had identical `SHA256SUMS`.
- Existing installed-wheel and source-distribution verification passed.
- `git diff --check` passed.

## Known limitations

- The immutable candidate does not yet exist: existing candidate validation
  requires its SHA to be reachable from merged `main`.
- No RC artifact is published, no Docker image is published, and no final
  `1.0.0` release is published.
- `djconnect-pi` remains pinned to `0.2.0` and in non-blocking OBSERVE until
  the exact public candidate is available.

## Deferred work

| Work | Reason for deferral | Priority |
| --- | --- | --- |
| Candidate build, Runtime/artifact/release qualification, and evidence bundle | Must use the exact merged mainline SHA. | Next increment |
| Public RC distribution and consumer qualification | Requires the immutable candidate and explicit public-artifact authorization. | Next increment |
| Final `1.0.0` publication, wider rollout, WARN, soft-fail, and required checks | Outside this candidate-preparation increment. | Post-candidate / post-1.0 as applicable |

## Recommended next prompt

Create the immutable candidate from merged `main`, qualify its existing public
artifacts and all four standard-profile capabilities, then run only
`djconnect-pi` against that exact public candidate in non-blocking OBSERVE.
