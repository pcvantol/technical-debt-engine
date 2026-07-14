# Package build reproducibility

## Canonical dependency policy

The runtime package has no third-party runtime dependencies. Its build backend
is exactly pinned in `pyproject.toml`; compatible ranges are not accepted for
build dependencies. `requirements/build-tools.txt` is the canonical build-tool
lock: every direct and transitive tool version is exact and every permitted
download has a SHA-256 hash. Install it with:

```sh
python -m pip install --require-hashes --no-deps -r requirements/build-tools.txt
```

Changing the build backend or build-tool lock is a packaging change and must
update both the exact pin and its hashes. There is intentionally no runtime
dependency lock because the published package declares none.

## Canonical build

Use an empty directory outside the source tree. The builder derives
`SOURCE_DATE_EPOCH` from the candidate commit unless it is supplied explicitly,
builds the source distribution and wheel with the pinned isolated tools, then
canonicalizes ZIP/TAR metadata that setuptools does not make stable.

```sh
python tools/package_build.py --output /tmp/tde-build
```

The output contains exactly one wheel, one source distribution,
`SHA256SUMS`, and `build-provenance.json`. The checksum file uses SHA-256.
The provenance record has a versioned schema and records the repository,
candidate SHA and branch, source-date epoch, build platform, Python/package
runtime versions, builder/tool versions, deterministic build identity, and
digest-bound artifact identities.

`artifactIdentity` is derived from the final artifact digest. `buildIdentity`
is derived only from candidate, schema, epoch, and pinned builder inputs; it
does not contain a clock, host path, or platform value. Platform data remains
in provenance as observed evidence, not identity input.

## Qualification

Build twice from the same clean candidate and compare both artifact types and
their `SHA256SUMS` files. Then qualify both artifacts through isolated virtual
environments:

```sh
python tools/verify_installed_package.py \
  --wheel /tmp/tde-build/*.whl --sdist /tmp/tde-build/*.tar.gz
```

The qualifier invokes only the installed `tde` console script. It verifies the
CLI and runtime paths, then dogfoods Code Size, Complexity, Policy, baseline,
comparison, Query, and report. The GitHub workflow
`.github/workflows/package-build.yml` runs these checks for pull requests and
manual dispatch, uploads evidence, and neither publishes nor creates a release.
