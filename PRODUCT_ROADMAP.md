# Product roadmap

## Current product truth

TDE `1.1.1` is the published and qualified public runtime. DJConnect is the
primary product; TDE is the supporting engineering tool for reliable DJConnect
pipeline decisions. Generation 1 and the bounded Generation 2 delivery are
complete. TDE 1.1 is the explicitly authorized, bounded cross-language
complexity parity increment.

## Generation 2 active roadmap

| Stream | Outcome | Gate before completion |
| --- | --- | --- |
| G2-A Coverage Completion | **Complete.** Existing CI artifacts are qualified canonical assessment evidence; TDE never produces them. | Public CLI/schema/policy/differential/qualification proof recorded against DJConnect CI artifacts. |
| G2-B Minimal Dependency Health | **Complete.** Platform-wide, package-manager-native dependency evidence for the active DJConnect repositories. | Inventory, bounded support, canonical evidence, policy, differential, qualification, and public-CLI proof recorded. |
| G2-C Security Gap Assessment | **Complete.** Existing GitHub-native and repository-native controls remain the decision owners; no TDE 1.0 security capability is justified. | Eight-repository factual inventory and explicit architecture decision recorded in [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md). |
| G2-D Consumer Integration | **Complete.** The exact public `1.1.1` CLI runs in non-blocking Observe mode on `main` for `djconnect`, `djconnect-pi`, `djconnect-api`, `djconnect-app`, `djconnect-esp32`, `djconnect-website`, and `djconnect-windows`. | Every consumer publishes valid, qualified evidence for `code_size`, `complexity`, `coverage`, and `dependency_health`. |
| G2-E Qualification and Release | **Complete.** Public `1.1.1` is released and qualified for the selected DJConnect consumers. | Public distribution, consumer qualification, retained evidence, and green post-merge Observe runs are recorded. |

Consumer integration remains Observe-only. It does not create required checks,
merge blocks, soft-fails, or consumer-side analyzer and policy duplication.

| TDE 1.1 Cross-language complexity parity | **Complete.** One canonical complexity capability now produces primary-product-language evidence for Python, TypeScript/JavaScript, Swift, C/C++, and C#. | Public 1.1.1 runtime; exact public pin in all seven Observe-only consumers; valid, qualified primary-language evidence and unchanged policy thresholds. |

## Release and operating model

Capabilities and consumer changes continue to merge in independently
reviewable PRs. A new public release requires an explicit DJConnect operational
need and qualification evidence; it is not automatic.

After `1.1.1`, TDE is maintenance-first: critical bug fixes, compatibility and
security maintenance, and capabilities justified by an explicit DJConnect
problem statement. No follow-on capability program begins automatically.
