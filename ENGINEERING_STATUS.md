# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current program | TDE 1.1 — Cross-language Complexity Policy Parity |
| Lifecycle state | `IMPLEMENTATION_REVIEWABLE`; TDE 1.0.5 and all seven Observe-only integrations are complete. |
| Current branch | `codex/tde-1-1-complexity-parity` |
| Current decision | `ADR-0065_CROSS_LANGUAGE_COMPLEXITY_POLICY_PARITY` |
| Repository truth | `1.0.5` is the current published runtime. The authorized 1.1 increment retains the four capability public contract and adds canonical primary-language complexity adapters without changing thresholds, qualification semantics, or Observe-only governance. |
| Coverage baseline | `djconnect`: 87.73% lines and 68.91% branches; `djconnect-pi`: 75.10% lines and 62.38% branches; `djconnect-website`: 96.59% lines and 82.86% branches; `djconnect-esp32`: 88.83% lines and 60.53% branches. Each fresh G2-A completion artifact is `VALID` with `QUALIFIED` runtime. |
| Dependency-health baseline | All eight repositories produced valid, qualified capability evidence. Current outdated findings: `djconnect` 3, `djconnect-api` 4, `djconnect-website` 1, `djconnect-windows` 15, `djconnect-esp32` 1, and `djconnect-app` 0; `djconnect-pi` is explicitly unavailable because its direct requirements are unpinned; `djconnect-firmware` has no supported manifest. |
| Next planned public release | `1.1.0`, only after public-wheel, adapter and cross-platform qualification evidence is complete and the reviewable release PR is approved. |
| Security decision | G2-C is complete: the factual eight-repository inventory found no selected-pilot decision that justifies a TDE 1.0 security capability. Existing native controls remain the decision owners; see [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md). |
| Next recommended engineering work | Complete adapter/parser/source-classification tests, qualify the exact public wheel, then open one draft PR per selected consumer. Do not merge automatically or alter Observe mode. |

## Deferred Work

| Description | Reason | Activation condition | Priority |
| --- | --- | --- | --- |
| All non-1.0 platform and capability ambitions | Post-1.0 maintenance-first operating model. | Explicit demonstrated DJConnect problem statement. | Post-1.0 |

Historical prompt and release records remain immutable under
`docs/history/prompts/`; they do not override this rolling current-state
handoff.
