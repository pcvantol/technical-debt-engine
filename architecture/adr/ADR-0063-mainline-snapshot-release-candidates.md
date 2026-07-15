# ADR-0063: Mainline Snapshot Release Candidates

## Status

Accepted — R1-GOV-2.

## Context

The R1-2B candidate `2d6132061807a433178a1ababc1709340cb937de` and current
main `0d7fea6961b1ad495525427fb473c0629b3eb53b` share parent
`a07271b9643961ab6f3b75672513a9fa253c6b92`. The candidate is a sibling of
main, not an ancestor. Main contains the Runtime, Docker, workflow, tooling,
and test changes required for the intended release. Publication correctly
stopped: the certified sibling bundle cannot represent the releasable mainline
product and no publication occurred.

## Decision

Candidates are immutable references to commits already reachable from `main`.
The candidate workflow accepts an exact SHA and rejects any SHA for which
`git merge-base --is-ancestor <candidate> main` fails. It checks out the exact
SHA, retains candidate-bound evidence and bundles, and does not publish.
Publication is a separate, manually dispatched, protected-environment process
that consumes the preserved bundle without rebuilding after explicit human
authorization.

## Consequences and migration

`2d6132061807a433178a1ababc1709340cb937de` is preserved as
`SUPERSEDED_NON_MAINLINE_CANDIDATE`; its evidence is immutable but it is never
publishable. After this correction is merged, a separate increment creates and
certifies a fresh candidate from synchronized main. Final release tagging and
all external publication remain out of scope for this decision.
