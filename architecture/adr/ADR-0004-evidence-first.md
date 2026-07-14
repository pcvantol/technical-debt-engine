# ADR-0004: Evidence First

## Status

Accepted

## Context

Automated engineering decisions need traceable facts rather than opaque conclusions.

## Decision

Use versioned, immutable, provenance-bearing evidence as the primary machine-readable result of assessment.

## Consequences

Reports and downstream consumers derive from canonical evidence; corrections create new evidence rather than mutating published records.

## Alternatives

Unversioned summaries and mutable result stores were rejected because they weaken auditability and compatibility.
