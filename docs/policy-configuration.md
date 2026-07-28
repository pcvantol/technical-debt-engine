# Declarative policy configuration

Pass an explicit JSON policy file to the public runtime:

```sh
tde --policy organization-policy.json assess --capability code_size /path/to/repository
```

Without `--policy`, TDE loads its bundled public Generation 1 policy. An explicit
path is never replaced by that default: a missing or invalid file blocks the
assessment before analyzers are planned or executed.

Each threshold rule declares its target and decision semantics. The current
public configuration contract supports `code_size.code_lines` for `code_size`
and `complexity.cyclomatic.maximum` for `complexity`.
The bundled Generation 1 policy warns above 50,000 repository code lines and
blocks above 75,000; an explicit policy file may choose different thresholds.

```json
{
  "identifier": "example.engineering-quality",
  "version": "2026.1",
  "scope": "repository",
  "owner": "Example Engineering",
  "description": "Repository quality policy.",
  "supportedCapabilities": ["code_size", "complexity"],
  "supportedSchemas": ["1.0.0"],
  "supportedRuntimeVersions": ["0.1.0"],
  "rules": [
    {
      "id": "example.code-size",
      "type": "threshold",
      "capability": "code_size",
      "metric": "code_size.code_lines",
      "operator": "greater_than",
      "threshold": {"warning": 25000, "blocking": 50000},
      "severity": {"warning": "WARNING", "blocking": "BLOCKING"},
      "enabled": true,
      "rationale": "Large repositories require deliberate decomposition."
    }
  ]
}
```

TDE validates required fields, capability and metric identifiers, operators,
duplicate identifiers, conflicting enabled rules and threshold ordering. The
assessment decision evidence records the resolved policy identifier, version,
source filename and canonical configuration hash. Capability evidence is not
changed when only policy configuration changes.
