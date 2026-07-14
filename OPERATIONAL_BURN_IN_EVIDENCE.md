# Operational Burn-In Evidence

The committed [burn-in evidence](burn-in/evidence.json) records three runs each for TDE, an empty repository, and a small multi-language repository using the installed Internal Release wheel. Normalized evidence hashes are identical per case after excluding documented nondeterministic fields: execution ID, runtime-qualification ID, timestamps, and integrity envelope.

The run records startup/execution durations, maximum RSS, temporary-directory lifecycle and observed orphan-process state. No orphan processes were observed.
