# ADR-0015: Capability Contract

## Status

Accepted

## Context

TDE requires independently evolvable engineering features without capability-specific runtime logic.

## Decision

Adopt one canonical, configuration-driven capability contract with explicit inputs, canonical outputs, validation, qualification, evidence, reporting, dependencies, ownership, and limitations.

## Consequences

The runtime orchestrates while capabilities provide behavior; capabilities never own reports or runtime context.

## Alternatives

Ad hoc analyzer-specific feature contracts were rejected because they undermine independent qualification.
