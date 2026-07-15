# Release Runtime

Release Runtime input is an immutable certified repository candidate, declared
release profile, semantic version plan, qualification evidence, and artifact
plan. Output is an immutable release manifest and
candidate/package/release/publication evidence records.

It validates plan completeness and hands executable work to GitHub Actions. It does not invoke build tools, package managers, registries, Docker, or GitHub publication APIs.

Publication uses the certified candidate rather than automatically using the
later `main` commit. Intervening commits must be classified as administrative
under [RELEASE_PUBLICATION.md](RELEASE_PUBLICATION.md); a non-administrative
commit requires a new candidate.
