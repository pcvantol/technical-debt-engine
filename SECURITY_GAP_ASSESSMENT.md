# Security Gap Assessment

## Decision

**No Security capability is included in TDE 1.0.** The minimum 1.0 scope is
to retain the existing GitHub-native and repository-native security controls as
the decision owners. TDE must not build an analyzer, a scanner, a policy, a
schema, or a normalizer for security evidence in 1.0.

This is an evidence-based scope reduction, not a claim that the repositories
have no security risk. The active DJConnect set already has native controls for
the risks this assessment could verify. The selected G2-D pilot does not yet
exist, so no concrete pipeline has demonstrated that it needs a cross-tool TDE
security decision. A normalizer without that consumer and decision would not
satisfy the Generation 2 investment test.

## Scope and method

The assessment covers the eight active DJConnect repositories in the completed
[Dependency Health inventory](docs/djconnect-dependency-health-inventory.md).
It is a configuration inventory, not an alert audit, vulnerability assessment,
or security certification.

On 2026-07-19, each default branch was inspected through the GitHub repository
and Actions APIs for repository security settings, enabled workflows, and
workflow source. The following were searched in tracked configuration and
workflow source: CodeQL, Dependabot, secret scanning, Dependency Review,
Semgrep, Gitleaks, Bandit, Ruff, package-manager vulnerability commands,
container scanners, and licence scanners. “Not found” below means no matching
tracked configuration or workflow command was found at that revision. It does
not make a statement about GitHub organization settings or uninspected external
systems.

The token used for this inventory cannot read Code Scanning, Dependabot, or
Secret Scanning alert endpoints. Consequently, this document records neither
alert counts nor alert state; it records only evidence that was accessible and
reproducible from the repositories and GitHub repository settings.

## Current security architecture

GitHub-native repository settings provide Secret Scanning and push protection
for all eight repositories. Dependabot security updates are enabled for six
repositories and disabled for `djconnect-windows` and `djconnect-firmware`.
Every repository has at least one active GitHub Actions workflow; all except
`djconnect-firmware` configure CodeQL. Seven repositories configure Semgrep;
the workflow is explicitly non-blocking where that configuration is visible.

The controls remain separate native decisions: GitHub security alerts, pull
request workflow results, and repository-specific quality or release checks.
No checked configuration exports a common security artifact for TDE, and TDE
currently has no selected consuming pipeline. That separation is compatible
with the Generation 2 boundary that TDE does not replace specialist security
platforms.

## Repository inventory

| Repository (main revision) | GitHub Actions and CodeQL | Dependabot / secrets | Linting and other observed security tooling | Package-manager security and notable absences |
| --- | --- | --- | --- | --- |
| `djconnect` (`06306ee72d68`) | Active `CodeQL` for Python on push, pull request, and a weekly schedule. Active Semgrep pull-request workflow uses `.semgrep/djconnect-security.yml`, with `continue-on-error: true`. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | Shared Python CI runs Ruff and Bandit (medium severity); both are configurable. | CI reports pip package freshness via `pip list --outdated`; no `pip-audit`/Safety, Dependency Review, container, or licence scanner found. |
| `djconnect-pi` (`55a2f343a6cc`) | Active Python CodeQL on push, pull request, and weekly schedule. Active Semgrep pull-request workflow uses `semgrep scan --config auto` and is non-blocking. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | Shared Python CI is invoked with Ruff and Bandit both non-blocking; a fixture-redaction check is present. | Native pip freshness report is inherited; no `pip-audit`/Safety, Dependency Review, container, or licence scanner found. |
| `djconnect-api` (`384c452068f9`) | Active JavaScript/TypeScript CodeQL on `main` push/PR and weekly schedule. Active Semgrep PR workflow invokes the shared non-blocking Semgrep workflow. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | CI typechecks and has a failing secret-pattern scan using `rg`. | `npm run deps:report` is a freshness report; no `npm audit`, Dependency Review, container, or licence scanner found. |
| `djconnect-website` (`bfca254f1a5c`) | Active JavaScript/TypeScript CodeQL on push, pull request, and weekly schedule. Active Semgrep PR workflow invokes the shared non-blocking workflow. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | Validation runs repository package/tool checks. | `npm run deps:check` is configured; no `npm audit`, Dependency Review, container, or licence scanner found. |
| `djconnect-windows` (`b1947ca3f795`) | Active C# CodeQL on push, pull request, and weekly schedule (`build-mode: none`). Active Semgrep PR workflow invokes the shared non-blocking workflow. | Dependabot security updates disabled; Secret Scanning and push protection enabled. | CI validates fixture security/log redaction. | CI reports outdated direct/transitive NuGet packages; no vulnerable-package command, Dependency Review, container, or licence scanner found. |
| `djconnect-app` (`27ac510c1f69`) | Active firmware CodeQL conditionally analyses tracked C/C++ source on `main` push, PR, and weekly schedule. `Firmware security scan` invokes the shared non-blocking Semgrep workflow. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | CI validates HA contract fixtures; firmware CI validates firmware metadata checksums. | SwiftPM manifest has no external dependencies in the Dependency Health baseline; no Dependency Review, Swift vulnerability, container, or licence scanner found. |
| `djconnect-esp32` (`42fe290b9abf`) | Active C/C++ CodeQL on `main` push, PR, and weekly schedule; it builds PlatformIO before analysis. | Dependabot security updates enabled; Secret Scanning and push protection enabled. | Active Gitleaks runs on push, PR, dispatch, and weekly schedule. CI validates contract-log redaction. | CI creates PlatformIO dependency reports; no PlatformIO vulnerability scanner, Dependency Review, container, or licence scanner found. |
| `djconnect-firmware` (`e7144d35e6cf`) | No CodeQL or Semgrep workflow found. Active workflows are delivery/governance oriented. | Dependabot security updates disabled; Secret Scanning and push protection enabled. | No tracked linting or security scanner found. | The Dependency Health baseline records no supported dependency manifest; no Dependency Review, package vulnerability, container, or licence scanner found. |

