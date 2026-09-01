# TDE development extension

This is the locally authored companion to the generated AI-development
projection. It does not replace the eight generic contracts. It records only
rules that exist because this repository engineers the Technical Debt Engine.

## TDE-local orientation and current-state records

Use `BOOTSTRAP.md` as the local entrypoint. TDE's current engineering truth is
recorded in `ENGINEERING_STATUS.md`, `REPOSITORY_STATUS.md`,
`MANAGEMENT_SUMMARY.md`, `ROADMAP_INDEX.md`, and `PROMPT_INDEX.md`. Immutable
prompt records live in `docs/history/prompts/`; they preserve the actual freeze
point and are never amended. TDE's `MERGED_UNRECONCILED` state is a permitted
administrative transition only when objective GitHub merge evidence exists and
rolling records still describe the preceding freeze point.

## TDE-specific method and evidence boundary

TDE's development method keeps its product-specific principles: explicit
versioned public contracts, isolated language adapters, immutable evidence,
deterministic qualification, declared policy, and least-privilege integration.
Architecture, capability, schema, Runtime, evidence-store, CLI/API, security,
release and Trusted Delivery semantics remain TDE product authority. They are
defined in the relevant product architecture, capability, schema, validation,
release, and security documents—not in the generic projection.

The TDE-local increment records additionally maintain current status,
management summary, prompt index, and immutable Prompt History. A reviewable
TDE change freezes Runtime, tests, product documentation and scope. A later
discovery is entered as TDE Deferred Work and requires its own subsequent
increment; it is not appended to the frozen change.

## TDE qualification and release behavior

TDE validates its own repository through its published/runtime CLI and its
repository-specific evidence producers. Applicable evidence may include Runtime
validation, capability execution, policy qualification, software assurance,
Trusted Delivery, release qualification and certification. These are TDE
product semantics, not a consumer's generic TDE integration contract.

Release candidates must follow `RELEASE_ARCHITECTURE.md`: the candidate is an
exact SHA reachable from `main`, preserved artifacts are identity-bound, and no
push or pull-request event publishes a release. Human authority remains
required for TDE architecture governance, exceptions, merge and release.

## Local navigation

- `ENGINEERING_METHOD.md` explains this TDE-specific extension boundary.
- `ENGINEERING_WORKFLOW.md` identifies the TDE-local records added to a change.
- `PROMPT_LIFECYCLE.md` defines the TDE status vocabulary.
- `CANONICAL_PROMPT_TEMPLATE.md` supplies the TDE-local status and release
  record fields.
- `REPOSITORY_GOVERNANCE.md` and `REPOSITORY_HYGIENE.md` identify TDE-specific
  authority and evidence preservation constraints.
