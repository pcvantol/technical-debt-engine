# Capability runtime

Capability planning turns configuration, candidate identity, and detected languages into an ordered independent capability plan. It records enabled, supported, unsupported, deferred, and blocked capabilities, together with dependencies and required adapters.

Capabilities remain independent: a capability never invokes another adapter directly and does not own global orchestration. The runtime resolves declared dependencies and execution order. Unsupported capabilities produce explicit limitations and can lead to `NOT_SUPPORTED` or `BLOCKED` according to policy; they are never mistaken for successful measurement.

Capability lifecycle is **planned → implemented → validated → qualified → deprecated → removed**. Lifecycle advancement is evidence- and contract-based, and does not require unrelated capabilities to advance.