All eight repositories expose GitHub’s dynamic `Dependency Graph` workflow.
No tracked `.github/dependabot.yml` was found in this inventory; the settings
above are GitHub repository settings, not a claimed Dependabot version-update
configuration.

## Capability matrix

| Security subject | Existing tool / factual coverage | Pipeline decision already possible | Missing canonical evidence | Potential TDE value | Decision |
| --- | --- | --- | --- | --- | --- |
| Dependency vulnerabilities | GitHub Dependabot security updates are enabled in six repositories; no vulnerability-audit workflow was found. | For enabled repositories, GitHub can present and update Dependabot security alerts; this assessment cannot read their state. | A readable, immutable alert result bound to the assessed commit. | Would only normalize GitHub alert evidence. No selected TDE consumer demonstrates a need. | Leave to GitHub; do not add to 1.0. |
| Committed secrets | GitHub Secret Scanning and push protection are enabled in all eight; `djconnect-esp32` also runs Gitleaks; API has a pattern scan. | GitHub push protection/scanning and the configured workflow checks can reject or alert on secret findings. | A common artifact for the native outcomes. | Duplicates native detection; a normalizer would have no proven consumer decision. | Leave to existing tooling. |
| Insecure code | CodeQL is configured in seven repositories for their observed Python, JS/TS, C#, or C/C++ sources; Semgrep is configured in seven and is non-blocking where visible; Python also uses Bandit. | CodeQL and blocking native jobs can report or gate code findings; Semgrep is observational. | A uniform result that represents native alert status and workflow outcome. | Normalization only; no missing pipeline decision is evidenced. | Leave to existing tooling. |
| Outdated packages | G2-B Dependency Health supplies qualified package-manager-native outdated evidence for all eight, with explicit unavailable states. | TDE already provides the bounded freshness decision. | None for the G2-B purpose. Vulnerability evidence is a different signal. | No additional security capability. | Already covered by G2-B; do not extend. |
| Dependency Review | No `actions/dependency-review-action` or equivalent workflow found. | None evidenced in the current configurations. | Pull-request dependency-diff advisory result. | Would require adopting/configuring a native GitHub control before TDE could normalize it. | Post-1.0 only if a selected pilot proves the missing PR decision. |
| Container security | No Trivy, Grype, Docker Scout, or equivalent scanner found. | None evidenced. | Image/SBOM vulnerability result. | Would require a scanner and an image-consuming pilot; that is a new security program. | Post-1.0. |
| Licence issues | No licence scanner found. Some repositories carry licence metadata or notices, which is not a scan. | None evidenced. | Dependency licence policy result. | Requires policy, scanner selection, and consumer decision. | Post-1.0. |

## Gap analysis

### Dependency vulnerabilities

1. **Uncaught risk:** this inventory cannot establish a uniform, commit-bound
   vulnerability result; two repositories also have Dependabot security updates
   disabled.
2. **Existing detection:** GitHub Dependabot security updates are configured in
   six repositories. G2-B deliberately measures outdatedness, not CVEs.
3. **Missing pipeline decision:** no selected DJConnect pipeline has shown that
   GitHub alert handling is insufficient or that a TDE gate is required.
4. **Normalization:** technically possible only after a readable native alert
   artifact is retained by a selected pipeline.
