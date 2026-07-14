# Platform Architect — Operational Reality Audit Entry Point

## Purpose

This is the single review entry point for the Platform Architect to assess the evidence-based operational reality of Technical Debt Engine on current `main` after Prompts 0–31.

**Audit decision: `TDE_PRODUCT_PARTIALLY_OPERATIONAL`**

The audit does not redesign architecture, add implementation, create a release, or start Generation 2 work. It distinguishes documented intent from executable, validated, qualified, released, and operational product behavior.

## Recommended review order

1. [Operational Reality Audit](OPERATIONAL_REALITY_AUDIT.md) — decision, command observations, dogfooding, release and DJConnect reality.
2. [Product Surface Matrix](PRODUCT_SURFACE_MATRIX.md) — installability, CLI, API, configuration, schemas, platforms and artifacts.
3. [Capability Reality Matrix](CAPABILITY_REALITY_MATRIX.md) — authoritative component-by-component truth classification.
4. [Implementation Inventory](IMPLEMENTATION_INVENTORY.md) — actual modules, registries, analyzers and no-op behavior.
5. [Test Reality Report](TEST_REALITY_REPORT.md) — test totals, coverage limits and false-maturity risks.
6. [Release Reality Report](RELEASE_REALITY_REPORT.md) — objective release and packaging conclusion.
7. [Documentation–Implementation Gap](DOCUMENTATION_IMPLEMENTATION_GAP.md) — historical claims corrected as current truth.
8. [Implementation Recovery Plan](IMPLEMENTATION_RECOVERY_PLAN.md) — prioritized, small-PR recovery sequence; not implementation authorization.

## Canonical navigation updates

- [Repository Status](REPOSITORY_STATUS.md) — current product status correction.
- [Management Summary](MANAGEMENT_SUMMARY.md) — management-level current truth.
- [Product Roadmap](PRODUCT_ROADMAP.md) and [Product Backlog](PRODUCT_BACKLOG.md) — recovery-oriented priorities.
- [Prompt Index](PROMPT_INDEX.md) — Prompt 32 audit traceability.

## Architectural baseline to preserve

The audit must be interpreted against, not used to replace, the frozen foundations:

- [Runtime Architecture](RUNTIME_ARCHITECTURE.md)
- [Schema Architecture](SCHEMA_ARCHITECTURE.md)
- [Capability Contract](CAPABILITY_CONTRACT.md)
- [Adapter SDK](ADAPTER_SDK.md)
- [Platform Strategy](PLATFORM_STRATEGY.md)
- [Platform Evolution Backlog](PLATFORM_EVOLUTION_BACKLOG.md)

## Review outcome expected

Confirm whether the evidence supports the `TDE_PRODUCT_PARTIALLY_OPERATIONAL` decision and use the recovery plan to select one explicitly scoped next prompt. Do not merge, release, or begin implementation as part of this review.
