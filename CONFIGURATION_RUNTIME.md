# Runtime configuration

Runtime configuration declares intent; it does not contain project-specific runtime code. Configuration is discovered during repository inspection and is bound to the candidate identity used for execution.

Projects may configure:

- enabled capabilities;
- adapter selection;
- thresholds;
- exclusions;
- report formats; and
- qualification policy.

Configuration is explicit, versioned where it affects a public contract, and validated before planning. Conflicting, malformed, unknown, or incomplete configuration fails closed. Configuration can constrain automatic discovery, but cannot fabricate language support, adapter availability, evidence, or qualification success.
