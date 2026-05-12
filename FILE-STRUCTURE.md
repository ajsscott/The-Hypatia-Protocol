# File Structure

Snapshot of the repo's directory layout. Verified against the working tree as of Phase 1.5 substrate pivot (2026-05-12).

```
The-Hypatia-Protocol/
├── .github/
│   └── workflows/validate.yml        CI: JSON + schemas + keyword-drift + pytest + (future) cargo
├── .gitattributes                    LF normalization + sanitization filter attribs
├── .gitignore                        Excludes secrets, venvs, exports, workspace, Rust target/, Tauri build
├── .editorconfig                     LF line endings, UTF-8, trim whitespace
├── .python-version                   3.11
├── .vscode/                          VS Code workspace settings (carried for Continue.dev autocomplete)
│
├── kernel/                           Compact always-loaded kernel (~4K tokens, Q-33 redistribution)
│   ├── 01-identity.md                Who Hypatia is, super-objective, irreducible self, non-negotiables
│   ├── 02-voice.md                   Register, cadence, prohibitions
│   ├── 03-critical-gates.md          Inbox boundary, destructive action tiers, security never-violates
│   └── 04-routing.md                 Request classification, Decision Routes A-F, skills-loading discipline
│
├── mcp-servers/                      Hypatia-specific MCP servers (Rust)
│   └── protocols/                    Serves protocols + kernel-archive as MCP resources
│       ├── Cargo.toml
│       ├── README.md
│       └── src/main.rs
│
├── frontend/                         Custom Tauri 2.0 desktop UI (Rust)
│   ├── README.md
│   ├── src-tauri/                    Tauri Rust backend
│   │   ├── Cargo.toml
│   │   ├── tauri.conf.json           App bundle config (name, icon, permissions, build)
│   │   ├── build.rs
│   │   ├── icons/                    .gitkeep for now; populate before bundle build
│   │   └── src/
│   │       ├── main.rs               Entry point + Tauri setup
│   │       ├── goose_client.rs       HTTP client for Goose daemon
│   │       └── commands.rs           Tauri commands exposed to frontend JS
│   └── src/                          Frontend (HTML/CSS/JS)
│       ├── index.html
│       ├── styles.css                Alexandrian palette
│       └── main.js
│
├── goose-config/                     Goose custom-distro config
│   ├── README.md
│   ├── config.yaml                   Provider (Ollama) + extensions (MCP servers) + system prompt source
│   ├── extensions.yaml               MCP server registrations (deferred — content in config.yaml)
│   ├── regen-system-prompt.sh        Build script: kernel/01-04.md → system-prompt.md
│   └── goosehints.md                 Per-session reminders Goose surfaces
│
├── hypatia-kb/                       Knowledge base
│   ├── README.md
│   ├── QUICKSTART.md                 Operating cheat sheet
│   ├── CUSTOMIZATION.md
│   ├── Hypatia-Protocol.md           FROZEN HISTORICAL (superseded by kernel/04-routing.md)
│   ├── lexicon.md
│   │
│   ├── protocols/                    20 protocol files (lazy-loaded via MCP)
│   │   ├── README.md
│   │   ├── CRITICAL-FILE-PROTECTION.md
│   │   ├── security.md
│   │   ├── librarian-{role,vault-structure,note-schemas,tooling,writing-rules,memory,lint,customize}.md  (8)
│   │   ├── researcher-{investigate,prompt-enhance}.md  (2)
│   │   ├── writer-{draft,summarize,executive}.md  (3)
│   │   └── assistant-{development,plan,problem-solve,proactive,ingest}.md  (5)
│   │
│   ├── Intelligence/                 patterns / knowledge / reasoning / cross-refs / synonym-map
│   │   ├── *.json (ships empty; Q-06)
│   │   └── intelligence-operations.md + learning-loop.md
│   │
│   ├── Memory/                       memory.json + session-index + cache
│   ├── Benchmarks/                   24-test harness (Phase 3 re-baseline)
│   ├── exports/                      Dataview markdown (gitignored)
│   └── vectorstore/                  Python + fastembed (Phase 3 → vectorstore-mcp)
│
├── inbox/                            Curation staging (Q-22)
│   ├── SCHEMA.md                     Capture frontmatter spec
│   └── preferences/                  Free-form markdown captures
│
├── workspace/                        Hypatia scratch (gitignored except README)
│   └── README.md
│
├── docs/                             Reference documentation
│   ├── Hypatia Build Plan.md         Current planning spine (Phase 1.5 pivot edition)
│   ├── hypatia-build-plan-addendum.md   Phase 1 close-out deltas
│   ├── port-inventory.md             File-by-file Bell disposition (historical)
│   ├── open-questions.md             Durable decisions log (Q-01 ... Q-33)
│   ├── phase-1.5-kernel-redistribution-design.md   Q-33 implementation design
│   ├── system-maintenance.md
│   ├── vault-librarian-reference.md  Frozen vault CLAUDE.md
│   ├── growth-spec-script-offload.md
│   ├── llm-wiki.md                   Geoff Huntley's pattern reference
│   ├── research/
│   └── reference/
│       ├── phase-1-kernel-archive/   The 11-file Phase 1 kernel (now MCP-resource source)
│       ├── nathaniel/                Frozen Bell historical artifacts
│       └── bell-steering-files/      Archived Bell .steering-files content
│
├── scripts/                          Python tooling
│   ├── setup.sh                      First-run setup (filters, deps)
│   ├── setup-filters.sh              Git sanitization filter config
│   ├── run-python.sh                 Python runner (venv-aware)
│   ├── save-session.py               Atomic save: JSON + index + inbox + export + commit-stage
│   ├── hypatia-git-commit.py         Wraps git commit with Hypatia identity from config
│   ├── check-keyword-drift.py        Kernel keyword-map vs protocol-declaration linter
│   ├── export-intelligence-to-markdown.py   Dataview-queryable markdown exports
│   ├── session-cache.py              Session-local SQLite cache (FTS5)
│   ├── cascade-correction.py
│   ├── removal-cascade.py
│   ├── maintenance.py
│   ├── reseed.py
│   ├── secure-fetch.py               MCP fetch security proxy
│   ├── full-maintenance.sh
│   ├── python-maintenance.sh
│   ├── harden-repo.sh
│   ├── git-filter-clean.py + smudge.py
│   ├── normalize-schemas.py
│   ├── validate-schemas.py
│   └── pre-commit-kb-validate.sh
│
└── tests/                            Pytest suites (175 passing as of Phase 1 close)
    ├── test_save_session.py          Inbox + markdown-export coverage
    ├── test_save_oob.py              End-to-end + out-of-bounds
    ├── test_schema_validation.py     Schema gate (Q-05)
    ├── test_keyword_drift.py         Kernel-map linter gate (Q-05)
    ├── test_protocols_mcp.py         MCP server tests (Phase 1.5; needs `cargo build` first)
    ├── test_session_cache.py
    ├── test_cascade_correction.py
    ├── test_removal_cascade.py
    ├── test_maintenance.py
    └── test_edge_cases.py

Workspace root:
├── pyproject.toml + uv.lock          Python deps
├── Cargo.toml                        Rust workspace (frontend + mcp-servers)
├── hypatia.config.yaml               Per-machine config (vault path, git identity, model)
├── LICENSE                           MIT, AJ Strauman-Scott 2026 + Bell attribution
├── README.md
├── AGENTS.md
├── FILE-STRUCTURE.md                 This file
├── POCKET-HQ.md                      Pattern reference (scaffold dirs removed in Phase 1)
├── CLAUDE.md                         Claude Code port notes (gitignored)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── SECURITY.md
```

