# Integration model

TDE is a standalone product. Consumers—including DJConnect—integrate only through stable public contracts:

- the `tde` CLI;
- declared configuration;
- the versioned Evidence Schema;
- documented exit codes; and
- released, immutable contracts or artifacts.

Consumers must never integrate through runtime internals, private adapter APIs, repository layout, or unreleased behavior. Public reusable workflows, if introduced later, are contracts with their own versioning and authorization model; workflow access does not imply artifact or release write access.

The intended future delivery chain is: Verification Runtime → TDE → Privacy Assessment → Security Assessment (future).
