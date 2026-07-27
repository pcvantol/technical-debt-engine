# G2-E-2 — RC1 Build-Tool Pin Repair

| Field | Record |
| --- | --- |
| Prompt ID | `G2-E-2` |
| Program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Branch | `agent/fix-rc1-build-tool-pin` |
| Implementation commit | `ba6000248c94dc7bb05fae617468620174afaf7b` |
| Pull Request | [#129](https://github.com/pcvantol/technical-debt-engine/pull/129) |
| Decision | `NO_GO_TDE_1_0_0_RELEASE_CANDIDATE_REPAIR_PREPARED` |
| Created / updated | 2026-07-27 / 2026-07-27 |
| Freeze reached | Yes — when PR #129 is made reviewable. |
| Prompt completed | Yes — candidate rebuilding begins only from merged `main`. |
| Pull Request created | Yes — draft #129 was created before this record. |
| Engineering stopped | Yes — no candidate, consumer, or publication action occurred in this repair increment. |

## Failing gate and root cause

Non-publishing candidate run
[30275763596](https://github.com/pcvantol/technical-debt-engine/actions/runs/30275763596)
failed at **Build package candidate**. The candidate workflow installed the
already hash-pinned `setuptools==83.0.0`, while `pyproject.toml` still required
`setuptools==80.9.0` as an isolated build dependency.

## Bounded repair and validation

The only change aligns the build-system requirement with
`setuptools==83.0.0`. No capability, analyzer, Runtime behavior, policy rule,
schema, ecosystem, consumer, or release target changed.

- Existing hash-pinned build tooling installed successfully.
- Two independent `1.0.0rc1` wheel/sdist builds produced identical checksums.
- Existing installed-wheel and source-distribution verification passed.
- `git diff --check` passed.

## Recommended next prompt

After PR #129 merges, rebuild the immutable candidate from the exact new
mainline SHA and rerun the existing candidate qualification workflow. Do not
change functionality or publish the final `1.0.0` release.
