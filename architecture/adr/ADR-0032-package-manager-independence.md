# ADR-0032: Package Manager Independence

## Status

Accepted

## Context

Runtime must not know package manager details.

## Decision

Use declarative ecosystem adapters behind Dependency Health.

## Consequences

New managers extend discovery without Runtime redesign.

## Alternatives

Runtime manifest parsing was rejected.
