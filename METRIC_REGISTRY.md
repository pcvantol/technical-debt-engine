# Metric registry

Metric keys are lower-case, dot-namespaced identifiers: `capability.metric_name[.submetric]`. Initial provisional keys include `code_size.physical_loc`, `code_size.logical_loc`, `complexity.cyclomatic`, `complexity.cognitive`, `maintainability.index`, `duplication.percentage`, `dependency.vulnerable_count`, and `test.coverage.line_percentage`.

TDE schema governance owns registration. Every key records owner, unit, valid scopes, aggregation semantics, definition, schema version, and compatibility. New keys are additive; deprecated keys retain mapping guidance; changed semantics require a new key or major compatibility change.

Code Size `0.1.0` registers `code_size.file_count` (files), `physical_lines`, `code_lines`, `comment_lines`, `blank_lines`, `source_lines`, `test_lines`, `documentation_lines`, `generated_lines`, `vendor_lines` (lines, repository/file/language scope, sum), and `test_to_source_ratio` (ratio, repository scope). See [CODE_SIZE_METRICS.md](CODE_SIZE_METRICS.md).
