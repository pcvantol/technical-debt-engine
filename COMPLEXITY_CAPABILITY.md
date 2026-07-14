# Complexity capability

`tde assess --capability complexity <repository>` executes Python cyclomatic-complexity analysis through the public CLI, Runtime, Execution Engine, registry-backed `complexity.radon` adapter, Radon, normalization, validation, Policy Engine, Runtime Qualification and immutable Evidence Store.

The canonical Generation 1 analyzer is [Radon](https://radon.readthedocs.io/) `6.0+`, installed separately and available on `PATH`. The adapter validates its version, invokes `radon cc --json <repository>` with an argument array and timeout, and preserves native JSON plus a SHA-256 hash in adapter evidence.

For supported Python symbols, canonical evidence contains cyclomatic repository, language, file and symbol measurements: average, maximum and four-band distribution. High (`>=11`), very high (`>=21`) and critical (`>=41`) symbols emit deterministic findings that bind the measured value, threshold, affected entity and measurement evidence reference. A repository without supported symbols has an explicit `complexity.missing` finding and limitation rather than fabricated measurements.

Generation 1 supports Python only. Radon availability/version, Python-only coverage, configured exclusions and no-symbol outcomes are structured limitations. The current evidence is qualified on the macOS audit host; cross-platform and non-Python analyzer qualification remain deferred.
