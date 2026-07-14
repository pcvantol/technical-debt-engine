# Policy compatibility

Compatibility is explicit and evaluated before policy execution:

`Runtime version → Policy supportedRuntimeVersions → Schema supportedSchemas → supportedCapabilities`

A policy whose runtime or evidence schema is not listed is blocked and cannot produce a passing qualification. Capability support is declared policy metadata; missing or unavailable capability evidence results in an explicit not-applicable or triggered decision, never silent substitution.
