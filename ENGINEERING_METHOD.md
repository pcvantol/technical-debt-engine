# Engineering method

This is TDE's canonical engineering constitution. It defines how the independent product is engineered by people and AI.

## Philosophy

| Principle | Purpose | Expected behavior | Engineering implications |
| --- | --- | --- | --- |
| Documentation First | Make intent inspectable before code. | Canonical documents state durable intent. | Update them with every relevant increment. |
| Architecture First | Preserve coherent boundaries. | Approved architecture precedes implementation. | Use ADRs for boundary-changing decisions. |
| Capability First | Keep product value modular. | Capabilities evolve independently. | Do not couple adapters to consumers. |
| Contract First | Protect consumers. | Public contracts are explicit and versioned. | Assess compatibility before change. |
| Evidence First | Ground decisions in facts. | Results retain provenance. | Treat evidence as immutable. |
| Qualification First | Make acceptance explicit. | Policy decides outcome from evidence. | Reject ambiguous or incompatible inputs. |
| Policy First | Make governance repeatable. | Policies are declared before enforcement. | Do not embed hidden rules. |
| Incremental Delivery | Keep review meaningful. | One prompt produces one focused PR. | Follow the mandatory workflow. |
| Prompt Ownership | Keep increments singular and accountable. | One prompt owns one objective, one increment, and one reviewable PR. | Do not expand prompt scope after implementation begins. |
| Fail Closed | Avoid false assurance. | Unknown or invalid states do not pass. | Surface blockers explicitly. |
| Immutable Evidence | Preserve traceability. | Published records are never mutated. | Issue new evidence for corrections. |
| Canonical Sources | Prevent drift. | Higher sources resolve conflict. | Do not create competing documents. |
| Long-Term Maintainability | Sustain the platform. | Decisions consider future ownership. | Prefer simple, documented contracts. |
| Vendor Neutrality | Preserve portability. | No vendor controls architecture. | Keep interfaces implementation-neutral. |
| Human Authority | Retain accountable judgment. | Humans approve governance, merge, and release. | Agents have no merge or release authority. |
| Repository Synchronization | Begin from accepted current state. | Synchronize and verify `main` before repository reading or planning. | Run `git switch main` and `git pull --ff-only`; stop if either command or verification fails. |
| Main Is Source of Truth | Ground work in accepted repository state. | Current `main` overrides conversation and historical plans. | Branch work starts from current `main`; history supplies context only. |
| Operational Reality Is Authoritative | Prevent plan-derived claims. | Observable repository evidence determines current state. | Status and recovery decisions cite executable, testable, or immutable evidence. |
| Repository-Native Continuity | Make future work self-describing. | Repository contents preserve handoff and immutable history. | Chat history is never required to continue engineering. |
| Repository Hygiene | Keep state observable and reproducible. | The repository is clean at increment completion. | Ignore operating-system artifacts and preserve intentional evidence and fixtures. |

## Lifecycle, freeze point, and definition of done

The engineering lifecycle is defined by [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md). Every increment validates its stated scope and produces one reviewable pull request. Prompt lifecycle is **Draft → Active → REVIEWABLE_FROZEN → MERGED_UNRECONCILED → MERGED_RECONCILED → Archived**, with optional **Superseded** for a prompt replaced before merge. `REVIEWABLE_FROZEN` means a ready pull request exists and implementation is frozen; it does not predict a human merge. `MERGED_UNRECONCILED` is the permitted transition in which GitHub proves merge into `main` but rolling current-state documents still truthfully describe the preceding Freeze Point. `MERGED_RECONCILED` means those rolling documents have been reconciled from objective GitHub evidence and the next increment may proceed. Only one prompt may be Active.

Each prompt owns exactly one engineering objective, one engineering increment, and one reviewable pull request. The increment ends when that reviewable pull request exists; merging is a separate human decision. A draft pull request may be used before reviewable state only to prepare mandatory finalization records in the same pull request. It is not a reviewable pull request and does not reach the Freeze Point.

