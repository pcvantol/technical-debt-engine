# Code Size qualification

The default policy is observational: valid, complete Code Size execution passes without size thresholds. Capability-specific threshold findings and warning/fail policy are deferred; existing repository size never fails by default. Analyzer unavailable, malformed output, invalid evidence, unsupported `cloc`, or analyzer timeout blocks the capability.

## Cross-platform installed-wheel qualification

The canonical [Code Size workflow](.github/workflows/code-size-cross-platform-qualification.yml) builds one wheel and installs it into isolated Ubuntu, macOS and Windows environments for Python 3.11 and 3.13. It provisions `cloc 2.10` from the official v2.10 release: the Unix Perl script on Ubuntu/macOS and the Windows executable on Windows. Each artifact is SHA-256 verified before it is put on `PATH`; Runtime still only discovers the executable on `PATH`.

Every matrix record captures Python, TDE, schema, capability, adapter and `cloc` versions, then verifies assessment, canonical evidence, automatic persistence, integrity-verified retrieval, persisted-only Query/report, tamper detection, missing/unsupported/timeout fail-closed behavior, and an installed-wheel dogfood assessment of TDE. The comparison excludes only raw native output/hashes and execution-envelope metadata, which vary with runner path and time. Repository, language and file metrics, classifications, findings, and Runtime Qualification must be equivalent.
