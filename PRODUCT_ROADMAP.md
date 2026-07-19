# Product roadmap

## Current product truth

TDE `0.2.0` is published and qualified. DJConnect is the primary product; TDE
is the supporting engineering tool for reliable DJConnect pipeline decisions.
Generation 1 is complete. Generation 2 is a deliberately compact path to
`1.0.0`, not an open-ended platform roadmap.

## Generation 2 active roadmap

| Stream | Outcome | Gate before completion |
| --- | --- | --- |
| G2-A Coverage Completion | Existing coverage artifacts become qualified canonical assessment evidence; TDE never produces them. | Public CLI/schema/policy/differential/qualification proof. |
| G2-B Minimal Dependency Health | **Complete.** Platform-wide, package-manager-native dependency evidence for the active DJConnect repositories. | Inventory, bounded support, canonical evidence, policy, differential, qualification, and public-CLI proof recorded. |
| G2-C Basic Security Evidence | Minimal normalized security evidence that adds one DJConnect assessment decision without duplicating native controls. | GitHub-native-tooling gap analysis and pilot decision proof. |
| G2-D Consumer Integration | A thin pinned public-CLI integration in a small selected DJConnect pilot set. | Observe → warn → soft-fail → required only after stability evidence. |
| G2-E Qualification and Release | One qualified public `1.0.0` release. | Artifact, consumer, limitation, and release qualification all green. |

The consumer set is selected before G2-D through repository research: active
development, real pipeline risk, supported analyzer/language, available
artifacts, practical duration, clear ownership, and no duplicate required
check. A Python repository and one non-Python repository are useful starting
shapes, not a preselected commitment.

## Release and operating model

Capabilities merge in independently reviewable PRs. There is no usual public
release per capability and no planned `0.3`, `0.4`, or `0.5` sequence. The
next planned release is `1.0.0`; an interim release requires an explicit
operational-necessity decision.

After `1.0.0`, TDE is maintenance-first: critical bug fixes, compatibility and
security maintenance, and capabilities justified by an explicit DJConnect
problem statement. No follow-on capability program begins automatically.
