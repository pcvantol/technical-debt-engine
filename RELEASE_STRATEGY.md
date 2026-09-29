# Release strategy

TDE `1.1.1` is the current published public runtime. No next public release is
scheduled. Engineering increments may merge for maintenance, but a merge is
not a publication trigger.

A maintenance release requires a demonstrated consumer or operational need,
qualified immutable package and distribution artifacts, compatibility evidence
for the public contracts, and a deliberate publication decision. The completed
Generation 2 release path is retained in [TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md)
as historical evidence.

CLI and package releases are versioned artifacts. Evidence-schema compatibility is declared in every release; incompatible schema changes require a new schema version and a clear consumer migration path. Released artifacts and evidence are immutable.
