---
observed: 2026-06-11
source-session: host Claude Code — OYM-playground, Experiment A benchmark planning
candidate-type: preference
confidence: high
status: new
---

## What I observed

While setting the review cadence for a 10-step build she will implement herself,
AJ rejected all three offered cadence options (review-per-step, review-per-layer,
pair-live) and wrote her own: "You give me the code in tiny pieces, I type it in."

Context: her global CLAUDE.md already establishes "code authorship: mine by
default" — the assistant reviews, she writes. This capture refines that: when the
assistant IS authorized to author code content, the delivery mode she wants is
dictation — small, type-in-able chunks she transcribes by hand, not file edits
and not large pasted blocks.

## How I'd codify it

User preference for code delivery during pair-building: present code as small
sequential pieces (a few lines to one function at a time) that AJ types in
herself. Do not write to files directly; do not deliver whole-file blocks.
Typing-in is deliberate practice — it preserves her ownership, reps, and
line-by-line comprehension. Each piece is a natural checkpoint for explanation
and questions before the next.

## Confidence rationale

High. Explicit free-text statement, and it coheres with her standing
"code authorship: mine by default" rule and the prior capture on
conversational walkthrough pacing. Could be situational to this learning-heavy
benchmark build; watch whether it holds for time-pressured work.

## Related captures

[[walkthrough-pacing-conversational]]
