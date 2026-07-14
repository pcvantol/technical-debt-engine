# Adapter discovery

Discovery reads the registry, resolved configuration, selected capability plan, language context, and compatibility constraints. It determines available, enabled, unsupported, and deprecated adapters with their reasons and limitations.

- **Available:** registered, supported, and compatible with requested context.
- **Enabled:** available and selected by configuration/planning.
- **Unsupported:** requested but language, analyzer, capability, version, or resource requirements cannot be met.
- **Deprecated:** registry-recognized with migration guidance; never silently selected where a compatible replacement exists.

Discovery is declarative and side-effect free. It does not load an adapter, execute a tool, or infer unregistered adapters.
