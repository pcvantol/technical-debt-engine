# Canonical prompt template

Use this template for every future canonical engineering prompt. The prompt defines exactly one coherent engineering increment and must name its objective, boundaries, required documentation, validation, and decision.

## Completion contract

Every prompt finishes with the following contract:

> Work only on a dedicated branch.
>
> Keep scope focused.
>
> Produce exactly one reviewable Pull Request.
>
> Update canonical documentation where required.
>
> Update Repository Status.
>
> Update Management Summary.
>
> Update Prompt Index.
>
> Validate.
>
> Leave the working tree clean.
>
> Stop.

## Final report contract

The final report must contain:

- Decision
- Branch
- Commit SHA
- Pull Request
- Validation
- Created documents
- Updated documents
- Outstanding blockers
- Recommended next prompt

The next canonical prompt must not begin until this prompt has produced its reviewable pull request. Merge remains a separate explicit engineering decision.
