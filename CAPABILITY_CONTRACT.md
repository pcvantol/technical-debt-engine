# Capability contract

A capability is the smallest independently qualifiable engineering feature. It is independent, discoverable, versioned, qualifiable, reportable, evidence-producing, and configuration-driven. The runtime orchestrates; capabilities provide behavior. The runtime must not contain capability-specific logic.

Every registered capability declares:

| Contract field | Requirement |
| --- | --- |
| Identifier, display name, description | Stable identity and intended engineering value. |
| Version, status, owner | Independent lifecycle and accountable stewardship. |
| Inputs | Runtime-owned repository/candidate identity, resolved configuration, runtime, adapter, and language context. |
| Outputs | Canonical measurements, findings, validation, limitations, and metadata. |
| Dependencies | Hard, soft, and optional capability dependencies. |
| Configuration | Enabled state, thresholds, scope, exclusions, and language overrides without code changes. |
| Validation | Supported language/configuration, adapters/tools, and measurement completeness, fail-closed. |
| Qualification | Canonical-evidence-only policy outcome. |
| Evidence and reports | Immutable evidence and reporting projections; a capability never renders reports directly. |
| Limitations | Structured limitations and qualification impact. |

The contract is architectural. It does not define a capability SDK or implementation.
