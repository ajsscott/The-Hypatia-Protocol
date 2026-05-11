# 10: Skills Loading

How Hypatia decides which protocol to load given user input. This file is the **single source of truth** for the protocol keyword map. When a protocol's in-file `**Keywords**:` line drifts from this map, this map wins.

A pre-commit gate (`scripts/check-keyword-drift.py`, Phase 1) enforces alignment between this file and each protocol's declared keywords.

---

## Always loaded

These load every session regardless of input:

- `.roo/rules-hypatia/01-identity.md`: who Hypatia is
- `.roo/rules-hypatia/02-voice.md`: how she speaks
- `.roo/rules-hypatia/03-anti-patterns.md`: what she avoids
- `.roo/rules-hypatia/04-session-gates.md`: boot sequence (Phase 1 pending)
- `.roo/rules-hypatia/05-tools.md`: tool inventory
- `.roo/rules-hypatia/06-cognitive.md`: reasoning protocols (Phase 1 pending)
- `.roo/rules-hypatia/07-intelligence-layer.md`: KB routing (Phase 1 pending)
- `.roo/rules-hypatia/09-security.md`: external content safety (Phase 1 pending)
- `.roo/rules-hypatia/10-skills-loading.md`: this file
- `.roo/rules-hypatia/11-decision-routes.md`: decision routing (Phase 1 pending; from `hypatia-kb/Hypatia-Protocol.md`)

---

## Keyword-triggered (lazy-load)

Scan user input for the keywords below. On match, `read_file` the corresponding protocol. Match the longest / most-specific keyword first.

### Librarian protocols (`hypatia-kb/protocols/`)

| Protocol | Keywords |
|---|---|
| `librarian-role.md` | librarian, vault, zettelkasten, Tabula, curate, ingest, query, lint, Seed, Tree, wiki, knowledge base, PKB |
| `librarian-vault-structure.md` | vault structure, Tabula, folders, Seeds, Trees, Mountains, Bases, Meridian, orientation, onboarding |
| `librarian-note-schemas.md` | schema, atomic note, frontmatter, YAML, naming, tag, kind, content_type, citekey, cite, embed, topics, aliases, Mountain hierarchy |
| `librarian-tooling.md` | Bases, plugin, YOLO, Obsidian, Templater, QuickAdd, Dataview, citation plugin, web clipper, RAG, embedding, vector DB |
| `librarian-writing-rules.md` | drift, landmine, refactor, guardrail, commit, approval, batch, sample, verify, lesson, prior incident, atomic commit, link rot |

### Ported Bell protocols (`hypatia-kb/*-protocol.md`)

> Note: some of these still require content adaptation per Phase 1 protocol-port work. Keywords listed below are the load-trigger map; the protocol files themselves may need rewrites before they read coherently as Hypatia content. Load-triggers are still correct.

| Protocol | Keywords | Adaptation status |
|---|---|---|
| `memory-protocol.md` | memory, remember, recall, history, capture, save memory, prune, retention | Adapt for Hypatia's inbox→consolidation flow |
| `maintenance-protocol.md` | maintenance, cleanup, health check, prune, integrity, housekeeping | Mostly portable |
| `planning-protocol.md` | plan, planning, roadmap, milestones, decompose, scope, phases | Mostly portable |
| `proactive-offering-protocol.md` | proactive, offer, suggest, anticipate, surface, flag | Mostly portable; adapt for Hypatia's curatorial reflex |
| `problem-solving-protocol.md` | problem, debug, troubleshoot, root cause, fix, investigate | Mostly portable |
| `summarization-protocol.md` | summarize, summary, distill, condense, tldr, brief | Portable |
| `writing-protocol.md` | write, draft, prose, edit, copy, rewrite, polish | Adapt for Hypatia's writing register (vs Bell's) |
| `research-protocol.md` | research, investigate, source, citation, study, paper, literature | Adapt for Hypatia's zettelkasten research flow |
| `prompt-enhancement-protocol.md` | prompt, refine prompt, enhance prompt, prompt engineering | Mostly portable |
| `customization-protocol.md` | customize, personalize, configure, tune | Rewrite for Hypatia's customization model |
| `development-protocol.md` | code, develop, programming, refactor, technical | Bell's was AWS/cloud-heavy; rewrite as universal dev practices |
| `executive-communication-protocol.md` | executive, stakeholder, leadership, exec comms | Likely deprecate; not Hypatia's primary use case |
| `security-protocol.md` | security, threat, credentials, secrets, access, permissions, exposure | Rewrite for vault-side security (token storage, git filter chain) |
| `CRITICAL-FILE-PROTECTION.md` | critical file, protected, lockdown, destructive operation, dangerous edit | Adapt for hypatia-kb-specific critical paths |

---

## Resolution rules

1. **Match longest keyword first.** "atomic note" beats "note"; "schema" alone is broader than "frontmatter schema."
2. **Multiple matches allowed.** A single input can trigger multiple protocols. Load all that apply.
3. **Always-loaded protocols never re-load.** They are in context from session start; do not `read_file` again unless an explicit refresh is needed.
4. **When no keyword matches**, default behavior:
 - For a question, answer from already-loaded context.
 - For a task, check `hypatia-kb/Hypatia-Protocol.md` Decision Routes to see if the task fits Route A-F.
 - If still ambiguous, ask the Scholar.
5. **When uncertain whether a keyword matches**, err toward loading. False positives are cheap; missed protocol coverage is expensive.

---

## Anti-drift discipline

Each protocol file MUST declare its own keywords at the top in a `**Trigger Keywords**:` line. The pre-commit gate compares those declarations against this file and fails the commit on mismatch. Three protocols spot-checked at Phase 0 audit showed drift between kernel keyword map and protocol declarations; this file replaces that drift-prone duplication with a single source.

When adding a new protocol or new keywords:

1. Add the row to this file's keyword table.
2. Add the matching `**Trigger Keywords**:` line in the protocol file.
3. Commit both together; the pre-commit gate will pass.

When the gate fails, the diff between this file and the protocol's declaration is the failure message. Fix in this file (single source) and re-export to protocols.

---

## Cross-references

- **Decision routing engine (Routes A-F)**: `hypatia-kb/Hypatia-Protocol.md` → `.roo/rules-hypatia/11-decision-routes.md`
- **Tool inventory**: `.roo/rules-hypatia/05-tools.md`
- **Anti-patterns governing all protocols**: `.roo/rules-hypatia/03-anti-patterns.md`
