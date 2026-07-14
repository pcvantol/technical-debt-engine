# Complexity qualification

Default qualification is observational PASS for valid analyzer evidence. Findings at cyclomatic complexity 21+ are HIGH and 41+ CRITICAL, but no hardcoded blocking policy is introduced. Explicit warning/blocking thresholds, baselines, comparisons, and trends are reserved for policy configuration.

## Cross-platform qualification

`complexity.radon` is qualified through the installed TDE wheel, never through
`PYTHONPATH` source execution. The canonical workflow installs `radon==6.0.1`
in a fresh virtual environment, records the exact version and wheel checksum,
and compares a projection of repository, language, file, symbol, finding and
Runtime Qualification evidence across Ubuntu, macOS and Windows on Python 3.11
and 3.13. Execution IDs, timestamps, durations and raw native output are
excluded from that comparison; no analytical fields are excluded.

The workflow also proves missing-Radon fail-closed behavior, persisted-evidence
integrity and tamper detection. A blocking policy result from the canonical
fixture or TDE dogfood run is an assessment result, not an analyzer failure.
