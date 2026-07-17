# Platform strategy

## Generation 2 — TDE 1.0 DJConnect Enablement Program

Generation 1 is complete and its foundations remain in force. Release `0.2.0`
is published and qualified. Generation 2 is a compact program that prepares
TDE for genuine use as a DJConnect pipeline decision-maker; it is not a general
platform-expansion program.

Every proposed increment must answer:

1. Which concrete DJConnect risk or manual process does it address?
2. Which DJConnect repository or pipeline consumes it?
3. Which public evidence or pipeline decision does it produce?
4. Why are existing tooling and TDE functionality insufficient?
5. Is it required for `1.0.0`, or post-1.0 work?

An increment without convincing answers is not active 1.0 work.

## Active workstreams

- **G2-A — Coverage Completion.** Finish and qualify the merged coverage
  capability through public contracts. It consumes existing artifacts only and
  never runs tests or generates coverage.
- **G2-B — Minimal Dependency Health.** Select only ecosystems used by the
  chosen pilot and produce the canonical evidence and policy decisions it
  needs. Unsupported ecosystems are explicit.
- **G2-C — Basic Security Evidence.** Normalize only the small set of evidence
  needed for a DJConnect decision, reusing specialized and GitHub-native tools
  where possible.
- **G2-D — DJConnect Consumer Integration.** Use one thin, pinned,
  reproducible GitHub Actions integration or reusable workflow; public TDE
  interfaces remain authoritative. Pilot phases are observe, warn, soft-fail,
  then required check after stable evidence.
- **G2-E — TDE 1.0 Qualification and Release.** Qualify the real artifacts and
  chosen consumers, record limitations, and publish `1.0.0` once.

## Boundaries

Generation 2 adds no cloud or dashboard product, Marketplace objective,
organization/multi-tenant governance, broad AI adviser, architecture suite, or
replacement for security, dependency, or quality platforms. The complete
deferred option set is retained in [PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md).

Engineering increments merge independently when ready, but a merge is not a
release trigger. The normal next public release is `1.0.0`; any interim public
release needs an explicit operational-necessity decision. Existing release
engineering is reused unless it demonstrably fails this program.
