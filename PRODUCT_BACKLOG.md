# Product backlog

## Active — maintenance-first

| Item | Concrete DJConnect value / intended consumer | Acceptance evidence | Explicit non-goals |
| --- | --- | --- | --- |
| Apple coverage improvement | Improve the separately reported Apple product coverage baseline from 38.37% through targeted UI and widget tests when the Apple team schedules the work. | A selected Apple test scope produces a reviewed canonical coverage artifact without changing TDE policy or thresholds. | TDE runtime/capability changes; coverage-threshold changes; treating the current 38.37% baseline as an integration failure. |
| TDE 1.1 complexity policy parity | Establish canonical primary-product-language complexity evidence for the seven selected DJConnect source consumers using one capability, policy and qualification route. | Public 1.1 runtime, adapter qualification, and seven reviewable Observe-only consumer PRs with provenance-rich primary-language complexity evidence. | Policy forks, threshold increases, consumer-local analyzers, automatic product refactoring, merge blocking, security/SBOM/dashboard work. |

## Completed in Generation 2

| Item | Concrete DJConnect value / validated consumers | Acceptance evidence | Explicit non-goals |
| --- | --- | --- | --- |
| G2-A Coverage completion | Existing CI coverage artifacts from `djconnect`, `djconnect-pi`, `djconnect-website`, and `djconnect-esp32` become reliable canonical evidence without test execution by TDE. | Public CLI parser, policy, baseline/differential, runtime and repository-qualification proof; fresh post-merge branch-coverage and real CI artifact validation. | Test execution, coverage generation, test-health analysis, consumer-CI integration. |
| G2-B Minimal dependency health | Every active DJConnect repository receives a package-manager-native outdated-dependency assessment for its actual ecosystem. | Platform inventory; bounded support statement; canonical evidence, policy, differential, qualification, and public-CLI proof. | General supply-chain suite, ecosystems absent from DJConnect, broad SBOM program. |
| G2-C Security gap assessment | The eight active DJConnect repositories have an evidence-based security architecture decision before TDE scope expands. | [Security Gap Assessment](SECURITY_GAP_ASSESSMENT.md): native controls inventoried; no selected-pilot decision requires TDE security evidence; no 1.0 capability approved. | New analyzer, runtime/schema/policy changes, dependency or security scanning, SBOM, dashboards, and release-engineering changes. |
| G2-D DJConnect consumer integration | The public, exactly pinned `1.0.5` CLI runs in Observe mode on `main` for all seven selected source consumers: `djconnect`, `djconnect-pi`, `djconnect-api`, `djconnect-app`, `djconnect-esp32`, `djconnect-website`, and `djconnect-windows`. | Every consumer executes `code_size`, `complexity`, `coverage`, and `dependency_health`, publishes `tde-observe-evidence`, and has a green post-merge `main` run. Canonical coverage is recorded for all seven: 88.63%, 75.78%, 89.14%, 38.37%, 88.83%, 96.59%, and 86.49% respectively. | Required checks, merge blocks, soft-fails, local source checkout, internal imports, or consumer-side analyzer/policy duplication. |
| G2-E 1.0 qualification and release | DJConnect consumes the qualified public `1.0.5` release through the public CLI. | `1.0.5` is the latest published release; all selected consumers run the exact public distribution and retain qualification evidence. | Release-per-capability practice or release-engineering expansion without a demonstrated gap. |

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
- Security-evidence normalization, Dependency Review evidence, container
  vulnerability evidence, licence evidence, and native code-scanning expansion
  without a selected DJConnect consumer and demonstrated missing decision.
