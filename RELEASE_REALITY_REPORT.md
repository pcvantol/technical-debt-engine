# Release Reality Report

## Classification

**INTERNAL_RELEASE_0_1_0_NOT_EXECUTED**

`pyproject.toml` and CLI constants use version `0.1.0`. Local wheels exist under `internal-release-artifacts/` and `dry-run-artifacts/`, and a fresh audit wheel was buildable. These facts do not establish a release.

| Check | Result |
| --- | --- |
| Git tag | None (`git tag -l`) |
| GitHub Release | None (`gh release list --limit 20`) |
| Published wheel/source distribution/binary | None proven |
| Approved release workflow | None; `.github/workflows` is absent |
| Immutable action references/provenance | Absent |
| Source archive/evidence bundle | Absent |
| Checksums | Local file checksums exist, but artifacts differ and are not release-bound |
| Isolated local install | Validated for a locally built wheel only |
| Dogfooding released artifact | Not possible |

`tde assure` and `tde trusted-delivery` exit 2, correctly identifying missing workflow, provenance and release-artifact evidence (and the audit workstation's untracked `.DS_Store` files). The local-worktree condition is environmental evidence, not proof about the committed source tree.
