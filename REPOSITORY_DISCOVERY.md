# Repository discovery

Repository discovery is an abstract runtime service, not a Git operation. It identifies analysis targets from explicit paths and configuration, then creates candidate identities that later stages validate.

Generation 1 supports the conceptual target forms: a single repository, workspace, monorepo, and multi-repository collection. A target may have no Git metadata. Git information, when present, is optional provenance rather than a prerequisite.

Discovery produces bounded candidates with source locations, declared roots, and discovery provenance. Inspection then determines metadata, filesystem inventory, ignore handling, configuration locations, candidate identity, and supported-language candidates. Ambiguous boundaries, unreadable roots, or conflicting configuration fail closed rather than selecting an arbitrary target.
