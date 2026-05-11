# Memory Protocol

**Purpose**: Persistent memory system for cross-session recall via file-based storage. Adapted from Bell's Nathaniel Protocol for Hypatia's inbox-pattern (captures during sessions; consolidation during scheduled maintenance).
**Last Updated**: 2026-05-11
**Trigger Keywords**: memory, remember, recall, history, capture, save memory, prune, retention, preferences, decisions

---

## Overview

Hypatia's memory system has TWO complementary write paths:

1. **CAPTURE** (during session): Hypatia writes free-form markdown observations to `inbox/preferences/<topic-slug>.md`. Schema defined in `inbox/SCHEMA.md`. No JSON validation overhead at capture time.
2. **CONSOLIDATE** (during maintenance): the Scholar reviews captures, decides what survives, and writes consolidated entries to `hypatia-kb/Memory/memory.json` (preferences, decisions) or `hypatia-kb/Intelligence/*.json` (patterns, knowledge, reasoning).

This split is (2026-05-11). It preserves review-before-canon: Hypatia's inferences during a session never become Hypatia's beliefs without the Scholar's explicit promotion.

**Storage locations**:
- Inbox captures: `inbox/preferences/<topic-slug>.md`
- Memory store: `hypatia-kb/Memory/memory.json`
- Memory index: `hypatia-kb/Memory/memory-index.json`
- Session logs: `hypatia-kb/Memory/sessions/session-YYYY-MM-DD-NNN.md`
- Session index: `hypatia-kb/Memory/session-index.json`

**Related systems**:
- Intelligence stores: `hypatia-kb/Intelligence/` (patterns, knowledge, reasoning, cross-references, synonym-map)
- Save command: `.clinerules/08-save-command.md`
- Intelligence layer (CSR routing): `.clinerules/07-intelligence-layer.md`

---

## Index Operations (CSR Pattern)

The memory system uses Context Signal Routing: load the lightweight `memory-index.json` first, then selectively retrieve relevant memories by ID from `memory.json`.

### Threshold rule

| `memory.json` size | INDEX-QUERY | Full load |
|---|---|---|
| Under 5,000 tokens | Practice (recommended) | Allowed |
| Over 5,000 tokens | **Mandatory** | Not allowed |

**Discipline principle**: Practice INDEX-QUERY even below threshold to build habit. Efficiency allows full load; discipline prefers selective.

**Ship-empty caveat**: memory.json launches empty. Until usage accumulates entries (post-consolidation), CSR queries return zero matches. Practice the pattern; expect empty until usage builds the corpus.

### INDEX-QUERY: retrieve relevant memories

**When**: session start, task context changes, Scholar references past.

