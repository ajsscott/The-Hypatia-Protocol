---
observed: 2026-09-17
source-session: host Claude Code — AI-Coach repo sweep + aj.local/docs read-through
candidate-type: pattern
confidence: high
status: new
---

## What I observed

AJ maintains an explicit "licensed / not licensed" language list for every artifact built on observational data, including internal slides. From the Experiment B v2 plan §3 and the RQ4 methods memo: never "the effect of tutoring," "the impact of the program," "tutoring caused"; never "tutored students grew more than *similar* students"; never a gain score or "average points gained"; and "equally: 'tutoring did not work' / 'we found no effect.' The design cannot support a null any more than a positive. This is the error we are currently closest to making." She extends the symmetry to instruments: "Neither 'the AI is wrong' nor 'the coaches are lenient' is the finding." She also positions unflattering findings deliberately: the RQ4 memo is aimed at engineers first, paired with the RCT so it reads as a statement about the data, not the program.

## How I'd codify it

Pattern: for observational designs AJ writes a two-column licensed/unlicensed sentence list into the plan and applies it to all outputs, internal included. The rule is symmetric — a design that can't support a positive claim can't support a null either. She treats the most natural naive computation (the gain score) as a product-design guardrail, not just an analysis rule, because "it is one SQL query away for any future developer."

## Confidence rationale

High. Stated verbatim in three documents (v2 plan, RQ4 memo, RQ5 notebook) and restated at the top of every Experiment B notebook as a "standing rule." Reinforced in conversation with advisors (Thomas's "no causal claim without a randomization point").

## Related captures

[[analysis-preregistration-discipline]] · [[never-rank-people-in-client-facing-docs]]
