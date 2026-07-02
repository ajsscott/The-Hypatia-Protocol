# 10: Skills Loading

How Hypatia decides which protocol to load given user input. This file is the **single source of truth** for the protocol keyword map. When a protocol's in-file `**Keywords**:` line drifts from this map, this map wins.

A pre-commit gate (`scripts/check-keyword-drift.py`) enforces alignment between this file, each protocol's declared keywords, and the routing table in `kernel/04-routing.md`.

---

## Always loaded

The always-loaded layer is the compact kernel (Q-33 redistribution), concatenated into Goose's system prompt every session:

- `kernel/01-identity.md`: who Hypatia is
- `kernel/02-voice.md`: how she speaks
- `kernel/03-critical-gates.md`: inbox boundary, destructive-action tiers, security never-violates
- `kernel/04-routing.md`: request classification, Routes A-F summary, this map's routing table

Everything below loads on demand as MCP resources served by the `hypatia-protocols` extension. This file itself is served as `protocol://detail/skills-map`.

---

## Keyword-triggered (lazy-load)

Scan user input for the keywords below. On match, load the corresponding protocol resource (`read_resource` on the `hypatia-protocols` extension). Match the longest / most-specific keyword first. Multiple matches load all that apply.

### Librarian protocols (`hypatia-kb/protocols/librarian-*.md`)

| Protocol | Keywords |
|---|---|
| `librarian-role.md` | librarian, vault, zettelkasten, Tabula, curate, ingest, query, lint, Seed, Tree, Mountain, wiki, knowledge base, PKB |
| `librarian-vault-structure.md` | vault structure, vault, Tabula, TabulaJacqueliana, folders, Seeds, Trees, Mountains, Slope, Trail, Bases, Meridian, orientation, onboarding, structure |
| `librarian-note-schemas.md` | schema, atomic note, atomic, frontmatter, YAML, naming, tag, taxonomy, kind, content_type, citekey, cite, embed, topics, aliases, Tree, Seed, Mountain, Mountain hierarchy |
| `librarian-tooling.md` | Bases, plugin, plugin stack, YOLO, Obsidian, Meridian, Templater, QuickAdd, Dataview, citation, citation plugin, web clipper, RAG, embedding, vector, vector DB |
| `librarian-writing-rules.md` | drift, landmine, refactor, guardrail, write, edit, commit, approval, batch, sample, verify, lesson, error, prior incident, atomic commit, link rot |
| `librarian-memory.md` | memory, remember, recall, history, capture, save memory, prune, retention, preferences, decisions |
| `librarian-lint.md` | maintenance, cleanup, health check, prune, integrity, housekeeping |
| `librarian-customize.md` | customize, personalize, configure, tune, adjust, set preference |

### Researcher protocols (`hypatia-kb/protocols/researcher-*.md`)

| Protocol | Keywords |
|---|---|
| `researcher-investigate.md` | research, investigate, source, citation, study, paper, literature, analyze, assess, compare, deep-dive, evaluate, explore |
| `researcher-prompt-enhance.md` | prompt, refine prompt, enhance prompt, prompt engineering, ambiguous, clarify-request, enhance-prompt, improve-prompt, prompt-enhancement, refine-prompt, unclear |

### Writer protocols (`hypatia-kb/protocols/writer-*.md`)

| Protocol | Keywords |
|---|---|
| `writer-draft.md` | write, draft, prose, edit, copy, rewrite, polish, brief, compose, document, memo, narrative, revise, summary, writing |
| `writer-summarize.md` | summarize, summary, distill, condense, tldr, brief, aggregate, minutes, recap, source synthesis, transcript |
| `writer-executive.md` | executive, stakeholder, leadership, exec comms, C-suite, CEO, CFO, CIO, CTO, board, investor, pitch, stakeholder presentation |

### Assistant protocols (`hypatia-kb/protocols/assistant-*.md`)

| Protocol | Keywords |
|---|---|
| `assistant-development.md` | code, develop, programming, refactor, technical, build, debug, dependency, deploy, implement, library, test |
| `assistant-plan.md` | plan, planning, climb, climbing, roadmap, breakdown, decompose, dependency, estimate, milestone, milestones, phases, prioritize, project, scope, timeline |
| `assistant-problem-solve.md` | problem, debug, troubleshoot, root cause, fix, investigate, analyze problem, decompose, diagnose, systematic, trace |
| `assistant-proactive.md` | proactive, offer, suggest, anticipate, surface, flag, next step |
| `assistant-ingest.md` | ingest, grow, growing, file source, process source, intake, onboard source, capture Seed, new source, file PDF, file article, drop in |

### Cross-cutting (`hypatia-kb/protocols/`)

| Protocol | Keywords |
|---|---|
| `security.md` | security, threat, credentials, secrets, access, permissions, exposure, sanitize, pii, classification |
| `CRITICAL-FILE-PROTECTION.md` | critical file, protected, lockdown, destructive operation, dangerous edit |

---

## Resolution rules

1. **Match longest keyword first.** "atomic note" beats "note"; "schema" alone is broader than "frontmatter schema."
2. **Multiple matches allowed.** A single input can trigger multiple protocols. Load all that apply.
3. **The always-loaded kernel never re-loads.** It is in context from session start; do not fetch it again unless an explicit refresh is needed.
4. **When no keyword matches**, default behavior:
 - For a question, answer from already-loaded context.
 - For a task, check the Decision Routes (`protocol://detail/decision-routes`, or the per-route splits `protocol://detail/decision-route-{a..f}`) to see if the task fits Route A-F.
 - If still ambiguous, ask the Scholar.
5. **When uncertain whether a keyword matches**, err toward loading. False positives are cheap; missed protocol coverage is expensive.

---

## Anti-drift discipline

Each protocol file MUST declare its own keywords at the top in a `**Trigger Keywords**:` line. The pre-commit gate compares those declarations against this file and fails the commit on mismatch. Phase 1 reconciliation (2026-05-12) resolved drift across 17 protocols by taking the union of kernel-listed and protocol-declared keyword sets; from this point forward, this file is the single source of truth and drift fails CI.

When adding a new protocol or new keywords:

1. Add the row to this file's keyword table.
2. Add the matching `**Trigger Keywords**:` line in the protocol file.
3. Commit both together; the pre-commit gate will pass.

When the gate fails, the diff between this file and the protocol's declaration is the failure message. Fix in this file (single source) and re-export to protocols.

---

## Cross-references

- **Decision routing engine (Routes A-F)**: `protocol://detail/decision-routes` (per-route splits at `protocol://detail/decision-route-{a..f}`)
- **Tool inventory**: `protocol://detail/tools`
- **Anti-patterns governing all protocols**: `protocol://detail/anti-patterns`
