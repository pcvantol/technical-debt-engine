# Adapter compatibility and isolation

Compatibility is explicit across runtime, adapter, capability, schema, analyzer, and consumer. The runtime validates the declared matrix before loading; unknown or incompatible versions fail closed. Consumers consume canonical evidence, not adapter internals.

Adapters are isolated: they may not communicate directly, modify runtime state, modify repository contents, write reports, or take qualification decisions. They return bounded output to the runtime, which normalizes, validates, qualifies, publishes evidence, reports, and determines exit status.
