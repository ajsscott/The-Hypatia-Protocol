# Intelligence Operations

**Purpose**: Detection, application, correction, and removal mechanics for the intelligence stores. This file holds operational specifics; `learning-loop.md` holds the consolidation methodology.
**Last Updated**: 2026-05-11 (Hypatia adaptation; substantially thinned from Bell's 446 L original)
**Trigger Keywords**: intelligence, pattern detection, knowledge detection, apply pattern, apply knowledge, correction cascade, removal cascade

---

## Scope and context

This file covers:

- How to **detect** when content is intelligence-worthy (during sessions, surfaces as inbox candidates).
- How to **apply** intelligence at runtime (confidence × context-match tables).
- How to **correct** when stale information is surfaced.
- How to **remove** entries with cascade safety.

It does NOT cover (see other files):

- **Consolidation methodology** (capture → quality gates → promote): `learning-loop.md`.
- **CSR retrieval pattern**: `.clinerules/07-intelligence-layer.md`.
- **Cognitive integration** (when intelligence fires during reasoning): `.clinerules/06-cognitive.md § Applying patterns, knowledge, reasoning`.
- **Save command flow** (records but doesn't auto-promote): `.clinerules/08-save-command.md`.

---

## Part 1: Quality standards (shared across stores)

### Content specificity

**Good** (specific, actionable):
- "Use jq for complex JSON transforms instead of replace_in_file"
- "Scholar prefers atomic Trees over composite ones"
- "Obsidian-linter overwrites multi-line YAML if Topics: and topics: coexist"

**Bad** (vague, not actionable):
- "Likes good code"
- "Prefers quality"
- "Linter is useful"

### Content length

| Type | Target | Note |
|---|---|---|
| Pattern (preference / approach) | 10-400 chars | "Prefers comprehensive documentation over minimal" |
| Pattern (failure) | 10-400 chars | "Skipped validation step. Read current state before modifying." |
| Knowledge content | 20-600 chars | Citation required |
| Context field | 5-30 chars | "Vault refactor" |

### Confidence assignment

| Evidence type | Base confidence |
|---|---|
| Scholar explicitly states | 0.90 |
| Scholar corrects approach | 0.85 |
| Verified in primary source | 0.85 |
| Scholar accepts suggestion | 0.70 |
| Observed behavior (3+ times) | 0.70 |
| Single observation | 0.60 |
| Inferred from context | 0.50 |

### Tag derivation

Extract 2-5 tags from content + context:

1. **Domain keywords** (zettelkasten, vault, librarian, python, vectorstore).
2. **Action keywords** (validation, refactor, optimization, ingest).
3. **Tool/tech names** (obsidian, ruff, fastembed, dataview).

**Don't tag**: common words ("the", "is", "for"), overly broad terms ("good", "better").

### Deduplication

Before adding a new entry:
1. Exact match on content → skip; increment `accessCount` on existing.
2. > 80% word overlap → skip; consider updating existing.
3. Same concept, different wording → merge into existing with better wording.

---

## Part 2: Pattern operations

### Detection signals (during sessions)

When the following signals surface during a session, capture to `inbox/preferences/*.md` for Scholar consolidation. Hypatia does NOT write directly to `patterns.json`.

| Signal | Type | Base confidence |
|---|---|---|
| "I prefer X" / "I like X" / "Always use X" | explicit preference | 0.90 |
| "No, do it this way" / corrects approach | correction | 0.85 |
| Chooses option A when given A/B/C | acceptance | 0.70 |
| Same choice 3+ times without prompting | observed behavior | 0.60 |
| "Don't do X" / rejects suggestion | negative (anti-preference) | 0.80 |
| Cognitive cycle: framework worked for problem type | approach | 0.80 |

### When NOT to capture patterns

- One-off situational choices.
- Contradicts existing high-confidence pattern (ask first, then capture as correction if confirmed).
- Inferred confidence < 0.5.
- Already exists in `patterns.json` (CSR-check before capturing).

### Pattern categories

| Category | Prefix | What it captures |
|---|---|---|
| preference | `pref` | Tool/tech choices, formatting, organizational style |
| approach | `appr` | Problem-solving methods that work |
| failure | `fail` | What to avoid and why |
| workflow | `proc` | Recurring task sequences and processes |
| communication | `comm` | Tone, verbosity, formality, response style |
| domain_practice | `appr` | Domain-specific conventions and standards (vault, zettelkasten) |
| tool_use | `appr` | Tool-specific behaviors, quirks, effective usage |
| collaboration | `appr` | Working style, review preferences, feedback patterns |

These are starter categories. Add domain-specific categories as they emerge during maintenance consolidation.

### Applying patterns at runtime

See `.clinerules/06-cognitive.md § Applying patterns`. Summary:

| Confidence | Context match | Action |
|---|---|---|
| > 0.8 | High | Apply automatically, no announcement |
| > 0.8 | Medium | Apply with brief mention |
| 0.5–0.8 | High | Suggest: "Based on a prior pattern, [X]" |
| 0.5–0.8 | Medium | Note if relevant |
| < 0.5 | Any | Do not surface |

### Failure pattern handling

Always check failure patterns before executing. If match:
- Confidence > 0.7: warn before proceeding.
- Confidence 0.5–0.7: mention the risk.
- Confidence < 0.5: note internally only.

---

## Part 3: Knowledge operations

### Detection signals (during sessions)

Capture to `inbox/preferences/*.md` when:

- Scholar states a fact about how a system works ("The linter runs lint-on-save across all open files, not just the active one").
- A primary source confirms a claim Hypatia previously held with uncertainty.
- Debugging surfaces a non-obvious cause-effect relationship ("Multi-line YAML duplicate keys cause obsidian-linter to corrupt frontmatter").
- Tool behavior contradicts documentation ("`replace_in_file` fails silently on JSON files > 400 lines").

### When NOT to capture knowledge

- Inferred without primary source AND confidence < 0.7.
- Already exists in `knowledge.json` (CSR-check first).
- Genuinely uncertain. Capture as `candidate-type: unsure` and let the Scholar route during consolidation.

### Applying knowledge at runtime

See `.clinerules/06-cognitive.md § Applying knowledge`. Summary:

| Confidence | Relevance | Action |
|---|---|---|
| > 0.8 | Direct match | Surface proactively |
| > 0.8 | Related | Mention if helpful |
| 0.7–0.8 | Direct match | Surface if asked or clearly relevant |
| < 0.7 | Any | Do not surface |

**Claim-match verification** before using a knowledge entry to flag an issue: verify the entry addresses the *specific claim*, not just the same topic. "Same topic" is not "same claim."

---

## Part 4: Reasoning operations

### Detection signals (during sessions)

Capture when:

- Scholar walks through reasoning aloud, especially across multiple steps ("first this, then this, which means...").
- Hypatia's own synthesis combines facts + context in a way that's reusable for similar future problems.
- Cross-source analysis reveals a connection or contradiction between Trees/Seeds.

### Reuse signal (CRITICAL)

Reasoning entries are retrieved by **problem shape and motivation pattern**, not by topic. The `reuse_signal` field is what makes future retrieval possible.

Examples:
- Topic: "RAG retrieval"; reuse signal: "When multi-source agreement is required but sources disagree on a sub-claim, surface the contradiction explicitly rather than picking one."
- Topic: "git workflow"; reuse signal: "When the cost of asking is a message and the cost of acting wrong is irreversible, ask."

If a reuse signal can't be written for an entry, the entry isn't ready for reasoning; reroute to knowledge.

### Applying reasoning at runtime

See `.clinerules/06-cognitive.md § Applying reasoning`. Intent-aware matching:

| Match type | Signal | Action |
|---|---|---|
| Reuse-signal + intent match | Strong | Surface proactively: "We figured out before that..." |
| Reuse-signal only | Medium | Mention if relevant |
| Intent match only | Weak | Internal note; do not surface |

---

## Part 5: Memory integration

Memory and Intelligence are distinct stores with complementary roles:

- **Memory (`memory.json`)**: granular facts and decisions specific to the Scholar (preferences, project state, commitments).
- **Intelligence (`Intelligence/*.json`)**: aggregated learnings (patterns, knowledge, reasoning) that generalize across contexts.

Both flow through Q-22 inbox-then-consolidate. The capture's `candidate-type` determines target store at consolidation time.

### Cross-references

Cross-references between intelligence and memory entries live in `cross-references.json`. When a knowledge entry is consulted (e.g., during INTERROGATE phase of Route F), check cross-references for related reasoning entries and surface them together.

---

## Part 6: Voice integration

Intelligence output passes through Hypatia's voice register (`.clinerules/02-voice.md`).

- Pattern application: brief, declarative. "Based on a prior pattern, [X]." not "Hmm, I noticed you've done this before, maybe we should..."
- Knowledge surface: cite the entry's source. "Per [source], X is true." Not "I remember reading that X."
- Reasoning surface: name the reuse signal. "We figured out before that [reuse_signal]. The current situation fits because [matching context]."
- Failure pattern warning: explicit + actionable. "Heads up: failure pattern `fail_NNN` says [what to avoid]. Suggest [what to do instead]."

---

## Part 7: Correction cascade

**Trigger**: Scholar corrects a fact. "That's wrong, it's actually X." Or Scholar updates information that contradicts existing entries.

**Why cascade**: a single-entry fix leaves stale data in other entries. The same fact may exist in knowledge, reasoning, patterns, and session logs. Fixing one and leaving the rest means the stale info resurfaces via CSR or semantic search.

### Behavior

1. **Acknowledge** the correction without defensiveness.
2. **Search all stores** (knowledge, reasoning, patterns, memory) for the stale claim, both CSR and semantic search.
3. **Fix all instances found**; don't stop at the first match.
4. **Never modify session logs**; session history is historical record. Annotate only with a forward-pointing note.
5. **Update indexes** after corrections are applied.
6. **Capture** the correction itself to inbox as `candidate-type: correction` for memory promotion.

### Anti-Patterns

- Fixing one entry and saying "updated" without checking for other instances.
- Modifying session logs (historical record is preserved).
- Skipping the search because "I think that's the only entry."

---

## Part 7b: Removal cascade

**Trigger**: Deleting, merging, or deduplicating intelligence entries during maintenance consolidation.

**Why cascade**: removing an entry without cleaning references creates broken links across the system. Other entries may reference the removed ID in indexes, cross-references, or derived conclusions.

### Behavior

1. **If merging near-duplicates**: combine tags from both entries into the kept entry before removing the duplicate.
2. **Remove the entry** from its store.
3. **Clean all references** across all stores and indexes. The removed ID must not appear anywhere.
4. **Update counts** to reflect new totals.
5. **Note the removal** in the consolidation pass log.

### Anti-Patterns

- Removing from store without checking for references elsewhere.
- Merging near-duplicates without combining tags first.
- Forgetting to update `cross-references.json` after a removal.

---

## Quick reference

| Operation | When | Where |
|---|---|---|
| Detect pattern | During session, on behavioral signal | Capture to `inbox/preferences/*.md` |
| Detect knowledge | During session, on fact statement | Capture to `inbox/preferences/*.md` |
| Detect reasoning | During session, on cross-step synthesis | Capture to `inbox/preferences/*.md` |
| Apply pattern | Pre-action check during routine work | Via CSR + confidence table |
| Apply knowledge | When directly relevant to current task | Via CSR + claim-match verification |
| Apply reasoning | When reuse signal matches problem shape | Via CSR + intent-aware matching |
| Correct stale entry | Scholar corrects a fact | Cascade across all stores |
| Remove entry | Maintenance consolidation | Cascade + index rebuild |

---

## Cross-references

- **Consolidation methodology (capture → promote)**: `learning-loop.md`
- **CSR routing pattern**: `.clinerules/07-intelligence-layer.md`
- **Cognitive application tables**: `.clinerules/06-cognitive.md § Applying patterns, knowledge, reasoning`
- **Save command (records but does NOT auto-promote)**: `.clinerules/08-save-command.md`
- **Memory protocol (capture-then-consolidate flow)**: `../memory-protocol.md`
- **Inbox capture format**: `../../inbox/SCHEMA.md`
- **Critical file protection (cascade safety on removal)**: `../CRITICAL-FILE-PROTECTION.md`

---

*Single source for intelligence operations. Data lives in JSON files; consolidation methodology lives in `learning-loop.md`; runtime application lives in `.clinerules/06-cognitive.md`.*
