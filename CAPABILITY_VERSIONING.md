# Capability versioning and compatibility

Capability version is independent of runtime version and schema version. Each registry entry declares compatibility with runtime, canonical schemas, adapters, and consumers.

Compatible additions may preserve a capability major version; changed metric semantics, finding identity, qualification behavior, or required dependencies require an explicit compatibility statement and appropriate version transition. Unsupported combinations are discoverable and fail closed rather than being inferred compatible.

Generation 2 may add an external capability SDK. Such plugins must satisfy this contract, registry discovery, isolation, compatibility declaration, validation, and human-governed registration; no plugin SDK is implemented now.
