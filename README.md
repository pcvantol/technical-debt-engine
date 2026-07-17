# Technical Debt Engine

Technical Debt Engine (TDE) is a standalone, capability-based engineering platform for measuring, normalizing, qualifying, and reporting technical debt across software projects.

TDE is project-independent, platform-independent, CI-independent, language-independent, and vendor-neutral. DJConnect is the first reference consumer; it does not own TDE's architecture, roadmap, or release lifecycle.

Release `0.2.0` is available as the PyPI distribution
[`technical-debt-engine-runtime`](https://pypi.org/project/technical-debt-engine-runtime/0.2.0/),
a [GitHub Release](https://github.com/pcvantol/technical-debt-engine/releases/tag/0.2.0),
and Docker image `docker.io/pcvantol/technical-debt-engine:0.2.0`. The Docker
OCI index is `sha256:8285a5082eaa1a5ac914b349ddec21c9e02cc4269421774d4f112383bc688ca9`;
no `latest` tag exists. See the [Runtime Qualification Report](RUNTIME_QUALIFICATION_REPORT_0.2.0.md)
for the immutable publication evidence and public-runtime validation.

## Product contracts

Consumers integrate only through the future `tde` CLI, configuration, evidence schema, exit codes, and stable released contracts—not runtime internals. See [INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

Operational repository assurance is available through `tde assure`; see [SOFTWARE_ASSURANCE.md](SOFTWARE_ASSURANCE.md) for its canonical evidence and candidate-artifact verification contract.

## Documentation

- [Product architecture](PRODUCT_ARCHITECTURE.md)
- [Platform vision](PLATFORM_VISION.md) and [platform strategy](PLATFORM_STRATEGY.md)
- [Engineering method](ENGINEERING_METHOD.md) and [session bootstrap](BOOTSTRAP.md)
- [Capability model](CAPABILITY_MODEL.md)
- [CLI specification](CLI_SPECIFICATION.md)
- [Code Size Runtime contract](CODE_SIZE_RUNTIME.md)
- [Evidence schema](EVIDENCE_SCHEMA.md)
- [Qualification model](QUALIFICATION_MODEL.md)
- [Roadmap](PRODUCT_ROADMAP.md) and [backlog](PRODUCT_BACKLOG.md)
- [Versioning](VERSIONING.md) and [release strategy](RELEASE_STRATEGY.md)
- [Package build reproducibility](PACKAGING.md)
- [Repository status](REPOSITORY_STATUS.md)

The documentation index is [PROMPT_INDEX.md](PROMPT_INDEX.md).
