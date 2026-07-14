# Code Size configuration

Default operation requires no configuration. Enable through resolved configuration: `{"capabilities":{"code_size":{"enabled":true}}}`. The current CLI exposes the equivalent `tde assess --capability code-size` route.

Classification defaults are project-neutral: `tests`, `test`, and `spec` are tests; `docs` and documentation extensions are documentation; `vendor`, `third_party`, and `node_modules` are vendor; `generated`, `build`, and `dist` are generated. Per-project include/exclude, thresholds, and overrides are deferred pending the canonical configuration-schema extension.
