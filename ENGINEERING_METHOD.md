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

## Lifecycle and definition of done

The engineering lifecycle is defined by [ENGINEERING_WORKFLOW.md](ENGINEERING_WORKFLOW.md). Every increment validates its stated scope and produces one reviewable pull request.

- **IMPLEMENTED:** the scoped change exists; this is not proof of correctness.
- **VALIDATED:** declared checks have passed; this is not a policy decision.
- **QUALIFIED:** compatible evidence has passed an explicit policy; this is not a release.
- **RELEASED:** an approved immutable artifact is published; this is not proof of operational adoption.
- **OPERATIONAL:** the released capability is intentionally running in its target context.

These states are distinct and must never be used interchangeably.

## Validation and documentation

Validation is proportional to risk and includes contract, documentation, and repository-state checks as applicable. Documentation is canonical rather than duplicative: alter the designated source, update status, summary, and prompt index, and record durable architectural choices as ADRs.

## Governance and lifecycle

Architecture, capability, and schema changes follow the architecture decision process and applicable ADRs. A capability moves from proposal through defined contract, independent adapter design, canonical mapping, qualification semantics, evidence compatibility, validation, and release readiness. Prompt lifecycle is Draft → Active → Completed → Deprecated → Archived, with exactly one canonical Active prompt.

## Evidence, qualification, release, and exceptions

Evidence is immutable, versioned, provenance-bearing, and primary for machine decisions. Qualification is deterministic and fail-closed for incompatible or incomplete evidence. Release readiness requires implemented, validated, qualified, and explicitly approved release scope; release authority remains human.

Exceptions are explicit, scoped, time-bounded, traceable, and never silently weaken policy. A freeze may limit changes to defined corrective work; freeze entry and exit are explicit governance decisions. Platform evolution occurs through small prompts, canonical documents, ADRs, compatibility declarations, and reviewable pull requests.

## Protection

The Engineering Method is canonical. Future modifications require a dedicated Engineering Governance prompt. Normal implementation prompts must not modify this document or its principles.
