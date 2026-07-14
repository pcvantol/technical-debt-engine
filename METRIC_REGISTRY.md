# Metric registry

Metric keys are lower-case, dot-namespaced identifiers: `capability.metric_name[.submetric]`. Initial provisional keys include `code_size.physical_loc`, `code_size.logical_loc`, `complexity.cyclomatic`, `complexity.cognitive`, `maintainability.index`, `duplication.percentage`, `dependency.vulnerable_count`, and `test.coverage.line_percentage`.

TDE schema governance owns registration. Every key records owner, unit, valid scopes, aggregation semantics, definition, schema version, and compatibility. New keys are additive; deprecated keys retain mapping guidance; changed semantics require a new key or major compatibility change.