**Signal-to-index mapping** (adapted for Hypatia's vault domain):

| Signal in Scholar's message | Index query |
|---|---|
| Vault, Seed, Tree, Mountain, librarian | `byTag["librarian"]` |
| Research, citation, source, paper | `byTag["research"]` |
| Code, build, implement, debug | `byTag["development"]` |
| Write, draft, compose, edit | `byTag["writing"]` |
| Plan, planning, roadmap, phases | `byTag["planning"]` |
| Process, workflow, approach | `byTag["workflow"]` |
| "Remember when", "last time", "we decided" | Search `summaries` |
| Route F triggered | `byConfidence["high"]` + `byConfidence["critical"]` |

**How** (Index-First flow):

1. Load `memory-index.json` if not already in context.
2. Match Scholar signals to index categories per the mapping above.
3. Collect relevant memory IDs (max 5).
4. Retrieve only those entries from `memory.json`.
5. Pull session logs only if deeper narrative is needed.
6. Surface naturally; do not announce "checking memory."

**Fallback**: if the index fails to parse, load full `memory.json` (legacy behavior). Log the parse failure.

### INDEX-UPDATE: sync index after memory changes

**When**: after Scholar's manual consolidation writes new entries to memory.json (during maintenance).

**How**:
1. Read updated `memory.json`.
2. For each new or modified entry, update `byTag`, `byType`, `summaries`, `recentIds`.
3. Update `stats` (totalEntries, activeEntries, nextId).
4. Update `lastUpdated`.
5. Validate index parses; verify entry counts match between index and store.

### INDEX-REBUILD: full index regeneration

**When**: manual trigger ("rebuild memory index"), index corruption detected, or major schema migration.

**How**:
1. Load `memory.json` entries.
2. Generate fresh `byTag`, `byType`, `summaries`, `recentIds` from scratch.
3. Write to `memory-index.json`.
4. Verify entry counts match.

---

## Memory operations

### CAPTURE: write to inbox (during session)

Replaces Bell's STORE operation. Hypatia does NOT write directly to `memory.json` during routine sessions. Captures go to `inbox/preferences/*.md` as free-form markdown.

**When to capture**:

- Scholar states a preference ("I prefer X over Y").
- Key decision made ("We decided to use X").
- Project state changes ("Project X is now in phase Y").
- Correction given ("Actually, it's X not Y").
- Pattern observed (repeated behavior worth noting).
- Anti-preference surfaced ("I don't want to do that again").

**How to capture** (per `inbox/SCHEMA.md`):

```markdown
---
observed: YYYY-MM-DD
source-session: <repo + brief context>
candidate-type: preference | pattern | knowledge | reasoning | unsure
confidence: high | medium | low
status: new
---

## What I observed
<1-3 sentences. Quote the Scholar's words if explicit.>

## How I'd codify it
<What the consolidated entry would look like in target JSON store.>

## Confidence rationale
<Why high/medium/low. What evidence backs it. Where it could be wrong.>

## Related captures
<Optional. Wikilinks to prior captures on the same topic.>
```

**File naming**: `inbox/preferences/<kebab-case-topic>.md`. Descriptive: `tab-indent-preference.md`, not `pref-1.md`.

**One observation per file.** Don't append to existing captures unless the new observation is genuinely the same data point reinforced (in which case bump confidence and note the second source-session).

### CONSOLIDATE: scholar promotes captures to stores (during maintenance)

The Scholar drives this. Hypatia assists when asked.

**When**: scheduled Hypatia maintenance sessions. Triggered by Scholar invocation (`"let's consolidate the inbox"`, `"review captures"`) or by inbox volume reaching attention threshold.

**How**:

1. **Review** `inbox/preferences/*.md` files with `status: new`.
2. **Decide** for each:
 - **Promote**: write a consolidated entry to the target JSON store. Update `status: consolidated` in the capture file.
 - **Reject**: flag with `status: rejected` and a `rejection-reason:` field. Capture stays in inbox as a record of Hypatia over-inferring.
 - **Defer**: leave as `status: new`; revisit next maintenance.
3. **Move consolidated captures** to `inbox/preferences/_consolidated/` (or delete; the Scholar's call).
4. **Update target store + index**:
 - Preferences / decisions / corrections → `memory.json` (new entry per format below).
 - Behavioral patterns → `Intelligence/patterns.json`.
 - Factual claims → `Intelligence/knowledge.json`.
 - Derived reasoning → `Intelligence/reasoning.json`.
5. **Validate** updated store + index parse correctly.

### RECALL: retrieve from memory.json

**When**:
- Session start (check recent / relevant memories). **ALWAYS FIRST.**
- Scholar references past ("last time", "remember when", "we discussed").
- Topic matches stored memory tags.
- Making a decision that prior context would inform.

**Priority**: index first, then selective memory retrieval, session logs last.

**How** (Index-First flow):
1. Load `memory-index.json`.
2. Match Scholar signals to index categories (see INDEX-QUERY mapping).
3. Collect relevant memory IDs (max 5).
4. Retrieve only those memories from `memory.json`.
5. Pull session logs only if narrative depth needed.
6. Surface naturally; do not announce "checking memory."

### SEARCH: find specific memories

**When**:
- Scholar asks about past decisions.
- Need context for current task.
- Verifying a preference before acting.

**How**:
- By type: `byType["preference"]` for all preferences.
- By tag: `byTag["development"]` for all development-tagged memories.
- By date: scan `summaries` filtered by `created` field.

### UPDATE: modify existing memory

**When** (Scholar-driven during maintenance, or Hypatia-driven when explicitly told to update a specific entry):
- Scholar corrects a stored memory.
- Confidence changes based on new info.
- Project state evolves.
- Preference changes.

**How**:
1. Find existing memory by id or content match.
2. Update relevant fields.
3. Bump `lastAccessed` date.
4. Re-run INDEX-UPDATE to sync.

### FORGET: remove from memory

**When**:
- Scholar explicitly asks ("forget that", "delete that memory").
- Memory becomes obsolete (project completed, preference changed).
- Confidence drops to zero.

**How**:
1. Find existing memory by id or content match.
2. Remove entry from `memory.json`, OR mark `"archived": true` if it might be useful later.
3. Re-run INDEX-UPDATE.
4. **If removing intelligence entries** (patterns, knowledge, reasoning): execute Removal Cascade per `Intelligence/intelligence-operations.md` Part 7b.

---

## Memory schema

### `memory.json` sections

| Section | Purpose |
|---|---|
| `instance_identity` | Hypatia identity placeholder (filled at voice-rewrite time) |
| `capture_taxonomy` | Counters tracking inbox-capture categories |
| `intelligence_system` | Learning state and session tracking |
| `proactive_behavior` | Offer history and preferences |
| `active_projects` | Project tracking with status, next actions |
| `implementation_triggers` | Feature triggers with thresholds |
| `memories` | Core memories (preferences, decisions, learnings, critical_safety) |
| `pattern_detections` | Session pattern observations pending consolidation |
| `confidence_events` | Prediction accuracy tracking |
| `domain_expertise` | Scholar's expertise levels by domain (expert / proficient / intermediate / learning) |
| `anti_preferences` | Explicit things to avoid (softer than critical_safety) |
| `session_metadata` | Current session stats |
| `last_session_snapshot` | Latest session counts (updated by save command) |

### Memory entry schema

```json
{
 "version": "4.0",
 "lastUpdated": "YYYY-MM-DD",
 "memories": {
 "mem-001": {
 "id": "mem-001",
 "type": "preference",
 "content": "Prefers atomic Tree notes over composite ones",
 "context": "Stated during zettelkasten setup discussion",
 "created": "YYYY-MM-DD",
 "lastAccessed": "YYYY-MM-DD",
 "accessCount": 0,
 "confidence": 0.9,
 "tags": ["zettelkasten", "atomicity", "trees"]
 }
 }
}
```

Note: `memories` is a dict keyed by ID, not an array. All CSR lookup paths assume dict access.

### Memory types

| Type | Description | Example |
|---|---|---|
| `preference` | Scholar's preferences | "Prefers direct communication" |
| `decision` | Choice made | "Decided to use Roo Code substrate" |
| `correction` | Fixed misunderstanding | "Address is 'Scholar', not 'Sir'" |
| `learning` | Discovered fact or technique | "Obsidian linter overwrites multi-line YAML" |
| `critical_safety` | Must-not-violate rules | "NEVER modify Memory or Intelligence stores during sessions; inbox-only" |
| `system` | System configuration or state | "Hypatia substrate is Roo Code" |

### Confidence levels

| Value | Meaning | When to use |
|---|---|---|
| 1.0 | Critical, must-not-violate | `critical_safety` type only |
| 0.9 | Explicitly stated, recently confirmed | Direct Scholar statement |
| 0.7 | Inferred or moderately certain | Observed pattern, not explicit |
| 0.5 | Uncertain or very old | Needs validation |

**Decay**: entries with `accessCount == 0` and `created > 180 days` decay by 0.05/month (floor: 0.7). Applied during monthly maintenance.

### Session index schema

```json
{
 "id": "session-YYYY-MM-DD-NNN",
 "date": "YYYY-MM-DD",
 "tags": ["topic-1", "topic-2"],
 "summary": "What happened this session (20-500 chars)",
 "outcome": "success | partial | blocked",
 "outcome_note": "Brief explanation (10-150 chars)"
}
```

Optional fields: `key_decisions`, `files_modified`, `memories_recalled`, `inbox_captures_created`.

---

## Behavioral triggers

### Session start
1. Read `memory-index.json`.
2. Check `recentIds` for memories accessed in the last 7 days.
3. Note any relevant to likely tasks based on session-index tags.
4. Hold in context; surface when relevant.

### During session

| Trigger | Operation |
|---|---|
| "I prefer.", "I like.", "Always use.", "Never use." | CAPTURE preference |
| "Let's go with.", "We decided.", "The plan is." | CAPTURE decision |
| "Remember that.", "Don't forget." | CAPTURE with high confidence |
| "Last time we.", "Remember when.", "What did we decide about." | RECALL |
| "Forget about.", "Delete that.", "Never mind that." | FORGET (with Scholar confirmation) |
| "Actually it's.", "I was wrong about.", "Correction:." | CAPTURE correction |

### Session end (save)
- See `.clinerules/08-save-command.md`. Save records the session, flushes inbox captures (stages them in git), updates `last_session_snapshot`. Save does NOT auto-consolidate captures into `memory.json`.

### Snapshot update (part of save)
Already specified in `.clinerules/08-save-command.md § Step 3`. The save command updates `last_session_snapshot` with current counts. This enables session-diff on next start.

---

## Anti-patterns

- **Auto-promotion of inbox captures during save**. Save records the session and stages the inbox; consolidation is the Scholar's explicit maintenance step. Auto-promotion violates.
- **Announcing "checking memory"**. Just do it. The Scholar should not need to see the mechanism.
- **Storing everything**. Be selective. Most session content is ephemeral.
- **Forgetting without confirmation for high-confidence items**. Explicit Scholar request required for `confidence >= 0.9` entries.
- **Letting memory.json grow unbounded**. Archive old items per retention rules.
- **Duplicating what's in patterns.json or knowledge.json**. memory.json holds preferences and decisions; intelligence stores hold patterns and facts.
- **Writing directly to memory.json without going through the capture-then-consolidate flow.** This is 's load-bearing rule.

---

## Validation

### Conformance gate (write-time, during consolidation)

Before writing any new memory entry to `memory.json`:

1. **Check required fields**: id, type, content, context, confidence, tags, created, lastAccessed, accessCount. Missing → add with defaults (`accessCount=0`, `lastAccessed=today`, `created=today`).
2. **Check confidence**: must be numeric 0.0-1.0. String detected → convert: critical=1.0, high=0.9, medium=0.7, low=0.5.
3. **Check type**: must be in enum (`preference`, `decision`, `correction`, `learning`, `critical_safety`, `system`). Unknown → flag `_needs_review: true`.
4. **Check id**: must match dict key. Must follow `mem-NNN` format.

Before writing any new session-index entry:

1. **Check required fields**: id, date, tags, summary, outcome, outcome_note.
2. **Check id format**: must match `session-YYYY-MM-DD-NNN`.
3. **Check outcome**: must be `success`, `partial`, or `blocked`.

### On RECALL
- If `memory.json` fails to parse, flag error and proceed without memory.
- Log missing required fields on any memory encountered.

### On Session Start
- Verify `memory.json` parses as valid JSON.
- Check `version` field exists.
- Flag memories with missing required fields (don't fail; just note).

---

## Pruning operations

Pruning prevents unbounded growth while preserving valuable context. Content is archived; metadata is destroyed.

### Retention rules

| Data | Retention | Min keep | Action |
|---|---|---|---|
| Session index entries | 60 days | 10 | Destroy |
| Session log files | 30 days | 10 | Archive to `Memory/archive/` |
| Pattern detections (consolidated=true) | 30 days | 5 | Destroy |
| Confidence events | 30 days | 5 | Destroy |
| Offer history | 60 days | 10 | Destroy |
| Completed projects | 14 days post-completion | 0 | Archive to `projects_archive` in `memory.json` |
| Resolved commitments | 30 days post-resolution | 0 | Destroy |
| Cancelled commitments | 14 days post-cancellation | 0 | Destroy |
| Open commitments | Never auto-prune | N/A | Scholar resolves or cancels |
| Consolidated inbox captures | 90 days | 0 | Archive to `inbox/preferences/_consolidated/_archive/` |
| Rejected inbox captures | 180 days | 0 | Keep indefinitely (pattern-recognition value for "Hypatia over-infers in X situation") |

**Principle**: archive *content* (logs, projects, captures). Destroy *metadata* (index entries, events, detections).

### PRUNE-CHECK

**When**: save command step 7 (per `.clinerules/08-save-command.md`).

**How**:
1. Count items in each data store.
2. Check oldest item age against retention.
3. If `count > min_keep` AND `oldest > retention`, flag for pruning.
4. Return list of stores needing pruning.
5. If none flagged, skip PRUNE-EXECUTE.

### PRUNE-EXECUTE

**When**: PRUNE-CHECK returns non-empty list.

**How**:
1. **Session logs**: move files older than 30 days to `Memory/archive/`; remove corresponding entries from `session-index.json`.
2. **Completed projects**: move to `projects_archive` array in `memory.json`.
3. **Pattern detections**: delete entries where `consolidated=true` AND older than 30 days.
4. **Confidence events**: delete entries older than 30 days (keep min 5 most recent).
5. **Offer history**: delete entries older than 60 days (keep min 10 most recent).
6. Update `stats` and `lastUpdated` in affected files.
7. Note pruning action in session log.

### PRUNE-MANUAL

**Trigger**: "prune", "cleanup", "archive old sessions".

**How**: run PRUNE-CHECK with `min_keep` set to 0 (force full evaluation against retention only).

**For full ecosystem maintenance** (beyond memory pruning): see `maintenance-protocol.md` for integrity checks, growth management, orphan detection, and coordinated cleanup across all data stores.

---

## Recovery

**`memory.json` corrupted (parse error)**:
1. Check for syntax errors (missing commas, brackets).
2. Restore from git history if available.
3. Manually reconstruct from recent session logs.
4. Re-validate after repair.

**Memory not being recalled**:
1. Verify memory exists in `memory.json`.
2. Check tags match expected triggers.
3. Confirm confidence level isn't below 0.5.
4. Check `lastAccessed`; may have been archived.

**Duplicate memories created**:
1. Search `memory.json` for similar content.
2. Merge duplicates; keep higher confidence.
3. Update INDEX-UPDATE to catch future duplicates.

**Inbox captures not being processed during maintenance**:
1. Verify Scholar invocation pattern triggers consolidation.
2. Check `inbox/preferences/*.md` files exist with `status: new`.
3. Verify Scholar is invoking consolidation (this is Scholar-driven, not auto).
4. If volume is overwhelming, ask Scholar to schedule a dedicated consolidation session.

**Data loss prevention**:
- `memory.json` is git-tracked. Commit regularly via save command.
- Save command checkpoints state.
- Session logs provide reconstruction path.
- Inbox captures provide a second-tier reconstruction source for content that hadn't yet been consolidated.

---

## Cross-references

- **Save command (where memory updates happen mechanically)**: `.clinerules/08-save-command.md`
- **Intelligence layer (CSR routing)**: `.clinerules/07-intelligence-layer.md`
- **Session gates (IMG fires before memory-touching inferences)**: `.clinerules/04-session-gates.md`
- **Inbox capture schema (entry point)**: `inbox/SCHEMA.md`
- **Vault maintenance (broader ecosystem cleanup)**: `maintenance-protocol.md`
- **Learning loop (consolidation algorithm for intelligence stores)**: `Intelligence/learning-loop.md`

---

*Memory is persistence. Persistence is continuity. Continuity is trust.*
