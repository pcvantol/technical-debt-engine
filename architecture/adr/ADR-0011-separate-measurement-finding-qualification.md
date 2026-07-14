# ADR-0011: Separate Measurement, Finding, and Qualification

## Status

Accepted

## Context

Quantitative observations, actionable findings, and policy decisions have different semantics and lifecycle.

## Decision

Model measurements, findings, validation, and qualification as separate schemas and records.

## Consequences

Qualification can remain analyzer-independent and reports cannot confuse execution status with policy outcome.

## Alternatives

A single unstructured result document was rejected because it obscures validation and comparison meaning.
