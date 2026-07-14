# ADR-0028: Canonical Complexity Model

## Status

Accepted

## Context

Analyzer output must be comparable without losing provenance.

## Decision

Normalize cyclomatic aggregate metrics and findings into canonical evidence while retaining native analyzer identity and raw hash.

## Consequences

Future analyzers map to the same metric namespace with explicit compatibility.

## Alternatives

Public native payloads were rejected.
