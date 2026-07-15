# Operational Trusted Delivery

`tde trusted-delivery` is an evidence-only candidate validator. It does not
qualify a release, approve publication, create a tag, or publish an artifact.

It consumes canonical Software Assurance evidence rather than reproducing its
assurance rules. It then binds that evidence to the Git candidate, a supplied
versioned delivery manifest, reproducible build artifacts, and immutable,
least-privilege GitHub workflow provenance.

```sh
tde --format json trusted-delivery . \
  --manifest /path/to/delivery-manifest.json \
  --artifact-directory /path/to/independent-build-one \
  --artifact-directory /path/to/independent-build-two
```

The manifest conforms to
[`schemas/trusted-delivery-manifest.schema.json`](schemas/trusted-delivery-manifest.schema.json).
Its candidate SHA, repository, branch, filenames, and SHA-256 checksums must
match the validated candidate and Software Assurance artifact records.

When a manifest and artifacts are intentionally absent before release work,
the command returns `PASS_WITH_WARNINGS` and records that limitation. A
supplied invalid manifest or artifact reference fails closed.

## Evidence example

The canonical JSON result contains:

```json
{
  "schemaId": "tde.trusted-delivery",
  "candidate": {"candidateIdentity": "candidate.git.<sha>", "repository": "<origin>", "branch": "<branch>"},
  "manifest": {"identity": "manifest.sha256.<digest>"},
  "artifacts": {"provenanceValidated": true},
  "workflow": {"immutableActions": true, "leastPrivilege": true},
  "softwareAssurance": {"assuranceId": "assurance.sha256.<digest>"},
  "decision": "PASS"
}
```

The decision expresses delivery-evidence integrity only. Release
Qualification, Release Certification, and publication remain outside this
increment.
