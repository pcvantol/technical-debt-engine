# Technical Debt Engine

Technical Debt Engine (TDE) is a standalone, capability-based engineering platform for measuring, normalizing, qualifying, and reporting technical debt across software projects.

TDE is project-independent, platform-independent, CI-independent, language-independent, and vendor-neutral. DJConnect is the first reference consumer; it does not own TDE's architecture, roadmap, or release lifecycle.

Generation 1 establishes the product foundation only. There is no production runtime, analyzer, package, or release in this repository yet.

## Product contracts

Consumers integrate only through the future `tde` CLI, configuration, evidence schema, exit codes, and stable released contracts—not runtime internals. See [INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

## Documentation

- [Product architecture](PRODUCT_ARCHITECTURE.md)
- [Capability model](CAPABILITY_MODEL.md)
- [CLI specification](CLI_SPECIFICATION.md)
- [Evidence schema](EVIDENCE_SCHEMA.md)
- [Qualification model](QUALIFICATION_MODEL.md)
- [Roadmap](PRODUCT_ROADMAP.md) and [backlog](PRODUCT_BACKLOG.md)
- [Versioning](VERSIONING.md) and [release strategy](RELEASE_STRATEGY.md)
- [Repository status](REPOSITORY_STATUS.md)

The documentation index is [PROMPT_INDEX.md](PROMPT_INDEX.md).
