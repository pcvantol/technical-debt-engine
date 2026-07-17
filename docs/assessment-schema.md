# Stable Assessment Schema

Assessment evidence is a public Runtime contract. The Runtime publishes JSON Schema
documents for `capability-evidence`, `policy-evidence`, `assessment-decision-evidence`,
`assessment-evidence`, and `repository-qualification-evidence` in `tde_runtime/schemas`.

Every evidence envelope includes `schema.name`, `schema.version`,
`schema.compatibilityVersion`, `schema.runtimeVersion`, and
`schema.assessmentVersion`. Consumers must select by schema name and compatibility
version, rather than depending on Runtime implementation details.

Use `tde schema --format json` to discover the installed schema names, versions, and
locations. The command is metadata-only: it does not inspect a repository or run an
analyzer.

Compatibility is defined as follows:

- Patch releases are fully backwards compatible.
- Minor releases may add optional fields only.
- Major releases may make breaking changes and must publish a new compatibility version.

The Runtime validates every emitted capability, policy, decision, and assessment
envelope before persistence. An incompatible or malformed schema is rejected
fail-closed.
