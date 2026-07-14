# Capability model

A capability is a named, independently evolvable measurement or decision function. Adapters collect observations; the canonical model, qualification, and evidence layers keep results comparable across languages.

## Generation 1

| Capability | Purpose |
| --- | --- |
| Code Size | Describe source volume and distribution. |
| Complexity | Measure structural complexity. |
| Maintainability | Normalize maintainability signals. |
| Duplication | Identify repeated code or structures. |
| Dependency Health | Assess dependency condition and exposure. |
| Test Health | Describe test presence and quality signals. |
| Baseline | Capture an immutable reference result. |
| Comparison | Compare two compatible evidence sets. |
| Qualification | Apply policy to evidence. |
| Evidence | Produce canonical, immutable results. |
| Reporting | Present results in human and machine formats. |
| Trend Analysis | Compare compatible evidence across time. |

## Future

- Architecture Health
- Documentation Health

## Intended adapter roadmap

Generation 1 intends independent adapters for Python, C#, Swift, JavaScript, TypeScript, C, and C++. An adapter is selected through repository discovery and language detection; no adapter is privileged by a consumer or CI system. Additional language adapters remain independent extensions of the same capability contract.

Capabilities must publish their input assumptions, canonical output mapping, and compatibility impact before they become stable.
