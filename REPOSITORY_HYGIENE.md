# Repository Hygiene

## Policy

Every engineering increment must finish with a clean repository. Operating-system artifacts, editor state, caches, logs, and disposable build output are not repository evidence and must not remain tracked or untracked. The canonical ignore policy is [`.gitignore`](.gitignore).

This policy does not authorize removal of generated engineering evidence, release evidence, or intentionally version-controlled fixtures. Cleanup is limited to artifacts that are demonstrably outside those categories.

## Required completion checks

Before a prompt is declared reviewable:

1. Run `git ls-files | rg '(^|/)\\.DS_Store$|(^|/)\\._[^/]+$'` and confirm that it returns no tracked operating-system artifacts.
2. Run `git status --short` and confirm that it returns no untracked operating-system artifacts.
3. Run `git diff --check` and confirm that it passes.
4. Leave `git status` clean.

If an artifact cannot be safely classified, record it as Deferred Work instead of removing it.
