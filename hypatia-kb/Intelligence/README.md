# Intelligence System

**Purpose**: Learning, adaptation, cognitive alignment, and knowledge accumulation.
**Last Updated**: 2026-05-11
**Pattern**: CSR (Context Signal Routing) for all data stores; RRF (Reciprocal Rank Fusion) for semantic+keyword fusion.

---

## Architecture

```
Intelligence/
├── patterns.json              # Behavioral patterns
├── patterns-index.json        # CSR routing index for patterns
├── knowledge.json             # Factual claims
├── knowledge-index.json       # CSR routing index for knowledge
├── reasoning.json             # Derived conclusions and analogies
├── reasoning-index.json       # CSR routing index for reasoning
├── cross-references.json      # Reverse lookup: pattern/knowledge → reasoning
├── synonym-map.json           # Synonym expansion for retrieval quality
├── intelligence-operations.md # Detection / application / correction / removal mechanics
├── learning-loop.md           # Consolidation methodology
└── README.md                  # This file
```

**Ship-empty** (Bell content wiped from all stores). Stores accumulate via the inbox-then-consolidate flow:

1. During sessions, Hypatia captures candidates to `inbox/preferences/*.md`.
2. During Scholar-driven maintenance, captures are reviewed and promoted to canonical stores via `learning-loop.md`.

---

## Data stores

| File | Captures | Schema in |
|---|---|---|
| `patterns.json` | Behavioral patterns: preferences, approaches, failure modes | `learning-loop.md § Entry Schemas` |
| `knowledge.json` | Factual claims: facts, solutions, tool behavior | `learning-loop.md § Entry Schemas` |
| `reasoning.json` | Derived conclusions: analogies, cross-source synthesis | `learning-loop.md § Entry Schemas` |
| `cross-references.json` | Reverse lookup: which reasoning entries depend on which patterns/knowledge | (rebuildable from `reasoning.json` `derived_from` field) |
| `synonym-map.json` | Bidirectional synonym map for query expansion | `_meta.usage` field |

Each data store has a corresponding `*-index.json` for CSR routing.

---

## Operational docs

| File | Covers |
|---|---|
| `intelligence-operations.md` | When to detect (signals during sessions), how to apply (confidence tables), correction cascade, removal cascade |
| `learning-loop.md` | Consolidation methodology (inbox → quality gates → canonical store), capture taxonomy, entry schemas, synthesis prompts |

---

## CSR (Context Signal Routing)

The retrieval pattern that keeps query cost constant as stores grow.

**Pattern**:
1. Read the lightweight `*-index.json` first.
2. Scan for signal matches via `byTag` / `byCategory` / `summaries`.
3. Fetch full entries by ID from the data store.
4. Apply confidence + relevance tables (see `.roo/rules-hypatia/06-cognitive.md`).

Full spec: `.roo/rules-hypatia/07-intelligence-layer.md`.

---

## RRF (Reciprocal Rank Fusion)

Code-level retrieval layer combining semantic + keyword rankings. Implemented in `../vectorstore/kb_query.py:268-290`.

Used when CSR returns empty or weak matches AND the query benefits from vocabulary bridging (Scholar's phrasing may not match entry tags).

---

## How content flows in

1. **Capture during sessions**: Hypatia writes free-form markdown observations to `inbox/preferences/<topic-slug>.md` per `inbox/SCHEMA.md`. Frontmatter specifies `candidate-type` (preference / pattern / knowledge / reasoning / unsure).

2. **Save command stages the captures**: per `.roo/rules-hypatia/08-save-command.md`, the save command `git add`s inbox files but does NOT promote to canonical stores.

3. **Maintenance consolidation**: Scholar invokes `inbox triage` or equivalent maintenance command. The flow per `learning-loop.md`:
   - Read each capture end-to-end.
   - Apply Quality Gates.
   - Dedup-check via CSR.
   - Decide: promote / reject / defer.
   - On promote: write canonical entry to target store; rebuild index.
   - On reject: mark `status: rejected` with `rejection-reason:`; capture stays in inbox as a record of over-inference.

4. **Application at runtime**: Hypatia consults stores via CSR during pre-action checks, troubleshooting, intelligence checkpoints, and Route F INTERROGATE. Confidence × context-match tables in `.roo/rules-hypatia/06-cognitive.md` govern when an entry surfaces.

---

## How content flows out (correction or removal)

### Correction cascade

When the Scholar corrects a fact, Hypatia:
1. Acknowledges.
2. Searches all stores (CSR + semantic) for the stale claim.
3. Fixes all instances; never modifies session logs.
4. Updates indexes.

Full procedure: `intelligence-operations.md § Part 7`.

### Removal cascade

When deduplicating or merging entries, Hypatia:
1. Combines tags from duplicates into the kept entry.
2. Removes the duplicate from its store.
3. Cleans all references across stores and indexes.
4. Updates counts.

Full procedure: `intelligence-operations.md § Part 7b`.

---

## Cross-references

- **Detection / application / correction mechanics**: `intelligence-operations.md`
- **Consolidation methodology (capture → promote)**: `learning-loop.md`
- **CSR pattern (the retrieval engine)**: `../../.roo/rules-hypatia/07-intelligence-layer.md`
- **Cognitive application (when entries surface during reasoning)**: `../../.roo/rules-hypatia/06-cognitive.md § Applying patterns, knowledge, reasoning`
- **Save command (records but does NOT auto-promote)**: `../../.roo/rules-hypatia/08-save-command.md`
- **Memory protocol (capture-then-consolidate flow)**: `../memory-protocol.md`
- **Inbox schema**: `../../inbox/SCHEMA.md`
- **RRF implementation**: `../vectorstore/kb_query.py`

---

*The intelligence stores compound through curation. Ship-empty; grow through deliberate consolidation; retrieve via CSR + RRF.*
