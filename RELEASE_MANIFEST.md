# Release Manifest

The canonical manifest is a versioned, immutable JSON-compatible record containing:

- candidate identity, release profile, and planned semantic version;
- runtime, schema, capability, adapter, and policy versions;
- planned artifact identities, formats, checksums, and provenance;
- qualification and evidence identities; and
- publication targets and operational-evidence references.

Checksums are assigned by the execution engine after artifact creation. A manifest is never amended; any change creates a new candidate.
