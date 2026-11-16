---
observed: 2026-10-30
source-session: host Claude Code — OYM AI-Coach, drafting the spring-2027 pipeline ticket set for Jira
candidate-type: preference
confidence: high
status: new
---

## What I observed

While turning a planning doc into Jira tickets, I asked AJ where a cited audit brief lived (the plan referenced it by path, and it wasn't on disk). She answered: "i don't know where it is. The jira document should be standalone and not reference other documents." She then accepted the stripping of ~36 inline source citations (meeting-transcript line refs, rubric line refs, audit tags) and paths to her local notes, with the underlying figures kept as plain statements. Repo code paths stayed — those are what a ticket touches.

Earlier in the same session she chose to enter the Jira tickets by hand rather than import a CSV, and had me delete the CSV and two superseded draft plans so only one current plan remained.

## How I'd codify it

User preference for documents that leave her machine: a tracker-bound plan (Jira, shared doc) must be self-contained — facts inline, no citations to private notes, transcripts or local files; only references allowed are to the code the work touches. Working notes and open questions are kept out of the shared artifact or clearly marked as not-for-tracker. She also prefers one current plan file over a trail of superseded drafts.

## Confidence rationale

High: explicit statement, immediately acted on, consistent with her earlier rule that code comments must be self-contained (no "slice N" / plan-doc references in docstrings) and with the no-real-names-in-fixtures rule — same instinct: an artifact is read by people who lack her context.

## Related captures

(First on this topic in the inbox; see Claude Code project memory `feedback-self-contained-comments` for the code-comment version.)
