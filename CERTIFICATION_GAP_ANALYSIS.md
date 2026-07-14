# Certification Gap Analysis

| Gap | Certification impact | Required resolution |
| --- | --- | --- |
| Runtime Qualification accepts empty capability evidence as `QUALIFIED` | Trustworthiness is overstated | Require configured/required capability completeness before qualification |
| Query Engine does not consume persisted Evidence Store records | The canonical read path is incomplete | Make Query Engine consume immutable store records |
| Reporting is not implemented | The declared Query Engine consumer chain is incomplete | Implement report rendering exclusively from query results |
| Analyzer validation is bounded to current tool/platform coverage | Capability confidence is not portable | Establish cross-platform and multi-language qualification evidence |
| Runtime retains legacy capability-specific execution helpers | Architecture consistency risk | Complete migration to Execution Engine ownership |
