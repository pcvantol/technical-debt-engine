# Prompt Finalization

## Before Freeze

Before a reviewable Pull Request exists, a prompt must validate its scoped work, run `git diff --check`, commit only scoped changes, push one dedicated branch, and open exactly one reviewable Pull Request.

## Freeze

The Prompt Freeze Point occurs immediately when the reviewable Pull Request exists.

- Engineering is complete and implementation is frozen.
- No additional implementation commits, Runtime changes, test changes, scope expansion, or immediate fixes are permitted.
- Documentation may not change except for the final Prompt Execution Report, [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md), [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md), [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md), [PROMPT_INDEX.md](PROMPT_INDEX.md), and the immutable prompt archive.
- The prompt may perform only those finalization actions, produce its final management summary, and stop.
- The Pull Request is the immutable boundary of one engineering increment. A new increment begins only after merge.

## Late Discoveries and Deferred Work

New work discovered after the Freeze Point must not be added to the existing Pull Request. Record it as Deferred Work, state why it was deferred, name the recommended follow-up prompt, assign a priority, and stop. Deferred Work is the input to the next engineering increment.

## Prompt Execution Report

The immutable prompt archive is the Prompt Execution Report. It must record the Prompt ID, title, branch, commit SHA, Pull Request, decision, validation summary, created and updated dates, known limitations, Freeze reached, Pull Request created, engineering stopped, Deferred Work, and recommended next prompt.

## Finalization Checklist

After the Freeze Point, complete only the permitted finalization records and leave the repository working tree clean apart from unrelated user-owned files that were explicitly preserved.

The archive is never edited after creation. Any correction is a later prompt with its own archive.
