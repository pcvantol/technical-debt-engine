# Qualification runtime

Qualification consumes validated normalized evidence only and remains analyzer-independent. It applies versioned policy to compatible evidence, optional baseline, comparison, severity model, regression semantics, and trend context.

Generation 1 concepts are baseline, comparison, policy, severity, regression, and trend. A baseline and comparison are immutable compatible evidence references; a trend is a sequence of compatible comparisons. Qualification never consumes raw analyzer output, substitutes incompatible baselines, or hides missing policy.

The outcome is a deterministic qualification record bound to evidence and policy provenance. Missing, incompatible, or incomplete inputs fail closed. This runtime contract implements the architecture of [QUALIFICATION_MODEL.md](QUALIFICATION_MODEL.md), not an analyzer-specific policy.
