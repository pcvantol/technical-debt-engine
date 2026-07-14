# Adapter versioning

Adapter, analyzer, runtime, schema, and capability versions evolve independently. A registry entry declares its compatible runtime range, schema range, capability versions, analyzer versions, and consumer-facing output semantics.

An adapter change that alters normalized metric meaning, finding identity, or canonical mapping requires an explicit compatibility statement and appropriate adapter version change. Analyzer upgrades are separately recorded in provenance and cannot be silently assumed compatible.
