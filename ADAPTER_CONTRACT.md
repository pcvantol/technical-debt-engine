# Adapter contract

Every adapter declares identifier, display name, version, lifecycle status, owner, supported languages/capabilities, supported analyzer and versions, configuration, inputs, outputs, and limitations.

The runtime supplies immutable context: repository identity, candidate identity, resolved configuration, language, capability, execution identity, and resource limits. An adapter receives this bounded context; it cannot modify runtime state or repository contents.

An adapter produces canonical draft measurements/findings, structured limitations, adapter/analyzer identity, and execution metadata. It never produces reports, takes qualification decisions, invokes another adapter, or directly communicates with another adapter. Its native analyzer may be Radon, Lizard, Roslyn, Swift tooling, ESLint, or a future authoritative tool; the runtime never invokes analyzers directly.
