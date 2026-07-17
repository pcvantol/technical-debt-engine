# ADR-0064: DJConnect Enablement Program and Minimal TDE 1.0 Scope

## Status

Accepted — Generation 2 initialization.

## Context

TDE `0.2.0` is published and qualified. Earlier strategy documents describe an
independent, expanding technical-debt platform. That direction is not the
current product need: DJConnect needs a small, reliable, maintainable pipeline
assessment tool, not a replacement for specialist security, dependency, or
quality platforms.

## Decision

1. DJConnect is the primary product; TDE is an enabling engineering tool.
2. TDE `1.0.0` scope is intentionally minimal and driven by demonstrated
   DJConnect consumers.
3. Generation 2 merges reviewable engineering increments independently, with
   no normal public release per capability.
4. The next planned public release is `1.0.0`.
5. After `1.0.0`, TDE defaults to maintenance-first.
6. New TDE work requires demonstrated DJConnect value, recorded through the
   investment test in roadmap governance.

The active program consists only of coverage completion, minimal dependency
health, basic security evidence, a phased selected-consumer integration, and
integrated `1.0.0` qualification/release. It preserves existing public
contracts and distribution mechanisms.

## Consequences and alternatives

Dashboards, cloud services, Marketplace positioning, multi-tenant governance,
general architecture analysis, broad AI advice, broad ecosystem expansion, and
the other deferred options remain post-1.0 backlog items; none is deleted.

Continuing the former platform-expansion roadmap was rejected because it lacks
a direct consumer need. Building independent release trains per capability was
rejected because it adds release cost before the DJConnect pilot is proven.
