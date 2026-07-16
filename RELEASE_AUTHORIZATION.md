# Internal Release Authorization

The immutable authorization record for the first Internal Release is
[`release/authorizations/internal-release-0.1.0.json`](release/authorizations/internal-release-0.1.0.json).
It binds approver `pcvantol`, the exact candidate, version, certified bundle,
checksum, publication workflow, and the separately approved tag, GitHub
Release, PyPI, and Docker Hub targets.

Authorization validation is deterministic and fail-closed:

```sh
PYTHONPATH=src python tools/verify_release_authorization.py \
  --record release/authorizations/internal-release-0.1.0.json \
  --candidate-sha 3fda62e72850f1c67f1554f7612580eccf16ae34 \
  --release-version 0.1.0 \
  --bundle-id bundle.sha256.e0c12c31b0ecf4b0bc6a9a4054717ed4d449c70ff90af9fc917f0ac87c6deeef \
  --bundle-checksum sha256:a4cbaab6cf23b294d9777c1086798a2e68bb1f1d916276eaeb32627f52b68377
```

The record does not authorize publication while the `internal-release` GitHub
Environment is absent. GitHub's Environment endpoint returned `404` on
2026-07-15T22:30:08Z. No Environment was created or changed in R1-3C, and no
tag, GitHub Release, PyPI upload, Docker upload, or `latest` tag was executed.

After an authorized administrator creates and protects that Environment with
the documented reviewers and credentials, R1-3D may re-verify the record and
perform the separately protected publication dispatch.
