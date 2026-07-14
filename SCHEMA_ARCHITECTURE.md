# Schema architecture

TDE separates eight versioned schema layers: Domain Model, Measurement Model, Finding Model, Evidence Envelope, Qualification Result, Reporting Projection, Configuration Contract, and Adapter Contract Metadata. The public contract is the validated Evidence Envelope and versioned reporting projections; raw analyzer output is never public evidence.

Machine-readable schemas live in [`schemas/`](schemas), fixtures in [`fixtures/`](fixtures), and the registry in [SCHEMA_REGISTRY.md](SCHEMA_REGISTRY.md). JSON Schema Draft 2020-12 is the canonical technology. Schemas use explicit `$id` values, local `$ref` references, and fail closed for unsupported versions or critical semantics.

Core fields cannot be overridden by extensions. Extensions use an owned `vendor.extension` namespace; non-critical extensions may be ignored, while critical semantics require a documented compatible consumer.
