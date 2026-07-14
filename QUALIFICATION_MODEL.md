# Qualification model

Qualification converts compatible evidence into an explicit policy decision. It must be deterministic for the same evidence, policy, and schema versions.

Generation 1 defines these concepts:

- **Baseline:** an immutable, compatible reference evidence set.
- **Compare:** a compatible assessment-to-assessment or assessment-to-baseline evaluation.
- **Policy:** declared thresholds, scope, exceptions, and version.
- **Severity:** a normalized consequence classification.
- **Regression:** a policy-defined deterioration relative to a compatible reference.
- **Fail closed:** missing, incompatible, malformed, or unqualified evidence cannot be treated as passing.

Qualification never silently substitutes an incompatible baseline or policy. Any future exception must be explicit in evidence and report output.
