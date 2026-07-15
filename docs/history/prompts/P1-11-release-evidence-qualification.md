# P1-11 — Release Evidence Qualification

| Field | Value |
| --- | --- |
| Prompt ID | `P1-11` |
| Branch | `codex/p1-11-release-evidence-qualification` |
| Implementation commit | `39f6331` |
| Pull request | Pending finalization |
| Decision | `RELEASE_EVIDENCE_PARTIALLY_QUALIFIED` |
| Created | 2026-07-15 |
| Updated | 2026-07-15 |
| Freeze reached | No — final validation and reviewable PR pending |
| Prompt completed | No |
| Pull request created | No |
| Engineering stopped | No |

## Objective evidence

- `tde release-qualify` now requires one or more explicit
  `--release-capability` values, executes the selected set through Runtime, and
  records selection, execution, Runtime Qualification, confidence, limitations,
  and Policy evidence.
- It writes immutable `*.release-evidence.json`; its canonical digest and
  content-derived identity are cross-referenced by the qualification manifest.
- `tde certify` reads and integrity-validates that persisted record rather than
  duplicating Runtime or Policy logic.
- Dogfooding two byte-identical TDE builds selected `code_size` and
  `complexity`. Runtime Qualification was `QUALIFIED`; Software Assurance and
  Trusted Delivery were `PASS`; Policy was `FAIL`; Release Qualification was
  `RELEASE_BLOCKED` / `NOT_READY`; certification was `RELEASE_NOT_CERTIFIED`.
- `PYTHONPATH=src python -m unittest discover -s tests -v` passed 82 tests.

## Known limitations

The selected candidate still fails its real policy evaluation. This is a
candidate-quality decision, not a missing, blocked, or not-applicable release
evidence condition. No release, tag, publication, or human approval occurred.

## Deferred Work

| Description | Reason | Priority | Recommended prompt |
| --- | --- | --- | --- |
| Resolve the selected candidate's Policy `FAIL`, rebuild, and recertify. | Qualification and certification correctly fail closed on the persisted policy decision. | `P1` | Release Policy Remediation and Recertification |
| Human approval and publication. | Outside this increment. | `P1` | Internal Release |
