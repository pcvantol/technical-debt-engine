# Capability Reality Matrix

| Component | Documented | Code exists | Executable | Tests | Evidence | Released | Operational | Truth state | Primary gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime discovery/inspection | Yes | Yes | Yes | Yes | Empty evidence | No | Limited | VALIDATED | Discovery is path hashing; language detection is always empty |
| Capability/adapter registries | Yes | Yes | Yes | Yes | Registry tuples | No | No | SCAFFOLDED | Hard-coded records; runtime report says 0 capabilities/adapters |
| Execution Engine | Yes | Yes | Yes | Yes | Direct API execution evidence | No | No | SCAFFOLDED | CLI does not surface execution; branching remains capability-specific |
| Code Size | Yes | Yes | Yes via API with `cloc 2.10` | Yes | Metrics via API | No | No | VALIDATED | CLI path is empty; host tool is undeclared/unpinned; macOS only |
| Complexity | Yes | Yes | Yes only when active Python has Radon | Yes | Direct adapter metrics | No | No | IMPLEMENTED | Isolated install lacks Radon; CLI path is empty; Python only |
| Maintainability | Yes | Yes | Yes via direct derived call | Indirect only | Derived metric | No | No | IMPLEMENTED | No CLI evidence; no findings; formula is unqualified |
| Dependency Health | Yes | Yes | Yes for `requirements.txt`, `pyproject.toml`, `package.json` | Indirect only | Count metric | No | No | IMPLEMENTED | No locks/findings; no NuGet/pnpm/Yarn/SPM/Conan/vcpkg; CLI path empty |
| Policy | Yes | Yes | Yes | Yes | Policy decision in evidence | No | No | VALIDATED | Empty evidence returns `NOT_APPLICABLE`; no durable policy registry |
| Baseline/Comparison | Yes | Yes | Yes | Yes | JSON baseline/comparison | No | Limited | VALIDATED | Operates on empty CLI evidence; no migration/concurrency controls |
| Trend | Yes | Yes | Yes | Yes | Baseline-history aggregation | No | Limited | VALIDATED | Not an Evidence Store trend and can trend empty evidence |
| Query | Yes | Yes | Yes | Yes | In-memory projection | No | No | BLOCKED | Does not query persisted Evidence Store records |
| Evidence Store | Yes | Yes | Yes | Yes | Filesystem JSON | No | Limited | VALIDATED | Prototype: no locking, migration, retention or cleanup |
| Runtime Qualification | Yes | Yes | Yes | Yes | Qualification object | No | No | BLOCKED | Empty evidence is incorrectly `QUALIFIED` with confidence 1.0 |
| Reporting | Yes | Partial | CLI payloads only | No renderer test | Console output | No | No | SCAFFOLDED | `report` is explicitly NOT_IMPLEMENTED |
| Software Assurance / Trusted Delivery | Yes | Yes | Yes | Yes | Failing evidence | No | No | BLOCKED | No workflows, provenance, clean candidate or release artifacts |
