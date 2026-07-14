# ADR-0002: Standalone Product

## Status

Accepted

## Context

TDE begins with DJConnect as a reference consumer but must serve arbitrary projects and consumers.

## Decision

TDE is an independent product with its own architecture, roadmap, governance, and release lifecycle.

## Consequences

Consumers integrate through stable public contracts and do not own TDE internals or planning.

## Alternatives

Embedding TDE as a DJConnect subsystem or plugin was rejected because it would compromise product independence.
