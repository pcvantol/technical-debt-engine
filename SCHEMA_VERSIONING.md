# Schema versioning

Public evidence, configuration, internal adapter contracts, report projections, metric registry, and policy schema have independent versions. Runtime version and schema version are separate identities and neither implies the other.

Schema versions follow Semantic Versioning: additive backward-compatible fields are minor changes; incompatible meaning, required fields, or removal are major changes; corrections that preserve meaning are patches. Unknown critical fields and unsupported major versions fail closed. Deprecations retain parsing guidance until their declared removal version; migrations create new records rather than mutate immutable evidence.

Schemas are hand-maintained canonical artifacts. Future generated models must derive from these schemas, never replace them. Publication is through immutable released contract artifacts; no schema is released by this prompt.
