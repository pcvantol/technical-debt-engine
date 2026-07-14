# AI session initialization

Every AI-assisted engineering session follows this mandatory flow:

```text
Read BOOTSTRAP
  ↓
Determine repository status
  ↓
Read ENGINEERING_STATUS and determine current main
  ↓
Determine active prompt and recovery-plan position
  ↓
Read required canonical documents
  ↓
State assumptions
  ↓
Implement focused increment
  ↓
Validate
  ↓
Update documentation
  ↓
Replace ENGINEERING_STATUS and archive the prompt
  ↓
Produce reviewable Pull Request
```

The session must distinguish, in its working record and final report, between:

- **Repository facts:** directly observable current state.
- **Architectural decisions:** approved canonical choices, normally backed by an ADR.
- **Recommendations:** non-binding proposed actions.
- **Assumptions:** provisional statements that need validation.
- **Unresolved questions:** decisions or facts that prevent safe inference.

AI consumes canonical documentation, follows established architecture, respects source authority, avoids duplicate or competing documents, and updates documentation when an architectural change is approved. AI must not infer architecture where canonical documents exist, create competing roadmaps, modify governance implicitly, or change engineering principles outside a dedicated Engineering Governance prompt. Current `main` is the source of truth; repository status and operational evidence override historical prompt order. The repository, not chat history, preserves engineering continuity.
