---
observed: 2026-10-21
source-session: host Claude Code (no project folder) — eMudhra CA compromise audit and remediation
candidate-type: preference
confidence: medium
status: new
---

## What I observed

During the eMudhra intermediate-CA compromise response, AJ first chose "hand me the
exact commands — I'll run them myself" (consistent with default `/supervise`), then
immediately reversed: "I lied. Run the updates yourself." The work was ops
remediation across ~12 trust stores and six repos — brew upgrades, mise installs,
conda channel surgery, `poetry update` in client lockfiles — not application code.

Earlier in the same session she asked for a parallel fan-out of sonnet subagents to
verify each row of a vendor-supplied patch table against primary sources rather than
trusting the table.

## How I'd codify it

For security-remediation and fleet-hygiene chores (trust-store refreshes, runtime
version bumps, lockfile dependency bumps), AJ prefers Claude to execute directly and
report diffs, rather than dictate commands for her to type. `/supervise` applies to
code she wants to learn by writing; it does not extend to repetitive ops execution
under incident time pressure. She still wants: every side-effect disclosed, lockfile
diffs shown before she commits, rollback path named per change, and no commits made
on her behalf.

## Confidence rationale

Medium. Explicit statement, but a single observation under incident urgency — could
be situational rather than a standing preference. Reinforced slightly by her asking
for subagent fan-out for verification work in the same session. Would move to high
if repeated in a non-incident ops context.

## Related captures

(First on this topic.)
