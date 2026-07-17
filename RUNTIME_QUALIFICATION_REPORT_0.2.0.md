# Runtime Qualification Report — 0.2.0

## Release identity

| Field | Value |
| --- | --- |
| Runtime version | `0.2.0` |
| Release commit | `44a34457454829e495cf9b460f3fa6bcc3bb6ab5` |
| GitHub Release | https://github.com/pcvantol/technical-debt-engine/releases/tag/0.2.0 |
| Certified candidate run | https://github.com/pcvantol/technical-debt-engine/actions/runs/29597785809 |
| Publication evidence | https://github.com/pcvantol/technical-debt-engine/actions/runs/29597969107 |
| Bundle ID | `bundle.sha256.5c32ab6f333334ea665fd304b4aeb365323f2597451f89adda2bee1ac870c573` |

## Qualified public contract

The certified candidate rebuilt the wheel and source distribution deterministically,
qualified the public Docker image, executed the public CLI, and validated the
canonical release bundle before publication.  The public release workflow completed
successfully after protected-environment approval.

| Target | Result | Immutable identity |
| --- | --- | --- |
| GitHub Release | published | tag `0.2.0` at the release commit |
| PyPI | published with Trusted Publishing | `technical-debt-engine-runtime==0.2.0` |
| Docker Hub | published | `pcvantol/technical-debt-engine:0.2.0` |
| Docker platforms | verified | `linux/amd64`, `linux/arm64` |

The Docker OCI index is
`sha256:8285a5082eaa1a5ac914b349ddec21c9e02cc4269421774d4f112383bc688ca9`.
No mutable `latest` tag was published.

## Public-runtime practice validation

An isolated macOS environment installed the released PyPI package and invoked only
the public `tde` CLI with cloc 2.10 available on `PATH`.

| Repository | Profile | Capability execution | Runtime qualification | Assessment decision |
| --- | --- | --- | --- | --- |
| Technical Debt Engine | `minimal` | `code_size` through cloc 2.10 | `QUALIFIED` | `PASS_WITH_WARNINGS` |
| DJConnect | `minimal` | `code_size` through cloc 2.10 | `QUALIFIED` | `FAIL` |

DJConnect's `FAIL` is a truthful result of the existing public policy threshold; it
is not an analyzer, execution, evidence, schema, or exit-code failure.  The complete
DJConnect scan was read-only and produced canonical evidence.

## Capability and schema coverage

- Analyzers: cloc 2.10 and Radon 6.0.1.
- Capabilities: `code_size` and `complexity`.
- Profiles: `minimal` and `standard`.
- Public schemas: capability, policy, assessment-decision, assessment,
  repository-qualification, and differential evidence.

## Remaining qualification automation

Existing GitHub qualification workflows already execute installed-wheel capability
coverage on Ubuntu, macOS, and Windows.  The dedicated Q0 workflow added with this
report consolidates the released wheel and PyPI paths against both reference
repositories.  Docker execution remains Linux-hosted because GitHub-hosted macOS and
Windows runners do not provide a Linux Docker daemon; the published OCI index itself
contains both supported Linux platforms.
