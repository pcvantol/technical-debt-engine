# Operational Release Qualification

`tde release-qualify` creates canonical, evidence-only release qualification.
It requires an explicit release-capability selection, executes that selection
through Runtime, and persists an integrity-bound Release Evidence record. It
consumes independently built artifact directories, Software Assurance, and
Trusted Delivery; it never tags, publishes, or creates a release.

```sh
tde --format json release-qualify . \
  --release-capability code-size \
  --release-capability complexity \
  --artifact-directory /path/to/build-one \
  --artifact-directory /path/to/build-two \
  --manifest-output /path/to/release-manifest.json
```

The output binds Git candidate identity, the selected capabilities, runtime
qualification (including execution, confidence, and limitations), policy
decision, artifacts/checksums/provenance, Software Assurance, Trusted Delivery,
and Release Qualification. The adjacent `*.release-evidence.json` record is
immutable: its digest and content-derived identity are referenced by the
manifest and then validated by Release Certification. Missing selection,
Runtime evidence, policy evidence, or an unexecuted required capability causes
`RELEASE_BLOCKED`.
