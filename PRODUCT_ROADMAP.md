# Product roadmap

## Operational product truth

TDE `1.1.1` is the published public runtime and the platform is now an
operational engineering-quality service for repository-independent consumers.
Its mission is to observe engineering quality through capability-based,
evidence-first analysis.

Generation 1 and Generation 2 are complete. TDE remains actively maintained,
but it is no longer an active consumer-integration delivery program. Normal
work follows a maintenance-first model.

## Completed milestones

| Milestone | Outcome |
| --- | --- |
| Generation 2 — Coverage completion | Existing consumer CI artifacts are canonical coverage evidence; TDE does not generate coverage itself. |
| Generation 2 — Dependency health | Package-manager-native outdated-dependency evidence is available for every selected DJConnect ecosystem. |
| Generation 2 — Security gap assessment | Existing GitHub-native and repository-native controls remain security decision owners; no security capability was justified. See [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md). |
| Generation 2 — Consumer integration | All seven selected DJConnect source consumers use the exact public `1.1.1` CLI in non-blocking Observe mode and publish qualified evidence for all four capabilities. |
| Generation 2 — Qualification and release | The public runtime and its selected consumers are qualified with retained canonical evidence. |
| TDE 1.1 — Cross-language complexity policy parity | One complexity capability evaluates Python, JavaScript/TypeScript, Swift, C/C++, and C# through the same canonical metric, thresholds, policy, and qualification route. |

## Operational maintenance

Priority is established by a demonstrated consumer or platform-maintenance
need. Normal work includes bug fixes, analyzer updates, dependency updates,
compatibility work, documentation, governance, and public-runtime maintenance.

TDE remains public, capability-driven, repository-independent, and
Observe-only. Consumer integration creates no required checks, merge blocks,
soft-fails, suppressions, or repository-specific policy forks.

## Future capability planning

New capabilities are not roadmap-driven. They may enter planning only after an
approved architectural assessment demonstrates that an engineering decision
cannot be made with the existing capability model.

```text
Architectural Assessment
  → Capability Decision
  → Implementation
  → Qualification
  → Public Runtime
  → Consumer Adoption
```

Routine product-quality findings remain owned by consumer repositories. They
do not create TDE roadmap work unless they demonstrate a missing engineering
decision and pass the architectural-assessment gate.
