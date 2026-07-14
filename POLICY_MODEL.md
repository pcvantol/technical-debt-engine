# Policy model

A policy is JSON and has `identifier`, `version`, `scope`, `owner`, `description`, `supportedCapabilities`, `supportedSchemas`, `supportedRuntimeVersions`, and `rules`. These required compatibility fields keep policies project-, runtime-, and language-independent.

Rules are currently `threshold`, `finding_severity`, `capability`, or `comparison_regression` rules. Evaluation returns only `PASS`, `PASS_WITH_WARNINGS`, `FAIL`, `BLOCKED`, or `NOT_APPLICABLE`, plus every triggered rule. Policy evidence records measured values, thresholds, affected capability/evidence, decision reason, and the execution qualification reference. A policy can be evolved independently by adding a versioned file and declaring its compatibility.
