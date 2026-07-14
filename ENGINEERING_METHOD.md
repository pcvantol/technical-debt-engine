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
| Fail Closed | Avoid false assurance. | Unknown or invalid states do not pass. | Surface blockers explicitly. |
| Immutable Evidence | Preserve traceability. | Published records are never mutated. | Issue new evidence for corrections. |
| Canonical Sources | Prevent drift. | Higher sources resolve conflict. | Do not create competing documents. |
| Long-Term Maintainability | Sustain the platform. | Decisions consider future ownership. | Prefer simple, documented contracts. |
| Vendor Neutrality | Preserve portability. | No vendor controls architecture. | Keep interfaces implementation-neutral. |
| Human Authority | Retain accountable judgment. | Humans approve governance, merge, and release. | Agents have no merge or release authority. |
| Main Is Source of Truth | Ground work in accepted repository state. | Current `main` overrides conversation and historical plans. | Branch work starts from current `main`; history supplies context only. |
| Operational Reality Is Authoritative | Prevent plan-derived claims. | Observable repository evidence determines current state. | Status and recovery decisions cite executable, testable, or immutable evidence. |
| Repository-Native Continuity | Make future work self-describing. | Repository contents preserve handoff and immutable history. | Chat history is never required to continue engineering. |

## Lifecycle, freeze point, and definition of done

The engineering lifecycle is defined by [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md). Every increment validates its stated scope and produces one reviewable pull request. Prompt lifecycle is **Draft → Active → Reviewable → Merged → Archived**, with optional **Superseded** for a prompt replaced before merge. Only one prompt may be Active.

The reviewable pull request is the immutable engineering boundary for its prompt. The Prompt Freeze Point is reached immediately when that pull request exists. At the Freeze Point, implementation is complete and engineering stops: no further implementation commits, Runtime changes, test changes, scope expansion, or immediate fixes are permitted. Only the final execution report, current-state updates, prompt archive, and final management summary may be completed after the Freeze Point. Late discoveries are recorded as Deferred Work for a subsequent prompt; they are never added to the frozen pull request. The next engineering increment starts only after merge.

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

## Validation and documentation

Validation is proportional to risk and includes contract, documentation, and repository-state checks as applicable. Documentation is canonical rather than duplicative: alter the designated source, update current engineering status, repository status, management summary, and prompt index, archive the prompt, and record durable architectural choices as ADRs.

## Governance and lifecycle

Architecture, capability, and schema changes follow the architecture decision process and applicable ADRs. A capability moves from proposal through defined contract, independent adapter design, canonical mapping, qualification semantics, evidence compatibility, validation, and release readiness. Prompt governance, lifecycle, and finalization are defined in [PROMPT_GOVERNANCE.md](PROMPT_GOVERNANCE.md), [PROMPT_LIFECYCLE.md](PROMPT_LIFECYCLE.md), and [PROMPT_FINALIZATION.md](PROMPT_FINALIZATION.md).

## Evidence, qualification, release, and exceptions

Evidence is immutable, versioned, provenance-bearing, and primary for machine decisions. Qualification is deterministic and fail-closed for incompatible or incomplete evidence. Release readiness requires implemented, validated, qualified, and explicitly approved release scope; release authority remains human.

Exceptions are explicit, scoped, time-bounded, traceable, and never silently weaken policy. A freeze may limit changes to defined corrective work; freeze entry and exit are explicit governance decisions. Platform evolution occurs through small prompts, canonical documents, ADRs, compatibility declarations, and reviewable pull requests.

## Protection

The Engineering Method is canonical. Future modifications require a dedicated Engineering Governance prompt. Normal implementation prompts must not modify this document or its principles.
