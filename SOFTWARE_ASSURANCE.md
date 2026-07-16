# Operational Software Assurance

`tde assure` evaluates a repository against the canonical Software Assurance
model without publishing a release or invoking Trusted Delivery.

It emits deterministic `tde.software-assurance` evidence covering repository
identity, branch and working-tree integrity; dependency declarations, exact
versions and hash-locked build tooling; immutable least-privilege workflows;
configuration schema compatibility and provenance; and canonical documentation.

Workflow references are parsed as `owner/repository[/path]@revision` and the
normalized owner, repository, optional path, and commit SHA are included in
the workflow evidence. Step-level actions, job-level reusable workflow calls,
and reusable workflow paths are immutable only when `revision` is a complete
40-character commit SHA. Branches, tags (including `latest`), missing or short
SHAs, expressions, variables, and matrix-derived references are rejected.

Candidate package artifacts are supplied explicitly because a repository does
not itself contain a release candidate. Build each candidate with
`tools/package_build.py`, then provide both independent outputs:

```sh
tde --format json assure . \
  --artifact-directory /path/to/first \
  --artifact-directory /path/to/second
```

Each directory must contain exactly one wheel, one source distribution,
`SHA256SUMS`, and `build-provenance.json`. Assurance recomputes artifact
digests, compares them with the manifest and provenance records, and requires
the two candidates to be byte-identical. With no supplied candidates the
repository checks remain operational but artifact assurance is explicitly a
limitation and the decision is `PASS_WITH_WARNINGS`.

The command is fail-closed: invalid repository, dependency, workflow,
configuration, documentation, or supplied artifact evidence results in `FAIL`.
It does not make delivery, release qualification, certification, or publication
decisions.
