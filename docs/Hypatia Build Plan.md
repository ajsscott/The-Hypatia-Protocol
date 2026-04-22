---
icon: 📎
kind:
  - Document
aliases:
  - Hypatia Plan
tags:
  - projectManagement/document
  - Hypatia
  - Obsidian
topics:
  - "[[Building a Persistent AI Partner A Context Engineering Case Study]]"
  - "[[Zettelkasten Note-Taking]]"
project: "[[Obsidian Processing]]"
parent: "[[Hypatia Build]]"
created: 2026-04-22 13:00
last_updated: 2026-04-22 13:00
complete: false
---

# Hypatia Build Plan

**Status:** draft for review. All 8 design decisions locked. Codebase analysis of `/Users/ajsscott/GitHub/TabulaJacqueliana/The-Nathaniel-Protocol` complete. Awaiting AJ approval before Phase 1 kickoff.

**Derived from:** [[Building a Persistent AI Partner A Context Engineering Case Study]] + [The-Nathaniel-Protocol repo](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (locally cloned).

**Companion Slope:** [[Hypatia Build]].

## Design decisions (locked 2026-04-22)

| # | Area | Decision |
|---|---|---|
| 1 | Runtime | Cline extension in VSCode |
| 2 | Scope | Bell's general-partner scope + zettelkasten PKB telos + autonomous listening |
| 3 | Repo | Fresh (MIT-licensed, own copyright, no fork) |
| 4 | Architecture | One persona + four skill clusters (Librarian / Researcher / Writer / Assistant) |
| 5 | Persona | "Hypatia" — voice = concise academic librarian, relationship = partner |
| 6 | Stores | JSON authoritative + markdown export layer; direct vault R/W/E |
| 7 | Phasing | A (Core) → C (Listening) → B (Retrieval) |
| 8 | Scope boundary | Hypatia's stores are INDEPENDENT of TabulaJacqueliana's `_src/_meta/` (portability) |

---

## Codebase analysis — key findings

### Nate's architecture at a glance

- **2,576-line monolithic kernel** at `.steering-files/steering/Nathaniel.md`. Always-loaded system prompt.
- **13 protocol files** at `Nate's-kb/*-protocol.md`, total ~7,000 lines. Keyword-triggered lazy-load.
- **1 decision engine** at `Nate's-kb/Nate-Protocol.md` (2,070 lines) containing Routes A-F.
- **JSON intelligence stores** at `Nate's-kb/Intelligence/` and `Nate's-kb/Memory/` — 11 stores with ~900 entries total.
- **Python backend** at `scripts/` + `Nate's-kb/vectorstore/` — ~6,600 LOC for save/validate/maintenance + retrieval (RRF + fastembed + CSR).
- **Sub-agent framework** at `.steering-files/agents/analyst/` — 4-file pattern (manifest + prompt + consciousness + specialization).
- **Pocket HQ scaffold** at root (`Projects/ Business/ Brand/ Life/ Archive/ docs/`) — mostly empty scaffolding.

### Critical architectural insights (reshape the plan)

1. **Keyword-triggering is 100% behavioral.** No dispatcher script. Kernel instructs the LLM: "Scan for KB triggers → match against keyword map → read matching protocol file via `fs_read`." Cline supports the same pattern identically; substrate change is trivial.

2. **Fusion algorithm is RRF** (Reciprocal Rank Fusion), not HRF. CSR = Context Signal Routing (tag/category lookup with synonym expansion). Earlier planning used "HRF" imprecisely.

3. **`consciousness.md` drifts from `Nathaniel.md`.** Bell's sub-agent personality extract is 2026-02-26 snapshot; kernel has evolved since. Design landmine — Hypatia needs single source of truth, not a periodic copy.

4. **Trigger-keyword drift.** Each protocol's in-file `**Keywords**:` line doesn't match the kernel's Protocol Keyword Map. Three protocols spot-checked all showed drift. Hypatia must enforce one canonical source.

5. **Flash-drive portability has three real gaps Bell doesn't solve:**
   - Python venv not portable (rebuild per machine)
   - fastembed model cache lives in `~/.cache/fastembed/` (90 MB, re-downloads per machine)
   - `save-session.py` uses POSIX `fcntl` locking → Windows requires WSL

6. **Intelligence stores carry Bell-personal content:**
   - `knowledge.json` — 447 entries, 11 Strands/Bedrock/Amazon SDK, 42 Kiro-tagged, 1 explicit Warner Bell bio (know-447)
   - `memory.json` — 24 memories, ~5 reference Nate/Kiro
   - `patterns.json` — 167 of 211 entries tagged `source: "Nate prime"`
   - `reasoning.json` — 19 of 126 entries mention Nathaniel/Kiro
   - `synonym-map.json` — ~5 of 41 groups are Bell-specific

   Cleanup strategy: use `reseed.py` (exists for exactly this) rather than hand-edit.

### Terminology reset

- **RRF** (Reciprocal Rank Fusion) — the retrieval fusion algorithm
- **CSR** (Context Signal Routing) — the tag/category indexing pattern
- **IMG** (Institutional Memory Gate) — Nate's "always query the KB first" gate
- **CSP** (Cognitive Synchronization Protocol) — Nate's SENSE → MODEL → ALIGN → ANTICIPATE → SYNC loop
- Drop "HRF" everywhere. Use RRF.

---

## Phase 1 — Core (2-3 weeks)

Goal: functional Hypatia in Cline, usable daily for manual-ingest + vault-librarian work. Intelligence stores scaffolded (empty JSON), schemas validated. No autonomous listening, no RRF/CSR retrieval, no confidence calibration loop.

### Week 1 — Repo scaffold + runtime integration

**Day 1-2: Repo initialization**
- Create new repo (location: `/Users/ajsscott/GitHub/Hypatia/` or flash drive path TBD). **Not nested inside TabulaJacqueliana.**
- `git init` + MIT LICENSE (AJ's copyright) + README stub + `.editorconfig` from Nate (verbatim) + `.gitignore` (Nate's version minus Kiro entries + `Nate's-kb/` renames).
- `pyproject.toml` with pinned dependencies (see § Dependencies below). Use `uv` for dependency management.
- Directory skeleton:
  ```
  Hypatia/
  ├── .clinerules/                     # Cline system-prompt rules (split from Nathaniel.md)
  ├── .vscode/settings.json            # Cline permissions mirroring .claude/settings.json pattern
  ├── hypatia-kb/                      # Hypatia's knowledge base (renamed from Nate's-kb)
  │   ├── Intelligence/                # patterns, knowledge, reasoning, cross-refs, synonym-map
  │   ├── Memory/                      # memory, session-index
  │   ├── protocols/                   # Protocol-as-MCP skill files (renamed from *-protocol.md root)
  │   └── vectorstore/                 # Python retrieval backend (Phase 3)
  ├── scripts/                         # Python tooling (save-session, validate, maintenance)
  ├── hypatia.config.yaml              # User-specific config: vault path, preferences, paths
  ├── pyproject.toml                   # Python deps pinned
  ├── uv.lock
  ├── LICENSE
  ├── README.md
  └── .gitignore
  ```
- Initial commit: `chore: initial scaffold`.

**Day 3-4: Kernel decomposition**
- Split Nathaniel.md (2,576 lines) into numbered `.clinerules/*.md` files. Target layout:
  ```
  .clinerules/
  ├── 01-identity.md              # ~60 lines — Hypatia name, super-objective, role, irreducible self
  ├── 02-voice.md                 # ~80 lines — concise academic librarian register (REWRITE from Bell's AAVE section)
  ├── 03-anti-patterns.md         # ~280 lines — from Nathaniel.md 638-921 (language, behavioral, truth, response, process)
  ├── 04-session-gates.md         # ~200 lines — IMG + Pre-Task Protocol + Session Start Gate + Destructive Action Gate
  ├── 05-tools.md                 # ~120 lines — Cline tool inventory (replaces Kiro's tool-inventory.md)
  ├── 06-cognitive.md             # ~250 lines — OBSERVE>QUESTION>DEDUCE + CSP + complexity gates
  ├── 07-intelligence-layer.md    # ~150 lines — tiered surfacing, confidence thresholds, claim-match verification
  ├── 08-save-command.md          # ~200 lines — 10-step atomic save workflow (adapts to Hypatia's KB paths)
  ├── 09-security.md              # ~140 lines — external content security + git hardening
  └── 10-skills-loading.md        # ~100 lines — explicit Protocol-as-MCP keyword-map + "how to load a skill"
  ```
- **Rewrite voice section entirely.** Bell's southern-urban AAVE voice doesn't transfer. Hypatia's voice = concise academic librarian: direct, peer-register, cites sources, no filler, devil's-advocate by default, mild warmth, no sycophancy.
- **Preserve anti-patterns verbatim** from Bell where applicable (language anti-patterns, prohibited structures, rigor-over-shortcuts). Add Hypatia-specific ones (zettelkasten: atomic-notes violations, basename collisions, sed-on-multiline-YAML, trust-agent-summarized-counts).
- **Replace proper nouns.** Grep for `Nate|Nathaniel|Kiro|Sir|Pocket HQ` across all decomposed files. Replace or strip per context.

**Day 5: Cline configuration**
- `.vscode/settings.json` with Cline auto-approval settings mirroring the TabulaJacqueliana `.claude/settings.json` permission philosophy: read-only git + grep + glob allowed; Edit/Write ASK per operation; destructive ops DENIED.
- Test: install Cline, open Hypatia repo in VSCode, verify `.clinerules/` loads, verify persona responds in correct voice, verify Hypatia can read + edit files in the repo.

**Deliverables end of Week 1:**
- Hypatia repo committable with persona boot-ready
- AJ can open VSCode, invoke Cline, Hypatia introduces herself as expected
- Commit: `chore: establish Hypatia kernel in .clinerules/`

### Week 2 — Intelligence stores + protocol files

**Day 6-7: Intelligence stores (empty, schemas validated)**
- Create `hypatia-kb/Intelligence/` with empty `patterns.json`, `knowledge.json`, `reasoning.json`, `cross-references.json`, `synonym-map.json` + matching `-index.json` files.
- Schema validator script `scripts/validate-schemas.py` ported verbatim from Bell (312 LOC, portable Python stdlib, coupled to schema not content — easy port).
- `hypatia-kb/Memory/` with `memory.json` + `memory-index.json` + `session-index.json` (all empty scaffolds).
- **Populate `hypatia-kb/Intelligence/synonym-map.json` with Hypatia-specific synonyms** (not Bell's). Domain-relevant terms: zettelkasten vocabulary (Seed/Tree/Mountain/atomic-note/block-ref/backlink), Obsidian concepts, AJ's workflow verbs.
- Seed `memory.json` with `instance_identity: { instance_name: "Hypatia", description: "zettelkasten PKB partner", created: "2026-04-22" }` and populate the 5-7 most consequential preferences from what we've already observed in TabulaJacqueliana sessions (peer register, devil's-advocate, atomic commits, etc.).

**Day 8-10: Protocol files (4 skill clusters)**
- Port Bell's 13 protocols → Hypatia's 4 skill clusters. Mapping:

  | Hypatia cluster | Purpose | Source protocols |
  |---|---|---|
  | **Librarian** | Vault hygiene, curation, save-session, lint, anti-patterns enforcement, consolidation | save-command (in 08), maintenance, memory, customization |
  | **Researcher** | Source-hierarchy research, comparative analysis, file-back-as-Tree | research, prompt-enhancement |
  | **Writer** | Draft, refine, restructure prose; format-aware (6-pager, memo, email, Tree note) | writing, summarization, executive-communication |
  | **Assistant** | General-purpose ingestor + problem-solving + planning | development, planning, problem-solving, proactive-offering (behavioral, lives in kernel) |

- Files to create at `hypatia-kb/protocols/*.md` (13 total — same count as Bell, different clustering):
  - `librarian-save.md` (adapted from save-command kernel section + memory-protocol)
  - `librarian-lint.md` (adapted from maintenance-protocol)
  - `librarian-memory.md` (adapted from memory-protocol)
  - `librarian-customize.md` (adapted from customization-protocol, used rarely)
  - `researcher-investigate.md` (adapted from research-protocol)
  - `researcher-prompt-enhance.md` (adapted from prompt-enhancement-protocol)
  - `writer-draft.md` (adapted from writing-protocol)
  - `writer-summarize.md` (adapted from summarization-protocol)
  - `writer-executive.md` (adapted from executive-communication-protocol)
  - `assistant-development.md` (adapted from development-protocol — shrink significantly; Bell's is 2,464 lines of AWS-specific stuff, strip to universal dev practices)
  - `assistant-plan.md` (adapted from planning-protocol)
  - `assistant-problem-solve.md` (adapted from problem-solving-protocol)
  - `assistant-ingest.md` (NEW — no Bell analog — the zettelkasten-specific Seed-creation workflow)

- **Normalize trigger keywords** — every protocol file has `**Keywords**:` line at top; ALSO has an entry in `.clinerules/10-skills-loading.md` keyword map. Write a `scripts/check-keyword-drift.py` linter that fails CI if the two diverge. Bell didn't do this; it's the drift landmine Hypatia avoids.

- **Strip Kiro-specific references** from every protocol during port. Grep for `.kiro/`, `Kiro IDE`, `kiro-cli`, `Sir`, `Nate`, WSL references, etc.

- **Add zettelkasten-specific content** to Librarian cluster:
  - Vault taxonomy (Seeds/Trees/Mountains/Seedlings/Forests, authority levels, what-goes-where)
  - Atomic-note principle + split heuristics
  - Block-ref `^cite-*` embedding contract
  - Frontmatter schemas per note type + kind-list-form convention
  - Tag taxonomy (lowercase camelCase, flat)
  - Obsidian wikilink + backlink behavior (basename resolution, rename-with-grep discipline)
  - Bases load-bearing fields
  - obsidian-linter + obsidian-git interaction

**Day 11-12: Decision routes**
- `hypatia-kb/protocols/decision-routes.md` — port Nate-Protocol.md Routes A-F verbatim with Hypatia-specific examples.
- **Apply the 4 fixes** I flagged earlier vs my TabulaJacqueliana port: restore Route E "just do it" override language; restore Route B expertise-detection in skip-explanation; tighten Route F verification-rule language (don't punt back to user); drop the CoV reference pointer that no longer exists.
- This is the ONE protocol always-loaded-by-default (not keyword-triggered) — goes in `.clinerules/` not `hypatia-kb/protocols/`. Add as `.clinerules/11-decision-routes.md`.

**Deliverables end of Week 2:**
- All 13 protocols drafted
- Intelligence stores scaffolded + schemas validated
- Keyword drift linter passes (empty keyword map + protocols → no drift yet)
- Commit: `feat: protocols + intelligence store scaffold`

### Week 3 — Save-session + tooling + vault integration

**Day 13-15: save-session.py port**
- Port Bell's `save-session.py` (883 LOC) to `scripts/save-session.py`. Core changes:
  - Rename `Nate's-kb/` → `hypatia-kb/` (4 files affected)
  - Strip Windows/WSL fallback paths (Phase 1 is Mac/Linux only; document as known limitation)
  - Replace hardcoded git identity `nate@pocket-hq.local` → read from `hypatia.config.yaml`
  - Strip Bell-personal PII blocklist from `reseed.py` (ship empty; user adds own if needed)
- Port `validate-schemas.py`, `pre-commit-kb-validate.sh`, `setup-filters.sh`, `run-python.sh`.
- Install pre-commit hook via `scripts/setup.sh` (Mac/Linux version of Bell's setup.sh — strip Kiro + Windows branches).

**Day 16-17: Vault integration layer**
- `hypatia.config.yaml` schema:
  ```yaml
  vault:
    path: /Users/ajsscott/GitHub/TabulaJacqueliana
    branch: work-safe
    linter_on_save: true
    auto_commit_interval_min: 15
  instance:
    name: Hypatia
    created: 2026-04-22
  preferences:
    register: concise-academic-librarian
    devil_advocate: true
  ```
- Protocol: whenever a skill needs vault access, it reads `hypatia.config.yaml` for the path. Flash-drive portability: config is per-machine (gitignored); Hypatia auto-prompts for vault path on first run if config is absent.
- Test: Hypatia invoked to "summarize this Tree and propose Trees to link to it" successfully reads from vault, proposes edits, AJ approves, Hypatia writes.

**Day 18-19: Markdown export layer**
- `scripts/export-intelligence-to-markdown.py` — reads Hypatia's JSON stores, writes markdown views at `hypatia-kb/exports/{patterns, knowledge, reasoning}.md` with Dataview-queryable frontmatter per entry.
- Integrated into `save-session.py` as final step (after JSON writes, regenerate markdown exports).
- Flash-drive portability: exports are regenerated from JSON per machine; not committed.

**Day 20-21: Testing + documentation + commit**
- Port Bell's script-side tests to `tests/` (1,843 LOC — substantial, but tests are mostly portable; paths rewrite).
- Port vectorstore tests scaffolding (`hypatia-kb/vectorstore/tests/`) — empty stubs for Phase 3; CI step ready.
- README.md with setup instructions, Cline wiring, first-session walkthrough.
- Commit: `feat: save-session + vault integration + markdown exports`

**Deliverables end of Week 3 / Phase 1:**
- Working Hypatia in Cline
- Reads/writes TabulaJacqueliana vault
- "Save session" command works end-to-end (writes to JSON stores, rebuilds indexes, regenerates markdown exports, git-commits)
- All 13 protocols loadable via keyword triggers
- Schema validator runs pre-commit
- AJ can use Hypatia daily for manual-ingest (paste URL/text/file → triage to Seed → draft Tree plan → commit)

**Phase 1 exit criteria:**
- [ ] AJ has used Hypatia to ingest 3+ real-world sources into the vault end-to-end
- [ ] Intelligence stores accumulated 10+ preferences + 5+ patterns organically
- [ ] At least one save-session command has fully succeeded with git commit
- [ ] No Kiro/Nate/Sir references remain in any file

---

## Phase 2 — Autonomous listening (3-4 weeks after Phase 1)

Goal: reduce capture cost by automatically surfacing ingestion-worthy content from AJ's digital surfaces. Pick 1-2 surfaces based on Phase 1 usage patterns — what she pasted most, what workflow felt highest-friction.

**Likely candidates (ranked by ease × value):**

1. **Obsidian Web Clipper hooks** — already installed in TabulaJacqueliana; clipper drops articles into `Seeds/Sources/Articles/`. Watcher script detects new files, invokes `assistant-ingest` protocol, proposes Seed enrichment + Tree plan.
2. **File-system watcher on vault** (`Seeds/` + `_attachments/`) — generic; catches anything added to those dirs regardless of clipper source.
3. **Zotero library watcher** — watches `LEVIEngineeringHub.bib` for changes; triggers Research Seed creation via citation-plugin format.
4. **Terminal / shell capture** — lightweight listener on a specific output dir (`~/Desktop/claude-captures/` or similar); user saves file → Hypatia picks up → proposes Seed.
5. **Email digest polling** — cron job reads specific Gmail label → turns each email into a Seed candidate. Heavier; auth required.
6. **Browser extension custom** — if clipper doesn't cover enough, a Hypatia-specific extension.

**My Phase 2 recommendation:** start with **#1 + #2** (Web Clipper + generic vault watcher). They share infrastructure (Python watchdog). Lowest effort, highest probability of daily use.

**New protocols:**
- `assistant-ingest.md` (already drafted in Phase 1) — handles triage of incoming material
- `assistant-monitor.md` (new) — the watcher logic + event → trigger mapping

**Infrastructure:**
- `scripts/hypatia-watcher.py` — daemon reading config for watch targets; each target has a dispatch rule (new file in Seeds/Sources/Articles → invoke assistant-ingest with `source_type=web_article`).
- System service: launchctl (Mac) / systemd (Linux) — Phase 2 assumes Mac; Windows deferred.
- Output: watcher writes a "pending ingest" queue file; next Hypatia session processes the queue.
- Flash-drive portability: watcher is per-machine (daemon config stays local).

**Phase 2 exit criteria:**
- [ ] Watcher runs continuously on AJ's daily machine
- [ ] New Web Clippings auto-trigger `assistant-ingest` with zero manual invocation
- [ ] AJ has processed 10+ auto-triggered Seeds without workflow friction

---

## Phase 3 — Retrieval (RRF + CSR + confidence calibration, 4-6 weeks after Phase 2)

Goal: advanced retrieval across intelligence stores. Bell's vectorstore ported nearly verbatim.

**Port targets from Bell's `vectorstore/`:**
- `concat.py` (83 LOC) — field concatenation + SHA-256 hashing. Ports 1:1.
- `kb_vectorize.py` (139 LOC) — full build. Rename paths only.
- `kb_sync.py` (159 LOC) — incremental re-embed. Rename paths only.
- `kb_query.py` (481 LOC) — RRF + CSR + filter. Rename paths. Fix the comment drift about tiebreak-by-distillation-level. Swap embedding model if AJ wants (default: all-MiniLM-L6-v2 for English; all-mpnet-base-v2 for more accuracy with higher cost).
- `kb_server.py` (85 LOC) — FastMCP stdio. Rename paths + `kb_` → `hypatia_` prefix on tool names.
- `kb_benchmark.py` (239 LOC) — optional; port for future model evaluations.
- `run-server.sh` (7 LOC) — rename.

**Dependencies added in Phase 3:**
- `fastembed >= 0.3, < 0.8`
- `numpy >= 1.24, < 3`
- `mcp >= 1.0`

**MCP integration:** Hypatia's vectorstore becomes a Cline MCP server. Cline config: `hypatia-vectorstore` server = `scripts/run-vectorstore-server.sh`. Cline auto-exposes `hypatia_search`, `hypatia_sync`, `hypatia_rebuild` tools.

**Confidence calibration loop (new, no Bell analog):**
- `scripts/calibration-tracker.py` — background job that reads `confidence_events[]` from memory.json (Hypatia logs `{prediction, actual}` pairs per save-session) and computes per-pattern-type calibration error.
- Weekly cadence: save-session includes "calibration review" in Part 6.
- Adjusts base confidence on patterns by task-type. Outputs to a `calibration-log.json`.
- This is the one thing Bell's system doesn't have — explicit calibration feedback. His manual review is "look at the stats, adjust manually." Hypatia automates.

**Phase 3 exit criteria:**
- [ ] Hypatia queries intelligence stores via MCP `hypatia_search` and returns sub-second results
- [ ] Vectorstore rebuilds complete in <10s for a 500-entry store
- [ ] Confidence calibration running weekly; at least one pattern's confidence adjusted by the automation

---

## Repo structure (target end of Phase 1)

```
Hypatia/
├── .clinerules/
│   ├── 01-identity.md                    Hypatia: name, super-objective, role
│   ├── 02-voice.md                       concise academic librarian register
│   ├── 03-anti-patterns.md               from Nathaniel.md 638-921, adapted
│   ├── 04-session-gates.md               IMG + Pre-Task + Session Start
│   ├── 05-tools.md                       Cline tool inventory
│   ├── 06-cognitive.md                   OBSERVE>QUESTION>DEDUCE + CSP
│   ├── 07-intelligence-layer.md          tiered surfacing, claim-match verify
│   ├── 08-save-command.md                10-step atomic save workflow
│   ├── 09-security.md                    external content + git hardening
│   ├── 10-skills-loading.md              Protocol-as-MCP keyword map (single source of truth)
│   └── 11-decision-routes.md             Routes A-F (always loaded)
├── .vscode/
│   └── settings.json                     Cline auto-approval config
├── hypatia-kb/
│   ├── Intelligence/
│   │   ├── patterns.json                 (empty at ship; accumulates on use)
│   │   ├── patterns-index.json
│   │   ├── knowledge.json
│   │   ├── knowledge-index.json
│   │   ├── reasoning.json
│   │   ├── reasoning-index.json
│   │   ├── cross-references.json
│   │   ├── synonym-map.json              (Hypatia-specific synonyms)
│   │   └── README.md                     what's in each store
│   ├── Memory/
│   │   ├── memory.json                   seeded with instance_identity + 5-7 preferences
│   │   ├── memory-index.json
│   │   └── session-index.json
│   ├── protocols/                        (13 files, 4 skill clusters)
│   │   ├── librarian-save.md
│   │   ├── librarian-lint.md
│   │   ├── librarian-memory.md
│   │   ├── librarian-customize.md
│   │   ├── researcher-investigate.md
│   │   ├── researcher-prompt-enhance.md
│   │   ├── writer-draft.md
│   │   ├── writer-summarize.md
│   │   ├── writer-executive.md
│   │   ├── assistant-development.md
│   │   ├── assistant-plan.md
│   │   ├── assistant-problem-solve.md
│   │   └── assistant-ingest.md           NEW — zettelkasten Seed-creation
│   ├── exports/                          (regenerated on save; gitignored)
│   │   ├── patterns.md
│   │   ├── knowledge.md
│   │   └── reasoning.md
│   └── vectorstore/                      (Phase 3)
│       ├── (all Python from Bell, path-renamed)
│       └── tests/
├── scripts/
│   ├── save-session.py                   Central save workflow
│   ├── validate-schemas.py               Schema validator
│   ├── check-keyword-drift.py            NEW — drift linter
│   ├── pre-commit-kb-validate.sh
│   ├── setup.sh                          (Mac/Linux only for Phase 1)
│   ├── setup-filters.sh
│   ├── run-python.sh
│   ├── export-intelligence-to-markdown.py
│   ├── hypatia-watcher.py                (Phase 2)
│   └── calibration-tracker.py            (Phase 3)
├── tests/
│   ├── test_save_session.py              ported from Bell
│   ├── test_schema_validation.py         new + some from Bell
│   ├── test_keyword_drift.py             new
│   └── ... (Bell's other script tests, ported)
├── .github/
│   └── workflows/
│       └── validate.yml                  JSON validity + scripts/ tests + vectorstore tests
├── hypatia.config.yaml.example           template; user copies to hypatia.config.yaml
├── pyproject.toml                        pinned deps
├── uv.lock
├── LICENSE                               MIT, AJ copyright
├── README.md                             setup + first-session walkthrough
├── .gitignore
├── .gitattributes
└── .editorconfig
```

---

## File-by-file customization strategy (Bell's repo → Hypatia)

| Bell's file | Disposition | Effort |
|---|---|---|
| `.steering-files/steering/Nathaniel.md` (2,576 lines) | **Decompose** into `.clinerules/01-11.md`. Rewrite voice section. Strip Kiro/Bell. | 2-3 days |
| `.steering-files/steering/tool-inventory.md` (119) | Adapt: replace Kiro tool names with Cline's; update the guidance per Cline's behavior. | 2 hours |
| `.steering-files/agents/analyst/*` (4 files, 729 lines) | **Defer to Phase 2+**. Keep pattern (4-file manifest+prompt+consciousness+specialization). When we need the "researcher" skill to have its own context, port these as a Cline custom mode. | Phase 2 |
| `.steering-files/settings/mcp.json` | Adapt: 3 MCP servers (time, secure-fetch, hypatia-vectorstore). Servers #2-3 pointing at Hypatia paths. | 30 min |
| `.steering-files/settings.json` (Kiro trustedCommands) | Replace with `.vscode/settings.json` using Cline's config schema. | 1 hour |
| `Nate's-kb/Nate-Protocol.md` (2,070 lines, Decision Routes A-F) | **Put into `.clinerules/11-decision-routes.md`**. Apply 4 flagged fixes. | 4 hours |
| `Nate's-kb/*-protocol.md` (13 files, ~7,000 LOC) | **Port all 13** → remap to 4-skill-cluster naming. Strip Kiro. Inject zettelkasten content. | 4-6 days |
| `Nate's-kb/Intelligence/*.json` + `-index.json` | Keep empty scaffold with schemas; let Hypatia's usage populate. | 1 day (schema validation setup) |
| `Nate's-kb/Memory/*.json` | Seed with Hypatia identity + 5-7 preferences. | 2 hours |
| `Nate's-kb/vectorstore/*` (Python, ~1,200 LOC) | **Port in Phase 3**. 1:1 with path renames. | 3-4 days (Phase 3) |
| `scripts/save-session.py` (883 LOC) | **Port in Phase 1.** Rename paths, strip Windows/WSL, config-ify git identity. | 1-2 days |
| `scripts/validate-schemas.py` + `pre-commit-kb-validate.sh` | Port verbatim with path rename. | 2 hours |
| `scripts/secure-fetch.py` (83 LOC) | Port verbatim with log-path rename (`~/.kiro/security.log` → `~/.hypatia/security.log`). | 30 min |
| `scripts/cascade-correction.py`, `maintenance.py`, `removal-cascade.py`, `reseed.py`, `session-cache.py`, `normalize-schemas.py` | Port with path renames. Strip Bell PII blocklist from `reseed.py`. | 1-2 days |
| `scripts/setup.sh` (Mac/Linux) | Rewrite to drop `.kiro/` deployment + Kiro CLI checks + Windows shim. Keep venv + git config + pre-commit hook setup. | 4 hours |
| `scripts/setup.bat` + `bootstrap-windows.ps1` + `setup-wsl.ps1` + `teardown.ps1` + `wsl-compact.ps1` | **Discard.** Phase 1 is Mac/Linux only. Revisit if Windows needed later. | — |
| `scripts/full-maintenance.sh` + `python-maintenance.sh` + `kiro-maintenance.sh` + `wsl-maintenance.sh` | **Discard** Kiro/WSL versions. Port `python-maintenance.sh` with macOS stat syntax fix. | 2 hours |
| `scripts/harden-repo.sh` + `setup-filters.sh` + `git-filter-*.py` | Port verbatim but replace Bell's PII template in `git-filter-clean.py` (user writes own regexes or deletes filter entirely). | 2 hours |
| `POCKET-HQ.md` | Keep-with-edits: strip Bell branding, preserve 5-principle framing. Rename to `ARCHITECTURE.md` or similar. | 1 hour |
| `Projects/ Business/ Brand/ Life/ Archive/ docs/` (Pocket HQ scaffold) | **Discard.** TabulaJacqueliana is the actual Pocket HQ; Hypatia repo doesn't need a second one. | — |
| `docs/system-maintenance.md` | Port verbatim (generic ops doc). | — |
| `docs/growth-spec-script-offload.md` | Discard (Bell's personal work). | — |
| `FILE-STRUCTURE.md` | Regenerate for Hypatia structure. | 1 hour |
| `QUICKSTART.md` + `CUSTOMIZATION.md` + `CRITICAL-FILE-PROTECTION.md` + `README.md` (inside Nate's-kb) | Rewrite per Hypatia architecture. | 1 day |
| `lexicon.md` (Bell's AAVE voice markers) | **Discard entirely**. Hypatia's voice is different; lexicon is a from-scratch write. | — |
| `tests/` (script tests, 1,843 LOC, 7 files) | Port verbatim with path renames. | 4-6 hours |
| `Nate's-kb/vectorstore/tests/` (4 files, 415 LOC) | Port in Phase 3. | — |
| `.github/workflows/validate.yml` | Port with path renames; add script-tests step (gap in Bell's CI). | 1 hour |
| `.github/ISSUE_TEMPLATE/*` | Skip unless going public. | — |
| `LICENSE` (MIT, Bell copyright) | Replace with AJ-copyright MIT. | 5 min |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md` | Skip — private PKB, not OSS project. | — |
| `.gitignore` | Port with Kiro line removals + path renames. | 30 min |
| `.gitattributes` | Port line 1 (LF normalize); drop lines 2-3 (sanitize-memory filter) unless AJ wants PII filter. | 15 min |
| `.editorconfig` | Port verbatim. | 0 min |

**Total file-level work for Phase 1:** ~12-18 days of focused work (2-3 weeks calendar).

---

## Dependencies (pyproject.toml baseline)

```toml
[project]
name = "hypatia"
version = "0.1.0"
description = "Zettelkasten PKB partner"
requires-python = ">=3.10"  # save-session.py uses X | None syntax
authors = [{name = "AJ Strauman-Scott", email = "aj.scott@renphil.org"}]
license = {text = "MIT"}

dependencies = [
    "numpy>=1.24,<3",
    # Phase 3: fastembed, mcp added conditionally
]

[project.optional-dependencies]
vectorstore = [
    "fastembed>=0.3,<0.8",
    "mcp>=1.0",
]
dev = [
    "pytest>=7",
    "hypothesis>=6",
    "ruff>=0.3",
    "mypy>=1.8",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Lockfile via `uv lock`; committed.

---

## Portability analysis

### What works cross-machine (committed to git, portable)

- All `.clinerules/` files (markdown)
- All `hypatia-kb/protocols/*.md`
- All `hypatia-kb/Intelligence/*.json` + `-index.json` (JSON, deterministic)
- All `hypatia-kb/Memory/*.json`
- All `scripts/*.py`
- `pyproject.toml` + `uv.lock` (pinned deps)

### What doesn't port cleanly (per-machine setup)

1. **Python venv** — must rebuild per machine (`./scripts/setup.sh` creates it).
2. **fastembed model cache** (~/.cache/fastembed/, 90 MB) — downloads on first run per machine.
3. **VSCode + Cline extension** — must be installed on each machine.
4. **`hypatia.config.yaml`** — per-machine (vault path differs; it's gitignored).
5. **`vectorstore/vectors.npy` + `metadata.json` + `config.json`** — rebuildable on each machine via `kb_vectorize.py`; gitignored.
6. **fcntl-based locking in save-session.py** — POSIX only. **Windows requires WSL.** Document as known limitation.
7. **Launchctl/systemd watcher service (Phase 2)** — per-machine daemon config.
8. **Homebrew/apt packages** (git, python3, uv) — per-machine install.

### Flash-drive setup story (user-facing)

1. User plugs USB into any Mac/Linux machine with VSCode + Cline + Python 3.10+ + git installed.
2. Opens Hypatia repo folder in VSCode.
3. First-run detection: `scripts/setup.sh` checks for `hypatia.config.yaml`. If absent, prompts for vault path. Writes config.
4. `setup.sh` creates venv if absent, installs deps.
5. VSCode + Cline picks up `.clinerules/` automatically.
6. Hypatia introduces herself; session starts.
7. On Phase 3: first `hypatia_search` tool call triggers fastembed download if cache absent.

**Realistic setup time per machine:** 10-15 min (dep install + fastembed download).

### Windows story (deferred)

Phase 1 is Mac/Linux only. For Windows support:
- `fcntl` → `portalocker` dep (add to pyproject)
- `setup.sh` → `setup.ps1` port
- stat -c syntax in `python-maintenance.sh` → cross-platform Python rewrite
- Path separators (forward/back slash) — paths in save-session.py use `os.path.join`, should work; verify.

Budget: 1-2 weeks to add Windows-native support. Defer unless needed.

---

## Risk register / landmines

**HIGH risk**

1. **Trigger-keyword drift** between `.clinerules/10-skills-loading.md` and each `protocols/*.md` file's `**Keywords**:` line. Bell has this bug; Hypatia solves via `scripts/check-keyword-drift.py` pre-commit.
2. **`consciousness.md` drift pattern** (Bell): sub-agent files can get stale against kernel. Hypatia mitigation: if we add sub-agent pattern in Phase 2+, enforce "consciousness is auto-extracted from .clinerules/ at build time, never hand-edited."
3. **Voice rewrite risk** — Bell's voice sections are irreducibly his (southern urban AAVE, "bet," "deadass"). Swapping to "concise academic librarian" is a from-scratch write; hard to get right on first pass. Iterate based on usage.
4. **fcntl = POSIX only** — users who switch to Windows mid-session lose save-session functionality without WSL. Document prominently. Phase 2+ decision: port to `portalocker` or leave as-is.

**MEDIUM risk**

5. **Intelligence store bootstrap** — empty at ship → first few weeks of usage produce sparse retrieval results. By design (per Bell's phasing); just set expectations.
6. **Cline tool name differences** — protocols that say `fs_read` (Kiro) must become `read_file` (Cline). ~40+ occurrences in Nathaniel.md. Grep-and-replace pass.
7. **Markdown export sync** — if user edits the markdown exports directly, writes bypass JSON. Mitigation: exports regenerated on every `save-session`; user edits will be overwritten. Document in README.
8. **Pre-existing TabulaJacqueliana `_src/_meta/` files** — will still exist, won't be referenced by Hypatia. No conflict, just redundancy. Decision 8 explicitly accepts this.

**LOW risk**

9. **MCP tool name collision** — if Hypatia's vectorstore registers `hypatia_search`, and user also has other MCP servers with similar names, Cline may show ambiguous tool choices. Namespace prefix handles.
10. **Cline extension API changes** — Cline is under active development; `.clinerules/` schema may change. Pin Cline version in README's minimum-version recommendation.
11. **obsidian-git + Hypatia commits** — Hypatia in the vault will create git commits; obsidian-git auto-backup every 15 min will also commit. Potential race / noise. Mitigation: same as TabulaJacqueliana today; not a new problem.

---

## Open questions before Phase 1 starts

1. **Repo location** — `/Users/ajsscott/GitHub/Hypatia/` local-only, GitHub public/private, or flash-drive primary?
2. **LICENSE** — MIT (match Bell), or Apache 2.0, or something else?
3. **Phase 1 scope of zettelkasten content** — inject all the TabulaJacqueliana vault conventions into protocols, or keep protocols generic and rely on `hypatia.config.yaml` for vault-specific hints?
4. **First real ingest target** — when Phase 1 exits, what's the first source AJ wants to ingest via Hypatia? (Informs Phase 2 listener priority.)
5. **Voice iteration** — AJ to review Week 1's draft of `02-voice.md` and give explicit feedback before Week 2 starts.
6. **Git commit ownership** — does Hypatia's commits attribute to AJ (same as her existing git config)? Or to Hypatia with a different identity? Probably AJ.

---

## Deliverables

- This Document (committed).
- [[Hypatia Build]] Slope (committed).
- Phase 1 completion: working Hypatia repo, deployable.
- Phase 2 completion: at least one autonomous listener running daily.
- Phase 3 completion: full RRF/CSR retrieval + confidence calibration loop.

## Next action

1. AJ reviews this plan; flags any changes to decisions, scope, or ordering.
2. On approval: create the new repo (AJ decides location), run `git init`, commit scaffold.
3. Day 1 of Phase 1 begins: decompose Nathaniel.md → `.clinerules/01-11.md`.

**Estimated total calendar time, Phase 1 only:** 2-3 weeks with ~40-60 hours of focused work, assuming 10-20 hours/week available.
