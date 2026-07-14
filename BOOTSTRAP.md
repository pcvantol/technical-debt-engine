# Bootstrap

This is the mandatory entry point for every human or AI engineering session. Start here before interpreting repository work or making changes.

## Canonical reading order

1. [BOOTSTRAP.md](BOOTSTRAP.md)
2. [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md)
3. [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md)
4. [MANAGEMENT_SUMMARY.md](MANAGEMENT_SUMMARY.md)
5. [PROMPT_INDEX.md](PROMPT_INDEX.md)
6. Current engineering work: the active prompt, its recovery-plan position, and applicable canonical documents.
7. [ENGINEERING_METHOD.md](ENGINEERING_METHOD.md), [PROMPT_FINALIZATION.md](PROMPT_FINALIZATION.md), [REPOSITORY_HYGIENE.md](REPOSITORY_HYGIENE.md), [PLATFORM_VISION.md](PLATFORM_VISION.md), [PLATFORM_STRATEGY.md](PLATFORM_STRATEGY.md), [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md), and [CANONICAL_SOURCE_HIERARCHY.md](CANONICAL_SOURCE_HIERARCHY.md)
8. Applicable ADRs in [architecture/adr](architecture/adr), then relevant product architecture and capability documents.

Consult [docs/history/prompts](docs/history/prompts) only when historical context is required. The repository must remain self-describing: chat history is never required for engineering continuity. If sources conflict, use the canonical hierarchy; do not infer a replacement architecture. One prompt owns one objective, one increment, and one reviewable Pull Request. A draft Pull Request is not frozen; when it becomes reviewable, the Prompt Freeze Point is reached. Do not continue engineering or add implementation after that point; record any late discovery as Deferred Work for the next prompt. Confirm repository hygiene with `git status --short` before completion.
