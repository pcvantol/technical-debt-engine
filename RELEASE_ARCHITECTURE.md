# Mainline Snapshot Release Architecture

## Canonical model

An Internal Release candidate is an immutable snapshot of an exact commit that
is already reachable from canonical `main`. It is never a feature-branch,
release-branch, detached sibling, dirty checkout, or local-only commit.

```text
MAINLINE_READY
  -> CANDIDATE_SNAPSHOT_CREATED
  -> CANDIDATE_BUILD_COMPLETE
  -> CANDIDATE_QUALIFIED
  -> CANDIDATE_CERTIFIED
  -> CERTIFIED_BUNDLE_PRESERVED
  -> HUMAN_AUTHORIZED
  -> PUBLICATION_IN_PROGRESS
  -> INTERNAL_RELEASE_PUBLISHED
```

The default candidate is the synchronized `main` HEAD. An earlier commit may be
selected only when it is already an ancestor of `main`, repository policy
supports the version boundary, and the selection is explicitly recorded.

## Candidate snapshot and freeze

The candidate record is a non-mutating, versioned evidence record containing
the exact SHA, version, release profile, actor, creation time, source branch,
and mainline SHA. The required invariant is:

```sh
git merge-base --is-ancestor <candidate-sha> main
```

Candidate creation occurs only after implementation is merged, main is
synchronized and clean, and CI has passed for the selected mainline SHA. The
candidate workflow checks out that SHA exactly. It creates no final release
tag. A release branch may contain administrative documentation or explicitly
authorized emergency remediation, but cannot be a candidate source until its
contents are merged to main and a new mainline snapshot is selected.

## Candidate-bound evidence and supersession

Every wheel, source distribution, OCI archive/index, checksum, provenance
record, manifest, qualification, certification, and preserved bundle must name
the same candidate SHA. Administrative main commits may update status,
governance, authorization evidence, prompt history, release notes, and
publication preparation; they do not modify the candidate or its artifacts.

A candidate is `SUPERSEDED` and cannot be published when an intended-release
product, package, dependency, build, Docker, workflow, test, artifact, or
material version change follows it; when remediation changes its inputs; or
when required evidence cannot be retained. Create a new candidate from the
updated mainline commit. Ambiguous release intent defaults to supersession.

## Bundle, authorization, and publication

Successful certification preserves a complete bundle outside temporary
workspace state, including distributions, OCI artifacts and index metadata,
checksums, all release-chain evidence, provenance, bundle manifest, and bundle
checksum. The retention record identifies its workflow run, artifact ID,
expiry, access control, and no-rebuild retrieval procedure.

Only after verified retrieval of a certified preserved bundle may a human
authorize specified targets. Authorization identifies candidate SHA, version,
bundle identity/checksum, approver, timestamp, and targets. The future manual,
protected-environment publication workflow must verify those inputs, create the
final immutable tag at the candidate SHA, publish only bundle contents, verify
the published identities, and generate evidence. It must never rebuild and
must not run on push or pull-request events.
