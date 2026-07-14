# ADR-0016: Capability Registry

## Status

Accepted

## Context

Consumers and runtime planning need reliable discovery without inspecting implementations.

## Decision

Use the canonical capability registry as the sole discovery source.

## Consequences

All capabilities declare lifecycle, ownership, adapters, languages, metrics, reports, and qualification support before discovery.

## Alternatives

Discovering capabilities from code, adapters, or configuration was rejected because it is non-deterministic and couples runtime planning to implementation.
