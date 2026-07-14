# Release Qualification Report — Generation 1 candidate

## Decision

**RELEASE_BLOCKED**

Candidate `tde-generation-1-f0baf98` is bound to `f0baf98c72ba2c3ed6e10f34f4c6670e32fe6469`, Runtime/CLI `0.1.0`, schema `1.0.0`, registered capability and adapter versions, and the default policy `1.0.0`. Its manifest is [candidate-generation-1.json](release/candidate-generation-1.json).

Objective validation passed: 41 tests, local schema fixtures, and `git diff --check`. Software Assurance and Trusted Delivery operate, but each returns `PASS_WITH_WARNINGS` on a clean candidate because no dependency lock/provenance, immutable GitHub Actions workflow, or release artifacts exist. Platform Certification remains `PLATFORM_NOT_CERTIFIED`.

No release, package, binary, or publication was created.
