# Engineering guidelines

- Favor explicit, versioned, machine-readable contracts.
- Keep language adapters isolated from the canonical model and consumers.
- Treat evidence as immutable and qualification as deterministic.
- Fail closed when configuration, evidence, policy, or compatibility is ambiguous.
- Use least privilege and do not add broad credentials or hidden integration paths.
- Keep documentation canonical: update the designated architecture, roadmap, or schema document rather than creating a duplicate.
- Add runtime only through a separately approved implementation scope.
- Follow [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md): one canonical prompt is one small engineering increment and terminates with exactly one independently reviewable pull request.
- Treat merge as a separate, explicit engineering decision; do not merge a canonical prompt's pull request automatically.
- Use [CANONICAL_PROMPT_TEMPLATE.md](CANONICAL_PROMPT_TEMPLATE.md) for every future canonical prompt, including its status, summary, and index updates.
