# DJConnect Production Pilot — Phase 1 (Observe)

## Status

G2-D is active in **OBSERVE** mode with one deliberately bounded consumer:
[`pcvantol/djconnect-pi`](https://github.com/pcvantol/djconnect-pi). This is
not a full platform rollout, a warning gate, a soft fail, or a required check.

## Selection

`djconnect-pi` was selected because it is an active Python/pip repository with
an existing GitHub Actions validation pipeline and a retained Cobertura coverage
artifact. It is the smallest useful production shape for the public
Python/Radon path and the pip ecosystem already represented in G2-B. The
selection does not commit a non-Python consumer or any additional rollout.

## Consumer contract

The merged consumer workflow installs exactly
`technical-debt-engine-runtime==0.2.0` and invokes only the public `tde` CLI.
It does not check out TDE source, import TDE runtime modules, change policies,
or run consumer test hooks. It uses the installed `standard` profile and a
declarative repository definition to produce assessment and repository
qualification evidence.

The workflow captures all TDE exit codes as observations, publishes
`tde-observe-evidence`, and exits successfully regardless of policy result.
The artifact contains CLI JSON output, runtime version, assessment evidence,
qualification evidence, and a summary. There was no pre-existing pilot
baseline, so this phase produces no differential evidence.

## Observed evidence

| Run | Ref | Workflow result | Observe step | Assessment | Qualification | Runtime / profile | Executed capabilities | Policy / repository qualification |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| [29684373080](https://github.com/pcvantol/djconnect-pi/actions/runs/29684373080) | PR #52 head | success | 3 s | 983 ms | 1,136 ms | `0.2.0` / `standard` | `code_size`, `complexity` | `FAIL` / `FAILED` |
| [29684757770](https://github.com/pcvantol/djconnect-pi/actions/runs/29684757770) | merged `main` | success | 3 s | 896 ms | 1,100 ms | `0.2.0` / `standard` | `code_size`, `complexity` | `FAIL` / `FAILED` |

The two successful observations have a mean assessment duration of **939.5 ms**
and a mean qualification duration of **1,118 ms**. The observe step measured
three seconds in both runs. This is a two-run observation, not a sufficient
stability history for a phase change.

## Practical findings

- **Stability and reproducibility:** both retained artifacts used the same
  runtime, profile, executed capability list, policy decision, and successful
  non-blocking workflow outcome.
- **Operational issue resolved:** the first PR attempt found Ubuntu's packaged
  `cloc 1.98`, while the published runtime requires `cloc 2.10+`. The merged
  workflow provisions the checksum-verified upstream `cloc 2.10`; both rows
  above succeeded with it.
- **False positives:** none have been classified from two runs. A `FAIL` policy
  decision is preserved as evidence and is not classified as a false positive.
- **Missing capability evidence:** the published `0.2.0` standard profile ran
  `code_size` and `complexity`; it did not execute coverage or dependency
  health. The consumer adds no workaround and records this as a release/pilot
  limitation.

## Next decision boundary

Remain in OBSERVE mode. Promotion to warn, soft fail, or required check needs a
documented stable-evidence period and an explicit decision; neither is made by
this record. Any change to the public runtime or to the released profile is
outside this consumer pilot.
