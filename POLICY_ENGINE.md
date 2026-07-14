# Policy Engine

The Policy Engine is the canonical decision layer between normalized evidence and Qualification. It loads a compatible, versioned policy, evaluates measurements, findings, limitations, configuration and thresholds, and emits immutable policy evidence.

The Runtime orchestrates the engine but contains no policy thresholds or decision rules. Qualification is a projection of Policy Engine output only. A blocked policy (invalid, absent, or incompatible) fails closed.

Generation 1 supports capability enablement through configuration, threshold rules, warning/blocking outcomes, ignore by disabling a rule, and not-applicable decisions when no inputs exist. Weighted, organization, enterprise, release, package, and cloud-distributed policies are future work.
