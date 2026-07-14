# ADR-0022: cloc Code Size Analyzer

## Status

Accepted

## Context

TDE needs deterministic, cross-language physical/code/comment/blank counts without duplicating language-aware counting.

## Decision

Use explicitly installed `cloc 2.10+` from PATH through `code_size.cloc`.

## Consequences

The adapter never downloads tools at runtime and blocks with installation guidance when cloc is absent.

## Alternatives

Reimplementing code counting was rejected because a mature native analyzer is available.
