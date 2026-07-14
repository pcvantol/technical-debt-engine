# P1-4 — Code Size Cross-Platform Qualification

| Field | Record |
| --- | --- |
| Prompt ID | `P1-4` |
| Prompt title | Code Size Cross-Platform Qualification |
| Branch | `codex/p1-4-code-size-cross-platform-qualification` |
| Qualification candidate commit SHA | `ee8c625bc3081f73f8f729a4216c75ba5fb50b85` |
| Pull request | [#46](https://github.com/pcvantol/technical-debt-engine/pull/46) |
| Decision | `CODE_SIZE_CROSS_PLATFORM_QUALIFIED` |
| Created / updated | 2026-07-14 / 2026-07-14 |
| Freeze reached | On reviewable transition of PR #46 |
| Prompt completed | On reviewable transition of PR #46 |
| Pull request created | Yes — initially draft to collect matrix evidence |
| Engineering stopped | On reviewable transition of PR #46 |

## Outcome

The existing Code Size capability is qualified through a GitHub-hosted installed-wheel matrix: Ubuntu, macOS and Windows with Python 3.11 and 3.13. The workflow builds one candidate wheel, installs it in an isolated environment on each target, provisions checksum-verified `cloc 2.10`, and invokes only the installed `tde` executable for the capability path.

GitHub Actions [run 29363505649](https://github.com/pcvantol/technical-debt-engine/actions/runs/29363505649) succeeded. Its comparison artifact records six equivalent analytical projections, `cloc 2.10` on every target, and candidate wheel checksum `sha256:59c3da9595954d61a4f02c7eab8b6b6cceaeb4dbe91216223d607d49e7782968`.

## Validation

- Installed-wheel `tde assess --capability code-size` passed on all six matrix targets.
- Every target persisted canonical evidence, verified Evidence Store retrieval and tamper detection, executed persisted-only Query and Code Size report, and dogfooded TDE itself.
- Missing `cloc`, unsupported `cloc 2.09`, and a timeout each failed closed with structured blocking output.
- Canonical repository/language/file metrics, classifications, findings and Runtime Qualification were equivalent across the matrix.
- Local isolated-package verification passed 60 tests; `git diff --check` passed.

## Known limitations

- The qualification evidence applies to `cloc 2.10` on GitHub-hosted runners only.
- Runtime does not install analyzers; it discovers a supported `cloc` executable from `PATH`.
- No release, deployment, publication, Runtime Architecture change or new capability is included.

## Deferred work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Qualify non-Python Complexity analyzers. | P1-4 owns Code Size only. | Future capability-specific prompt | `P1` |
| Update immutable action revisions before their supported Node runtime is removed. | GitHub Actions emitted Node.js 20 compatibility notices for pinned action revisions; this does not invalidate the qualification evidence. | Workflow-maintenance prompt | `P2` |

## Recommended next prompt

Determine after review and merge. Do not add work to this frozen increment.
