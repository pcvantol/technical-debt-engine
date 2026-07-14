# ADR-0018: Capability Qualification

## Status

Accepted

## Context

Capabilities must produce explainable policy decisions without analyzer coupling.

## Decision

Require qualification to consume validated canonical evidence and use the canonical result vocabulary.

## Consequences

Execution states remain separate from qualification and incomplete evidence fails closed.

## Alternatives

Native-tool pass/fail interpretation was rejected because it is not portable or policy-governed.
