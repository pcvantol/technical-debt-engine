# ADR-0008: Canonical Normalized Domain Model

## Status

Accepted

## Context

Adapters need a project-, language-, and analyzer-independent public contract.

## Decision

Adopt the versioned normalized Domain Model and its separated schema layers as the only public contract for analysis results.

## Consequences

Raw analyzer output remains internal and every adapter normalizes before validation, qualification, or reporting.

## Alternatives

Exposing native analyzer payloads was rejected because it couples consumers to tools.
