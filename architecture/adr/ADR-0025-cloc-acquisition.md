# ADR-0025: cloc Acquisition

## Status

Accepted

## Context

Analyzer installation must be safe and reproducible.

## Decision

Require an explicitly installed PATH executable; do not download mutable binaries or execute package scripts at runtime.

## Consequences

Packaging and cross-platform distribution are deferred to a later qualified increment.

## Alternatives

Runtime download/bundling was rejected pending explicit licensing and distribution approval.
