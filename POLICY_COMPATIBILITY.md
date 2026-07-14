# Policy compatibility

Compatibility is explicit and evaluated before policy execution:

`Runtime version → Policy supportedRuntimeVersions → Schema supportedSchemas → supportedCapabilities`

A policy whose runtime or evidence schema is not listed is blocked and cannot produce a passing qualification. Policy discovery precedence is bundled default, then workspace, then repository; the last compatible policy with the selected identifier wins. Capability support is declared policy metadata; a required `capability` rule turns missing capability evidence into an explicit decision, never silent substitution.
