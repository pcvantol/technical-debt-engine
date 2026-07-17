# Release strategy

Release `0.2.0` is published and qualified. Generation 2 merges independently
reviewable increments, but merge is not a public-release trigger. The next
planned public release is `1.0.0`; an interim release requires an explicit
operational-necessity decision.

Delivery proceeds through these stages:

- **Current:** qualified `0.2.0` public runtime.
- **Enablement:** compact consumer-driven capability and pilot completion.
- **Stable:** qualified `1.0.0` after selected DJConnect consumer proof.

CLI and package releases are versioned artifacts. Evidence-schema compatibility is declared in every release; incompatible schema changes require a new schema version and a clear consumer migration path. Released artifacts and evidence are immutable.
