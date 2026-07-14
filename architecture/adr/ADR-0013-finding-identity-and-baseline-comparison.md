# ADR-0013: Finding Identity and Baseline Comparison

## Status

Accepted

## Context

Baselines need to distinguish semantic finding changes from incidental location movement.

## Decision

Use deterministic finding identity and explicit transitions: unchanged, new, resolved, moved, and modified; baselines reference immutable validated evidence.

## Consequences

Comparisons disclose incompatibility rather than inventing cross-tool or cross-language equivalence.

## Alternatives

Location-only identities were rejected because ordinary edits create false new findings.
