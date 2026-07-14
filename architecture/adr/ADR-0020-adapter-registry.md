# ADR-0020: Adapter Registry

## Status

Accepted

## Context

Runtime planning requires deterministic adapter discovery and compatibility checking.

## Decision

Use a registry as the sole discovery source; prohibit hardcoded adapter lists.

## Consequences

Each adapter publishes identity, ownership, lifecycle, support, mapping, and compatibility before discovery.

## Alternatives

Code scanning and configuration-only discovery were rejected because they are non-deterministic and bypass governance.
