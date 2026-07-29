# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current program | TDE 1.1 — Cross-language Complexity Policy Parity |
| Lifecycle state | `OPERATING`; TDE 1.1.1 and all seven Observe-only integrations are complete. |
| Current branch | `main` |
| Current decision | `ADR-0065_CROSS_LANGUAGE_COMPLEXITY_POLICY_PARITY` |
| Repository truth | `1.1.1` is the current published runtime. It completes the authorized 1.1 primary-language complexity parity increment while retaining the four capability public contract, thresholds, qualification semantics, and Observe-only governance. |
| Coverage baseline | Fresh 1.1.1 `main` evidence is `VALID` and `QUALIFIED` for all seven consumers: `djconnect` 88.63%, `djconnect-pi` 75.78%, `djconnect-api` 89.14%, `djconnect-app` 38.37%, `djconnect-esp32` 88.83%, `djconnect-website` 96.59%, and `djconnect-windows` 86.49%. |
| Dependency-health baseline | Fresh 1.1.1 evidence is valid for all seven consumers. Outdated dependencies are: `djconnect` 0, `djconnect-api` 3, `djconnect-app` 0, `djconnect-esp32` 1, `djconnect-website` 0, and `djconnect-windows` 15; `djconnect-pi` remains explicitly unavailable because its direct requirements are unpinned. |
| Next planned public release | None. Maintenance releases require a demonstrated consumer problem. |
| Security decision | G2-C is complete: the factual eight-repository inventory found no selected-pilot decision that justifies a TDE 1.0 security capability. Existing native controls remain the decision owners; see [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md). |
| Assessment and qualification baseline | Every selected consumer's latest public `1.1.1` `main` evidence is non-FAIL: `djconnect`, `djconnect-api`, `djconnect-pi`, and `djconnect-website` remain `PASS_WITH_WARNINGS`; post-remediation `djconnect-app` is 29 ([30473879160](https://github.com/pcvantol/djconnect-app/actions/runs/30473879160)), `djconnect-esp32` 25 ([30478582271](https://github.com/pcvantol/djconnect-esp32/actions/runs/30478582271)), and `djconnect-windows` 25 ([30482356905](https://github.com/pcvantol/djconnect-windows/actions/runs/30482356905)). All seven are `QUALIFIED`. |
| Next recommended engineering work | None required for TDE integration. Remain maintenance-first; activate Apple coverage improvement or dependency servicing only through a selected product need. `PASS_WITH_WARNINGS` is the accepted operating outcome; strict `PASS` is not an active requirement. |

## Deferred Work

| Description | Reason | Activation condition | Priority |
| --- | --- | --- | --- |
| All non-1.0 platform and capability ambitions | Post-1.0 maintenance-first operating model. | Explicit demonstrated DJConnect problem statement. | Post-1.0 |

Historical prompt and release records remain immutable under
`docs/history/prompts/`; they do not override this rolling current-state
handoff.
