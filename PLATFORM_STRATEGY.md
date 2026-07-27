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

- **G2-A — Coverage Completion.** **Complete.** Existing CI artifacts from
  `djconnect`, `djconnect-website`, and `djconnect-esp32` are qualified through
  public contracts. TDE consumes them only and never runs tests or generates
  coverage.
- **G2-B — Minimal Dependency Health.** Select only ecosystems used by the
  chosen pilot and produce the canonical evidence and policy decisions it
  needs. Unsupported ecosystems are explicit.
- **G2-C — Security Gap Assessment.** **Complete.** Existing GitHub-native and
  repository-native controls remain decision owners; no TDE 1.0 security
  capability is justified.
- **G2-D — DJConnect Consumer Integration.** `djconnect-pi` is the sole
  selected, thin, pinned public-CLI consumer and remains non-blocking in
  Observe. Wider rollout or phase promotion is post-1.0 work.
- **G2-E — TDE 1.0 Qualification and Release.** Create one immutable candidate,
  qualify its real artifacts and selected consumer, record limitations, and
  publish `1.0.0` once. The binding sequence is in [TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md).

## Boundaries

Generation 2 adds no cloud or dashboard product, Marketplace objective,
organization/multi-tenant governance, broad AI adviser, architecture suite, or
replacement for security, dependency, or quality platforms. The complete
deferred option set is retained in [PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md).

Engineering increments merge independently when ready, but a merge is not a
release trigger. The normal next public release is `1.0.0`; any interim public
release needs an explicit operational-necessity decision. Existing release
engineering is reused unless it demonstrably fails this program.
