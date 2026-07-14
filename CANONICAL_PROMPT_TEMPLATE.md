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
> Own exactly one engineering objective and increment. Do not expand scope after implementation begins.
>
> Treat the reviewable Pull Request as the Prompt Freeze Point. After it exists, do not change implementation, Runtime code, tests, or scope.
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

## Freeze contract

The reviewable Pull Request is the immutable boundary of the engineering increment. A draft Pull Request may be used before reviewable state to include finalization records in the same Pull Request; it does not reach the Freeze Point. Once the Pull Request becomes reviewable, engineering is complete. The prompt may only create its final Prompt Execution Report, update current repository status records, archive the prompt, report Deferred Work, and stop.

Late discoveries must not be fixed in the frozen Pull Request. Record each one as Deferred Work for a new prompt after merge.

## Deferred Work template

| Description | Reason | Recommended prompt | Priority |
| --- | --- | --- | --- |
| _Describe the deferred work._ | _Explain why it cannot enter the frozen PR._ | _Name the next owning prompt._ | `P0` / `P1` / `P2` |

## Prompt Execution Report contract

The immutable archive is the Prompt Execution Report. It must include:

- Prompt ID and title
- Branch, commit SHA, and Pull Request
- Decision and validation summary
- Created and updated dates
- Known limitations
- Freeze reached
- Prompt completed
- Pull Request created
- Engineering stopped
- Deferred Work
- Recommended next prompt

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
- Deferred work
- Recommended next prompt

The next canonical prompt must not begin until this prompt has produced its reviewable pull request. Merge remains a separate explicit engineering decision.
