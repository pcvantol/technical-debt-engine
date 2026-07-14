# ADR-0024: Code Size Observational Qualification

## Status

Accepted

## Context

The first capability must not turn existing repository size into an implicit release gate.

## Decision

Use default observational PASS for valid complete evidence; thresholds remain future policy configuration.

## Consequences

Missing analyzer/evidence blocks, while ordinary size does not fail without explicit policy.

## Alternatives

Fixed default limits were rejected as project-specific assumptions.
