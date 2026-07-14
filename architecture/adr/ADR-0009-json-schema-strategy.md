# ADR-0009: JSON Schema Strategy

## Status

Accepted

## Context

TDE needs portable, machine-readable, independently verifiable contracts.

## Decision

Use hand-maintained JSON Schema Draft 2020-12 artifacts with explicit IDs, local references, and deterministic development validation.

## Consequences

Schemas are canonical inputs to future generated models; no runtime model generation is introduced now.

## Alternatives

Proprietary schema formats and code-first contracts were rejected for portability and transparency reasons.
