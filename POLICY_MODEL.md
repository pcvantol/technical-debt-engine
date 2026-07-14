# Policy model

A policy is JSON and has `identifier`, `version`, `scope`, `owner`, `description`, `supportedCapabilities`, `supportedSchemas`, `supportedRuntimeVersions`, and `rules`. These required compatibility fields keep policies project-, runtime-, and language-independent.

Rules are currently either `threshold` rules (metric key, direction, warning and blocking thresholds) or `finding_severity` rules. Evaluation returns `PASS`, `WARNING`, `BLOCKED`, or `NOT_APPLICABLE`, plus every triggered rule. A policy can be evolved independently by adding a versioned file and declaring its compatibility.
