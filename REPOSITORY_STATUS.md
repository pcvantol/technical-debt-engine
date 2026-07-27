# Repository status

| Field | Value |
| --- | --- |
| Generation | 2 — TDE 1.0 DJConnect Enablement Program |
| Product relationship | DJConnect is the primary product; TDE is its supporting engineering and pipeline-assessment tool. |
| Release state | `0.2.0` published and qualified on PyPI, GitHub Releases, and Docker; next planned public release is `1.0.0`. |
| Runtime and contracts | Public CLI, Runtime Execution Engine, registry capabilities, canonical evidence, declarative policies, assessment profiles, stable schemas, qualification, baselines, differentials, and distribution remain existing foundations. |
| Coverage completion | G2-A is operationally complete. TDE consumes existing CI coverage artifacts and does not run tests or create coverage; fresh post-merge branch evidence from `djconnect` and `djconnect-pi` plus public CLI, baseline/differential, and qualification validation complete the capability proof. |
| Active scope | The failed `1.0.0rc1` candidate is preserved as NO-GO evidence; the RC1 release-capability selection repair merged in PR #130 and RC2 preparation is reviewable in PR #131. After merge, a new immutable RC2, selected-consumer qualification, and integrated release remain. G2-A Coverage Completion, G2-B Minimal Dependency Health, and G2-C Security Gap Assessment are complete; G2-C approved no TDE 1.0 security capability. See [TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md). |
| Dependency-health baseline | Eight active DJConnect repositories were assessed with valid, qualified evidence. Current outdated findings are 3 (`djconnect`), 4 (`djconnect-api`), 1 (`djconnect-website`), 15 (`djconnect-windows`), 1 (`djconnect-esp32`), and 0 (`djconnect-app`); `djconnect-pi` has unavailable outdated evidence because its direct requirements are unpinned, and `djconnect-firmware` has no supported manifest. |
| Integration state | `djconnect-pi` is the sole selected G2-D consumer. Three successful public-CLI `0.2.0` Observe runs are retained; the pipeline remains non-blocking. No wider consumer set or enforcement phase is committed. |
| Operating model after 1.0 | Maintenance-first; only critical fixes, compatibility/security maintenance, or concrete DJConnect-problem-driven work. |

Earlier release-candidate, audit, and planning material remains historical
evidence. Current operational and roadmap truth is in
[ENGINEERING_STATUS.md](ENGINEERING_STATUS.md), [ROADMAP_INDEX.md](ROADMAP_INDEX.md),
and [PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md).
