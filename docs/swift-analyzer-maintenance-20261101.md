# Swift analyzer maintenance

Objective: repair the real Swift declaration-boundary conflict demonstrated by
DJConnect App main `73d114a919f090d53bcc0aa464433638995c7d2a`, without changing
consumer source, excluding symbols or relaxing duplicate-evidence validation.
The original TDE 1.1.1/Lizard 1.23.0 diagnostic reports
`complexity.symbol.duplicate`, causing validation and persistence to fail closed.

Qualify the published Lizard 1.24.3 parser and prepare a new TDE maintenance
candidate. Keep public schemas, policy thresholds, required capabilities and
immutable original evidence unchanged. Source readiness, package publication
and consumer adoption are separate outcomes.


## Qualified scope

- Pin Lizard 1.24.3, whose upstream Swift fixes distinguish `.init`, `self.init`
  and initializer references from declarations. Keep the generic CSV adapter
  and its conflicting-symbol rejection unchanged.
- Enforce the full `(1, 24, 3)` minimum using patch-aware executable discovery;
  retain two-component minimum compatibility for other analyzers.
- Prepare runtime/CLI/package version 1.1.2. Add that runtime to the existing
  policy's compatibility list; all rule IDs, thresholds and profile selections
  remain unchanged. This is not an evidence-policy waiver.
- Upstream references: https://github.com/terryyin/lizard/releases/tag/1.24.2
  and https://github.com/terryyin/lizard/releases/tag/1.24.3 .

## Validation

The two real-analyzer regressions assert actual function line ranges and CCN,
including the method after delegated initialization. Both fail with 1.23.0 and
pass with 1.24.3. The 162-test suite succeeds with one existing opt-in Docker
integration test skipped. The first full local attempt lacked cloc; its log is
retained, and the final run uses the original hash-pinned cloc 2.10 executable.

On an unchanged checkout of Apple main 73d114a, the public candidate CLI consumes
the original main xccov JSON. Both `assess` and `qualify` exit 2 and persist
canonical evidence: all four capabilities are VALID; runtime is QUALIFIED;
assessment is FAIL and repository qualification FAILED. There are 354 findings,
including seven policy-blocking critical product findings. Source lines 95,401
exceed the existing 75,000 threshold and product CCN maximum 62 exceeds 30.
The existing installed-wheel complexity matrix now runs the four Swift/discovery
regressions on each Linux/macOS/Windows and Python 3.11/3.13 target, after
resolving the exact same wheel's declared dependencies. Its missing-analyzer
negative case remains unchanged.

These are consumer debt findings, not analyzer-invalid evidence. No finding was
removed, threshold changed or original evidence overwritten.

This isolated candidate test does not establish published-package adoption,
Windows/Linux execution, Docker acceptance or an operational consumer fix.
The Apple workflow remains pinned to the published 1.1.1 until a certified
maintenance release is separately approved and published.
