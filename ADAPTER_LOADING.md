# Adapter loading

Generation 1 uses local adapter discovery from controlled repository/runtime locations, selected exclusively through the registry. Loading verifies identifier, version, contract compatibility, and isolation before creating an adapter instance.

Future package and plugin discovery must preserve the same registry authority, compatibility validation, isolation boundary, provenance, and explicit trust policy. Signed adapters are a future trust mechanism, not a current requirement.

An adapter instance is scoped to one execution context. It cannot mutate global runtime state, repository contents, or another adapter's context. Load failure yields an explicit unsupported or blocked adapter result.
