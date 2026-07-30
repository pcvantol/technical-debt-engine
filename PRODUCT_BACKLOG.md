# Product backlog

TDE is an operational engineering platform. This backlog contains only active
platform work. Routine product-quality findings, such as Apple UI coverage,
are owned and scheduled by their consumer repository; they are not TDE backlog
items.

## Operational Maintenance

No active items. Qualify bug fixes and public-runtime servicing against a
demonstrated consumer or operational need.

## Platform Compatibility

No active items. Compatibility work covers supported toolchains, package
managers, platforms, and public-contract consumers when evidence shows a
concrete breakage or pending incompatibility.

## Analyzer Maintenance

No active items. Analyzer version, parser, and evidence-normalization updates
require compatibility evidence and unchanged public-contract semantics unless
an approved architecture decision says otherwise.

## Documentation

No active items. Documentation and governance updates are maintained whenever
they are needed to keep canonical operational truth accurate.

## Future Capability Candidates

No candidate is approved for implementation. A candidate begins only with an
approved architectural assessment proving that the existing capability model
cannot support a required engineering decision.

Deferred examples include security-evidence normalization, duplicate code,
documentation health, test-health analysis, waiver workflows, dashboards,
hosted services, additional ecosystems, and AI remediation. They are not
commitments and must not be activated through routine consumer findings.

## Completed milestones

| Item | Completion record |
| --- | --- |
| Generation 2 coverage completion | Canonical CI coverage artifacts are assessed through the public CLI without test execution by TDE. |
| Generation 2 dependency health | All selected consumers have package-manager-native evidence; their latest qualified `main` evidence reports zero outdated dependencies. |
| Generation 2 security gap assessment | The evidence-based decision retained GitHub-native and repository-native controls as the security decision owners. |
| Generation 2 consumer integration | Seven selected DJConnect source consumers use exactly pinned public-runtime Observe workflows and publish `tde-observe-evidence`. |
| Generation 2 qualification and release | Public runtime and selected-consumer qualification evidence are retained. |
| TDE 1.1 complexity policy parity | Cross-language primary-product complexity evidence is canonical and qualified for all seven consumers. |
