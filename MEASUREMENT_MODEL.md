# Measurement model

Each normalized measurement has a measurement ID, capability ID, namespaced metric key, numeric/categorical value, unit, scope, target entity, aggregation, source adapter/tool, optional confidence, and structured limitations.

Supported scopes are repository, workspace, language, file, module, type, function, dependency, and test suite. Aggregation is explicit: count, sum, mean, median, percentile, maximum, minimum, ratio, percentage, distribution, or categorical state. Metric meaning is never encoded only in display text.

See [`schemas/measurement.schema.json`](schemas/measurement.schema.json) and [METRIC_REGISTRY.md](METRIC_REGISTRY.md).