5. **Analyzer:** not justified; a new analyzer would duplicate GitHub or a
   specialist dependency-vulnerability service.
6. **TDE 1.0:** not necessary on repository evidence.
7. **Deferral:** safe to post-1.0; reconsider only with a selected pipeline and
   a documented missing decision.

### Secrets

1. **Uncaught risk:** no common TDE record proves the result of GitHub secret
   scanning or the repository-specific Gitleaks/pattern scans.
2. **Existing detection:** GitHub Secret Scanning and push protection cover all
   eight; ESP32 adds Gitleaks and API adds a pattern scan.
3. **Missing pipeline decision:** none: the existing controls already own
   reject/alert behaviour.
4. **Normalization:** possible in principle, but it would only duplicate the
   native outcome.
5. **Analyzer:** not justified; it would duplicate GitHub and Gitleaks.
6. **TDE 1.0:** not necessary.
7. **Deferral:** safely leave entirely to existing tooling unless a pilot needs
   an evidence-retention format that GitHub cannot provide.

### Insecure code

1. **Uncaught risk:** `djconnect-firmware` has no CodeQL/Semgrep workflow;
   other repositories do not share one blocking Semgrep policy.
2. **Existing detection:** CodeQL covers the observed languages in the other
   seven repositories; Semgrep covers seven; Bandit covers the Python shared
   path.
3. **Missing pipeline decision:** the gap is a native-control coverage choice,
   not an evidenced need for a cross-repository TDE decision.
4. **Normalization:** would only summarize native code-scan results.
5. **Analyzer:** not justified; it would recreate CodeQL/Semgrep/Bandit scope.
6. **TDE 1.0:** not necessary.
7. **Deferral:** safe. If `djconnect-firmware` becomes a selected pilot, first
   decide whether it needs a native scanner; only then assess retained native
   evidence.

### Dependency Review, container security, and licences

1. **Uncaught risk:** no native PR dependency-review result, image
   vulnerability result, or dependency-licence result is configured.
2. **Existing detection:** none was found for these topics.
3. **Missing pipeline decision:** none is documented for a selected pipeline.
4. **Normalization:** impossible today because no canonical native result is
   produced.
5. **Analyzer:** would require new scanner, policy, and evidence design,
   contrary to this assessment’s non-goals and the 1.0 boundary.
6. **TDE 1.0:** not necessary.
7. **Deferral:** post-1.0 candidates only after the investment test identifies
   a concrete DJConnect consumer and decision.

## Minimal 1.0 scope and architecture decisions

| Candidate | Architecture decision | Rationale |
| --- | --- | --- |
| Security evidence normalizer | **Do not include in 1.0.** | No G2-D pilot is selected and no missing pipeline decision is demonstrated. A normalizer would expand public contracts without value proof. |
| Security analyzer | **Do not include in 1.0.** | Native GitHub and specialist tools already detect the covered subjects; missing subjects have no proven consumer decision. |
| GitHub-native controls | **Leave to existing tooling.** | They remain the source and owner of secret, code, and Dependabot security outcomes. |
| Package freshness | **Keep G2-B only.** | Qualified outdated-dependency evidence already exists and must not be represented as vulnerability evidence. |
| Dependency Review | **Post-1.0 candidate.** | Activate only after a selected PR pipeline needs a dependency-diff advisory decision. |
| Container vulnerability evidence | **Post-1.0 candidate.** | Requires an image-producing selected pilot and specialist scanner evidence. |
| Licence evidence | **Post-1.0 candidate.** | Requires a concrete licence policy and affected consumer. |

The required G2-C acceptance outcome is therefore satisfied by the negative
architectural decision: **no minimal TDE Security capability exists for 1.0 on
current repository evidence.** The next security change, if any, must first
name the selected pipeline, the native evidence it retains, and the pipeline
decision that cannot already be made by its existing control.

## Post-1.0 candidates

- Normalizing a selected pilot’s immutable GitHub vulnerability-alert outcome,
  if the pilot proves a decision that GitHub’s native check cannot make.
- Enabling and retaining native Dependency Review evidence for a selected
  pull-request pipeline, then reassessing whether normalization has value.
- Container vulnerability evidence for a selected image-producing pipeline.
- Licence evidence for a consumer with an explicit licence policy.
- Native code-scanning coverage for `djconnect-firmware`, if that repository is
  selected and its owner demonstrates a concrete pipeline risk.

None of these are commitments, analyzers, policies, schemas, or implementation
work. They remain subject to the Generation 2 investment test in
[PLATFORM_STRATEGY.md](PLATFORM_STRATEGY.md).
