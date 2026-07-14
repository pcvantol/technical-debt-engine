# Capability configuration

Each capability exposes declarative configuration for `enabled`, thresholds, scope, exclusions, and language overrides. Configuration follows the canonical precedence and validation rules in [CONFIGURATION_SCHEMA.md](CONFIGURATION_SCHEMA.md).

Configuration selects and constrains registered behavior only. It cannot create a capability, adapter, analyzer support, metric, or qualification outcome, and must not require project-specific code changes.
