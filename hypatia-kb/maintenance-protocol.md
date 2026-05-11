# Maintenance Protocol

**Purpose**: Unified maintenance, health verification, and cleanup operations across the Hypatia ecosystem (`hypatia-kb/Memory/`, `hypatia-kb/Intelligence/`, vectorstore, sessions).
**Last Updated**: 2026-05-11
**Trigger Keywords**: maintenance, cleanup, health check, prune, integrity, housekeeping

---

## Overview

Cross-cutting maintenance that no single protocol owns: integrity verification, growth management, coordinated cleanup across `hypatia-kb/Memory/`, `hypatia-kb/Intelligence/`, vectorstore, and supporting files.

**Relationship to other protocols**:

- `memory-protocol.md` owns memory CRUD operations and pruning rules (retention thresholds, PRUNE-CHECK/EXECUTE).
- `Intelligence/learning-loop.md` owns pattern/knowledge consolidation and index sync validation.
- `CRITICAL-FILE-PROTECTION.md` owns safety rails for destructive operations.
- `.roo/rules-hypatia/04-session-gates.md § Destructive Action Gate` governs every modify-state step.
- This protocol orchestrates across all of them and adds integrity/growth coverage.

**Principle**: this protocol does not duplicate rules defined elsewhere. It references them. If a retention threshold lives in `memory-protocol.md`, this protocol calls it, not redefines it.

