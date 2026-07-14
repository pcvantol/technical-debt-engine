# Capability discovery

Discovery reads the registry and resolved configuration to expose available, enabled, unsupported, and experimental capabilities. It returns capability ID, version, lifecycle status, category, applicable languages, required adapters, dependency state, and limitation reasons.

- **Available:** registered and applicable to the runtime/candidate context.
- **Enabled:** available and selected by resolved configuration.
- **Unsupported:** requested but language, adapter, dependency, or compatibility requirements cannot be met.
- **Experimental:** explicitly marked by a future registry entry; experimental status never implies stable qualification support.

Discovery is declarative and side-effect free. It does not execute adapters or infer unregistered behavior.
