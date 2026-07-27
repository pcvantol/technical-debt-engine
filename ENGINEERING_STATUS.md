# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Lifecycle state | `RC1_PREPARATION_READY`; G2-A, G2-B, and G2-C are complete and the remaining 1.0 work is deliberately bounded. |
| Current branch | `main` |
| Current decision | `TDE_1_0_RC1_CANDIDATE_PENDING_MAINLINE` |
| Repository truth | `0.2.0` is published and qualified. Generation 1 is complete. G2-A completed public CLI, baseline/differential, and qualification proof, then validated fresh post-merge branch-coverage artifacts from `djconnect` and `djconnect-pi`; TDE does not run tests or generate coverage. G2-B covers the eight active DJConnect repositories with native pip, npm, NuGet, SwiftPM, and PlatformIO evidence where applicable. G2-D has three successful `djconnect-pi` Observe runs using the exact public `0.2.0` CLI; the retained artifacts and limitations are recorded in [the Phase 1 Observe record](docs/djconnect-observe-pilot.md). |
| Coverage baseline | `djconnect`: 87.73% lines and 68.91% branches; `djconnect-pi`: 75.10% lines and 62.38% branches; `djconnect-website`: 96.59% lines and 82.86% branches; `djconnect-esp32`: 88.83% lines and 60.53% branches. Each fresh G2-A completion artifact is `VALID` with `QUALIFIED` runtime. |
| Dependency-health baseline | All eight repositories produced valid, qualified capability evidence. Current outdated findings: `djconnect` 3, `djconnect-api` 4, `djconnect-website` 1, `djconnect-windows` 15, `djconnect-esp32` 1, and `djconnect-app` 0; `djconnect-pi` is explicitly unavailable because its direct requirements are unpinned; `djconnect-firmware` has no supported manifest. |
| Next planned public release | `1.0.0`, after the immutable `1.0.0rc1` candidate is qualified with the selected consumer, artifacts, Runtime, and release evidence. See [TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md). |
| Security decision | G2-C is complete: the factual eight-repository inventory found no selected-pilot decision that justifies a TDE 1.0 security capability. Existing native controls remain the decision owners; see [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md). |
| Next recommended engineering work | From merged `main`, create and qualify the immutable `1.0.0rc1` candidate, then run the selected `djconnect-pi` consumer against that exact public candidate in OBSERVE mode. Do not promote to warn, soft fail, required, or wider rollout. |

## Deferred Work

| Description | Reason | Activation condition | Priority |
| --- | --- | --- | --- |
| All non-1.0 platform and capability ambitions | Post-1.0 maintenance-first operating model. | Explicit demonstrated DJConnect problem statement. | Post-1.0 |

Historical prompt and release records remain immutable under
`docs/history/prompts/`; they do not override this rolling current-state
handoff.
