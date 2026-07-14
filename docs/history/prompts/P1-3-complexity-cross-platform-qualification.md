# P1-3 — Complexity Cross-Platform Analyzer Qualification

| Field | Record |
| --- | --- |
| Prompt ID | `P1-3` |
| Branch | `codex/p1-3-complexity-cross-platform-qualification` |
| Pull Request | Pending draft creation |
| Decision | Pending required GitHub-hosted matrix evidence |

## Qualification design

- One wheel is built on Ubuntu and installed without source checkout imports on
  Ubuntu, macOS and Windows, for Python 3.11 and 3.13.
- Every isolated environment provisions `radon==6.0.1`, records its resolved
  version and wheel checksum, and exercises version, inspect, assessment,
  target validation, persisted Query and persisted report.
- The workflow validates persisted evidence through the Evidence Store, tests a
  tampered record fail-closed, tests missing Radon fail-closed, and runs an
  installed-wheel dogfood assessment of TDE itself.
- The final comparison allows only execution IDs, timestamps, durations and raw
  native output to differ. It fails closed on any analytical difference.

## Cleanup result

PR #43 is merged and its remote branch is absent. Local
`codex/p1-2-complexity-vertical-slice` is retained: GitHub squash merging and a
branch-only finalization commit prevent ancestry-based proof that it has no
remaining merge candidate. This is a fail-closed cleanup outcome and does not
block this isolated qualification branch.

## Known limitations and deferred work

- No non-Python Complexity analyzer is qualified or claimed.
- Final decision, candidate SHA, workflow run identities and matrix records are
  added only after the GitHub-hosted workflow completes while this PR is draft.
