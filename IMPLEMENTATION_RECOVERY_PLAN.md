# Implementation Recovery Plan

This plan starts from current `main`, preserves the frozen Generation 1 contracts and makes one focused, reviewable PR per item. It is a recovery proposal, not implementation authorization.

1. **P0 — Make the public CLI execute one configured capability.** Trace CLI configuration into the Execution Engine, prove `tde assess --capability code-size` executes `cloc`, and fail closed when it cannot. Add an installed-CLI integration test.
2. **P0 — Make evidence and Runtime Qualification truthful.** Validate actual stage outputs, make missing required/selected capability evidence blocked, and report actual planned/executed capabilities and adapters.
3. **P1 — Establish the minimal usable vertical slice.** Ship Code Size's normalized metrics, classification and stable exits through the CLI; state `cloc` provisioning/version requirements explicitly.
4. **P1 — Add Complexity only with a packaged/an explicit analyzer dependency.** Prove Python/Radon behavior from an isolated environment before claiming it as a CLI capability.
5. **P1 — Make policy operate on the real CLI evidence.** Test threshold blocking and decision-to-exit-code mapping using the installed CLI.
6. **P1 — Make baseline and comparison operate on actual Code Size evidence.** Preserve compatibility and immutable baseline semantics; use controlled fixture revisions.
7. **P2 — Close persistence/query integration.** Query stored records read-only, then layer trends on persisted compatible evidence. Defer remote/cloud storage.
8. **P2 — Establish repeatable packaging.** Define dependencies, one version source, wheel and source-distribution verification, then provenance/reproducibility and pinned CI workflow.
9. **P1 — Internal release decision.** Only after the preceding slice, create a human-approved internal release artifact and evidence. Do not publish under this plan.
10. **P2 — DJConnect integration.** It is safe to begin only after a released/pinned CLI executes the Code Size flow with stable evidence schema and exit codes; select the consumer repository explicitly first.

Defer reporting renderer, broader dependency ecosystems, distributed execution, cloud storage, IDE work and Innovation Lab work until the minimal public CLI flow is proven.
