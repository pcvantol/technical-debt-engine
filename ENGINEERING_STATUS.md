# Current Engineering Status

| Field | Current state |
| --- | --- |
| Current program | Generation 2 — TDE 1.0 DJConnect Enablement Program |
| Lifecycle state | `ACTIVE`; G2-B is complete and the remaining 1.0 work is deliberately bounded. |
| Current branch | `main` |
| Current decision | `G2_B_MINIMAL_DEPENDENCY_HEALTH_CLOSED` |
| Repository truth | `0.2.0` is published and qualified. Generation 1 is complete. G2-B now covers the eight active DJConnect repositories with native pip, npm, NuGet, SwiftPM, and PlatformIO evidence where applicable. `coverage` implementation merged at `a2cf9be`; G2-A remains the first outstanding capability completion because its end-to-end public qualification is still required. |
| Dependency-health baseline | All eight repositories produced valid, qualified capability evidence. Current outdated findings: `djconnect` 3, `djconnect-api` 4, `djconnect-website` 1, `djconnect-windows` 15, `djconnect-esp32` 1, and `djconnect-app` 0; `djconnect-pi` is explicitly unavailable because its direct requirements are unpinned; `djconnect-firmware` has no supported manifest. |
| Next planned public release | `1.0.0`, after the compact 1.0 scope and integrated qualification are complete. |
| Next recommended engineering work | Complete G2-A Coverage Completion and select the small G2-D pilot set; then perform the G2-C GitHub-native security-tooling gap analysis before proposing any security analyzer work. |

## Deferred Work

| Description | Reason | Activation condition | Priority |
| --- | --- | --- | --- |
| All non-1.0 platform and capability ambitions | Post-1.0 maintenance-first operating model. | Explicit demonstrated DJConnect problem statement. | Post-1.0 |

Historical prompt and release records remain immutable under
`docs/history/prompts/`; they do not override this rolling current-state
handoff.
