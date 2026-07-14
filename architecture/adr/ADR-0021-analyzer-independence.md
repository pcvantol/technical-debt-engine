# ADR-0021: Analyzer Independence

## Status

Accepted

## Context

Native analyzers are authoritative for their own measurements but must not shape TDE runtime or public contracts.

## Decision

Only adapters invoke analyzers and map their identity/output to canonical adapter output; runtime never invokes analyzers directly.

## Consequences

Consumers depend on canonical evidence, not a specific tool, and adapters remain isolated from one another.

## Alternatives

Duplicating analyzer logic or exposing raw tool output as public contract was rejected.
