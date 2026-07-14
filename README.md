# Technical Debt Engine

Technical Debt Engine (TDE) is a standalone, capability-based engineering platform for measuring, normalizing, qualifying, and reporting technical debt across software projects.

TDE is project-independent, platform-independent, CI-independent, language-independent, and vendor-neutral. DJConnect is the first reference consumer; it does not own TDE's architecture, roadmap, or release lifecycle.

The repository contains an operational development package and reproducible
candidate-build foundation. No package has been published and no release exists.

## Product contracts

Consumers integrate only through the future `tde` CLI, configuration, evidence schema, exit codes, and stable released contracts—not runtime internals. See [INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

## Documentation

- [Product architecture](PRODUCT_ARCHITECTURE.md)
- [Platform vision](PLATFORM_VISION.md) and [platform strategy](PLATFORM_STRATEGY.md)
- [Engineering method](ENGINEERING_METHOD.md) and [session bootstrap](BOOTSTRAP.md)
- [Capability model](CAPABILITY_MODEL.md)
- [CLI specification](CLI_SPECIFICATION.md)
- [Evidence schema](EVIDENCE_SCHEMA.md)
- [Qualification model](QUALIFICATION_MODEL.md)
- [Roadmap](PRODUCT_ROADMAP.md) and [backlog](PRODUCT_BACKLOG.md)
- [Versioning](VERSIONING.md) and [release strategy](RELEASE_STRATEGY.md)
- [Package build reproducibility](PACKAGING.md)
- [Repository status](REPOSITORY_STATUS.md)

The documentation index is [PROMPT_INDEX.md](PROMPT_INDEX.md).
