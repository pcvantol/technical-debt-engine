# Product backlog

## Active — required for 1.0

| Item | Concrete DJConnect value / intended consumer | Acceptance evidence | Explicit non-goals |
| --- | --- | --- | --- |
| G2-C Basic security | A selected pilot receives one useful normalized security decision beyond existing native checks. | Native-tooling gap analysis; canonical evidence; policy and pilot proof. | Security-platform replacement, broad scanning, duplicate GitHub-native checks. |
| G2-D CI integration and production pilot | Selected DJConnect pipelines run pinned TDE and retain evidence. | Immutable version/artifact; evidence artifacts; observe/warn/soft-fail history; required-check proof only where stable. | Consumer-side analyzer/policy duplication; unpinned checkout integration. |
| G2-E 1.0 qualification and release | DJConnect can trust one certified release across chosen distribution paths. | Green artifact and consumer qualification; known limitations; one `1.0.0` publication bundle. | Per-capability public releases; release-engineering expansion without a proven gap. |

## Completed in Generation 2

| Item | Concrete DJConnect value / validated consumers | Acceptance evidence | Explicit non-goals |
| --- | --- | --- | --- |
| G2-A Coverage completion | Existing CI coverage artifacts from `djconnect`, `djconnect-pi`, `djconnect-website`, and `djconnect-esp32` become reliable canonical evidence without test execution by TDE. | Public CLI parser, policy, baseline/differential, runtime and repository-qualification proof; fresh post-merge branch-coverage and real CI artifact validation. | Test execution, coverage generation, test-health analysis, consumer-CI integration. |
| G2-B Minimal dependency health | Every active DJConnect repository receives a package-manager-native outdated-dependency assessment for its actual ecosystem. | Platform inventory; bounded support statement; canonical evidence, policy, differential, qualification, and public-CLI proof. | General supply-chain suite, ecosystems absent from DJConnect, broad SBOM program. |

## Conditional — only if the pilot proves necessary

- Simple CI usability improvement.
- Limited cache.
- One additional language adapter.
- One additional policy operator.
- Limited waiver capability.

Each requires the same DJConnect value, consumer, acceptance-evidence, and
non-goal record before activation.

## Post-1.0 options

These are deferred, not removed. Concrete DJConnect practice determines future
activation and priority:

- Duplicate code; documentation health; generic architecture rules;
  bounded-context analysis; layering and module-ownership governance.
- Extended exception and waiver workflows; organization-wide policy inheritance.
- Dashboards, hosted API, cloud service, and Marketplace positioning.
- AI remediation adviser; general SARIF aggregation; test-health and flaky-test
  analysis; repository-health or marketing composite scores.
- Broad language/ecosystem coverage outside the selected pilot; performance
  work without a demonstrated bottleneck; parallel execution, caching, and
  incremental analysis without operational evidence.
- Any release-per-capability practice.
