# Evidence schema

TDE evidence is a versioned, immutable, machine-readable record of one repository candidate assessment and its qualification context. Its canonical contract is [`schemas/evidence.schema.json`](schemas/evidence.schema.json).

## Requirements

- Every record declares schema identity/version and separate runtime identity/version.
- A published evidence record is immutable; corrections produce a new record with provenance.
- JSON is the canonical interchange representation; Markdown and SARIF are projections.
- Markdown is a human-readable rendering, not the authoritative data source.
- SARIF is an interoperable reporting projection where applicable.
- Future extensions must be additive or versioned; consumers must reject unsupported incompatible versions.

## Integrity and minimization

The content digest covers canonical serialized fields excluding the digest field itself and nondeterministic execution observations. It binds candidate, resolved configuration digest, adapter/tool identities, schema version, and stable normalized domain data. Timestamps, execution IDs, and environment observations are intentionally nondeterministic and recorded separately.

Evidence excludes source-file contents, secrets, environment variables, credentials, complete private paths, personal data, dependency tokens, and signing material by default. Paths and identifiers are redacted according to resolved policy. Optional future signatures do not change the core envelope.

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
