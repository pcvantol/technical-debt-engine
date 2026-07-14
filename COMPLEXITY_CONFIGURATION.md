# Complexity configuration

Complexity uses the canonical `.tde.yml` configuration discovered by `RuntimeConfiguration`; `--config` and `--capability complexity` resolve through the same model and are included in the evidence configuration digest.

```yaml
capabilities:
  complexity:
    enabled: true
    thresholds:
      high: 11
      veryHigh: 21
      critical: 41
    ignoredPaths: "generated/**,vendor/**"
    ignoredSymbols: "legacy_handler"
```

Thresholds must be positive integers and satisfy `high < veryHigh < critical`. Because the Generation 1 parser intentionally accepts mapping-only YAML, ignored paths and symbols are comma-separated strings. CLI capability selection preserves the configured Complexity settings while enabling the capability.
