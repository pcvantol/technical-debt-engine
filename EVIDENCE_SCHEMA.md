# Evidence schema

TDE evidence is a versioned, immutable, machine-readable record of an assessment and its qualification context.

## Requirements

- Every record declares a schema version and producer identity.
- A published evidence record is immutable; corrections produce a new record with provenance.
- JSON is the canonical interchange representation.
- Markdown is a human-readable rendering, not the authoritative data source.
- SARIF is an interoperable reporting projection where applicable.
- Future extensions must be additive or versioned; consumers must reject unsupported incompatible versions.

## Conceptual envelope

```json
{
  "schemaVersion": "0.x",
  "evidenceId": "immutable identifier",
  "createdAt": "RFC 3339 timestamp",
  "subject": { "repository": "declared target", "revision": "optional immutable revision" },
  "producer": { "tdeVersion": "0.x", "adapterVersions": {} },
  "observations": [],
  "qualification": {},
  "provenance": {}
}
```

Field definitions, identifiers, compatibility rules, and SARIF mappings will be versioned before implementation.
