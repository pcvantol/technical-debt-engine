# Policy configuration

Runtime configuration accepts a top-level `policy` object. It may contain `id`, `repository`, `workspace`, and `overrides`. Repository and workspace values are directories containing policy JSON files; built-in policies remain available and are discovered dynamically.

`overrides` maps a rule ID to an object containing `enabled`, `warning`, or `blocking`. The CLI provides the same override path through `--policy DIRECTORY` and repeatable `--policy-override RULE=JSON`. For example: `tde --policy-override 'complexity.maximum={"warning":10,"blocking":20}' inspect .`.

Overrides affect only the selected execution and are recorded in policy evidence as qualification inputs.
