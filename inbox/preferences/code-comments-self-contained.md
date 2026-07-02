---
observed: 2026-06-24
source-session: host Claude Code — OYM AI-Coach Experiment A benchmark build
candidate-type: preference
confidence: high
status: new
---

## What I observed

AJ told me to stop putting references to the planning/design document in code
comments — e.g. decision IDs like "(D42)" or "Step 1" — because "the plan won't
be available to someone reading the comments later." She asked me to "make it a
rule." She had already been silently stripping these refs out of code I dictated
(the schemas.py comments came back with the "(D45)"-style tags removed).

## How I'd codify it

User preference: **code comments and docstrings must be self-contained.** Never
cite external planning/design docs or their identifiers (decision IDs, "Step N",
"the plan") in code — a future reader won't have them. The *why* goes in the
comment itself, in plain language. (Cross-references to real, durable artifacts a
reader can actually find — a DB table name, a vendor, a standard — are fine; it's
the ephemeral planning-doc pointers that are banned.)

## Confidence rationale

High. Explicit directive ("make it a rule"), reinforced by her having already
acted on it (pre-stripping the refs when typing). Consistent with her general
loud/explicit-over-implicit engineering stance.

## Related captures

(First on this topic.)
