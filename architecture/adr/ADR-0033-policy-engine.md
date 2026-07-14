# ADR-0033: Policy Engine

## Decision

Introduce a standalone, configuration-driven Policy Engine as the sole owner of policy evaluation.

## Consequences

The Runtime orchestrates policy evaluation and records Policy Evidence; it does not embed policy thresholds or policy decisions.
