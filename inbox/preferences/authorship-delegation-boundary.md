---
observed: 2026-08-05
source-session: host Claude Code — OYM-playground, Experiment B deid pipeline rebuild
candidate-type: pattern
confidence: medium
status: new
---

# AJ delegates infrastructure code, reserves analysis code

During the de-identification pipeline rebuild (crosswalk module + three
build-script reworks), AJ progressively delegated authoring to Claude:
first "dictate and I'll type" (per the python-authorship goal card), then
"edit the existing scripts while I type deid.py", then "write deid.py as
well today" — explicitly exiting supervise mode for the whole work
package.

The boundary she appears to draw: **plumbing/infrastructure code
(ID crosswalks, build scripts, validation gates) is delegable; the
analysis code that answers research questions is hers to write.** The
learning goal is about becoming an ML engineer, and she seems to treat
statistical/analysis fluency as the core of that, not data-pipeline
boilerplate.

Also observed: when Dippy denied Claude's writes to the project tree, AJ
resolved it by explicitly widening permission (plan-mode exit) rather
than reverting to hand-typing — deliberate choice, not drift.

**Caveat:** single session, under deadline pressure (Experiment B
deliverables due early September). Could be schedule-driven rather than a
stable boundary. Watch whether she also delegates analysis code when
time-pressed; that would change the interpretation.
