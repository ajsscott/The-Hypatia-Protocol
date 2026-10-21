---
observed: 2026-09-28
source-session: host Claude Code — OYM AI-Coach, COACH-209 Data Bazaar loader (identity map)
candidate-type: pattern
confidence: medium
status: new
---

# Ask the client before encoding an interpretation of their data

When a loader design choice turned on *what the client's people were doing*
(7 sessions whose HiLink host was not a registered tutor; three candidate
rules for "which HOST is the tutor"), AJ declined all three options in the
multiple-choice prompt and answered: "Let me ask OnYourMark. Can you give me
more information so I can slack message them?"

She then insisted on running the confirming counts before sending, and the
counts overturned one of Claude's inferences (a name-match "these are
coaches" guess was wrong for one of the two people). The message was
rewritten to ask questions rather than assert a story.

**Pattern:** for decisions that encode a belief about the client's practices
or people into a data model, AJ prefers to leave the honest, visible gap
(here: 7 rows in a data-quality check) and ask the client, rather than pick
the rule that makes the check read zero. Consistent with
`ground-truth-verification-protocol.md` and
`observational-claims-language-rules.md`: state counts, not narratives, when
talking to the client.

**How Hypatia should apply it:** when a design fork depends on facts only
the client has, offer "ask them" as an explicit option and draft the
question with verified numbers and no inferred motives.
