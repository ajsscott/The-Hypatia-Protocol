---
observed: 2026-05-19
source-session: renphil-tact-scripts — error handling refactor
candidate-type: preference
confidence: high
status: new
---

## What I observed

AJ interrupted a file write mid-flight to reject a WHAT comment on an `except Exception`
backstop clause. The comment described what the clause caught and why — both visible from
the code itself. She said: "write the same code you were about to without the comment.
write why, only if needed, not what."

## How I'd codify it

No comment if the code is self-explanatory, even for constructs that look unusual. Only
add a comment when the WHY is hidden — an SDK quirk, a non-obvious invariant, a
workaround for specific external behavior. "This catches X to prevent Y" is a WHAT
comment if X and Y are already readable from the code. Removing the comment should not
confuse a future reader with full access to the code.

## Confidence rationale

High. AJ stated this explicitly and mid-action, which is a stronger signal than
post-hoc feedback. Consistent with the existing `code-quality-pattern-cluster.md`
capture on WHY-only comments. Not situational — she applied the same principle in the
earlier session's comment sweep.
