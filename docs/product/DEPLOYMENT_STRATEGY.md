# Deployment Strategy

## Purpose and status

Technical Debt Engine (TDE) is an Engineering Runtime delivered as products
that consumers can install, pin, embed, or run in their own environments. This
document is the canonical product definition for those delivery products. It
defines targets and lifecycle only; it does not authorize a build, publication,
deployment, release, Runtime change, or capability change.

A target being **supported by this strategy** means that it is a first-class
product form for the named generation. It does not mean that an artifact is
currently published. Publication remains subject to the Release Runtime,
qualification, provenance, approval, and release evidence.

## Deployment philosophy

Deployment is independent from Runtime Architecture. The Runtime owns analysis,
canonical evidence, qualification, reporting, and stable API contracts;
distribution packages those contracts without changing them. Consumers use
released, versioned products only and do not import adapter or Runtime internals
as a deployment mechanism.

```text
Engineering Runtime
        ↓
Distribution products
        ↓
Independent consumers
```

Distribution may add installation, packaging, platform metadata, and release
provenance. It must not redefine capability semantics, evidence schemas,
qualification, or Runtime ownership.

## Generation 1 supported targets

The following are the official Generation 1 deployment targets. Their release
availability is governed separately by the release lifecycle.

| Target | Product responsibility | Primary consumers |
| --- | --- | --- |
| Python Package (PyPI) | Publish versioned wheel and source distribution with declared compatibility and provenance. | CLI users, Python environments, automation. |
| GitHub Releases | Publish immutable release metadata, checksums, notes, and approved release assets. | Direct-download and audited consumers. |
| Homebrew | Deliver a reviewed formula that installs the released CLI artifact. | macOS and Linux developer workstations. |
| Docker | Provide a versioned image that executes the released CLI without host-language installation. | CI/CD, containers, self-hosted runners. |
| GitHub Action | Package released CLI execution as a versioned Action interface. | GitHub Actions workflows and repositories. |
| Python Runtime API | Distribute the supported public Python library through the Python package. | Embedders, automation, integrations. |

## Canonical distribution products

| Product form | Responsibility | Distribution relationship |
| --- | --- | --- |
| Python wheel | Default installable Python product; includes CLI entry point and public library. | Primary PyPI artifact; may be attached to a GitHub Release. |
| Source distribution | Auditable and reproducible source package for supported Python installation flows. | Published alongside the wheel when release-qualified. |
| Standalone executables | Platform-specific CLI product for consumers that cannot use Python packaging. | Versioned GitHub Release assets; package-manager feeds may reference them. |
| Docker image | Containerized CLI runtime with explicit tag, digest, and provenance. | Container registry product; GitHub Release metadata references the immutable digest. |
| GitHub Release assets | Immutable checksums, SBOM/evidence bundles, executables, source, and release notes. | Release record for all directly consumable artifacts. |
| GitHub Action | Versioned workflow-facing wrapper around a released TDE product. | Action consumers pin an immutable release-compatible version. |
| Python library | Public Runtime API distributed by the Python package. | Embedded use; not an adapter or implementation-internal distribution channel. |

## Consumer model

| Consumer | Consumption model |
| --- | --- |
| CLI | Installs or invokes a released `tde` executable. |
| Python Library | Pins a released Python package and uses only the documented public Runtime API. |
| GitHub Actions | Pins a released Action version and supplies repository/configuration inputs. |
| CI/CD | Uses the CLI package, container image, or Action without coupling to Runtime internals. |
| Docker | Runs the published image locally, in CI, or on a self-hosted platform. |
| Future Dashboard | Consumes released evidence and stable product interfaces; no Runtime coupling. |
| Future Cloud | Uses released products and explicit service contracts. |
| Future IDE | Integrates through versioned CLI/library contracts. |
| Future MCP | Uses an explicitly released server/product contract. |

## Installation philosophy

Preferred installation order is:

1. PyPI
2. Homebrew
3. Docker
4. GitHub Releases
5. Native package managers

PyPI is the default package source. Homebrew and Docker provide ergonomic
workstation and isolated-runtime options. GitHub Releases are the canonical
direct asset and provenance surface. Native package managers are secondary
channels: they must consume approved immutable release artifacts and may not
become an independent source of Runtime behavior.

## GitHub Action target

The GitHub Action is a first-class deployment target, not a Runtime extension.
Its high-level architecture is a versioned workflow interface that resolves a
released TDE product, supplies repository and configuration inputs, invokes the
CLI, and exposes canonical evidence, report locations, and exit status to the
workflow consumer. It must not embed a separate analyzer, capability, or
qualification implementation.

Action qualification requires an immutable Action revision, least-privilege
permissions, fork-safe behavior, a pinned released TDE artifact, supported
input/output contracts, and release-compatible evidence. This increment does
not implement an Action.

## Docker target

Docker packages the released CLI for local CLI execution, CI execution, and
self-hosted execution. A future dashboard may be hosted alongside compatible
services, but dashboard hosting is not part of the CLI image definition. Each
image must carry an immutable digest, version, provenance, and qualification
evidence. This increment does not build or publish an image.

## Python library target

The Python package delivers the supported public Runtime API for library
consumers, embedding, automation, and integrations. Library consumers pin a
released compatible version and use public contracts; deployment does not grant
access to private Runtime or adapter implementation details. This strategy does
not add or alter any API.

## Release profiles and lifecycle

| Profile | Intended channel | Purpose |
| --- | --- | --- |
| Development | Local or ephemeral candidate artifacts | Engineering feedback; never a consumer release claim. |
| Internal | Controlled internal distribution | Operational validation with explicit provenance and approval. |
| Stable | Public supported channels | Supported, immutable consumer product. |
| Future Enterprise | Planned controlled enterprise channels | Evaluated only after stable product and governance evidence. |

```text
Development → Qualification → Internal Release → Stable Release → Future Public Ecosystem
```

At every transition, Release Runtime planning, qualification, artifact
provenance, human approval, and immutable release evidence remain required.
The strategy neither relaxes release gates nor creates a release commitment.

## Future targets

Generation 2 evaluates winget, Chocolatey, APT, DNF, Pacman, and IDE
integrations as secondary distribution or consumer surfaces. They remain
planned; none are implemented or supported for publication by this document.

Generation 3 research includes a REST API, MCP Server, cloud-hosted Runtime,
and organization service. These are future roadmap hypotheses, not deployment
targets or service commitments.

## Product positioning and evolution guardrails

TDE is an Engineering Runtime, CLI, Python Library, GitHub Action, and Docker
Runtime product. Future deployment targets extend these released product forms;
they do not redefine the Runtime, evidence model, capability contracts, or
consumer independence. The release architecture and its evidence gates remain
the governing implementation path.
