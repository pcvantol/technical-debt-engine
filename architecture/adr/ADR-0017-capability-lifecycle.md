# ADR-0017: Capability Lifecycle

## Status

Accepted

## Context

Capability maturity and availability need to be explicit and independent.

## Decision

Adopt PLANNED, IMPLEMENTED, VALIDATED, QUALIFIED, DEPRECATED, and REMOVED as the capability lifecycle.

## Consequences

Capability status cannot be inferred from runtime or release state and registry changes remain traceable.

## Alternatives

Using only release versions was rejected because it cannot represent independent capability maturity.
