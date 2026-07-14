# ADR-0027: Complexity Analyzer Selection

## Status

Accepted

## Context

Languages need native complexity analyzers with one normalized model.

## Decision

Use Radon 6.0.1 for implemented Python support; reserve Lizard, Roslyn, ESLint, and Swift tooling through adapters.

## Consequences

Only Python is validated; future analyzers do not redesign Runtime.

## Alternatives

One universal analyzer was rejected because it cannot provide trustworthy language coverage.
