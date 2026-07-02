---
observed: 2026-06-24
source-session: host Claude Code — OYM AI-Coach Experiment A benchmark build
candidate-type: preference
confidence: high
status: new
---

## What I observed

AJ asked that code comments "write the WHY not the what — document decisions,
not only code function," and that they be "efficient, succinct, and optimized
for the next programmer to understand the code's intent as well as its function."
This came right after a related directive to keep comments self-contained (no
planning-doc references).

## How I'd codify it

User preference for code comments: **comments explain intent and the decision
behind the code, not a restatement of what the line already does.** Succinct over
verbose. The bar is: the next programmer should grasp *why* this exists / why it
was done this way, fast — not just *what* it does (which the code shows). Pairs
with the self-contained rule (see related): the WHY lives in the comment, in
plain language, with no external-doc pointers.

## Confidence rationale

High. Explicit directive, phrased as a standing preference ("make my comments..."),
and the second comment-style rule she's given in the same session — a consistent
signal about how she wants code documented.

## Related captures

[[code-comments-self-contained]]
