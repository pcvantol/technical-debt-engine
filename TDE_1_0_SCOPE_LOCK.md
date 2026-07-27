# TDE 1.0 Scope Lock and Release Direction

## Decision

TDE `1.0.0` is a compact DJConnect enablement release, not a new capability
program. It makes the already completed assessment capability available through
one immutable public distribution, proves it with the selected consumer, and
then publishes it once. No capability, analyzer, runtime contract, policy,
schema, dashboard, or release-engineering expansion is authorized by this
decision.

TDE is **not** SonarQube, Dependabot, or GitHub Advanced Security. It is a
repository-independent normalization layer: it turns bounded, existing quality
information into reproducible assessment and qualification evidence for a
DJConnect pipeline decision. The specialized tools remain the owners of their
own security, dependency, and code-scanning decisions.

## Repository evidence reviewed

| Subject | Recorded repository fact | Product consequence |
| --- | --- | --- |
| Published Runtime | `technical-debt-engine-runtime` `0.2.0` is the current published and qualified distribution. | A consumer must use a published, exact-pinned distribution; source checkout is not consumer evidence. |
| Completed capability work | G2-A Coverage Completion and G2-B Minimal Dependency Health are complete. The source `standard` profile declares `code_size`, `complexity`, optional `coverage`, and optional `dependency_health`. | These are the only assessment capabilities available for the 1.0 release path. |
| Current consumer observation | `djconnect-pi` is the selected G2-D consumer. Its three retained successful Observe runs used public `0.2.0`, profile `standard`, and executed only `code_size` and `complexity`; the assessment was `FAIL` and repository qualification `FAILED`, while the workflow remained successful. | Observe proves non-blocking public-CLI operation, not a WARN or required-check decision, and does not prove the completed optional capabilities in a released distribution. |
| Security | The factual eight-repository assessment found no selected-pipeline decision that requires TDE security evidence. GitHub-native and repository-native controls remain owners. | No security capability belongs in 1.0. |
| Release foundations | Runtime qualification, artifact qualification, release qualification, and distribution foundations exist. | 1.0 reuses these foundations; it does not redesign release engineering. |

The third Observe record was merged in PR [#123](https://github.com/pcvantol/technical-debt-engine/pull/123). Earlier rolling status records still reported two runs and an unselected consumer. This review reconciles those rolling records to the immutable pilot evidence; it does not alter the historical record.

## Scope classification

### Necessary for 1.0

1. Create one immutable `1.0.0` release candidate from current `main` that
   carries the frozen public Runtime and the completed `standard` profile.
2. Run the selected `djconnect-pi` consumer against that exact candidate using
   only the public CLI, retain capability, assessment, differential when
   available, and qualification evidence, and record explicit unavailable
   states where the consumer has no applicable artifact or supported manifest.
3. Qualify the candidate, its package artifacts, the selected consumer, and
   known limitations through the existing release chain.
4. Publish one qualified immutable public `1.0.0` release after those
   qualifications are green.

### Necessary before the public release

- The exact release candidate must replace `0.2.0` for the final consumer
  qualification. The current Observe evidence is valid operational evidence,
  but it cannot prove capabilities absent from that published distribution.
- The selected consumer result must be reproducible and its limitations must
  be recorded. `FAIL` or `FAILED` assessment outcomes are evidence, not
  automatic release blockers, unless the existing release qualification says
  otherwise.
- The existing artifact, Runtime, consumer, and release qualification chain
  must be complete for the same immutable candidate.

### Consumer rollout

`djconnect-pi` remains the sole selected consumer through release. Its current
integration remains OBSERVE and non-blocking. Rollout to another DJConnect
repository, WARN, soft-fail, required checks, caching, adapters, policy
operators, or waivers requires a separate post-1.0 investment decision with a
named consumer, missing pipeline decision, retained evidence, and explicit
non-goals. “All repositories” is not a 1.0 acceptance criterion.

### Post-1.0

- Security-evidence normalization and any Dependency Review, container,
  licence, secret, or code-scanning expansion.
- A broader consumer rollout or any enforcement-phase promotion.
- Additional analyzers, language/ecosystem coverage, dashboards, hosted
  services, AI remediation, SARIF aggregation, test health, caches, parallel
  execution, policy operators, and waiver workflows.

## Release sequence

```text
Current Pi Observe evidence
        ↓
Immutable 1.0.0 release candidate
        ↓
Selected Pi consumer qualification
        ↓
Artifact + Runtime + release qualification
        ↓
One public immutable 1.0.0 release
        ↓
Evidence-led post-1.0 consumer rollout
```

This ordering is intentional. A consumer can only qualify the exact public
Runtime that release intends to distribute. It prevents the completed coverage
and dependency-health work from being represented as consumer-proven before it
is present in the immutable candidate.

## Architecture decisions

| Candidate | Decision | Evidence-based rationale |
| --- | --- | --- |
| New Security capability | Exclude from 1.0. | The Security Gap Assessment found no missing selected-pipeline decision and assigned existing controls as decision owners. |
| Dependency vulnerability scanning | Exclude from 1.0. | Dependency Health measures freshness, not CVEs; vulnerability evidence remains a native-tool concern without a proven consumer gap. |
| Coverage and Dependency Health | Include only as already completed capability content. | Both have completion evidence and are declared in the source standard profile; no further feature work is authorized. |
| `djconnect-pi` | Keep as the selected 1.0 consumer. | Three successful, retained-artifact Observe runs demonstrate public-CLI operation. |
| Other DJConnect repositories | Do not enroll for 1.0. | No repository-specific investment case or public-candidate qualification is recorded. |
| WARN / soft-fail / required check | Post-1.0. | Current evidence is Observe-only and the active exit criteria explicitly exclude promotion without a separate decision. |

## Readiness conclusion

**Yes.** After the remaining bounded release work, TDE is ready for public
`1.0.0` without a new capability. Readiness means that the immutable candidate,
the selected consumer, the release artifacts, and their qualification evidence
are all green and limitations are published. It does not mean universal
consumer rollout, security-platform replacement, or enforcement activation.

## Canonical follow-up

The next implementation prompt is: **“Create and qualify the immutable TDE
1.0.0 release candidate, then run the selected `djconnect-pi` consumer against
that exact public candidate in OBSERVE mode and retain the complete evidence
bundle.”** Its scope is release-candidate and consumer qualification only.
