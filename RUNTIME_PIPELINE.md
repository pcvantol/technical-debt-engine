# Runtime pipeline

```text
Repository Discovery → Repository Inspection → Language Detection → Capability Planning
→ Adapter Planning → Adapter Dispatch → Native Analyzer Execution → Normalization
→ Validation → Qualification → Evidence → Reporting → Exit Status
```

| Stage | Purpose | Inputs | Outputs | Responsibilities | Failure modes | Ownership |
| --- | --- | --- | --- | --- | --- | --- |
| Repository Discovery | Establish target boundaries. | Invocation, configuration, paths. | Repository candidates. | Abstract target discovery. | No target or ambiguous boundary. | Runtime. |
| Repository Inspection | Describe candidate context. | Candidate, filesystem, configuration. | Metadata and inventory. | Inspect files, ignores, identity. | Unreadable or inconsistent target. | Runtime. |
| Language Detection | Identify applicable languages. | Inspected inventory. | Language set and confidence. | Detect multiple supported languages. | Unknown or ambiguous language. | Runtime. |
| Capability Planning | Decide requested work. | Configuration, language set, capability catalog. | Capability plan. | Classify enabled, supported, unsupported, dependencies. | Unsatisfied capability dependency. | Runtime. |
| Adapter Planning | Select measurements. | Capability plan, language set, adapter catalog. | Adapter plan. | Order adapters, resources, parallel opportunities. | Required adapter unavailable. | Runtime. |
| Adapter Dispatch | Create controlled executions. | Adapter plan, target context. | Dispatch records. | Invoke adapters independently. | Dispatch or isolation failure. | Runtime. |
| Native Analyzer Execution | Produce native observations. | Adapter request and tool environment. | Raw analyzer output. | Measure only. | Tool missing, failed, or malformed output. | Adapter. |
| Normalization | Map observations to canonical data. | Raw output and adapter identity. | Canonical observations. | Preserve meaning and provenance. | Unsupported or lossy mapping. | Runtime. |
| Validation | Establish evidence validity. | Canonical data and identities. | Validated or blocked record. | Check completeness and compatibility. | Any invalid identity, schema, or completeness state. | Runtime. |
| Qualification | Apply policy. | Validated evidence, policy, baseline. | Qualification result. | Compare and classify fail-closed. | Incompatible policy or baseline. | Runtime. |
| Evidence | Publish immutable result. | Validated evidence and qualification. | Versioned evidence record. | Bind provenance and timestamps. | Serialization or immutability failure. | Runtime. |
| Reporting | Render evidence. | Canonical evidence only. | JSON, Markdown, or SARIF report. | Produce human and machine views. | Unsupported format or render failure. | Runtime. |
| Exit Status | Signal execution state. | Pipeline result and limitations. | Canonical status. | Provide automation outcome. | Ambiguous state is BLOCKED. | Runtime. |

No downstream stage consumes raw analyzer output directly. A stage failure is represented explicitly and never silently converted into success.