---

## Path routing reference

| Domain | Path | Purpose |
|---|---|---|
| Compact kernel (always-loaded) | `kernel/` | Identity + voice + critical gates + routing instinct |
| MCP server (Rust) | `mcp-servers/protocols/` | Serves 32 protocol resources to Goose |
| Frontend (Rust + Tauri) | `frontend/` | Hypatia's desktop app |
| Goose distro | `goose-config/` | Provider + extensions + system prompt source |
| Per-machine config | `hypatia.config.yaml` | Vault path, git identity, paths, preferences |
| Knowledge base | `hypatia-kb/` | All protocols, intelligence, memory, vectorstore |
| Protocols | `hypatia-kb/protocols/` | 20 lazy-load cluster + cross-cutting protocols |
| Intelligence | `hypatia-kb/Intelligence/` | patterns / knowledge / reasoning / cross-refs / synonym-map |
| Memory | `hypatia-kb/Memory/` | memory.json + session logs + cache |
| Vectorstore | `hypatia-kb/vectorstore/` | fastembed + RRF semantic search |
| Inbox | `inbox/preferences/` | Free-form captures awaiting Scholar consolidation |
| Workspace | `workspace/` | Per-machine scratch (gitignored except README) |
| Build docs | `docs/Hypatia Build Plan.md` + `docs/*-addendum.md` | Planning spine + corrections |
| Phase 1 kernel archive | `docs/reference/phase-1-kernel-archive/` | The 11-file Phase 1 kernel, now MCP-resource source |
| Bell reference | `docs/reference/nathaniel/` + `bell-steering-files/` | Frozen historical artifacts |
| Scripts | `scripts/` | Setup, save, validation, maintenance, git filters |
| Tests | `tests/` + `hypatia-kb/vectorstore/tests/` | Pytest suites |

---

## Notes on state

- **`kernel/`** is the always-loaded compact system prompt (~4K tokens). Hypatia's identity, voice, critical gates, and routing instinct. Loaded by Goose at session start.
- **`docs/reference/phase-1-kernel-archive/`** holds the Phase 1 11-file kernel (~20K tokens). Now serves as MCP-resource source via `mcp-servers/protocols/` (Q-33 redistribution).
- **`hypatia-kb/protocols/`** consolidates the entire protocol layer; cluster-prefixed naming.
- **`mcp-servers/protocols/`** is the Rust MCP server that serves `protocols/` + `phase-1-kernel-archive/` as resources to Goose.
- **`frontend/`** is the custom Tauri 2.0 desktop UI (Phase 1.5 v1 scaffold; Phase 2 adds menubar/USB/screen).
- **`goose-config/`** is the Goose custom-distro config; tells Goose how to load Hypatia + which MCP servers to register.
- **`hypatia-kb/Hypatia-Protocol.md`** is frozen historical reference. Live decision routing is `kernel/04-routing.md` + `docs/reference/phase-1-kernel-archive/11-decision-routes.md` (via MCP).
- **Roo Code substrate (Phase 1)** was abandoned during the 2026-05-12 pivot. `.roomodes` deleted. `.roo/rules-hypatia/` content moved to `docs/reference/phase-1-kernel-archive/`.
