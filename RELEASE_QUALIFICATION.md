# Operational Release Qualification

`tde release-qualify` creates canonical, evidence-only release qualification.
It consumes two independently built artifact directories, Software Assurance,
and Trusted Delivery; it never tags, publishes, or creates a release.

```sh
tde --format json release-qualify . \
  --artifact-directory /path/to/build-one \
  --artifact-directory /path/to/build-two \
  --manifest-output /path/to/release-manifest.json
```

The output binds Git candidate identity, runtime/schema/capability/policy
versions, artifacts/checksums/provenance, assurance identity, Trusted Delivery
identity, and the resulting `READY` or `NOT_READY` decision.
