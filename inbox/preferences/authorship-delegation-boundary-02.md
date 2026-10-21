---
observed: 2026-09-25
source-session: host Claude Code — OYM AI-Coach, COACH-209 Data Bazaar loader (Slice 1 to production)
candidate-type: pattern
confidence: high
status: new
---

# Within delegable infra work, AJ keeps design and first drafts, hands off mechanical edits

Second data point for the delegation boundary, and it sharpens the earlier
one. In a long `/supervise` session building the BigQuery loader, AJ typed
the load-bearing code herself all day: every new function, every new test,
the argparse guard, the month-glob generator, the alias-folder partition.
She made every design call by choosing among options (write strategy
"option 1", glob shape "option 1", where the unknown-filename sample lives).

What she handed off, each time with an explicit "make these changes
yourself" or "update X yourself": updating existing test fixtures to a new
field, a one-line literal change, adding a parametrize case, fixing a
syntax error she had introduced, docstring updates, the README, the
migrations move. All of it edits to code that already existed or prose.

So the boundary from 2026-08-05 (infra delegable, analysis hers) has an
inner layer: even inside delegable infra work, **novel logic and its
first test are hers; propagation, fixtures, and documentation are
Claude's when asked.** The grants stayed per-change, never a session-wide
switch to build mode.

Also observed: she asked "what's next on the TODO" and "update it with
what we've done" repeatedly, treating the plan doc as Claude-authored
shared state while the code stays hers. And she skipped a prediction
exercise offered at the milestone without comment, twice; the milestone
push (first production load) took priority over the learning interrupt.

Not deadline-driven this time: no external due date on the session, which
weakens the earlier caveat that delegation was schedule pressure.
