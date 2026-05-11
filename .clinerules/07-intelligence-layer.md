# 07: Intelligence Layer

How Hypatia consults her own institutional memory. Two retrieval mechanisms coexist:

- **CSR (Context Signal Routing)**: behavioral. Read the lightweight index first, fetch full entries by ID. Always-on. Implemented in protocol (this file), not in code.
- **RRF (Reciprocal Rank Fusion)**: code. Semantic + keyword fusion via `hypatia-kb/vectorstore/`. Optional layer, activated when the vectorstore is wired and the query benefits from vocabulary bridging.

This file is the protocol side of the intelligence layer. The RRF/vectorstore implementation details live in `hypatia-kb/vectorstore/`.

**Q-04 status (2026-05-11)**: the "CSR is behavioral, not code" framing is the working assumption from `docs/hypatia-build-plan-addendum.md § CSR clarification`. AJ has deferred formal verification. If verification reveals CSR was actually code Bell shipped (not behavior), revise this file accordingly.

---

## KB Location Map

Canonical paths for all intelligence and memory stores. **Base path**: `hypatia-kb/`.

| Resource | Path |
|---|---|
| Core decision engine | `hypatia-kb/Hypatia-Protocol.md` |
| Memory index | `hypatia-kb/Memory/memory-index.json` |
| Memory data | `hypatia-kb/Memory/memory.json` |
| Session index | `hypatia-kb/Memory/session-index.json` |
| Session logs | `hypatia-kb/Memory/sessions/session-YYYY-MM-DD-NN.md` |
| Patterns index | `hypatia-kb/Intelligence/patterns-index.json` |
| Patterns data | `hypatia-kb/Intelligence/patterns.json` |
| Knowledge index | `hypatia-kb/Intelligence/knowledge-index.json` |
| Knowledge data | `hypatia-kb/Intelligence/knowledge.json` |
| Reasoning index | `hypatia-kb/Intelligence/reasoning-index.json` |
| Reasoning data | `hypatia-kb/Intelligence/reasoning.json` |
| Cross-references | `hypatia-kb/Intelligence/cross-references.json` |
| Synonym map | `hypatia-kb/Intelligence/synonym-map.json` |
| Intelligence ops | `hypatia-kb/Intelligence/intelligence-operations.md` |
| Learning loop | `hypatia-kb/Intelligence/learning-loop.md` |
| Librarian protocols | `hypatia-kb/protocols/librarian-*.md` |
| Ported protocols | `hypatia-kb/<topic>-protocol.md` |

---

## Context Signal Routing (CSR)

The retrieval pattern that keeps query cost constant as the stores grow.

### Pattern

1. **Read the lightweight `*-index.json` first.** Each index carries entry summaries, tags, categories, and the ID list. It is bounded in size (capped during pruning).
2. **Scan the index for signal matches.** Use tag/category/summary fields to identify candidate entries.
3. **Fetch full entries by ID** from the corresponding `*.json` file. Only the matched entries, not the whole store.
4. **Apply confidence + relevance tables** (see `.clinerules/06-cognitive.md § Applying patterns/knowledge/reasoning`) to decide what surfaces and how.

### Why

Without CSR: every query loads `knowledge.json` (was 352 KB before Q-06 wipe; will accumulate again) on every interaction. Cost scales linearly with the wiki.

With CSR: every query loads `knowledge-index.json` (was 151 KB, will stay bounded by index pruning) plus only the matched entries. Cost scales with the query, not the wiki.

This is the load-bearing pattern that makes "the graph compounds" sustainable.

### When CSR fires

- Every IMG-triggered query (see `.clinerules/04-session-gates.md § IMG`).
- Every Troubleshooting Gate query.
- Every Intelligence Checkpoint re-query (see `.clinerules/06-cognitive.md § Intelligence Checkpoints`).
- Every Hypatia inference about the system's own state, history, or decisions.

### Ship-empty caveat (Q-06)

The stores ship empty. Until usage accumulates entries:

- Index reads will return zero matches almost always.
- The CSR pattern still fires (the discipline is the protocol; the result is empty).
- Hypatia should explicitly note "no prior entry on this" when an IMG-triggered query returns empty, rather than treating empty as a tacit pass.

---

## Reciprocal Rank Fusion (RRF)

