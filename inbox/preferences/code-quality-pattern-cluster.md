---
observed: 2026-05-19
source-session: renphil-tact-scripts — error handling refactor + meeting debrief
candidate-type: pattern
confidence: high
status: new
---

## What I observed

Across a multi-session refactor of a Python queue-worker, AJ demonstrated a
consistent cluster of code-quality preferences that she both applied proactively
and aligned with explicitly when her senior engineers (Ruth Schafer, Zachary
Levonian) articulated them in a 2026-05-18 working session. She said of the
error-handling principle: "My instincts having very little formal background
training in this is errors everywhere — put the error everywhere. But it's very
interesting to be like 'no, we want to put all the errors in the same place.'"
She accepted the framing immediately and applied it without pushback.

## How I'd codify it

AJ's code-quality pattern cluster:
- **Loud-fail over silent-recovery.** Bare `except Exception` is a smell she
  actively hunts; every catch site should name the narrowest applicable type.
  She ran a grep inventory of all catch sites and narrowed each one.
- **Centralized error classification.** In a queue-driven system, error handling
  is control flow — the classification function is the single authority; everything
  below re-raises. She accepted this as the right model as soon as it was framed.
- **Explicit config over scattered defaults.** Deployment-variable values belong
  in a named config file; she treated discovering a hardcoded default in application
  code as something to fix, not leave.
- **WHY comments only.** She ran a pass to remove all WHAT comments (section
  headers, step narration) and preserve only hidden-constraint and SDK-quirk
  comments. Treated this as non-negotiable cleanup, not optional polish.
- **One-screen functions with name-ability as the extraction signal.** She applied
  the "one verb plus one object" heuristic from Zach and decomposed several
  functions exceeding ~60 lines without prompting.

## Confidence rationale

High. These weren't single observations — each preference showed up across
multiple files and multiple exchanges over two sessions. The error-handling
principles were explicitly stated by AJ in the meeting transcript. The comment
and function-size preferences were observed through what she approved vs. rejected
during edits.
