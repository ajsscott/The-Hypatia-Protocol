# Hypatia's Knowledge Base

**The brain.** Everything Hypatia knows, captures, and remembers lives here. This is the operational guide.

---

## Ecosystem map

| Layer | Location | What it does |
|---|---|---|
| **Kernel** | `.clinerules/` (11 files) | Identity, voice, anti-patterns, gates, tools, cognitive layer, intelligence layer, save command, security, skills-loading, decision routes |
| **Legacy decision-routing reference** | `Hypatia-Protocol.md` | Bell's original Routes A-F (superseded by `.clinerules/11-decision-routes.md`; retained for archaeology) |
| **Protocols** | `*.md` (13 files in this directory) | Domain-specific behavior (memory, maintenance, research, writing, etc.); keyword-triggered lazy-load |
| **Librarian protocols** | `protocols/librarian-*.md` (5 files + README) | Vault-specific librarian behavior migrated from TabulaJacqueliana CLAUDE.md (Phase 0) |
| **Intelligence** | `Intelligence/` | Three learning layers: patterns, knowledge, reasoning (ship empty; grow via inbox consolidation) |
| **Memory** | `Memory/` | Session logs, entity memory, project tracking (ship empty) |
| **Vectorstore** | `vectorstore/` | Hybrid semantic + keyword search over the KB. Source code git-tracked; artifacts rebuildable via `kb_vectorize.py` |
| **Benchmarks** | `Benchmarks/` | Self-testing artifacts inherited from Bell; may be deprecated or rebuilt in Phase 1.5 |

---

## Intelligence system

Three stores that compound over time:

| Store | File | What it captures |
|---|---|---|
| **Patterns** | `Intelligence/patterns.json` | Behavioral patterns: preferences, approaches, failure modes |
| **Knowledge** | `Intelligence/knowledge.json` | Factual claims: facts, solutions, tool behavior |
| **Reasoning** | `Intelligence/reasoning.json` | Derived conclusions: analogies, cross-store synthesis |

Each store has a lightweight index (`*-index.json`) for Context Signal Routing (CSR). Full entries loaded on-demand, not eagerly. See `.clinerules/07-intelligence-layer.md` for the CSR pattern.

Cross-references (`Intelligence/cross-references.json`) link entries across stores. Retrieving a pattern can surface the reasoning that explains it.

**Ship-empty**: at launch, all stores are empty. The Scholar consolidates from `inbox/preferences/*.md` captures during scheduled maintenance.

See `Intelligence/README.md` for architecture details and `Intelligence/learning-loop.md` for consolidation rules.

---

## Memory system

| File | Purpose |
|---|---|
| `Memory/memory.json` | Persistent memories, active projects, commitments, preferences, domain expertise levels |
| `Memory/memory-index.json` | CSR routing index |
| `Memory/session-index.json` | Session fingerprints for context-aware greetings and continuity |
| `Memory/sessions/session-*.md` | Full session logs (created by save command) |

See `memory-protocol.md` for CRUD operations and capture-then-consolidate flow.

---

## Protocols (this directory)

13 domain protocols + 5 librarian protocols, keyword-triggered via `.clinerules/10-skills-loading.md`:

### Domain protocols

| Protocol | Triggers |
|---|---|
| `memory-protocol.md` | memory, remember, recall, capture, save memory, prune |
| `maintenance-protocol.md` | maintenance, cleanup, health check, integrity, housekeeping |
| `planning-protocol.md` | plan, roadmap, estimate, scope, breakdown, milestone |
| `research-protocol.md` | research, investigate, source, citation, paper, literature |
| `writing-protocol.md` | write, draft, compose, edit, polish, narrative |
| `summarization-protocol.md` | summarize, distill, condense, tldr, recap, minutes |
| `problem-solving-protocol.md` | diagnose, root cause, decompose, trace, debug |
| `proactive-offering-protocol.md` | proactive, offer, suggest, anticipate, surface, flag |
| `prompt-enhancement-protocol.md` | enhance-prompt, clarify-request, refine-prompt, ambiguous |
| `development-protocol.md` | code, develop, programming, refactor, implement, test |
| `customization-protocol.md` | customize, personalize, configure, tune |
| `executive-communication-protocol.md` | executive, stakeholder, leadership (edge case for Hypatia) |
| `security-protocol.md` | security, threat, credentials, secrets, sanitize, pii |

### Librarian protocols (Phase 0 migration)