The reviewable pull request is the immutable engineering boundary for its prompt. The Prompt Freeze Point is reached immediately when the pull request becomes reviewable. At the Freeze Point, implementation is complete and engineering stops: no further implementation commits, Runtime changes, test changes, production-documentation changes, scope expansion, immediate fixes, or next-increment work are permitted. Only the Prompt Execution Report, current-state updates, prompt archive, and final management summary may be completed after the Freeze Point. Late discoveries are recorded as Deferred Work for a subsequent prompt; they are never added to the frozen pull request. The next engineering increment starts only after merge.

- **IMPLEMENTED:** the scoped change exists; this is not proof of correctness.
- **VALIDATED:** declared checks have passed; this is not a policy decision.
- **QUALIFIED:** compatible evidence has passed an explicit policy; this is not a release.
- **RELEASED:** an approved immutable artifact is published; this is not proof of operational adoption.
- **OPERATIONAL:** the released capability is intentionally running in its target context.

These states are distinct and must never be used interchangeably.

## Operational reality and recovery

Engineering proceeds from current repository reality, not historical prompt order:

```text
Current main → Repository Status → Current Engineering Status → Recovery Plan → Next Engineering Increment
```

Roadmaps and prompt archives guide context but do not override observable current repository state. [ENGINEERING_STATUS.md](ENGINEERING_STATUS.md) is the primary handoff and is completely replaced by each prompt. Immutable historical context is preserved in [docs/history/prompts](docs/history/prompts).

## Prompt initialization

Repository synchronization and post-merge reconciliation are the first engineering steps of every prompt:

```text
Repository Synchronization → Current Main Verification → Objective Previous Pull Request Verification → Post-Merge State Classification → Rolling Status Reconciliation → Canonical Repository Read → Implementation Reality Check → Engineering Planning
```

The synchronization commands are `git switch main` followed by `git pull
--ff-only`. Any failure stops engineering. After synchronization, verify the
checked-out branch, `HEAD`, repository and working-tree cleanliness, tracking
branch, and fast-forward status. Only then read the canonical repository state
listed in [BOOTSTRAP.md](BOOTSTRAP.md), perform the implementation reality
check, and plan the increment. Current `main` overrides conversation history,
historical prompts, previous AI assumptions, prompt examples, and engineering
memory.

A reviewable pull request cannot truthfully record its own future merge. After
human merge, the next session verifies the previous PR through GitHub, confirms
that current `main` contains its accepted merge commit and that its immutable
Prompt History exists, then classifies the state. When only rolling status
documents lag, reconcile them as mandatory initialization inside the next
substantive prompt; this is not a second objective or a historical rewrite.
Stop for a material inconsistency: an unmerged or unverifiable PR, stale main,
uncommitted work, missing Prompt History, absent accepted change, or current
status claiming implementation absent from main.

## Validation and documentation

Validation is proportional to risk and includes contract, documentation, and repository-state checks as applicable. Documentation is canonical rather than duplicative: alter the designated source, update current engineering status, repository status, management summary, and prompt index, archive the prompt, and record durable architectural choices as ADRs.

## Governance and lifecycle

Architecture, capability, and schema changes follow the architecture decision process and applicable ADRs. A capability moves from proposal through defined contract, independent adapter design, canonical mapping, qualification semantics, evidence compatibility, validation, and release readiness. Prompt governance, lifecycle, and finalization are defined in [PROMPT_GOVERNANCE.md](PROMPT_GOVERNANCE.md), [PROMPT_LIFECYCLE.md](PROMPT_LIFECYCLE.md), and [PROMPT_FINALIZATION.md](PROMPT_FINALIZATION.md).

## Evidence, qualification, release, and exceptions

Evidence is immutable, versioned, provenance-bearing, and primary for machine decisions. Qualification is deterministic and fail-closed for incompatible or incomplete evidence. Release readiness requires implemented, validated, qualified, and explicitly approved release scope; release authority remains human.

Exceptions are explicit, scoped, time-bounded, traceable, and never silently weaken policy. A freeze may limit changes to defined corrective work; freeze entry and exit are explicit governance decisions. Platform evolution occurs through small prompts, canonical documents, ADRs, compatibility declarations, and reviewable pull requests.

## Protection

The Engineering Method is canonical. Future modifications require a dedicated Engineering Governance prompt. Normal implementation prompts must not modify this document or its principles.
