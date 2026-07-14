# Code Size configuration

Default operation requires no configuration. `tde` discovers a mapping-only `.tde.yml` in the repository root; JSON is also accepted because it is valid YAML. Enable through resolved configuration:

```yaml
schemaVersion: "1.0.0"
capabilities:
  code_size:
    enabled: true
```

`--config <path>` explicitly selects another configuration and `--capability code-size` is the CLI override. CLI and Runtime API both resolve through `RuntimeConfiguration` and bind the canonical configuration digest into evidence.

Classification defaults are project-neutral: `tests`, `test`, and `spec` are tests; `docs` and documentation extensions are documentation; `vendor`, `third_party`, and `node_modules` are vendor; `generated`, `build`, and `dist` are generated. Per-project include/exclude, thresholds, and overrides are deferred pending the canonical configuration-schema extension.
