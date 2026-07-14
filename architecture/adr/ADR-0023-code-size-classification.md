# ADR-0023: Code Size File Classification

## Status

Accepted

## Context

Code Size needs portable source/test/documentation/generated/vendor separation.

## Decision

Use deterministic, project-neutral relative-path defaults with future configuration overrides.

## Consequences

Classification is visible in evidence and not repository-specific.

## Alternatives

Hardcoded consumer paths were rejected.
