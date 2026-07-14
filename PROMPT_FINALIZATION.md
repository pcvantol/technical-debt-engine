# Prompt Finalization

Before a prompt is declared Reviewable, it must:

1. Validate the scoped work and run `git diff --check`.
2. Replace [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md) with the current state.
3. Update [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md), [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md), and [PROMPT_INDEX.md](PROMPT_INDEX.md).
4. Create exactly one immutable archive record in [docs/history/prompts](docs/history/prompts) with the required metadata.
5. Commit only scoped changes, push one dedicated branch, and open exactly one reviewable pull request.
6. Leave the repository working tree clean apart from unrelated user-owned files that were explicitly preserved.

The archive is never edited after creation. Any correction is a later prompt with its own archive.
