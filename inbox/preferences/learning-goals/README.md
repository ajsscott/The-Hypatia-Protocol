# Learning goals

Active MCII goal cards for the session-start picker.

## Convention

One card per file, kebab-case slug (`neural-network-fundamentals.md`).
Each card has frontmatter:

```yaml
---
title: Short human-readable label shown in the picker
status: active   # active | paused | archived
created: 2026-07-27
---
```

Body: the full MCII goal card produced by the `learning-goal` skill —
desired outcome, mental contrast, obstacles, if-then plans.

## Lifecycle

- **active** — surfaces in the SessionStart picker.
- **paused** — hidden from the picker but kept for reactivation.
- **archived** — retired; keep for retrospective.

Flip status by editing the frontmatter. No deletes — history stays.

## How the picker works

The hook at `~/GitHub/other/sandboxed_claude/hooks/pick-learning-goal.sh`
runs at every session start, lists cards with `status: active` (default
when absent), and injects them into the session context. Claude then asks
which one to focus on today.

`README.md` (this file) is skipped by the picker.
