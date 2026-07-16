# Internal Release Authorization

## Canonical authorization policy

TDE currently has one objectively verified repository maintainer: owner and
only direct collaborator `pcvantol`. For this operating model, a **Single
Maintainer Release Authorization** is valid only when all of the following are
true: an explicit authorization record binds the exact candidate and preserved
bundle; the manual publication workflow re-verifies that record and bundle; and
the `internal-release` protected Environment requires that maintainer. GitHub
self-approval is permitted only because no independent maintainer exists; it
does not eliminate the explicit authorization-record, bundle-verification, or
publication-evidence requirements.

If the repository gains multiple maintainers, independent approval becomes
mandatory before any publication. The `internal-release` Environment must then
require an independent reviewer and prevent self-review. This policy changes
automatically with the objectively verified maintainer model; an existing
single-maintainer authorization never waives the future team requirement.

The immutable authorization record for the prior Internal Release attempt is
[`release/authorizations/internal-release-0.1.0.json`](release/authorizations/internal-release-0.1.0.json).
It binds approver `pcvantol`, the exact candidate, version, certified bundle,
checksum, publication workflow, and the separately approved tag, GitHub
Release, PyPI, and Docker Hub targets. A new record is required for every new
candidate/bundle; this historical record does not authorize the current one.

Authorization validation is deterministic and fail-closed:

```sh
PYTHONPATH=src python tools/verify_release_authorization.py \
  --record release/authorizations/internal-release-0.1.0.json \
  --candidate-sha 3fda62e72850f1c67f1554f7612580eccf16ae34 \
  --release-version 0.1.0 \
  --bundle-id bundle.sha256.e0c12c31b0ecf4b0bc6a9a4054717ed4d449c70ff90af9fc917f0ac87c6deeef \
  --bundle-checksum sha256:a4cbaab6cf23b294d9777c1086798a2e68bb1f1d916276eaeb32627f52b68377
```

The current `internal-release` Environment exists and is consistent with the
single-maintainer policy: its required reviewer is `pcvantol` and GitHub permits
self-review. It remains a protected human-authorization boundary. No tag,
GitHub Release, PyPI upload, Docker upload, or `latest` tag has been executed.

R1-4B must create and validate a fresh record binding the current candidate,
bundle, checksum, approved targets, and publication workflow before any
separately protected publication dispatch.
