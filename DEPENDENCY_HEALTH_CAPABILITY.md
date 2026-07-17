# Dependency Health capability

`dependency_health` `1.0.0` is deliberately limited to the selected
DJConnect API consumer: npm projects with a committed `package-lock.json`.
It normalizes existing package metadata and stable npm CLI output; it neither
creates an SBOM nor performs package management.

Canonical adapter evidence records the ecosystem (`npm`), package manager,
direct, transitive, unknown, and outdated dependency lists, plus npm analyzer
identity/version. Repository metrics explicitly count direct, transitive,
unknown, and outdated dependencies. If an npm project, npm executable, or
registry-backed outdated result is unavailable, that fact is explicit
`UNAVAILABLE` evidence rather than inferred data.

Generic policies may threshold unknown and outdated dependency counts. The
capability participates in normal baseline, differential, and qualification
flows with no special rule. It is optional in the standard profile, so a
repository without the supported npm/lockfile shape remains valid.

Python, NuGet, SBOM generation, licenses, CVE data, dependency updates,
automatic fixes, publishing, and lockfile rewriting are out of scope for 1.0.
