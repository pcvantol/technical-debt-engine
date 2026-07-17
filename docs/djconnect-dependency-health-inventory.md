# DJConnect dependency-health inventory

## Selection for G2-B

The selected 1.0 dependency-health consumer is `pcvantol/djconnect-api`.
Its root `package.json` and committed `package-lock.json` identify npm as the
package manager, and its active `ci-cd.yml` pipeline provides a practical
consumer path. npm can supply lockfile-backed direct/transitive evidence and
native `npm outdated --json` evidence without introducing a second dependency
analysis product.

`pcvantol/djconnect-pi` was inspected but is not selected for this capability:
it declares Python dependencies in `pyproject.toml` but does not provide a
committed Python lockfile. It therefore cannot presently provide reproducible
transitive and outdated evidence for this narrow 1.0 capability. Python support
is post-1.0 until a concrete consumer and reliable artifact exist.

No NuGet repository is selected: `djconnect-windows` contains project files,
but no selected 1.0 pipeline or lockfile-backed consumer evidence was identified
for this increment.

## Scope record

| Item | Decision |
| --- | --- |
| Ecosystem | npm only |
| Package manager | npm with `package-lock.json` |
| Consumer | `pcvantol/djconnect-api` |
| Native analyzer | `npm outdated --json --package-lock-only` |
| Evidence source | `package.json`, `package-lock.json`, native npm output |
| Unsupported | Python, NuGet, other JavaScript package managers, unlocked npm projects |

TDE reads these inputs and normalizes evidence only. It does not install,
update, publish, or rewrite dependencies.
