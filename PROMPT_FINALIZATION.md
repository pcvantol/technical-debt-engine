# Prompt Finalization

## Before Freeze

Before a reviewable Pull Request exists, a prompt must validate its scoped work, run `git diff --check`, commit only scoped changes, and push one dedicated branch. A draft Pull Request may be opened solely to obtain its metadata and include the mandatory Prompt Execution Report and status records in that same Pull Request. A draft is not reviewable and does not reach the Freeze Point.

## Freeze

The Prompt Freeze Point occurs immediately when the Pull Request becomes reviewable. One prompt owns exactly one objective, one engineering increment, and one reviewable Pull Request; the increment ends at this point and merge remains a separate decision.

- Engineering is complete and implementation is frozen.
- No additional implementation commits, Runtime changes, test changes, production-documentation changes, scope expansion, immediate fixes, or next-increment work are permitted.
- Documentation may not change except for the final Prompt Execution Report, [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md), [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md), [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md), [PROMPT_INDEX.md](PROMPT_INDEX.md), and the immutable prompt archive.
- The prompt may perform only those finalization actions, produce its final management summary, and stop.
- The Pull Request is the immutable boundary of one engineering increment. A new increment begins only after merge.

## Late Discoveries and Deferred Work

New work discovered after the Freeze Point must not be added to the existing Pull Request. Record its description, why it was deferred, a priority, and the recommended follow-up prompt, then stop. Deferred Work is the input to the next engineering increment.

## Prompt Execution Report

The immutable prompt archive is the Prompt Execution Report. It must record the Prompt ID, title, branch, commit SHA, Pull Request, decision, validation summary, created and updated dates, known limitations, Freeze reached, Prompt completed, Pull Request created, engineering stopped, Deferred Work, and recommended next prompt.

## Finalization Checklist

Before the Pull Request becomes reviewable, include the Prompt Execution Report and final status records in that Pull Request wherever possible. After the Freeze Point, complete only the permitted finalization records and leave the repository working tree clean. The repository may not retain untracked operating-system artifacts.

The archive is never edited after creation. Any correction is a later prompt with its own archive.
