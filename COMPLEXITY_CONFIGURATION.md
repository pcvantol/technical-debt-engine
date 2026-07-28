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

The adapter classifies, but does not exclude, supported symbols. Paths in test/spec directories or with test/spec filenames are `TEST`; fixture/test-data paths are `FIXTURE`; verification paths and `validate_` or `verify_` filenames are `VERIFICATION`; remaining symbols are `PRODUCT_SOURCE`. The bundled Generation 1 policy evaluates its warning and blocking complexity threshold only against `complexity.cyclomatic.product.maximum`. Tests, fixtures and verification harnesses remain visible in evidence and findings but do not change that production-source decision.
