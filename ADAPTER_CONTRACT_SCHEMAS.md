# Adapter contract schemas

The adapter input contract is a runtime-to-adapter request containing execution and candidate identity, root/scope/files, language, capability, adapter configuration, exclusions, resource limits, requested native format, temporary output location, and cancellation/deadline metadata. It is architectural only; no SDK is implemented.

The adapter output contract records adapter/tool identity and version, execution result, native-output reference/hash, measured scope, completeness, draft normalized observations or payload reference, warnings/errors, limitations, and timing. It is internal. Raw output remains adapter-owned, optional in retained evidence, hash-referenced when retained, redacted as needed, excluded from public reports by default, and subject to explicit retention policy.

See [`schemas/adapter.schema.json`](schemas/adapter.schema.json).
