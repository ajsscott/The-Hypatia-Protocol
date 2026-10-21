---
observed: 2026-10-15
source-session: host Claude Code — OYM AI-Coach, redaction recall review (COACH-209)
candidate-type: pattern
confidence: medium
status: new
---

When a quality check has two kinds of failure with different stakes, AJ
gates on the harmful one and reports the costly one. The redaction bar
stayed "recall >= 0.95 and zero full names surviving" (a surviving name is a
FERPA disclosure); precision, which fell from 0.99 to 0.81 when the NER
layer came in, became a reported column in the README table rather than a
floor in the pass rule. Rationale she accepted: a floor on readability
could block a redaction that leaks nothing.

She also accepted a structural over-redaction (reading-passage characters
and game names in quoted tutor speech become [NAME]) once it was shown the
model was right that they are names and nothing in the text could separate
them from students, and asked that it be documented rather than hidden.

Apply: when proposing a pass/fail rule, separate harm from cost; propose
gating only on harm, make cost visible to the dataset owner, and say in the
docs what the system does wrong on purpose.
