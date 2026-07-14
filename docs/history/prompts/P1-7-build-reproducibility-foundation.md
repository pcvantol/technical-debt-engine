# P1-7 — Build Reproducibility Foundation

| Field | Record |
| --- | --- |
| Prompt ID | `P1-7` |
| Title | Build Reproducibility Foundation |
| Branch | `codex/p1-7-build-reproducibility-foundation` |
| Candidate commit SHA | `5a99556e63de51cca29da6face552e018084a7cf` |
| Pull request | [#54](https://github.com/pcvantol/technical-debt-engine/pull/54) |
| Decision | `BUILD_REPRODUCIBILITY_FOUNDATION_PARTIALLY_OPERATIONAL` |
| Created | 2026-07-14 |
| Freeze reached | Yes — immediately when PR #54 became reviewable. |
| Prompt completed | Yes — engineering stopped at the reviewable pull request. |

## Validation summary

- `PYTHONPATH=src python -m unittest discover -s tests -v`: 71 tests passed.
- `git diff --check` passed.
- Two independent clean builds of candidate `5a99556` produced byte-identical
  wheel and source-distribution artifacts.
- SHA-256 checksums: wheel
  `96705bed1c27e20ecd0479f61c357917117a4e6a95dcbe27db3a52731403a141`;
  source distribution
  `469501fdce682cb24b455e752ec8c96e518dae9f63ec87e5c3c47a0ea7ae8b84`.
- Isolated installation of both artifacts invoked only the installed `tde`
  entrypoint and verified CLI, Runtime, Code Size, Complexity, Policy,
  baseline, comparison, Query, and report.

## Created artifacts

- `requirements/build-tools.txt` — exact, SHA-256-hash-locked build tools.
- `tools/package_build.py` — canonical wheel/sdist build, metadata
  normalization, checksums, identity and provenance.
- `tools/verify_installed_package.py` — isolated installed-package dogfood
  qualification.
- `.github/workflows/package-build.yml` — least-privilege, immutable-action
  pull-request/manual workflow with evidence upload only.
- `PACKAGING.md` — canonical dependency, build, provenance, and qualification
  policy.

## Updated artifacts

- `pyproject.toml`, `README.md`, `ENGINEERING_STATUS.md`,
  `REPOSITORY_STATUS.md`, `MANAGEMENT_SUMMARY.md`, and `PROMPT_INDEX.md`.

## Known limitations

- GitHub-hosted workflow run `29367776918` failed before its second build:
  setuptools rewrote a tracked egg-info manifest, and the clean-candidate
  guard then correctly blocked the second build.
- No release, publication, release qualification, or release certification is
  created by this increment.

## Deferred work

| Description | Reason | Priority | Recommended prompt |
| --- | --- | --- | --- |
| Repair hosted two-build source-tree isolation. | The first hosted setuptools build mutates a tracked egg-info manifest, blocking the second clean candidate build. | `P1` | Build reproducibility workflow repair |

## Recommended next prompt

Repair hosted two-build source-tree isolation after review and merge of PR #54.
