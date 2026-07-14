# Configuration

TDE discovers `.tde.yml` at the repository root unless `--config <path>` is supplied. CLI and Runtime use the same `RuntimeConfiguration.discover` resolution and produce the same `configurationDigest` in evidence.

```yaml
schemaVersion: '1.0.0'
capabilities:
  code_size:
    enabled: true
```

Use `--capability code-size` to enable Code Size for `assess`, `run`, `validate`, `inspect`, and `report`. Use `--store-location <directory>` to choose the Evidence Store; otherwise Code Size assessment stores evidence under `<repository>/.tde/evidence`.

The `.tde.yml` parser intentionally supports mappings only. Unsupported configuration or schema versions block execution rather than being ignored.
