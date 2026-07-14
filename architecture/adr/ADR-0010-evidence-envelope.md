# ADR-0010: Immutable Evidence Envelope

## Status

Accepted

## Context

Evidence must bind output to a candidate, configuration, tools, and schema without retaining sensitive source data.

## Decision

Use one immutable evidence envelope with provenance, integrity digest, candidate binding, controlled redaction, and separate runtime/schema versions.

## Consequences

Corrections create new evidence; hashes exclude their own digest and no secrets or source contents are included by default.

## Alternatives

Mutable aggregate reports were rejected because they cannot provide reliable provenance.
