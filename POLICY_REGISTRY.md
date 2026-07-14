# Policy registry

Policy discovery is file-based: the engine discovers every `*.json` policy in its bundled policy directory and optional workspace or repository directories. It validates each contract before use; discovery does not require a Runtime code change.

| Identifier | Version | Scope | Status |
| --- | --- | --- | --- |
| `tde.generation-1.default` | 1.0.0 | repository | Operational |

The default policy supports the validated Generation 1 capabilities and standard runtime/schema version `0.1.0` / `1.0.0`.
