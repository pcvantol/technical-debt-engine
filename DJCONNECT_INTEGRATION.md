# DJConnect Reference Consumer Integration

## Decision

**REFERENCE_CONSUMER_INTEGRATION_READY**

DJConnect must invoke a released, pinned `tde` CLI and ingest its canonical evidence only. It must not import Runtime modules, adapters, or capability implementations.

TDE `0.1.0` is released and consumers may pin either PyPI distribution
`technical-debt-engine-runtime==0.1.0` or Docker OCI index
`sha256:aa648019045a442a0dbce029ee11ecb15c7755d845205fa8f07467e0faf18679`.
Several local DJConnect repositories exist (`djconnect`, `djconnect-api`,
`djconnect-app`, `djconnect-pi`, and others), but no target repository was
specified and none was modified.

Once a target repository is explicitly selected, DJConnect should own repository
discovery, policies, thresholds and exclusions; TDE owns analysis. Evidence
ingestion must validate schema/runtime versions, repository/candidate identity
and integrity before platform aggregation.
