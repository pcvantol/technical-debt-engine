# TDE bootstrap

This is the local entrypoint. First use the generated projection in
`docs/ai-development/`, then read `TDE_DEVELOPMENT_EXTENSION.md` beside it.
The projection supplies the generic development contract; this repository
supplies the product-specific TDE context.

For TDE orientation, read `ENGINEERING_STATUS.md`, `REPOSITORY_STATUS.md`,
`MANAGEMENT_SUMMARY.md`, `ROADMAP_INDEX.md`, `PROMPT_INDEX.md`, the applicable
architecture/ADR/capability documentation, and the local extension. Consult
`docs/history/prompts/` only for historical context. TDE's current-state and
freeze vocabulary is defined by the local extension and `PROMPT_LIFECYCLE.md`.

Validate the committed projection offline:

```sh
python3 docs/ai-development/validate_projection.py \
  --profile tde \
  --source-commit ec070e399ff4dbd92e760370002995fe4f4d52d6 \
  --extension-identity TDE_DEVELOPMENT_EXTENSION
```