| Protocol | Triggers |
|---|---|
| `protocols/librarian-role.md` | librarian, vault, zettelkasten, Tabula, curate, ingest, query, lint |
| `protocols/librarian-vault-structure.md` | vault structure, Tabula, folders, Seeds, Trees, Mountains, Bases |
| `protocols/librarian-note-schemas.md` | schema, atomic note, frontmatter, naming, tag, kind, content_type, citekey |
| `protocols/librarian-tooling.md` | Bases, plugin, YOLO, Obsidian, Templater, citation plugin, RAG |
| `protocols/librarian-writing-rules.md` | drift, landmine, refactor guardrail, commit, batch verify, lesson |

---

## Operating the system

### Commands

| Command | What happens |
|---|---|
| `save` | Atomic save: session log + index update + last_session_snapshot + inbox flush + vectorstore sync + git commit (per `.clinerules/08-save-command.md`) |
| `detailed save` | Same as save with full accounting per step |
| `health check` | Non-destructive ecosystem audit (per `maintenance-protocol.md`) |
| `full maintenance` | Health check + cleanup with confirmation |
| `inbox triage` | Surface inbox captures for Scholar's consolidation decisions |
| `customize` | See `customization-protocol.md` for runtime preference adjustments |

### Maintenance rhythm

- **Every session**: invoke `save` before ending. Captures session state to logs + index + snapshot, stages inbox captures, runs git hardening. Skipping saves means lost continuity.
- **Monthly**: Hypatia reminds on the 1st-3rd. Run `health check` to audit, `full maintenance` to clean up.
- **After major changes**: if JSON files were manually edited, run `health check` to verify index-to-data sync.
- **Inbox consolidation**: scheduled separately from save. Scholar invokes `"let's consolidate the inbox"` or `"review captures"` during dedicated maintenance time.

### Context window management

The context window is the scarcest resource. Habits that keep usage lean:

- **Trust CSR routing.** Don't ask Hypatia to "load everything." The system loads lightweight indexes (~500 tokens each) and fetches full entries only when signals match.
- **Save frequently on long sessions.** Captures learnings + lets you start fresh without losing progress.
- **Save before context limits.** Context exhaustion mid-save is the primary data-loss risk.

---

## Customization

Two paths (per `customization-protocol.md`):

1. Runtime commands: `"less proactive"`, `"I'm expert in X"`, `"don't suggest Y"`. Captures flow through inbox.
2. Direct edits to `.clinerules/*` for kernel-level changes (requires Scholar confirmation; Tier 1 destructive per `.clinerules/04-session-gates.md`).

**Locked at the kernel level** (immutable via runtime commands):
- Name: Hypatia
- Pronouns: she/her
- Address: "Scholar"
- Voice register: Greco-Roman Alexandrian scholar
- Anti-patterns, gates, decision routes

**Customizable at runtime**:
- Proactive frequency
- Anti-preferences
- Domain expertise calibration
- Tag / schema / drafting preferences

---

## Adding new protocols

1. Create `[domain]-protocol.md` in this directory or `protocols/` (subdir for librarian-style).
2. Add trigger keywords to `.clinerules/10-skills-loading.md`.
3. Pre-commit gate (`scripts/check-keyword-drift.py`, Phase 1) validates alignment.

---

## Data files

All `.json` files use the CSR (Context Signal Routing) pattern:

- Index files (`*-index.json`) contain routing metadata: tags, categories, confidence, summaries.
- Full data (`*.json`) loaded on-demand when signals match.
- Break-even at ~30 items; significant token savings at scale.

Schema documented in each file's `_schema` field (where present) or in `memory-protocol.md` / `Intelligence/intelligence-operations.md`.

---

## Detailed documentation

| Doc | Covers |
|---|---|
| `CRITICAL-FILE-PROTECTION.md` | Safety rails for destructive operations + inbox boundary enforcement |
| `Intelligence/README.md` | Intelligence architecture overview |
| `Intelligence/intelligence-operations.md` | How intelligence surfaces during work |
| `Intelligence/learning-loop.md` | Consolidation algorithm, quality gates, capture rules |
| `maintenance-protocol.md` | Health check procedures, pruning thresholds, integrity verification |
| `protocols/README.md` | Librarian protocol index + reading order |
| `vectorstore/SETUP.md` | Vectorstore setup |
| `vectorstore/BENCHMARK.md` | Vectorstore benchmark protocol |

---

## Cross-references

- **Kernel (always-loaded)**: `.clinerules/`
- **Save command**: `.clinerules/08-save-command.md`
- **Protocol keyword map (single source of truth for triggers)**: `.clinerules/10-skills-loading.md`
- **Inbox capture flow**: `inbox/SCHEMA.md`
- **Build plan**: `docs/Hypatia Build Plan.md` + `docs/hypatia-build-plan-addendum.md`

---

*This is Hypatia's brain. It grows through deliberate consolidation, not accretion. Treat saves like commits: early, often, always.*
