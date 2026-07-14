# Adapter configuration

Adapter configuration is a scoped portion of resolved canonical configuration. It may declare enabled state, thresholds, paths, native analyzer options, timeouts, exclusions, and resource limits.

Configuration is validated before loading, does not contain secrets in evidence, and cannot alter the adapter's registry identity, supported capabilities, or public contract. Invalid, unknown, or incompatible options fail closed with structured limitations.
