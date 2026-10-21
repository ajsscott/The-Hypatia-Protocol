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

## Reinforced 2026-09-22 (host Claude Code — AI-Coach, Data Bazaar loader slice 1)

AJ opened with "give me the code in small chunks and tell me where to put it tiny
piece by tiny piece. We should work conversationally." After ~10 exchanges she said:
"Whatever you need to remember about the way we're communicating right now, this
conversation and how you're having me build is EXACTLY how I want to be guided,
always."

The loop she endorsed, concretely:

1. One shell command or one code chunk (2–15 lines) per assistant turn, with the
   exact file and insertion point named.
2. Test first: she types the failing test, runs it, pastes the failure. Assistant
   confirms the failure is the expected one before giving the module code.
3. Module code just large enough to turn that test green. Run. Paste. Next.
4. Design calls (e.g. int/str coercion in an id helper) are handed to her as a
   choice with a recommendation; she writes that test herself, assistant reviews
   her code on request and names concrete defects (a paste accident in a test
   string, `assert x raise TypeError` syntax) rather than rewriting the file.
5. No file writes by the assistant. No whole-file blocks. No "here's everything,
   run it."

The prior caveat ("could be situational to this learning-heavy build") is
withdrawn — she said "always," in a production-repo context, not a sandbox.

## Confidence rationale

High. Two explicit statements, three months apart, in different repos, the second
one generalizing with "always." Coheres with "code authorship: mine by default,"
the python-authorship learning goal card, and the conversational-walkthrough
pacing capture.

## Related captures

[[walkthrough-pacing-conversational]]
