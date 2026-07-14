# ADR-0019: Adapter SDK

## Status

Accepted

## Context

The runtime needs extensible analyzer integration without analyzer-specific orchestration.

## Decision

Adopt the Adapter SDK as the sole supported extension mechanism between runtime and native analyzers.

## Consequences

Adapters own analyzer interaction and return bounded canonical output; future extension types do not redesign the runtime.

## Alternatives

Direct runtime-to-tool integrations were rejected because they compromise analyzer independence.
