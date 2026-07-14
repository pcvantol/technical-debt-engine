# ADR-0003: Capability Architecture

## Status

Accepted

## Context

Technical-debt assessment must support independent languages, projects, and engineering signals.

## Decision

Organize TDE around independently evolvable capabilities and adapters that map to a canonical technical-debt model.

## Consequences

Adapters remain isolated from consumers, while comparable output is normalized through documented capability contracts.

## Alternatives

A monolithic, language-specific analyzer was rejected because it cannot preserve independence and extensibility.
