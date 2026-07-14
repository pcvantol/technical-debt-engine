# Configuration schema

The canonical project configuration filename is `.tde.yml`; its data contract is [`schemas/configuration.schema.json`](schemas/configuration.schema.json). It supports schema version, capabilities, adapter/analyzer preferences, thresholds, exclusions, generated/vendor paths, report formats, policy, baseline, suppressions, redaction, and execution limits.

Resolution precedence is: CLI overrides → explicit configuration file → repository configuration → workspace configuration → runtime defaults. The final resolved configuration and digest bind into evidence. Secrets must not be embedded in configuration or evidence.
