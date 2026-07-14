# Release Certification Gap Analysis

| Gap | Certification consequence | Required resolution |
| --- | --- | --- |
| GitHub Actions workflow is absent | No immutable, least-privilege reproducible execution | Implement and validate pinned workflow contracts |
| Dependency lock/provenance absent | Dependency graph is not reproducibly attributable | Establish lock/provenance process |
| Release artifacts and checksums absent | Artifact identity cannot be verified | Implement artifact build and manifest checksum execution |
| `PLATFORM_NOT_CERTIFIED` | Underlying canonical foundation is not trusted | Resolve platform certification gaps and recertify |
| Reporting absent | Release evidence cannot be projected end-to-end | Implement query-driven reporting |
