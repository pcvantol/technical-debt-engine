# Certified Candidate Publication Boundary

## Canonical rule

Publication publishes the immutable, certified release candidate. It does not
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

## Publication contract

When all intervening commits are `ADMINISTRATIVE` and a human authorizes the
release, the immutable version tag and GitHub Release reference the certified
candidate SHA. PyPI receives the certified wheel and source distribution; any
Docker publication uses the certified image only and never rebuilds from
current `main`. Publication evidence records the candidate SHA, administrative
merge SHA(s), per-commit classification, publication SHA, artifact identities,
and timestamps.

This boundary does not publish anything itself.

R1-2B provides a retained, checksum-bound non-published OCI bundle for candidate
`2d6132061807a433178a1ababc1709340cb937de`. Any future Docker Hub action must
use that certified image evidence after explicit human authorization; it must
not rebuild from a later branch or `main`.
