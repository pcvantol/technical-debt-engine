# Report projection schemas

Reporting projects canonical evidence into JSON, Markdown, or SARIF. JSON is canonical evidence or an explicitly versioned projection; Markdown is human-readable and non-canonical; SARIF maps compatible findings while retaining canonical evidence identity.

Repository-level metrics are not forced into SARIF where its semantics do not fit. See [`schemas/report.schema.json`](schemas/report.schema.json).
