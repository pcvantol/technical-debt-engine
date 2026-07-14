# Maintainability model

Generation 1 derives `maintainability.index` as a bounded 0–100 repository index from canonical evidence: `100 - average cyclomatic complexity × 3 - code lines / 1000`. This is a transparent initial representation, not a native analyzer metric. Its only inputs are normalized Code Size and Complexity measurements.
