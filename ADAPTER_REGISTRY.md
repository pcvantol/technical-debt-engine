# Adapter registry

The registry is the sole source for adapter discovery. The runtime has no hardcoded adapter list. Registration requires the full adapter contract, owner, independent version/status, type, languages/capabilities, analyzer compatibility, configuration schema, canonical-output mapping, limitations, and compatibility statement.

## Generation 1 entries

| ID | Version | Status | Type | Analyzer | Languages / capabilities |
| --- | --- | --- | --- | --- | --- |
| `python.radon` | 0.x | PLANNED | Language / Metric | Radon | Python; code size, complexity, maintainability |
| `universal.lizard` | 0.x | PLANNED | Language / Metric | Lizard | Supported languages; code size, complexity |
| `dotnet.roslyn` | 0.x | PLANNED | Language / Metric | Roslyn | C#; future declared capabilities |
| `swift.tooling` | 0.x | PLANNED | Language / Metric | Swift tooling | Swift; future declared capabilities |
| `javascript.eslint` | 0.x | PLANNED | Language / Metric | ESLint | JavaScript, TypeScript; future declared capabilities |

All entries are declarations only. No adapter, analyzer invocation, or executable registration exists.
