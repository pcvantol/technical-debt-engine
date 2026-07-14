# Product architecture

TDE is a standalone runtime organized around capabilities and stable evidence contracts. Adapters are independent of consumers and of one another.

```text
CLI
  ↓
Repository Discovery
  ↓
Language Detection
  ↓
Capability Adapters
  ↓
Canonical Technical Debt Model
  ↓
Qualification
  ↓
Evidence
  ↓
Reporting
```

- **CLI** accepts explicit user intent, configuration, and target locations.
- **Repository Discovery** establishes the analysis boundary and source inventory.
- **Language Detection** selects applicable adapters without prescribing a project layout.
- **Capability Adapters** collect capability-specific observations in their native ecosystems.
- **Canonical Technical Debt Model** normalizes observations into versioned, comparable records.
- **Qualification** applies an explicit policy to a baseline and/or comparison.
- **Evidence** emits immutable machine-readable records.
- **Reporting** renders evidence for people and automation.

This is an architectural contract, not an implementation. No component currently exists as runtime code.
