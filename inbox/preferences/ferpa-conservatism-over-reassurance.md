---
observed: 2026-09-17
source-session: host Claude Code — AI-Coach repo sweep + aj.local/docs transcripts (June–Sept 2026)
candidate-type: pattern
confidence: high
status: new
---

## What I observed

When a trusted senior colleague told AJ that sending child-session video to a third-party API carried "functionally zero" risk and that anonymizing video was "not a practical problem," she still routed the benchmark through approved vendors only, submitted the question to counsel, and said: "I'm trying to be really adherent to the legal. I'm trying really hard." She built a "legal gate in code" (adapters refuse `real_child` data unless `legal_status == approved`), treated speaker embeddings as FERPA biometric records to be computed transiently and never persisted, deleted a GPU VM rather than stopping it because child audio had touched its boot disk, and keeps every student-level artifact under a gitignored tree with a build-time gate that fails on raw identifiers. She frames it as future-proofing for handoff, not personal caution: "future proof in terms of FERPA as well."

## How I'd codify it

Pattern: on student/child data AJ takes the conservative legal path even when colleagues she respects call the risk negligible. She encodes the constraint in tooling (gates, de-id boundaries, transient-only compute, delete-don't-stop) rather than relying on judgment at run time, and she asks counsel early because the answer has weeks of lead time. Reassurance from peers does not move her; a written determination does.

## Reinforced 2026-09-22 (host Claude Code — AI-Coach, Data Bazaar loader tests)

Unprompted, AJ replaced a real tutor's slug that I had put in unit-test fixtures
(`Gabriele-A_...`, copied from the repo's own CLAUDE.md examples) with a synthetic
`Tutor-X_2025-01-01T12-35-00Z`, accepting the cost of recomputing a pinned hash and
re-dating three fixtures. Extends the pattern from student data to tutor
identifiers, and from runtime artifacts to test code that will be committed.
Lesson for the assistant: never seed fixtures with names lifted from real data,
even when the repo's own docs use them.

## Confidence rationale

High. Explicit statements in her own words across the 2026-06-22 and 2026-06-24 transcripts, then sustained in design decisions (D6, D9, D26 in the Experiment A plan; the 2026-07-09 runbook's "Delete, don't stop"; the deid rebuild of 2026-08-05) over three months.

## Related captures

[[yolo-rejection-rationale]] · [[analysis-preregistration-discipline]]
