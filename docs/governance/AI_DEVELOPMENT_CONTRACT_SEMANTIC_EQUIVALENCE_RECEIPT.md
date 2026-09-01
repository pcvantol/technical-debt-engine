# AI Development Contract Semantic Equivalence Receipt

- Receipt schema: `1`
- Repository: `pcvantol/technical-debt-engine`
- Reviewed base: `3add7cb2288a5324fcea2750a915e27d1f5e59d9`
- Adoption branch: `codex/ai-development-projection`
- Central authority: `pcvantol/ai-development-contracts`
- Central source commit: `ec070e399ff4dbd92e760370002995fe4f4d52d6`
- Profile / extension: `tde` / `TDE_DEVELOPMENT_EXTENSION`
- Projection digest: `34d04daa1668d5ee1288a22d77aa143fecf4e167cb7fdc443d4082cb3ed45d77`

## Authority boundary

The generated projection is the sole authoring location for generic
AI-development contracts. TDE retains product authority for Technical Debt
Engine and Trusted Delivery architecture, evidence model, Runtime,
implementation, CLI/API, public contracts, security and release semantics.
TDE's local development extension records only repository/product-specific
additions.

## Section-level matrix

| Source / stable section | Concept | Classification | Canonical destination | Cleanup action | Status |
| --- | --- | --- | --- | --- | --- |
| `BOOTSTRAP.md` / synchronization | clean, synchronized branch/base preflight | GENERIC_PROJECTED | `AI_BOOTSTRAP_CONTRACT` | removed duplicated instructions; retained local entrypoint | PROVEN |
| `BOOTSTRAP.md` / reading order | TDE status, roadmap, ADR and capability orientation | TDE_DEVELOPMENT_EXTENSION | `TDE_DEVELOPMENT_EXTENSION` | retained as thin local navigation | PROVEN |
| `ENGINEERING_METHOD.md` / philosophy | evidence, policy, adapters, qualification, public contracts | TDE_PRODUCT_AUTHORITY | TDE architecture/capability/evidence docs | unchanged | PROVEN |
| `ENGINEERING_METHOD.md` / lifecycle and recovery | TDE rolling status and immutable Prompt History | TDE_DEVELOPMENT_EXTENSION | extension + `PROMPT_LIFECYCLE.md` | retained, local semantics only | PROVEN |
| `ENGINEERING_METHOD.md` / validation and release | TDE qualification and release decisions | TDE_PRODUCT_AUTHORITY | validation/release architecture | unchanged | PROVEN |
| `ENGINEERING_WORKFLOW.md` / generic branch-review flow | bounded work, reviewable change, handoff | GENERIC_PROJECTED | `PROMPT_INITIALIZATION_CONTRACT`, `BRANCH_WORKTREE_CONTRACT`, `HANDOFF_CONTRACT` | projection is normative; TDE workflow is local record sequence | PROVEN |
| `ENGINEERING_WORKFLOW.md` / TDE records | status replacement and immutable prompt archive | TDE_DEVELOPMENT_EXTENSION | extension | retained | PROVEN |
| `PROMPT_GOVERNANCE.md` / generic initialization | branch/base/state and bounded authorization | GENERIC_PROJECTED | `AI_BOOTSTRAP_CONTRACT`, `PROMPT_INITIALIZATION_CONTRACT` | projection is normative | PROVEN |
| `PROMPT_GOVERNANCE.md` / current work sources | TDE status/recovery documents | TDE_DEVELOPMENT_EXTENSION | extension | retained | PROVEN |
| `PROMPT_FINALIZATION.md` / generic review handoff | validation, bounded change, handoff | GENERIC_PROJECTED | `VALIDATION_EVIDENCE_CONTRACT`, `HANDOFF_CONTRACT` | projection is normative | PROVEN |
| `PROMPT_FINALIZATION.md` / freeze and archive | TDE Runtime/test/product-doc/evidence freeze | TDE_DEVELOPMENT_EXTENSION | extension | retained | PROVEN |
| `PROMPT_LIFECYCLE.md` / state table | TDE `MERGED_UNRECONCILED` reconciliation vocabulary | TDE_DEVELOPMENT_EXTENSION | extension | retained | PROVEN |
| `CANONICAL_PROMPT_TEMPLATE.md` / initialization and completion | generic prompt, branch and validation mechanics | GENERIC_PROJECTED | bootstrap/prompt/branch/validation contracts | projection is normative | PROVEN |
| `CANONICAL_PROMPT_TEMPLATE.md` / reports and release candidate | TDE Prompt History, release-candidate identity and publication guard | TDE_DEVELOPMENT_EXTENSION | extension + `RELEASE_ARCHITECTURE.md` | retained | PROVEN |
| `REPOSITORY_GOVERNANCE.md` | architecture, roadmap, product contracts and TDE scope | TDE_PRODUCT_AUTHORITY | TDE governance/product docs | unchanged | PROVEN |
| `REPOSITORY_HYGIENE.md` / clean worktree | generic clean-state requirement | GENERIC_PROJECTED | `AI_BOOTSTRAP_CONTRACT`, `VALIDATION_EVIDENCE_CONTRACT` | reduced to TDE evidence-preservation exception | PROVEN |
| `REPOSITORY_HYGIENE.md` / evidence fixtures | generated/release evidence preservation | TDE_DEVELOPMENT_EXTENSION | extension | retained as local exception | PROVEN |
| `ENGINEERING_GUIDELINES.md` | adapters, evidence, qualification and public contracts | TDE_PRODUCT_AUTHORITY | TDE implementation/product documentation | unchanged | PROVEN |
| `REPOSITORY_DISCOVERY.md` | discovery Runtime semantics | TDE_PRODUCT_AUTHORITY | TDE Runtime documentation | unchanged | PROVEN |
| `agents/*` | TDE engineering roles | TDE_PRODUCT_AUTHORITY | TDE agent model | unchanged | PROVEN |
| `docs/history/prompts/*` | immutable historical provenance | HISTORICAL_ONLY | existing prompt history | unchanged | PROVEN |

## Zero-loss result and cleanup

The affected standalone generic bootstrap and hygiene text was retired only
after the projection and extension destinations above were present. Product
authority documents and immutable history were not moved or deleted. The
remaining local documents are either TDE product authority, historical
provenance, or local extension/navigation; they are not alternate generic
contract sources.

- Documents reviewed: 12 active development/governance surfaces plus immutable
  prompt history and agent/product references.
- Semantic sections classified: 22.
- Unresolved before cleanup: 0.
- Unresolved after cleanup: 0.
- Generic standalone sections retired: bootstrap synchronization/preflight and
  generic hygiene requirements.
- TDE product documents changed: no.
