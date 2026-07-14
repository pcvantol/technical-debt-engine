# Repository initialization report

Date: 2026-07-14

## Repository identity

- Owner / repository: `pcvantol/technical-debt-engine`
- URL: <https://github.com/pcvantol/technical-debt-engine>
- Visibility: public
- Default branch: `main`
- Description: Capability-based CLI for measuring, qualifying and reporting technical debt across languages and projects.
- Homepage: unset
- License: `LICENSE_DECISION_PENDING`
- Initial ownership: `pcvantol`; direct collaborator read-back lists only `pcvantol` (admin).

## Effective configuration

- Topics: `technical-debt`, `code-quality`, `maintainability`, `static-analysis`, `cyclomatic-complexity`, `software-metrics`, `developer-tools`, `cli`, `sarif`, `evidence`, `qualification`, `python`, `dotnet`, `swift`, `javascript`, `cpp`, `ci-cd`.
- Squash merge is enabled; merge commits and rebase merges are disabled; merged head branches are automatically deleted.
- Auto-merge is enabled. Issues are enabled; discussions and wiki are disabled. No project was created.
- GitHub Actions is enabled with all actions allowed, a read-only default `GITHUB_TOKEN`, and workflow pull-request approval disabled. Native SHA pinning is disabled, matching DJConnect; no cross-repository workflow exists yet, so no exception is claimed or inherited.
- Security read-back: Dependabot alerts and security updates are enabled; secret scanning and push protection are enabled; private vulnerability reporting is enabled. CodeQL default setup was deliberately not enabled because the product languages and workflow do not yet exist.
- The active `Trusted Delivery main integrity` ruleset applies to the default branch, requires a pull request, requires resolved review conversations, prohibits deletion and non-fast-forward updates, and has no bypass actors. Its approval count is zero: this enforces the normal pull-request path without an artificial independent-review deadlock for the single maintainer. No required status check was added because the trusted-delivery workflow and checks do not yet exist.

## DJConnect baseline and deviations

Live `pcvantol/djconnect` read-back on 2026-07-14 established: `main`, squash-only merges, automatic head-branch deletion, Actions enabled, read-only workflow tokens, workflow PR approval disabled, native SHA pinning disabled, and the same integrity ruleset with no bypass actors. DJConnect additionally requires `Trusted Delivery qualification / Qualify trusted delivery` on `main`; TDE does not yet have that workflow, so requiring it would permanently block the repository.

Intentional deviations:

- Wiki is disabled for TDE per its initialization brief (DJConnect currently enables it).
- TDE has no required status check until its governed workflows exist. The eventual intended check is the Trusted Delivery qualification check; its enforcement is pending a future governance prompt. The current pull-request rule preserves single-maintainer compatibility and does not create an artificial independent-review deadlock.
- No reusable workflow, release/artifact contract, package, deployment, environment, release secret, signing setup, or broad PAT was created.

## GitHub App authorization

Confirmed on 2026-07-14 after the DJConnect Trusted Delivery installation was authorized: the Engineering Platform GitHub App connector's installed-repository read-back returns `pcvantol/technical-debt-engine` (repository ID `1300429609`) with effective `admin`, `maintain`, `push`, `triage`, and `pull` permissions. This is direct evidence that the installed App can read the repository and has the repository scope needed for subsequent Engineering Platform workflows.

The local OAuth credential still cannot call the App-only installation REST endpoint; that limitation does not negate the successful App-connector read-back. No App credential, installation token, or broad PAT was exposed or created.

## Content and validation

- Initial commit: `3c30654273ae5a44f41d38b7deb5b0e66ac54e38` (`chore: initialize Technical Debt Engine repository`).
- `main` exists and is the default branch. The only bootstrap content before this record was `README.md`; no runtime, analyzer, workflow, package metadata, or language-specific ignore file was created.
- No tag, release, package, deployment, or environment has been created.
- The remote origin is the authenticated canonical HTTPS equivalent: `https://github.com/pcvantol/technical-debt-engine.git`.

## Final decision

`TDE_REMOTE_REPOSITORY_INITIALIZED`

The remote repository is initialized, its settings have been read back, and the required GitHub App repository accessibility has been proved.
