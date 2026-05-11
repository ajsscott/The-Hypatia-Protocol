# Learning Loop

**Purpose**: Consolidation methodology. How captures in `inbox/preferences/*.md` get promoted (or rejected) into the canonical intelligence stores (`patterns.json`, `knowledge.json`, `reasoning.json`) and memory store (`memory.json`).
**Last Updated**: 2026-05-11 (Hypatia adaptation; substantially restructured from Bell's save-auto framing)
**Trigger Keywords**: consolidate, learning loop, promote inbox, intelligence consolidation, capture review

---

## Scope and context

Bell's learning-loop ran AUTOMATICALLY during the save command (Parts 3a/3b/3c/3d). For Hypatia, the inbox boundary moved consolidation OFF the save path and INTO Scholar-driven maintenance sessions.

This file holds the consolidation methodology: how to look at inbox captures, decide which become canonical entries, and write them with quality gates applied. The learning loop is invoked when the Scholar runs `inbox triage` or similar maintenance commands.

**Save vs. consolidate**:
- **Save** (`.roo/rules-hypatia/08-save-command.md`): records the session, stages inbox files, runs vectorstore sync. Does NOT promote captures to stores.
- **Consolidate** (this file): Scholar-invoked maintenance step. Reviews inbox captures, applies quality gates, promotes survivors to canonical stores, rejects others (with rationale captured).

---

## Consolidation flow

For each `inbox/preferences/*.md` capture with `status: new`:

1. **Read the capture** end-to-end. Frontmatter + body.
2. **Classify** by `candidate-type` field (preference / pattern / knowledge / reasoning / unsure).
3. **Apply Quality Gates** (see below).
4. **Dedup-check** against existing entries in the target store via CSR.
5. **Decide**:
   - **Promote**: write a new entry to the target store; update index; mark capture `status: consolidated`.
   - **Reject**: mark capture `status: rejected` with `rejection-reason:` field. Capture stays in inbox as a record of Hypatia over-inferring.
   - **Defer**: leave `status: new`; revisit next maintenance.
6. **Update indexes** (rebuild from source).
7. **Move consolidated captures** to `inbox/preferences/_consolidated/` (or delete; Scholar's call).

---

## Capture taxonomy

Each capture classifies into one of these categories. Use the `candidate-type` field in capture frontmatter; this taxonomy is the canonical type list.

| Type | Goes to | Definition |
|---|---|---|
| **preference** | `memory.json` `memories` | Scholar likes/dislikes ("I prefer atomic Trees over composite ones") |
| **decision** | `memory.json` `memories` | Choice made ("Decided to use Roo Code") |
| **correction** | `memory.json` `memories` | Fixed misunderstanding |
| **learning** | `memory.json` `memories` | Discovered fact or technique |
| **critical_safety** | `memory.json` `memories` | Must-not-violate rule |
| **system** | `memory.json` `memories` | System configuration or state |
| **pattern (approach)** | `patterns.json` | How Scholar tends to approach a class of problem |
| **pattern (failure)** | `patterns.json` | A failure mode that recurs; every failure pattern must answer "what to do instead" |
| **knowledge** | `knowledge.json` | Factual claim (must have citation or evidence) |
| **reasoning (recorded)** | `reasoning.json` | Stated reasoning the Scholar walked through |
| **reasoning (synthesized)** | `reasoning.json` | Derived from cross-source analysis (Hypatia's synthesis during maintenance) |
| **commitment** | `memory.json` `commitments` | Promise the Scholar made; tracked for deadlines |
| **anti-preference** | `memory.json` `anti_preferences` | Explicit "don't do X" |

---

## Consolidation pattern A: preferences and decisions

For captures with `candidate-type: preference` (or decision, correction, learning, critical_safety, system):

1. Apply Quality Gates.
2. Dedup against `memory.json` `memories`. Read field: `entry.content`. Normalize (lowercase, trim). Exact match → update existing entry's `accessCount` + `lastAccessed`, skip writing new.
3. If unique: write new entry per Memory Entry Schema (see § Entry Schemas).
4. Update `memory-index.json` `byType`, `byTag`, `summaries`, `recentIds`.
5. Update `stats.totalEntries`, `stats.activeEntries`, `stats.nextId`.

---

## Consolidation pattern B: patterns

For captures with `candidate-type: pattern`:

1. Apply Quality Gates.
2. Failure-pattern check: if the capture is a failure pattern, verify it answers "what to do instead." If not, reject with that rationale.
3. Dedup against `patterns.json` entries. Read field: `entry.content`. Normalize. Exact match → update existing; >80% word overlap → log "similar exists" and reject (or merge, Scholar's call).
4. If unique: write new entry per Pattern Entry Schema.
5. Tag Quality Gate: minimum 2 tags, at least one domain-specific, isolation check.
6. Rebuild `patterns-index.json` from `patterns.json` (full rebuild, idempotent at <300 entries).

---

## Consolidation pattern C: knowledge

For captures with `candidate-type: knowledge`:

1. Apply Quality Gates.
2. Verify confidence ≥ 0.7 (knowledge requires evidence; below this threshold, reject or reroute to reasoning).
3. Dedup against `knowledge.json` entries.
4. If unique: write new entry per Knowledge Entry Schema. Ensure citation source is named.
5. Tag Quality Gate.
6. Rebuild `knowledge-index.json`.

---

## Consolidation pattern D: reasoning

For captures with `candidate-type: reasoning`:

Three sub-types:

### D-recorded

Stated reasoning the Scholar walked through during a session.

1. Apply Quality Gates.
2. Dedup-check.
3. If unique: write per Reasoning Entry Schema with `provenance: "recorded"`.

### D-synthesized

Derived from cross-source analysis Hypatia performed during maintenance.

1. Re-read 3+ recent session logs.
2. Apply synthesis prompts (see § Synthesis Prompts below).
3. Filter via three-check gate (see § Three-check filter).
4. Survivors get written with `provenance: "synthesized"`.

### D-cross-session

When 3+ sessions have elapsed since the last cross-session consolidation:

1. Load recent session logs (last 3-5).
2. Run cross-session prompt: "what concepts surfaced across multiple sessions that didn't get atomized?"
3. Filter via three-check gate.
4. Survivors get written with `provenance: "cross_session"`.
5. Update `last_cross_session_synthesis` in `memory.json`.

---

## Save-time discovery capture

When save operations themselves surface novel findings (duplicates found, schema drift corrected, index integrity gaps, stale references cleaned, merge decisions made), these become candidates for inbox captures.

- **Max 3 captures per save** (prevents save bloat).
- **Quality gate**: only genuinely novel discoveries. "Updated an index" is not a discovery. "Found that schema X drifts because of Y" is.
- **Route to inbox** as `candidate-type: knowledge` or `pattern`. NOT directly to stores (per `.roo/rules-hypatia/08-save-command.md`).

---

## Quality Gates

**Run before promoting any inbox capture to a canonical store.**

### Content length

| Type | Target | Action if over |
|---|---|---|
| Pattern (preference / approach) | 10-400 chars | Condense, or promote with `_needs_trim: true` |
| Pattern (failure) | 10-400 chars | Condense, or promote with `_needs_trim: true` |
| Knowledge | 20-600 chars | Condense, or promote with `_needs_trim: true` |

`_needs_trim` entries are trimmed during scheduled maintenance, not during the consolidation itself.

### Failure pattern prevention rule

Every new failure pattern must answer "what to do instead."

- ✗ Bad: "Skipped validation step."
- ✓ Good: "Skipped validation step. Read current state before modifying."

### Specificity

No vague terms ("good", "better", "quality"). Rewrite with specifics.

### Deduplication

Before adding any new entry:

1. Read field: `entry.content` for comparison.
2. Normalize text (lowercase, trim).
3. Exact match → skip; update existing entry's access fields.
4. > 80% word overlap → log "similar exists"; consider merge or reject.

### Confidence assignment

| Evidence type | Base confidence |
|---|---|
| `explicit_statement` (Scholar explicit) | 0.90 |
| `user_correction` (Scholar corrected Hypatia) | 0.85 |
| `user_acceptance` (Hypatia proposed, Scholar accepted) | 0.70 |
| `observed_behavior` (inferred from pattern) | 0.55 |
| `single_instance` (one occurrence only) | 0.40 |

Knowledge entries require confidence ≥ 0.7. Pattern entries can land below if the capture rationale justifies it.

### Tag Quality Gate

Run after tag assignment for every new entry:

1. **Minimum 2 tags** per entry.
2. **No overly generic single-word tags** ("code", "work", "thing"). Tags route queries; they should be specific.
3. **At least one domain-specific tag** (not just category-level like "technical" or "process").
4. **Isolation check**: does this entry share at least one tag with an existing entry? Zero overlap → flag: "this entry shares no tags with existing entries; isolated entries are harder to find via CSR." Flag, not blocker; some entries are genuinely unique.

### Synonym-aware retrieval

When scanning index tags during retrieval, also consult `Intelligence/synonym-map.json`. If a query keyword matches a synonym map key, expand the search to mapped synonyms. The map is bidirectional: A → B implies B → A.

Maintenance: add new entries when CSR misses are detected. Cap at ~100. Prune during monthly maintenance.

---

## Synthesis prompts (for D-synthesized reasoning)

When deriving reasoning entries from cross-session content, apply these prompts during consolidation:

- **P1 (Intent prompt)**: "What was the underlying motivation across these sessions? Phrase as the Scholar's question, not the answer."
- **P5 (Counter-source prompt)** (conditional, when contradictory sources surfaced): "What's the contradicting claim? Which source does each side cite?"
- **P6 (Sharpen prompt)**: "Rewrite this so the reuse signal is recognizable. Future Hypatia should match it on the shape of the problem, not the topic."
- **P7 (Distillation prompt)**: "What's the single sentence that captures the reusable insight? Discard everything that's just narrative."
- **P8 (Three-check filter)**: see below.

---

## Three-check filter

Before writing any synthesized reasoning entry, run all three:

1. **Reusable?** Will Future Hypatia retrieve this via problem-shape match, not topic match?
2. **Distinct from knowledge?** Knowledge entries are facts; reasoning entries are derived conclusions. If this is a fact, route to knowledge instead.
3. **Has a clear reuse signal?** A phrase or motivation pattern that future queries can match. If you can't write the reuse signal, the entry isn't ready.

Survive all three → write. Fail any → reject and capture rationale in the inbox.

**SYNTH ZERO-CHECK**: if a consolidation pass would write 0 synthesized survivors, STOP. Name each prompt run. State what each surfaced (even if "nothing"). Then write 0 with prompt outputs as justification. Missing outputs = incomplete step.

---

## Failure outcome tracking

During consolidation, after pattern promotion (Pattern B), run one retrospective question (re-read recent session logs before answering):

> "Did any failure pattern prevent a mistake this session, or has any pattern been observed to fail to prevent its intended mistake?"

If yes: update the pattern entry's `outcome_count` (prevention) or surface that the pattern needs revision (failed to prevent). This is the feedback signal that keeps patterns calibrated.

---

## Entry Schemas

### Memory entry

```json
{
  "id": "mem-NNN",
  "type": "preference|decision|correction|learning|critical_safety|system",
  "content": "<10-300 chars>",
  "context": "<5-100 chars: why this matters>",
  "created": "YYYY-MM-DD",
  "lastAccessed": "YYYY-MM-DD",
  "accessCount": 0,
  "confidence": 0.9,
  "tags": ["tag1", "tag2"]
}
```

### Pattern entry

```json
{
  "id": "pat-NNN",
  "category": "approach|failure",
  "content": "<10-400 chars>",
  "tags": ["tag1", "tag2"],
  "confidence": 0.85,
  "created": "YYYY-MM-DD",
  "lastAccessed": "YYYY-MM-DD",
  "accessCount": 0,
  "outcome_count": {"prevented": 0, "missed": 0}
}
```

### Knowledge entry

```json
{
  "id": "know-NNN",
  "content": "<20-600 chars>",
  "tags": ["tag1", "tag2"],
  "confidence": 0.85,
  "source": "<citation or evidence reference>",
  "created": "YYYY-MM-DD",
  "lastAccessed": "YYYY-MM-DD",
  "accessCount": 0
}
```

### Reasoning entry

```json
{
  "id": "reason-NNN",
  "intent": "<one-sentence question framing>",
  "reuse_signal": "<phrase or motivation pattern for retrieval>",
  "content": "<the derived conclusion>",
  "tags": ["tag1", "tag2"],
  "confidence": 0.80,
  "provenance": "recorded|synthesized|cross_session",
  "derived_from": ["source-id-1", "source-id-2"],
  "created": "YYYY-MM-DD",
  "lastAccessed": "YYYY-MM-DD",
  "accessCount": 0
}
```

---

## Index rebuild (after any store write)

Indexes are derived from store content. Rebuild from source after each consolidation pass (not incremental):

1. Read all entries from the source store.
2. For each, build: `byTag`, `byCategory` (or `byType`, `byProvenance`), `byConfidence` (where applicable), `summaries` (first 150 chars of content).
3. Preserve: `recentIds` (prepend new/updated IDs, slice to 20).
4. Set `stats` (totalEntries, activeEntries, nextId).
5. Write complete index.

**Why rebuild not incremental**: incremental updates drift under context pressure. Full rebuild is idempotent and self-correcting. At <300 entries per store, cost is negligible.

### Validation spot-check

After rebuild:

1. Count check: index `stats.totalEntries` == actual entry count.
2. Spot check: pick 3 entries, verify tags appear in `byTag`.
3. Confidence check: `byConfidence` sums to total.

On failure: re-run rebuild.

---

## Failure modes

- **Skipped quality gates**: writes ungated entries; degrades the wiki over time.
- **Skipped dedup check**: creates duplicate entries that fragment retrieval.
- **Auto-consolidation during save**: violates the inbox boundary; should be Scholar-invoked during maintenance.
- **Empty justification for "0 survivors"**: SYNTH ZERO-CHECK exists to catch this; never write 0 without named prompt outputs.
- **Incremental index updates**: drift under context pressure; always rebuild.
- **Promoting captures without reading them**: the consolidation step REQUIRES reading the capture body, not just trusting frontmatter `candidate-type`.

---

## Cross-references

- **Save command (the path that stages inbox but does NOT auto-consolidate)**: `.roo/rules-hypatia/08-save-command.md`
- **Inbox capture format (input to consolidation)**: `inbox/SCHEMA.md`
- **Memory protocol (CAPTURE / CONSOLIDATE operations)**: `memory-protocol.md`
- **Maintenance protocol (where consolidation triggers fire)**: `maintenance-protocol.md`
- **Intelligence layer (CSR routing during dedup and retrieval)**: `.roo/rules-hypatia/07-intelligence-layer.md`
- **Cognitive Application tables (how consolidated entries are surfaced)**: `.roo/rules-hypatia/06-cognitive.md § Applying patterns, knowledge, reasoning`
- **Critical file protection (Tier 1 destructive treatment of direct store writes)**: `../CRITICAL-FILE-PROTECTION.md`

---

*Consolidation is curation, not accretion. The Scholar's review is the load-bearing step. Quality gates exist because the alternative is a wiki that grows faster than it gets smarter.*
