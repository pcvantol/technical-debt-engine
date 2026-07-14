# Adapter SDK architecture

The Adapter SDK is TDE's only supported extension mechanism between the analyzer-independent runtime and native analyzers.

```text
Runtime → Capability Planner → Adapter Registry → Adapter Loader
→ Adapter Instance → Native Analyzer → Adapter Output → Normalization
```

The runtime owns orchestration. Adapters own analyzer interaction: they wrap native analyzers, never duplicate analyzer logic, normalize analyzer identity, and produce canonical adapter output. Adapters remain independently versioned and are not runtime extensions by special case.

Generation 1 recognizes Language, Metric, Dependency, and Duplication adapter types. Future adapter types must register through this SDK and require no runtime redesign. Generation 2 may add third-party, community, commercial, and signed adapters subject to registry, isolation, compatibility, and human-governed trust requirements; none are implemented now.
