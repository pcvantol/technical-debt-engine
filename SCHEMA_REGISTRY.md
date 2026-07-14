# Schema registry

| Schema | ID | Version | Class | Owner | Compatibility | File | Examples | Consumers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Domain | `tde.domain` | 1.0.0 | Public | Schema governance | SemVer | `schemas/domain.schema.json` | evidence | Runtime, adapters |
| Measurement | `tde.measurement` | 1.0.0 | Public | Schema governance | SemVer | `schemas/measurement.schema.json` | multi-language | Evidence, reports |
| Finding | `tde.finding` | 1.0.0 | Public | Schema governance | SemVer | `schemas/finding.schema.json` | multi-language | Evidence, reports |
| Evidence | `tde.evidence` | 1.0.0 | Public | Schema governance | SemVer | `schemas/evidence.schema.json` | minimal, partial | Consumers |
| Validation | `tde.validation` | 1.0.0 | Public | Schema governance | SemVer | `schemas/validation.schema.json` | evidence | Runtime |
| Qualification | `tde.qualification` | 1.0.0 | Public | Qualification governance | SemVer | `schemas/qualification.schema.json` | pass, fail | Reports |
| Baseline | `tde.baseline` | 1.0.0 | Public | Schema governance | SemVer | `schemas/baseline.schema.json` | baseline | Qualification |
| Comparison | `tde.comparison` | 1.0.0 | Public | Schema governance | SemVer | `schemas/comparison.schema.json` | comparison | Qualification |
| Configuration | `tde.configuration` | 1.0.0 | Public | Product governance | SemVer | `schemas/configuration.schema.json` | suppression | Runtime |
| Adapter | `tde.adapter` | 1.0.0 | Internal | Adapter governance | SemVer | `schemas/adapter.schema.json` | adapter result | Runtime |
| Report | `tde.report` | 1.0.0 | Public | Reporting governance | SemVer | `schemas/report.schema.json` | future | Consumers |
