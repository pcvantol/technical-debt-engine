# Dependency Health capability

`dependency_health` `1.0.0` is deliberately limited to dependency ecosystems
actually used by the DJConnect platform. It normalizes existing package metadata
and stable package-manager output; it neither creates an SBOM nor performs
package management.

Canonical adapter evidence records each ecosystem, package manager, direct,
transitive, unknown, and outdated dependency lists, plus analyzer identity and
version. Ecosystem metrics explicitly count direct, transitive, unknown, and
outdated dependencies. If a native analyzer or registry-backed result is
unavailable, that fact is explicit `UNAVAILABLE` evidence rather than inferred
data.

The capability supports pip, npm, NuGet, SwiftPM, and PlatformIO only because
the current DJConnect platform inventory requires them. Generic policies may
threshold unknown and outdated dependency counts. The capability participates
in normal baseline, differential, and qualification flows with no special rule.
It is optional in the standard profile, so a repository without a supported
manifest remains valid.

SBOM generation, licenses, CVE data, dependency updates, automatic fixes,
publishing, and lockfile rewriting are out of scope for 1.0.
