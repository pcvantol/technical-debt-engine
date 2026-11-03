# Repository status

| Field | Value |
| --- | --- |
| Generation | Generations 1 and 2 complete; operational maintenance. |
| Product relationship | DJConnect is the primary product and a qualified consumer; TDE provides repository-independent public engineering-quality contracts. |
| Release state | `1.1.1` is the current published public runtime. Maintenance candidate `1.1.2` is under source review; publication is not authorized by this source increment. |
| Runtime and contracts | Public CLI, Runtime Execution Engine, registry capabilities, canonical evidence, declarative policies, assessment profiles, stable schemas, qualification, baselines, differentials, and distribution remain existing foundations. |
| Capabilities | `code_size`, `complexity`, `coverage`, and `dependency_health`; TDE consumes existing coverage artifacts rather than running tests. |
| Consumer baseline | Seven selected consumers use non-blocking Observe mode. Apple main `73d114a` is BLOCKED on published 1.1.1; the 1.1.2 candidate produces valid four-capability evidence with a genuine policy FAIL. |
| Active scope | `M-SWIFT-20261101`: demonstrated Swift analyzer identity conflict; fixed upstream parser under qualification. No new capability. |
| Dependency-health baseline | Latest qualified `main` evidence reports zero outdated dependencies for all seven selected consumers. |
| Operating model | Maintain public contracts, analyzers, dependencies, compatibility, documentation, and qualification evidence as needed. |

Earlier release-candidate, audit, and planning material remains historical
evidence. Current operational and roadmap truth is in
[ENGINEERING_STATUS.md](ENGINEERING_STATUS.md), [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md),
and [PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md). The completed 1.0 program is
preserved in [TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md).
