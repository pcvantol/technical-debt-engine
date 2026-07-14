# Platform Evolution Backlog

## Completed / operational

Generation 1 has established the runtime, canonical evidence, four initial capabilities, policy, baseline/comparison/trend, query, store, execution, runtime qualification, release architecture, Software Assurance and Trusted Delivery.

## Priority gap closure

1. Complete Query Engine consumption of persisted Evidence Store records according to [Persistence Architecture](docs/product/PERSISTENCE_ARCHITECTURE.md).
2. Make Runtime Qualification fail closed for empty required capability evidence.
3. Complete report rendering exclusively from Query results.
4. Remove remaining legacy Runtime capability execution ownership.
5. Establish pinned workflow, dependency provenance, artifact reproducibility and cross-platform capability qualification before release progression.

## Planned platform evolution

Cloud Evidence Store, Remote Query API, distributed/parallel execution, package distribution, public release and IDE integration are additive only; they must preserve frozen Generation 1 contracts. Package and consumer targets follow [Deployment Strategy](docs/product/DEPLOYMENT_STRATEGY.md); persistence evolution follows [Persistence Architecture](docs/product/PERSISTENCE_ARCHITECTURE.md); implementation remains separately qualified and approved.

## Backlog hygiene

Duplicate release-readiness items are consolidated under the priority gap-closure list. Historical technical-debt release gates and consumer-specific work are not Generation 2 platform work.
