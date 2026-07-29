# Technical Debt Engine

DJConnect is the primary product. Technical Debt Engine (TDE) is its compact,
supporting engineering tool for producing reliable pipeline assessment
decisions through public evidence and CLI contracts.

TDE 1.1.1 completes the consumer-driven DJConnect enablement program and the
authorized cross-language primary-product complexity parity increment. It adds
no new capability and does not change Observe-only governance. See the
[roadmap](PRODUCT_ROADMAP.md) and [active backlog](PRODUCT_BACKLOG.md).

Release `1.1.1` is the current public baseline and is exactly pinned by all
seven selected DJConnect source consumers.

## Product contracts

Consumers integrate only through the public `tde` CLI, configuration, evidence
schema, exit codes, and stable released contracts—not runtime internals. See
[INTEGRATION_MODEL.md](INTEGRATION_MODEL.md).

The `complexity` capability discovers the dominant canonical product language:
Python uses Radon; JavaScript/TypeScript, Swift, C/C++ and C# use Lizard. All
five normalize to `complexity.cyclomatic.product.maximum` and the same policy.
See the [complexity support matrix](docs/complexity-support-matrix.md).

Operational repository assurance is available through `tde assure`; see [SOFTWARE_ASSURANCE.md](SOFTWARE_ASSURANCE.md) for its canonical evidence and candidate-artifact verification contract.

## Documentation

- [Product architecture](PRODUCT_ARCHITECTURE.md)
- [Platform vision](PLATFORM_VISION.md) and [platform strategy](PLATFORM_STRATEGY.md)
- [Engineering method](ENGINEERING_METHOD.md) and [session bootstrap](BOOTSTRAP.md)
- [Capability model](CAPABILITY_MODEL.md)
- [CLI specification](CLI_SPECIFICATION.md)
- [Code Size Runtime contract](CODE_SIZE_RUNTIME.md)
- [Cross-language complexity support](docs/complexity-support-matrix.md) and
  [ADR-0065](architecture/adr/ADR-0065-cross-language-complexity-policy-parity.md)
- [Evidence schema](EVIDENCE_SCHEMA.md)
- [Qualification model](QUALIFICATION_MODEL.md)
- [Roadmap](PRODUCT_ROADMAP.md) and [backlog](PRODUCT_BACKLOG.md)
- [Versioning](VERSIONING.md) and [release strategy](RELEASE_STRATEGY.md)
- [Package build reproducibility](PACKAGING.md)
- [Repository status](REPOSITORY_STATUS.md)

The documentation index is [PROMPT_INDEX.md](PROMPT_INDEX.md).
