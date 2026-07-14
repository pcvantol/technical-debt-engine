# Platform Release Architecture

The Release Runtime is the evidence-based orchestration boundary for releasing TDE itself. It plans immutable candidates, artifacts, packages, versions, and release evidence; it never builds software or publishes artifacts.

Canonical flow: repository → build → package → release candidate → qualification → evidence → Release Runtime → GitHub Actions → publication → operational evidence. GitHub Actions is the future execution engine. This increment creates no workflow, package, release, or version.
