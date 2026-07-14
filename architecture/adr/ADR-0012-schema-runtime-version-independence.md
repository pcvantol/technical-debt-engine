# ADR-0012: Schema and Runtime Version Independence

## Status

Accepted

## Context

Runtime releases and public contract evolution do not necessarily occur together.

## Decision

Record and version runtime and each schema family independently.

## Consequences

Consumers validate compatibility explicitly instead of inferring it from runtime version.

## Alternatives

A single combined version was rejected because it cannot describe compatible runtime-only or schema-only changes.
