# ADR-0007: Canonical Source Hierarchy

## Status

Accepted

## Context

AI-assisted and long-lived engineering requires a reliable way to resolve conflicting documentation and implementation.

## Decision

Adopt [CANONICAL_SOURCE_HIERARCHY.md](../../CANONICAL_SOURCE_HIERARCHY.md) as the authority order for repository sources.

## Consequences

Higher canonical documents prevail; lower sources are corrected through focused increments rather than silently overriding intent.

## Alternatives

Peer-level documents and implementation-as-authority were rejected because they permit undocumented architectural drift.
