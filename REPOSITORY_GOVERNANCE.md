# Repository governance

TDE product governance owns architecture, roadmap, documentation authority, and public contracts. The platform is maintenance-first: bug fixes, analyzer updates, dependency updates, compatibility work, documentation, governance, and public-runtime maintenance follow the established public-contract and qualification model. Architecture changes follow the ADR process; roadmap changes follow [ROADMAP_GOVERNANCE.md](ROADMAP_GOVERNANCE.md); canonical documents follow the source hierarchy.

New capabilities require an approved architectural assessment showing that an
engineering decision cannot be made using the existing capability model.
Routine product-quality findings belong to consumer repositories and do not
implicitly authorize TDE scope expansion.

AI contributors may read canonical sources, propose and implement focused changes, validate declared scope, and prepare a reviewable pull request. They may not implicitly modify governance, infer a replacement architecture, merge pull requests, approve their own governance changes, or create releases.

Every increment declares appropriate validation and leaves the repository valid. Human authority approves architecture governance, merge, exceptions, and release. The repository uses least privilege and stable public integration contracts.
