# ADR-0026: Complexity Capability

## Status

Accepted

## Context

TDE needs an analyzer-rich reference capability.

## Decision

Implement Complexity as a capability-independent, adapter-normalized vertical slice.

## Consequences

Runtime consumes capability/adapter contracts, never analyzer names.

## Alternatives

Analyzer-specific runtime logic was rejected.
