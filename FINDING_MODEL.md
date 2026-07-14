# Finding model

Each canonical finding contains stable finding and rule IDs, capability, canonical severity and category, title and description, affected entity/location, evidence references, state, remediation guidance, baseline relationship, regression, confidence, suppressibility, and limitations.

Finding identity is deterministically derived from capability, rule, normalized target identity, and stable semantic fingerprint. Comparison classifies equivalent findings as unchanged, new, resolved, moved, or modified. Native severities are retained in adapter provenance but map only to the canonical vocabulary.

See [`schemas/finding.schema.json`](schemas/finding.schema.json).
