# ADR-0006: CLI First

## Status

Accepted

## Context

TDE needs a portable integration surface for people, automation, and diverse CI environments.

## Decision

The canonical `tde` CLI is the first integration surface, alongside stable configuration, evidence, and exit-code contracts.

## Consequences

Consumers avoid runtime internals and can adopt released CLI contracts independently of CI or vendor.

## Alternatives

Consumer-specific plugins and direct internal APIs were rejected because they increase coupling and reduce portability.
