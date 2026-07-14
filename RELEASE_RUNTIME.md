# Release Runtime

Release Runtime input is a repository candidate, declared release profile, semantic version plan, qualification evidence, and artifact plan. Output is an immutable release manifest and candidate/package/release/publication evidence records.

It validates plan completeness and hands executable work to GitHub Actions. It does not invoke build tools, package managers, registries, Docker, or GitHub publication APIs.
