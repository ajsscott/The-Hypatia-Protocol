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

Retired 2026-11-20. The session-start picker hook was removed in the
claude-config redesign, and learning now runs through engineer-school. The
cards stay here as a record.

`README.md` (this file) is skipped by the picker.
