---
observed: 2026-05-11
source-session: sandboxed_claude — Hypatia Phase 0 resume
candidate-type: pattern
confidence: medium
status: new
---

## What I observed

When presented with three sequential options ordered by ascending cost
(2: ~5-min CLAUDE.md patch; 1: smoke-test infra; 3: ~717-line Phase 0
content migration), AJ accepted the proposed cheap-fix-first ordering
verbatim: "Yes, 2 → 1 → 3." She then explicitly framed the day's
ambition: "Let's try to get past phase 0 and build as much of Hypatia as
we can today."

## How I'd codify it

**Pattern (`patterns.json` candidate):** When AJ has a daily work window,
she prefers a sequence that (a) clears cheap mechanical fixes first,
(b) validates load-bearing infrastructure before depending on it, and
(c) saves the heaviest work for after both are settled. Don't propose
the big task first if there's a cheap precondition still open.

**Pace signal:** AJ frames work in day-sized chunks ("today") not
sprint- or phase-sized. When she says "build as much as we can today,"
she means progress is the metric, not phase-completion. Don't pad with
research/planning when she's expressed daily-ship appetite.

## Confidence rationale

Medium. Two related signals from a single exchange — the ordering
acceptance is one data point (she could have just been agreeing with
my recommendation), but the explicit "build as much as we can today"
framing strengthens the pace half. Will firm up to high if observed
again in a second session with a different task mix.

## Related captures

(First on this topic.)
