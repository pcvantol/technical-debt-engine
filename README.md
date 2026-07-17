# Technical Debt Engine

DJConnect is the primary product. Technical Debt Engine (TDE) is its compact,
supporting engineering tool for producing reliable pipeline assessment
decisions through public evidence and CLI contracts.

Generation 2 is the consumer-driven **TDE 1.0 DJConnect Enablement Program**.
It does not expand TDE into a general platform: its active scope is coverage
completion, minimal dependency and security evidence, selected DJConnect CI
consumption, and one integrated `1.0.0` qualification and release. See the
[roadmap](PRODUCT_ROADMAP.md) and [active backlog](PRODUCT_BACKLOG.md).

Release `0.2.0` is available as the PyPI distribution
[`technical-debt-engine-runtime`](https://pypi.org/project/technical-debt-engine-runtime/0.2.0/),
a [GitHub Release](https://github.com/pcvantol/technical-debt-engine/releases/tag/0.2.0),
and Docker image `docker.io/pcvantol/technical-debt-engine:0.2.0`. The Docker
OCI index is `sha256:8285a5082eaa1a5ac914b349ddec21c9e02cc4269421774d4f112383bc688ca9`;
no `latest` tag exists. See the [Runtime Qualification Report](RUNTIME_QUALIFICATION_REPORT_0.2.0.md)
for the immutable publication evidence and public-runtime validation.

## Product contracts

Consumers integrate only through the public `tde` CLI, configuration, evidence
schema, exit codes, and stable released contracts—not runtime internals. See
[INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

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
