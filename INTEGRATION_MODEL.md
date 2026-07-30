# Integration model

TDE is an operational, standalone engineering-quality platform. Consumers—including DJConnect—integrate only through stable public contracts:

- the `tde` CLI;
- declared configuration;
- the versioned Evidence Schema;
- documented exit codes; and
- released, immutable contracts or artifacts.

Consumers must never integrate through runtime internals, private adapter APIs, repository layout, or unreleased behavior. Public reusable workflows, if introduced later, are contracts with their own versioning and authorization model; workflow access does not imply artifact or release write access.

## Observe-only governance

Consumer execution is evidence-only and non-blocking. TDE does not create
required checks, merge blocks, soft-fails, suppressions, or repository-specific
policy forks. Consumers pin the public runtime and invoke the public CLI; they
do not install, select, or duplicate analyzers and policies.

Routine product-quality findings are handled by the consumer repository. A TDE
change is warranted only by a demonstrated platform-maintenance need or an
approved architectural capability decision.

## Complexity parity public contract

`tde assess` and `tde qualify` discover a repository's primary product language
from canonical source classification and resolve registered complexity adapters
inside the published runtime. Consumers must only pin the runtime and invoke the
public CLI; they must not install or select Radon/Lizard adapters themselves.
The resulting `complexity.cyclomatic.product.maximum` follows the existing
policy and qualification path. TDE remains Observe-only in consumer workflows.

## Runtime recovery public contract

`tde assess --capability code_size <repository>` is the public entrypoint for
Code Size analysis. It invokes the Runtime pipeline, which resolves the
capability and `cloc` adapter, writes immutable canonical evidence to
`.tde/evidence` by default, and evaluates Runtime Qualification. Consumers must
use the evidence rather than invoking `cloc` themselves.

The stable runtime exit codes are `0` (`SUCCESS`), `2` (`FAILED_CLOSED`), `3`
(`EXECUTION_ERROR`), `4` (`NOT_SUPPORTED`), and `5`
(`ANALYZER_NOT_FOUND`). A non-zero result never represents a degraded or
silently skipped analysis.

New capability work follows this gated chain: Architectural Assessment →
Capability Decision → Implementation → Qualification → Public Runtime →
Consumer Adoption.
