# Certified Mainline Candidate Publication Boundary

## Canonical rule

Publication publishes the immutable, certified mainline release candidate. It does not
automatically publish the later `main` commit. The candidate SHA, its certified
artifacts, their checksums, provenance, Release Qualification, and Release
Certification are the publication inputs and remain immutable.

The canonical lifecycle is:

```text
Certified Candidate → Administrative Merge → Human Authorization → Publication
```

An administrative merge may advance `main` after certification without
invalidating the candidate. Human authorization is still mandatory, and no
publication is implied by certification or merge.

## Candidate identity and commit classification

Before publication, read the candidate identity from the canonical candidate
record and verify its immutable Release Qualification and `RELEASE_CERTIFIED`
Certification. Do not require `HEAD` to equal the candidate SHA. Instead,
classify every commit in `candidate..main`:

```sh
git rev-list --reverse <candidate-sha>..main
git diff-tree --no-commit-id --name-only -r <commit-sha>
git merge-base --is-ancestor <candidate-sha> main
```

A commit is `ADMINISTRATIVE` only when every change is limited to rolling
engineering status, prompt history, release notes, release-governance
documentation, or publication documentation/evidence. It must not change
Runtime, capabilities, dependencies, package contents, build or packaging
configuration, artifacts, Docker definitions, workflows, or any other
implementation contributing to release artifacts.

Any `PRODUCT`, `PACKAGE`, `DEPENDENCY`, `BUILD`, `ARTIFACT`, or `WORKFLOW`
commit after the candidate invalidates the publication boundary. Stop and
create a new release candidate; never reinterpret such a commit as
administrative.

A candidate for which the ancestry command fails is a
`SUPERSEDED_NON_MAINLINE_CANDIDATE`, not an administrative exception. Preserve
its evidence and create a fresh candidate from synchronized main.

## Publication contract

When all intervening commits are `ADMINISTRATIVE` and a human authorizes the
release, the immutable version tag and GitHub Release reference the certified
candidate SHA. PyPI receives the certified wheel and source distribution; any
Docker publication uses the certified image only and never rebuilds from
current `main`. Publication evidence records the candidate SHA, administrative
merge SHA(s), per-commit classification, publication SHA, artifact identities,
and timestamps.

This boundary does not publish anything itself.

R1-2B provides retained historical evidence for sibling candidate
`2d6132061807a433178a1ababc1709340cb937de`. It is not publishable because it
is not an ancestor of main; it must never be promoted or rebuilt. Future Docker
Hub action uses only a certified bundle from a mainline candidate after explicit
human authorization.

## Internal publication infrastructure (R1-3B)

The canonical workflow is [`.github/workflows/internal-release-publish.yml`](.github/workflows/internal-release-publish.yml). It has `workflow_dispatch` as its only trigger. Its default `dry_run: true` retrieves the named bundle artifact, verifies every checksum and identity, verifies `RELEASE_QUALIFIED` / `READY` and `RELEASE_CERTIFIED`, and validates the authorization assertion's structural binding. It neither rebuilds nor publishes an artifact.

The guarded `publish` job requires `dry_run: false` and the protected `internal-release` Environment. It re-verifies the same preserved bundle, then defines the GitHub Release, PyPI Trusted Publishing, and Docker Hub path. Docker uses only `docker.io/pcvantol/technical-debt-engine:<version>` and never `latest`; its published digest becomes publication evidence.

### `internal-release` Environment contract

Configure this Environment outside R1-3B before any non-dry-run dispatch:

| Control | Required configuration |
| --- | --- |
| Approval | In the verified single-maintainer model, require the sole maintainer and permit self-review only with an explicit candidate-bound authorization record. If multiple maintainers exist, require an independent reviewer, prevent self-review, and restrict the Environment to the default branch. |
| Permissions | Preflight is read-only (`actions: read`, `contents: read`). Only the protected publish job receives `contents: write` and `id-token: write`. |
| PyPI | Configure PyPI Trusted Publishing for this repository, workflow, and Environment. A future fallback may use only a project-scoped, upload-only `PYPI_API_TOKEN`, never a broad account token. |
| Docker Hub | Set `DOCKERHUB_USERNAME` as an Environment variable and `DOCKERHUB_TOKEN` as an Environment secret, scoped to `pcvantol/technical-debt-engine` with push-only access. |
| Inputs | Require exact candidate SHA, version, source run, artifact name, and a JSON assertion binding reviewer identity/time, candidate, bundle ID/checksum, and all three targets. |

Environment approval is the human authorization boundary. The JSON input is deliberately only a deterministic structure/binding check; R1-3C owns human authorization.

## Current R1-4A publication readiness

Candidate `04b39c51e2e36a5ac70059f2c030e7cadd37dbe0` has a complete,
retrieved, checksum-verified certified bundle from run `29483960813`. Its
qualification and certification are passing, and the publication workflow is
manual-only and bundle-consuming. GitHub confirms that `internal-release`
exists, has sole maintainer `pcvantol` as required reviewer, and allows
self-review. R1-GOV-5 establishes that configuration as canonical only while
there is one maintainer. R1-4B must still create explicit authorization for
this bundle before any non-dry-run dispatch.

R1-4B has recorded that authorization in
`release/authorizations/internal-release-0.1.0-04b39c51.json`. The retrieved
bundle preflight is ready, but this document does not dispatch the manual
workflow or publish any artifact. R1-4C owns the separately protected
publication operation.

## R1-4D publication attempt

Run `29526820939` passed the preflight and immediate pre-publication bundle
re-verification, then failed in `Create immutable Git tag and GitHub Release
from the certified bundle`. The runner had no configured Git committer identity
for the annotated tag. No tag, GitHub Release, Docker publication, PyPI upload,
or publication evidence was created; Docker and PyPI steps were skipped. A
workflow identity repair is a candidate-to-main workflow change, so a fresh
candidate is mandatory before a later publication attempt.

## R1-4E deterministic tagger identity

Before an annotated tag can be created, the protected publication job configures
repository-local Git identity `Technical Debt Engine Release Automation` with
`technical-debt-engine-release[bot]@users.noreply.github.com`. The job verifies
both effective local values and retains `tagger-identity.json` with its
publication evidence. It does not read runner-global or developer Git settings.

## R1-4G publication outcome

Protected run `29529932503` published immutable tag `0.1.0` at
`223ccfe4b3646f1907ee7e2d7a8c07e8989badd7`, its GitHub Release, and Docker
Hub OCI index `sha256:aa648019045a442a0dbce029ee11ecb15c7755d845205fa8f07467e0faf18679`.
PyPI did not receive the certified distributions because the pinned
`pypa/gh-action-pypi-publish` GHCR container returned `manifest unknown`.
The workflow therefore skipped publication evidence. No `latest` tag exists;
the preserved artifacts must not be rebuilt for any completion operation.
