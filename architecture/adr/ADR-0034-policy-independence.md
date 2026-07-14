# ADR-0034: Policy independence

## Decision

Policies are JSON contracts with explicit identifiers, versions, ownership, scope, and runtime/schema/capability compatibility.

## Consequences

Policies can be added or revised through discovery without Runtime modifications. Incompatible policy inputs fail closed.