**Ship-empty caveat**: at launch, the intelligence and memory stores are empty. Health checks pass trivially. Growth budgets apply once usage accumulates entries. Run maintenance during the first months mostly to verify the pipelines wire correctly, not to prune (there's nothing to prune yet).

---

## Trigger Conditions

| Trigger | Action |
|---|---|
| `maintenance` or `health check` | Run HEALTH-CHECK (non-destructive) |
| `full maintenance` or `deep cleanup` | Run HEALTH-CHECK + CLEANUP-EXECUTE |
| `integrity check` | Run HEALTH-CHECK Part 1a only |
| `cleanup` | Execute cleanup on previously identified issues |
| Save command Part 7 | PRUNE-CHECK runs automatically (per `memory-protocol.md`) |
| Monthly (first session of month) | Proactive offer: "Monthly maintenance due. Run health check, Scholar?" |

---

## Part 1: HEALTH-CHECK

**Purpose**: Non-destructive audit of ecosystem state. Reports issues, changes nothing.
**When**: On trigger, monthly proactive, or before any cleanup operation.

### 1a. Integrity verification

Verify index-to-data sync across all data stores.

**Patterns**:
1. Collect all IDs from `patterns-index.json` byCategory, byTag, byConfidence, summaries.
2. Collect all IDs from `patterns.json` entries.
3. Compare: flag IDs in index but not data (phantom), IDs in data but not index (unindexed).
4. Check for duplicate IDs in data entries.
5. Verify `stats.totalEntries` matches actual unique entry count in both index and data files.
6. Verify byConfidence and byCategory arrays have no duplicate IDs.

**Knowledge**:
1. Same comparison: `knowledge-index.json` vs `knowledge.json`.
2. Verify stats match actual counts.
3. Check for duplicate IDs.

**Reasoning**:
1. Same comparison: `reasoning-index.json` vs `reasoning.json`.
2. Verify stats match actual counts.
3. Check for duplicate IDs.
4. Verify byType arrays reference valid reasoning IDs.
5. Verify byProvenance counts sum to total entries (recorded + synthesized + cross_session = total).

**Memory**:
1. Compare `memory-index.json` summaries keys vs `memory.json` memories keys.
2. Verify stats match actual counts.
3. Check byTag arrays reference valid memory IDs.

**Sessions**:
1. Compare `session-index.json` entry IDs vs actual `session-*.md` files in `hypatia-kb/Memory/sessions/`.
2. Flag: index entries with no corresponding file.
3. Flag: files within 30-day window with no corresponding index entry.
4. Check ID format consistency (all use `session-YYYY-MM-DD-NNN` format).

**Cross-References**:
1. Collect all source IDs from `cross-references.json`.
2. Verify each source exists in `patterns.json` or `knowledge.json`.
3. Collect all reasoning IDs from referenced_by arrays.
4. Verify each reasoning ID exists in `reasoning.json`.
5. Flag orphaned references.
6. If `cross-references.json` missing: rebuild from `reasoning.json` derived_from fields (recovery path).

**Synonym map**:
1. Verify `synonyms` keys are bidirectional (if A→B exists, B→A should resolve to the same cluster).
2. Check synonym targets exist as tags in at least one index.
3. Flag dangling synonym targets.

**Vectorstore**:
1. Check if `vectorstore/config.json` exists (vectorstore is optional).
2. If exists: read entry count from `vectorstore/metadata.json`.
3. Compare entry count against sum of patterns + knowledge + reasoning entries.
4. Flag drift if counts don't match (run `kb_sync.py` to resolve).
5. Verify model version in `config.json` matches `MODEL_NAME` in `kb_vectorize.py`.
6. If vectorstore missing: note as INFO, not error (system degrades gracefully to CSR-only).

**Inbox**:
1. Count files in `inbox/preferences/` by status (new / consolidated / rejected).
2. Flag if `new` captures exceed 20 (consolidation backlog signal).
3. Flag if any capture has malformed frontmatter (missing required fields).

### 1b. Growth assessment

Report current sizes against budgets. Budgets are monitoring thresholds for reporting only. Retention and pruning rules remain owned by `memory-protocol.md`.

| Resource | Budget | Metric | Source of truth |
|---|---|---|---|
| `memory.json` | 2,500 lines | `wc -l` | This protocol |
| `patterns.json` entries | 300 max | Unique entry count | This protocol |
| `knowledge.json` entries | No cap (monitor) | Entry count | This protocol |
| `reasoning.json` entries | No cap (monitor) | Entry count | This protocol |
| Session log files (active) | 30-day window | File count outside window | `memory-protocol.md` |
| Session index entries | 60-day window | Entry count outside window | `memory-protocol.md` |
| `active_projects` | 15 active max | Count where status=active | This protocol |
| Inbox `preferences/` (new) | 20 max | Files with `status: new` | This protocol |
| Vectorstore entries | Match source stores | Entry count vs sum of stores | This protocol |
| Vectorstore disk | 5 MB | `du -sh vectorstore/*.npy *.json` | This protocol |
| Model cache (`/tmp/fastembed_cache/`) | Active model only | Count of cached models | This protocol |
| Total KB disk | 10 MB | `du -sh hypatia-kb/` | This protocol |

**Budget rationale**:

- `memory.json` 2,500 lines: realistic ceiling based on schema with reasonable usage (preferences + decisions + projects + commitments + transient sections).
- patterns 300: heuristic ceiling; consolidation of similar patterns keeps quality high.
- knowledge / reasoning: no cap. Quality gates at write time (confidence thresholds, dedup checks, taxonomy sweep) prevent junk. CSR and RRF handle retrieval at any scale.
- `active_projects` 15: more than this means stale projects aren't being archived.
- Inbox `new` 20: backlog signal for Scholar's consolidation cadence.
- Vectorstore 5 MB: depends on store size; bigger ceiling than Bell's 2 MB since Hypatia may accumulate more.
- Total KB 10 MB: git performance still fine at this size.

### 1c. Staleness detection

Additionally, check for entries with `_needs_trim: true` flag in `patterns.json`, `knowledge.json`, `reasoning.json`. These exceeded content length targets at write time and need condensing.

| Check | Threshold | Action |
|---|---|---|
| Active projects not touched 90+ days | Flag as stale | Report for Scholar decision |
| Completed/dropped projects older than 14 days | Flag for archive | Report for cleanup |
| Memories not accessed 90+ days | Flag for review | Report for cleanup |
| Inbox captures with `status: new` older than 30 days | Flag for consolidation | Report for Scholar attention |

**Saved query shortcuts** (via `kb_query.py` or MCP `kb_search`):

- `--saved stale-high-confidence`: high confidence entries not accessed in 90+ days.
- `--saved never-accessed`: entries with zero access count.
- `--saved low-confidence`: entries below 0.5 confidence.
- `--saved refinement-candidates`: L1 entries with `accessCount >= 3` but confidence too low.
- `--saved confidence-outliers`: low confidence but high access count (frequently used but untrustworthy).

### 1d. Health report format

```
ECOSYSTEM HEALTH CHECK: [Date]

INTEGRITY:
 Patterns: [OK|ISSUES] - [detail if issues]
 Knowledge: [OK|ISSUES] - [detail if issues]
 Reasoning: [OK|ISSUES] - [detail if issues]
 Memory: [OK|ISSUES] - [detail if issues]
 Sessions: [OK|ISSUES] - [detail if issues]
 Cross-refs: [OK|ISSUES] - [detail if issues]
 Synonym map: [OK|ISSUES] - [detail if issues]
 Vectorstore: [OK|ISSUES|MISSING] - [detail if issues]
 Inbox: [OK|BACKLOG|MALFORMED] - [N new captures, oldest from YYYY-MM-DD]

GROWTH:
 memory.json: [X]/2,500 lines [OK|OVER]
 patterns.json: [X]/300 entries [OK|OVER]
 knowledge.json: [X] entries (monitor)
 reasoning.json: [X] entries (monitor)
 Session logs: [X] active, [Y] overdue for archive
 active_projects: [X]/15 active, [Y] stale, [Z] archivable
 Inbox (new): [X]/20 files [OK|BACKLOG]
 Total KB: [X]MB/10MB [OK|OVER]
 Vectorstore: [X] entries (source: [Y]) [OK|DRIFT]
 Model cache: [X] models cached, [Y]MB [OK|STALE]

STALENESS:
 Stale projects: [list or "none"]
 Archivable projects: [list or "none"]
 Inbox aging (>30d): [list or "none"]

CLEANUP NEEDED: [YES|NO]
 [If YES, list specific operations needed]
```

---

## Part 2: CLEANUP-EXECUTE

**Purpose**: Fix issues found by HEALTH-CHECK.
**When**: After HEALTH-CHECK reports issues, with Scholar confirmation.
**Safety**: All operations follow `CRITICAL-FILE-PROTECTION.md`. Read before write. Confirm before delete.

**Destructive Action Gate**: every step modifies state. Before each step, execute the Destructive Action Gate from `.roo/rules-hypatia/04-session-gates.md`: identify what's changing, classify risk tier, verify current state (read the file), confirm before executing Tier 1-2 actions.

### Execution order

Run cleanup operations in this specific order to prevent cascading issues:

1. **Integrity fixes** (fix data first, before pruning).
2. **Session archival** (move files, update index).
3. **Memory pruning** (clean transient data from `memory.json`).
4. **Project archival** (move completed projects).
5. **Growth reduction** (if still over budget after 1-4).
6. **Vectorstore sync** (reconcile with source stores after any data changes).
7. **Orphan detection** (only if explicitly requested).
8. **Verification pass** (re-run integrity check to confirm clean state).

**Rollback**: if any step fails mid-execution, STOP. Do not proceed to the next step. Note what completed and what didn't in the session log. Re-run HEALTH-CHECK to assess current state before retrying. For file moves, check both source and destination to determine which files moved successfully.

### 2a. Integrity fixes

**DESTRUCTIVE**: Modifies `patterns.json`, `patterns-index.json`, `knowledge.json`, `knowledge-index.json`, `reasoning.json`, `reasoning-index.json`, `session-index.json`.

**Duplicate IDs in data files**:
1. Read both duplicate entries fully.
2. Keep the more recent (by `lastUpdated`); merge any unique tags from the older.
3. Remove the older entry.
4. Update corresponding index file to remove duplicate references.
5. Recount and update stats in both data and index files.

**Phantom index entries** (in index, not in data):
1. Remove the ID from all index arrays (byCategory, byTag, byConfidence, summaries, recentIds).
2. Recount and update stats.

**Unindexed data entries** (in data, not in index):
1. Add the entry to appropriate index arrays based on its category, tags, and confidence.
2. Recount and update stats.

**Stats mismatches**:
1. Recount actual unique entries in data file.
2. Update stats in both data and index files to match.

**Session ID format normalization**:
1. For index entries without `session-` prefix, prepend it.
2. Verify the corrected ID matches an actual file.
3. If no matching file exists, remove the index entry.

**Index rebuild** (when issues are too numerous to fix individually):
- Reference `Intelligence/learning-loop.md` Step 9 (Sync Validation Gate) for the rebuild procedure.
- Rebuild index from data file entries, regenerating all routing arrays.

### 2b. Session archival

**DESTRUCTIVE**: Moves files, modifies `session-index.json`.

Execute per `memory-protocol.md` Pruning rules:

1. Identify session log files older than 30 days (not already in `Memory/archive/`).
2. Move files to `hypatia-kb/Memory/archive/`.
3. For each moved file, check if its ID exists in `session-index.json`.
4. If yes and entry is older than 60 days: remove from `session-index.json`.
5. If file had no index entry: no index action needed.
6. Update `session-index.json` stats.

**Minimum keep**: per `memory-protocol.md`, always retain at least 10 entries in `session-index.json` regardless of age.

### 2c. Memory pruning

**DESTRUCTIVE**: Modifies `memory.json`.

Execute per `memory-protocol.md` Retention Rules. Do not invent new thresholds. Authoritative rules:

| Section | Rule (per `memory-protocol.md`) |
|---|---|
| `pattern_detections` | `consolidated=true` AND older than 30 days, min keep 5 |
| `confidence_events` | Older than 30 days, keep min 5 most recent |
| `offer_history` | Older than 60 days, keep min 10 most recent |
| `session_metadata` | Reset to current session if stale |

### 2d. Project archival

**DESTRUCTIVE**: Modifies `memory.json`.

1. Identify projects where status is `complete`, `completed`, or `dropped` AND `last_touched` is 14+ days ago.
2. Move to `projects_archive` array in `memory.json` (create if doesn't exist).
3. Remove from `active_projects` array.
4. Update `memory-index.json` if any project-related memories affected.

### 2e. Growth reduction

**DESTRUCTIVE**: Modifies `memory.json`, potentially `patterns.json`, `knowledge.json`. Requires Scholar confirmation before executing.

Only runs if `memory.json` is still over the 2,500-line budget after steps 2c and 2d.

1. **Memories**: Identify memories not accessed in 90+ days with confidence < 0.8. Present list to Scholar for confirmation before archiving.
1b. **Memory confidence decay**: Entries with `accessCount == 0` and `created > 180 days`: reduce confidence by 0.05 (floor: 0.7), flag as `_stale_candidate` for review.
2. Archive confirmed memories (mark `archived: true`), update `memory-index.json`.

If `patterns.json` over 300 entries:
1. Identify patterns with confidence < 0.5 AND not accessed in 60+ days.
2. Present list to Scholar for confirmation.
3. Archive low-value patterns, update `patterns-index.json`.

If `knowledge.json` quality review needed (periodic, not budget-triggered):
1. Identify entries with confidence < 0.7 AND not accessed in 60+ days.
2. Present list to Scholar for confirmation.
3. Archive confirmed entries, update `knowledge-index.json`.

If `reasoning.json` quality review needed (periodic, not budget-triggered):
1. Same shape; check confidence + lastAccessed.
2. Present list, archive on confirmation.

### 2f. Vectorstore sync

**DESTRUCTIVE**: Modifies vectorstore files (`vectors.npy`, `metadata.json`, `config.json`).

Run after any data changes (integrity fixes, pruning, archival) to keep vectorstore in sync with source stores.

| Scenario | Command | Notes |
|---|---|---|
| After maintenance | `uv run python hypatia-kb/vectorstore/kb_sync.py` | Incremental, fast |
| Entry count drift after sync | `uv run python hypatia-kb/vectorstore/kb_vectorize.py` | Full rebuild |
| Model changed | `uv run python hypatia-kb/vectorstore/kb_vectorize.py` | Full rebuild required |

**Cache cleanup** (if model changed):
```bash
# List cached models
ls /tmp/fastembed_cache/
# Remove non-active models
rm -rf /tmp/fastembed_cache/models--<non-active-model>
```

**Benchmark after model upgrade**: run `uv run python hypatia-kb/vectorstore/kb_benchmark.py` first. See `vectorstore/BENCHMARK.md` for protocol.

### 2g. Inbox triage (maintenance)

**NOT destructive** in itself; surfaces what Scholar should act on.

1. List `inbox/preferences/*.md` files where `status: new`, sorted by `observed` date.
2. Group by `candidate-type` (preference / pattern / knowledge / reasoning / unsure).
3. For each: surface the capture's "How I'd codify it" section as a promote-or-reject proposal.
4. The Scholar decides per-capture: promote, reject, defer.
5. Hypatia executes the promotion writes when the Scholar approves (consolidation flow per `memory-protocol.md § CONSOLIDATE`).

Inbox triage IS the consolidation flow's surface. It runs as a step of maintenance, not as a separate operation.

### 2h. Orphan detection and cleanup

**Only runs if explicitly requested.** Not part of standard maintenance.

### 2i. Verification pass

After all cleanup operations:
1. Re-run HEALTH-CHECK Part 1a (integrity verification).
2. Re-run HEALTH-CHECK Part 1b (growth assessment).
3. Confirm all issues resolved.
4. Report final state vs pre-cleanup state.

---

## Part 3: Cadence and automation

### Automated (every save)

Save command Part 7 runs PRUNE-CHECK per `memory-protocol.md`. This covers retention-based pruning only (session archival, detection cleanup, offer history). Save command also runs vectorstore sync (`kb_sync.py`) to keep semantic search current. Neither runs integrity checks or growth assessment. Those require explicit triggers.

**Known risk**: PRUNE-CHECK can be skipped during save if the checklist item is marked without execution. If health check reveals overdue pruning, that indicates save-time pruning has been skipped.

### Monthly proactive (first session of month)

Wired in `.roo/rules-hypatia/04-session-gates.md` (Session Start Gate):

- **Trigger**: session start + date is 1st-3rd of month.
- **Action**: offer `"Monthly maintenance due. Run health check, Scholar?"`
- **Confidence**: 0.9 (time-based, high reliability).
- **Counts toward**: max 3 proactive offers per session.

### Intelligence system health (monthly, part of health check)

```
[ ] Schema conformance spot-check: run validate-schemas.py
 (scripts/validate-schemas.py). If errors found, run
 normalize-schemas.py. If only warnings, classify manually.

[ ] Confidence decay + staleness review (single pass):
 Entries with accessCount == 0 and created > 180 days:
 - Reduce confidence by 0.05 (floor: 0.7 for knowledge,
 0.5 for patterns/reasoning)
 - Flag as _stale_candidate
 - Knowledge: re-validate against current docs/APIs
 - Patterns: check if behavior still applies
 - Reasoning: check if derived_from sources still valid
 Action per entry: re-validate (update lastAccessed),
 archive, or delete.
 If deleting: execute Removal Cascade
 (Intelligence/intelligence-operations.md Part 7b).

[ ] Tag health: check singleton tag rate. If above 40%, run tag
 consolidation (merge singletons into semantically equivalent
 common tags, update synonym-map).

[ ] Access audit: entries with accessCount == 0 and created > 90
 days. Review for relevance. Re-tag, archive, or confirm.

[ ] Inbox aging: captures with status: new older than 30 days.
 Scholar should consolidate or reject; aging captures suggest
 the consolidation cadence is too slow.
```

### On-demand

Scholar can trigger at any time with trigger keywords listed above.

### Post-major-change

After any of these events, suggest a health check:

- KB restructuring (moving files, renaming protocols).
- Major save with 5+ new patterns or knowledge entries.
- Index rebuild operations.
- Version upgrades to `memory.json` or `patterns.json` schema.

This is a behavioral guideline, not an automated trigger. Relies on pattern recognition during task completion.

---

## Part 4: References

### Protocols this document references

| File | What this protocol uses |
|---|---|
| `memory-protocol.md` | Retention thresholds, PRUNE-CHECK/EXECUTE rules, min-keep values |
| `CRITICAL-FILE-PROTECTION.md` | Safety rails for destructive operations |
| `Intelligence/learning-loop.md` | Consolidation status checks, index rebuild (Step 9 Sync Validation Gate) |
| `Intelligence/intelligence-operations.md` | Knowledge quality gates, pattern application rules |
| `.roo/rules-hypatia/04-session-gates.md` | Destructive Action Gate procedure |
| `.roo/rules-hypatia/09-security.md` | Defense-in-depth rules, git sanitization |
| `inbox/SCHEMA.md` | Inbox capture format |

### Documents that reference this protocol

| File | Section |
|---|---|
| `.roo/rules-hypatia/10-skills-loading.md` | Protocol keyword map |
| `memory-protocol.md` | Pruning Operations (cross-reference) |
| `hypatia-kb/protocols/librarian-writing-rules.md § Active initiatives` | Vault maintenance Slope reference |

---

## Anti-Patterns

- Do not run CLEANUP-EXECUTE without HEALTH-CHECK first.
- Do not skip the Destructive Action Gate before any Part 2 step.
- Do not skip the verification pass (2i) after cleanup.
- Do not modify index files without reading the corresponding data file first.
- Do not run growth reduction (2e) without Scholar confirmation.
- Do not archive active projects without confirming status with the Scholar.
- Do not invent retention thresholds; use `memory-protocol.md` as source of truth.
- Do not treat this protocol as a replacement for save-time pruning (they complement).
- Do not auto-promote inbox captures during cleanup. consolidation requires Scholar's per-capture decision.

---

## Quick Reference

| Command | What it does |
|---|---|
| `health check` | Non-destructive audit, reports issues |
| `full maintenance` | Health check + cleanup with confirmation |
| `integrity check` | Index-to-data sync verification only |
| `cleanup` | Execute cleanup on previously identified issues |
| `inbox triage` | Surface inbox captures for Scholar's consolidation decisions |

---

*Prevention through regular maintenance beats emergency cleanup. The Hypatia ecosystem ships empty and grows through deliberate consolidation. Run maintenance to verify the pipelines wire correctly during early months, then more substantively as usage accumulates real data.*
