# Memory Directory

**Purpose**: Session memory, conversation continuity, and context management.
**Last Updated**: 2026-05-11

---

## Directory structure

```
Memory/
├── README.md                 # This file
├── memory.json               # Scholar's preferences, projects, commitments
├── memory-index.json         # CSR index for memory retrieval
├── session-index.json        # CSR index for session lookup (60-day rolling window)
├── session-archive.json      # Archived session fingerprints (created by first prune cycle)
├── sessions/                 # Individual session logs (created by save command)
│   └── session-YYYY-MM-DD-NNN.md
└── archive/                  # Session logs older than 30 days
```

**Ship-empty** (Bell content wiped per the ship-empty convention). Memory accumulates only through Scholar-driven consolidation of inbox captures (see `../memory-protocol.md` and `../Intelligence/learning-loop.md`).

---

## File purposes

### `memory.json`

Core memory store. Sections:
- `memories`: Scholar's preferences, decisions, corrections, learnings, critical-safety rules, system facts.
- `active_projects`: project tracking with status, next actions, last_touched.
- `commitments`: promises tracked for deadlines.
- `pattern_detections`: session pattern observations pending consolidation.
- `confidence_events`: prediction accuracy tracking.
- `proactive_behavior`: offer history.
- `domain_expertise`: Scholar's expertise levels by domain.
- `anti_preferences`: explicit "don't do X" rules.
- `last_session_snapshot`: latest counts (updated by save command).
- `capture_taxonomy`: counters for inbox-capture categories.
- `instance_identity`: Hypatia identity (Scholar address, voice register).

Full schema: `../memory-protocol.md § Memory schema`.

### `memory-index.json` (CSR pattern)

Lightweight routing index for memory retrieval:
- `byTag`, `byType` dimensions.
- `summaries` for quick scanning.
- `recentIds` for recency-based access.

### `session-index.json` (CSR pattern)

Lightweight session fingerprints for context loading. Each fingerprint: `id`, `date`, `tags`, `summary`, `outcome`, `outcome_note`.

- ~50 tokens per fingerprint vs ~1,500 for full session log.
- 60-day rolling window; older entries archived.

### `session-archive.json`

Fingerprints for sessions older than 60 days. Enables historical recall without loading full logs.

### `sessions/`

Individual session logs written by the save command. Format per `.roo/rules-hypatia/08-save-command.md § Step 1`.

### `archive/`

Session logs older than 30 days. Moved here during maintenance per `../maintenance-protocol.md § Part 2b Session Archival`.

---

## How memory flows in

Per the inbox-then-consolidate pattern:

1. **During sessions**: Hypatia captures memory candidates (preferences, decisions, corrections, etc.) to `inbox/preferences/*.md` with frontmatter `candidate-type: preference` (or similar).
2. **Save command**: stages inbox captures via git. Does NOT promote to `memory.json`.
3. **Scholar consolidation** (during maintenance): reviews captures, applies Quality Gates, promotes survivors to `memory.json`. See `../Intelligence/learning-loop.md § Consolidation pattern A`.

The save command DOES write to `memory.json` for narrow mechanical-metadata exceptions: `last_session_snapshot`, `proactive_behavior.offer_history` consolidation, session_metadata reset.

---

## Retention rules

Per `../memory-protocol.md § Pruning operations`:

- Session logs (sessions/): 30-day retention, then archived to `archive/`.
- Session index entries: 60-day window, min keep 10.
- Pattern detections (consolidated): 30 days, min keep 5.
- Confidence events: 30 days, min keep 5 most recent.
- Offer history: 60 days, min keep 10.

Full maintenance flow: `../maintenance-protocol.md`.

---

## Cross-references

- **Memory CRUD operations + Q-22 capture flow**: `../memory-protocol.md`
- **Save command (mechanical writes during save)**: `../../.roo/rules-hypatia/08-save-command.md`
- **Consolidation methodology**: `../Intelligence/learning-loop.md`
- **Maintenance + retention rules**: `../maintenance-protocol.md`
- **Inbox capture format**: `../../inbox/SCHEMA.md`
- **CSR routing pattern**: `../../.roo/rules-hypatia/07-intelligence-layer.md`
