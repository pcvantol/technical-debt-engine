# DJConnect Reference Consumer Integration

## Decision

**REFERENCE_CONSUMER_INTEGRATION_BLOCKED**

DJConnect must invoke a released, pinned `tde` CLI and ingest its canonical evidence only. It must not import Runtime modules, adapters, or capability implementations.

At this time TDE has no Git tag or GitHub Release, so no released CLI exists to pin. In addition, several local DJConnect repositories exist (`djconnect`, `djconnect-api`, `djconnect-app`, `djconnect-pi`, and others) and no target repository was specified. No DJConnect repository was modified.

Once a released CLI and target repository are explicitly available, DJConnect should own repository discovery, policies, thresholds and exclusions; TDE owns analysis. Evidence ingestion must validate schema/runtime versions, repository/candidate identity and integrity before platform aggregation.