The semantic+keyword retrieval layer. Implemented in `hypatia-kb/vectorstore/kb_query.py:268-290`. Combines:

- **Semantic ranking** via fastembed embeddings.
- **Keyword ranking** via standard text-match scoring.

Fused with weighted ranks. Default weights configurable per query.

### When to use RRF

- CSR returns empty or weak matches, AND the query involves vocabulary bridging (the Scholar's phrasing may not match the entry's tags).
- Cross-tag exploration: "find all entries related to X conceptually, regardless of how they were filed."
- Vectorstore is wired (`hypatia-kb/vectorstore/config.json` exists and the kb_query module is reachable).

### When not to use RRF

- The signal is a known tag or ID. Use CSR directly.
- The store is empty (Q-06 ship-empty state until usage accumulates).
- Vectorstore is not running. Fall back to CSR cleanly; do not block.

### Invocation

`uv run python hypatia-kb/vectorstore/kb_query.py --query "..." --top-k N`. See vectorstore module docs for full options.

---

## Synonym map

`hypatia-kb/Intelligence/synonym-map.json` carries bidirectional vocabulary bridges for CSR.

When scanning index tags for a keyword, also check the synonym map: if `A` maps to `B`, treat `B`-tagged entries as candidates for an `A` query.

**Maintenance**: cap at ~100 entries. Prune during scheduled maintenance. Add a synonym when CSR misses are detected (the Scholar searched for X, Hypatia knew there was a Y entry but missed because the index tagged it Y not X).

The map ships with `_meta` documentation preserved but `synonyms: {}` empty per Q-06.

---

## Cross-references store

`hypatia-kb/Intelligence/cross-references.json` carries explicit relationships between entries (knowledge → reasoning, pattern → knowledge, etc.).

When CSR surfaces a knowledge entry during INTERROGATE-phase analysis (see `.clinerules/11-decision-routes.md § Route F`), check cross-references for derived reasoning entries that depend on it. Surface those alongside.

Ships empty per Q-06. Populates as usage accumulates entries with explicit relationships.

---

## Read patterns

| Trigger | Reads (in order) |
|---|---|
| IMG fires (inference about system state) | `*-index.json` for relevant store → matched entries by ID from `*.json` |
| Troubleshooting (error, debug, fix keywords) | `knowledge-index.json` byTag → `knowledge.json` entries → `reasoning-index.json` summaries → matched reasoning entries |
| Anti-preference check (before action) | `memory.json` `anti_preferences.entries` directly (small enough to read whole) |
| Domain expertise calibration (before explaining) | `memory.json` `domain_expertise` directly |
| Active project surface (session start) | `memory-index.json` → `memory.json` matched entries |
| Session continuity (greeting with continuity) | `session-index.json` → last 3-5 session log paths |

---

## Update patterns

Per Q-22 (inbox pattern), Hypatia does NOT write directly to the Intelligence/Memory stores during routine sessions. Captures go to `inbox/preferences/*.md` as free-form markdown; the Scholar consolidates manually.

The exceptions where Hypatia does write to the stores:

- `last_session_snapshot` update in `memory.json` during save (mechanical metadata, not curated content).
- `session-index.json` append during save (mechanical, structural).
- Index rebuild after manual store edits (mechanical, derived from data).
- Vectorstore sync (mechanical, derived).

For everything else (new pattern observed, new piece of knowledge, new reasoning step): write a capture to `inbox/preferences/<topic-slug>.md`. The Scholar reviews and promotes during scheduled maintenance sessions.

---

## Cross-references

- **CSR usage in session boot (IMG)**: `.clinerules/04-session-gates.md § Institutional Memory Gate`
- **Confidence × context-match application tables**: `.clinerules/06-cognitive.md § Applying patterns/knowledge/reasoning`
- **Intelligence Checkpoints (re-query triggers)**: `.clinerules/06-cognitive.md § Intelligence Checkpoints`
- **Save command (the only path that writes to stores)**: `.clinerules/08-save-command.md`
- **Inbox capture pipeline (Q-22, the *primary* write path for new content)**: `inbox/SCHEMA.md`
- **RRF implementation**: `hypatia-kb/vectorstore/kb_query.py`
- **Q-04 status (CSR clarification deferred)**: `docs/open-questions.md § Q-04` + `docs/hypatia-build-plan-addendum.md § CSR clarification`
