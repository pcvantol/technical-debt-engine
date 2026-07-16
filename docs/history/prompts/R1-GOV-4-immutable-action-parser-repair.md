# R1-GOV-4 — Immutable GitHub Action Reference Parser Repair

| Field | Immutable record |
| --- | --- |
| Prompt ID | R1-GOV-4 |
| Title | Immutable GitHub Action Reference Parser Repair |
| Branch | `codex/immutable-action-parser` |
| Implementation commit | `ed74a833c1a8fa52e1de91dfbc3e5542ee8cfe64` |
| Pull Request | Draft [#74](https://github.com/pcvantol/technical-debt-engine/pull/74) |
| Decision | `IMMUTABLE_ACTION_PARSER_OPERATIONAL` |
| Created and updated | 2026-07-16 |
| Freeze reached | No — this immutable record is committed while PR #74 is draft, before it becomes reviewable. |
| Prompt completed | Yes; reviewable transition is the Freeze Point. |
| Pull request created | Yes — draft PR #74. |
| Engineering stopped | Required immediately after the reviewable transition. |

## Scope and root cause

This increment repairs only Software Assurance's immutable GitHub Action
reference parser. The former regular expression accepted only `- uses:` lines.
It therefore rejected the valid SHA-pinned job `publish` step `Publish the
certified Python distributions using Trusted Publishing` in
`.github/workflows/internal-release-publish.yml`:

```yaml
uses: pypa/gh-action-pypi-publish@6733eb7d741f0b11ec6a39b58540dab7590f9b7d
```

No workflow source was modified.

## Delivered behavior

`parse_action_reference` normalizes owner, repository, optional path, and
commit SHA for `owner/repository[/path]@revision`. It recognizes SHA-pinned
step-level actions, job-level reusable workflows, and reusable workflow paths.
Only complete 40-character commit SHAs are immutable. Branches, tags,
`latest`, missing or short SHAs, expressions, variables, and matrix-derived
references remain rejected.

## Validation

- `PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'`: 98 tests passed.
- `git diff --check`: passed.
- Software Assurance against the two retained independent package-build directories from successful non-publishing Actions run `29451595432`: `PASS`; `workflowIntegrity=true`; 40 immutable action references recognized, including the exact PyPI reference above.
- Trusted Delivery consumer validation with the repaired Software Assurance evidence: `PASS`; it consumes the assurance decision and does not duplicate parser logic.
- Release Qualification remains operational for retained candidate `3fda62e72850f1c67f1554f7612580eccf16ae34`; this increment creates no candidate.

## Known limitations

The parser intentionally supports GitHub's external action and reusable-workflow
reference form only. Unsupported or malformed YAML scalar forms fail closed.
The retained artifact validation is non-publishing evidence; it does not create
or recertify a current-mainline Release Candidate.

## Deferred Work

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| Create and certify the current mainline Release Candidate. | Parser repair is complete; release-candidate creation and publication are outside this increment. | R1-4A — Create and Certify Current Mainline Release Candidate | `P0` |

This archive is immutable. Any correction requires a later prompt archive.
