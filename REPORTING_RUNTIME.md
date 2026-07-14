# Reporting runtime

Reporting consumes canonical evidence only. It never consumes raw analyzer output directly and cannot bypass validation or qualification.

Generation 1 reporting views are:

- Repository Summary
- Capability Summary
- Findings
- Qualification
- Trend

Reports render canonical evidence as JSON, Markdown, or SARIF where applicable. Each view preserves evidence identity, schema version, limitations, and qualification provenance so a report remains traceable without becoming a competing source of truth.
