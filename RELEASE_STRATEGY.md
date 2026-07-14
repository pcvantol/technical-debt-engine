# Release strategy

No release is created by this bootstrap. Future delivery proceeds through these stages:

- **Bootstrap:** documentation and contract preparation during `0.x`.
- **Alpha:** early CLI and adapter feedback; contracts may change with explicit migration notes.
- **Beta:** feature-complete candidate releases with defined compatibility expectations.
- **Stable:** supported CLI releases, beginning at `1.0.0`.

CLI and package releases are versioned artifacts. Evidence-schema compatibility is declared in every release; incompatible schema changes require a new schema version and a clear consumer migration path. Released artifacts and evidence are immutable.
