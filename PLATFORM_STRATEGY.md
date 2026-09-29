# Platform strategy

## Operational mode

Generations 1 and 2 are complete. TDE `1.1.1` is the published public runtime.
The platform is maintained for repository-independent, evidence-first quality
assessment. Seven selected DJConnect consumers use the four public capabilities
in non-blocking Observe mode. There is no active delivery program or scheduled
public release.

## Investment test

Prioritise a proposed increment only when it identifies:

1. A concrete consumer or operational problem and the affected repository,
   pipeline, or public contract.
2. The engineering decision or evidence that is currently unavailable or
   incorrect.
3. Why existing TDE capabilities and other tooling do not resolve the problem.
4. The smallest change, acceptance evidence, compatibility impact, and known
   limitations.
5. Whether a maintenance release is needed and how its artifacts and consumers
   will be qualified.

Bug fixes, analyzer and dependency updates, compatibility work, and
documentation are normal maintenance when this test demonstrates a need.
Consumer quality findings remain with the consumer unless they expose a TDE
platform problem.

## Capability and release boundaries

New capabilities require an approved architectural assessment before they enter
the backlog. Implementation then follows a capability decision, qualification,
public runtime delivery, and consumer adoption. TDE remains public,
capability-driven, repository-independent, and Observe-only; consumer
integration adds no required checks, merge blocks, soft-fails, suppressions, or
repository-specific policy forks by default.

Merging an engineering increment does not trigger publication. A maintenance
release requires a demonstrated need, compatible public contracts, and
qualified immutable artifacts. Deferred product ideas in
[Product Backlog](PRODUCT_BACKLOG.md) are not scheduled commitments.

The completed Generation 2 program and its release decisions remain in
[TDE 1.0 Scope Lock](TDE_1_0_SCOPE_LOCK.md) as historical context.
