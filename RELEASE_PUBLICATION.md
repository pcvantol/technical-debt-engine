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
| Approval | Require the release owner and an independent repository maintainer; prevent self-review and restrict the Environment to the default branch. |
| Permissions | Preflight is read-only (`actions: read`, `contents: read`). Only the protected publish job receives `contents: write` and `id-token: write`. |
| PyPI | Configure PyPI Trusted Publishing for this repository, workflow, and Environment. A future fallback may use only a project-scoped, upload-only `PYPI_API_TOKEN`, never a broad account token. |
| Docker Hub | Set `DOCKERHUB_USERNAME` as an Environment variable and `DOCKERHUB_TOKEN` as an Environment secret, scoped to `pcvantol/technical-debt-engine` with push-only access. |
| Inputs | Require exact candidate SHA, version, source run, artifact name, and a JSON assertion binding reviewer identity/time, candidate, bundle ID/checksum, and all three targets. |

Environment approval is the human authorization boundary. The JSON input is deliberately only a deterministic structure/binding check; R1-3C owns human authorization.
