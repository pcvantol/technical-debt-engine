# ADR-0014: Project-Independent Candidate Identity

## Status

Accepted

## Context

TDE must assess source trees that have no Git history or remote.

## Decision

Candidate identity explicitly supports immutable Git commit SHA where available, content digest fallback, or declared identity with validation status.

## Consequences

Evidence remains portable and validation can fail closed when identity is insufficient for a requested decision.

## Alternatives

Requiring a Git SHA was rejected because it excludes valid project-independent use.
