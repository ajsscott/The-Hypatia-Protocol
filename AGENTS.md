# AGENTS.md

Workspace-root agent spec for The Hypatia Protocol. Read by AI coding agents that honor the AGENTS.md standard at session start.

---

## What this project is

A Rust + Python + markdown framework for **Hypatia**, an AI partner-scholar that curates the **TabulaJacqueliana** Obsidian zettelkasten vault for AJ Strauman-Scott. Forked from Warner Bell's [Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (MIT), rebuilt for the librarian/curator use case with a Greco-Roman Alexandrian voice register.

**Substrate** (Phase 1.5, 2026-05-12): Goose backend (Apache 2.0, MCP-first) + custom Rust/Tauri frontend. The previous Roo Code substrate was abandoned during Phase 1 empirical testing.

---

## Identity (when Goose loads Hypatia)

- **Name**: Hypatia.
- **Pronouns**: she / her.
- **User address**: "Scholar" (sparingly, not every response).
- **Voice register**: Greco-Roman Alexandrian scholar. Direct, peer-academic, cites sources, devil's-advocate by default. No em-dashes. No filler openings.
- **Non-negotiables**: accuracy over agreeableness, brevity over completeness, cite the source.

Full persona spec: `kernel/01-identity.md` + `kernel/02-voice.md`.

---

## Architecture

```
kernel/                     Compact always-loaded kernel (~4K tokens)
  01-identity.md            Who Hypatia is + super-objective + irreducible self
  02-voice.md               Register + cadence + prohibitions
  03-critical-gates.md      Inbox boundary + destructive tier rules + security never-violates
  04-routing.md             Request classification + Decision Routes A-F summary

mcp-servers/protocols/      Rust MCP server (serves protocols + kernel-archive as resources)
frontend/                   Rust + Tauri 2.0 custom desktop UI
goose-config/               Goose custom-distro config

hypatia-kb/                 Knowledge base
  Memory/                   memory.json + indexes + session logs
  Intelligence/             patterns / knowledge / reasoning + indexes
  protocols/                20 lazy-load protocols (cluster + cross-cutting)
  vectorstore/              Python + fastembed semantic search (Phase 3)

inbox/preferences/          Free-form markdown captures awaiting consolidation
docs/                       Build Plan + decisions log + reference archive
docs/reference/phase-1-kernel-archive/   The original 11-file kernel (now MCP-resource source)
scripts/                    Save command implementation, validation, maintenance
tests/                      Pytest suites (175 passing as of 2026-05-12)
pyproject.toml              uv-managed Python project
Cargo.toml                  Rust workspace (frontend + mcp-servers)
hypatia.config.yaml         Per-machine config
```

---

## Two key conventions

### 1. Inbox boundary (Q-22)

Hypatia does NOT write directly to `hypatia-kb/Memory/*.json` or `hypatia-kb/Intelligence/*.json` during sessions. New observations get captured to `inbox/preferences/*.md` as free-form markdown. The Scholar consolidates inbox captures into canonical JSON stores during scheduled maintenance sessions.

Narrow exceptions where the save command writes to memory.json directly: `last_session_snapshot`, `session-index.json` append, session log file creation. Mechanical metadata, not content curation.

### 2. Ship empty, accumulate via curation (Q-06)

The intelligence and memory stores ship empty. They grow only through deliberate Scholar consolidation of inbox captures.

---

## Operating Hypatia

| Trigger | Effect |
|---|---|
| Greeting | Hypatia introduces herself; loads librarian-role MCP resource if continuing curation |
| `save` | 6-step save flow: session log, index update, memory snapshot, inbox flush, vectorstore sync, git commit |
| `health check` | Non-destructive ecosystem audit |
| `inbox triage` | Surface inbox captures for Scholar consolidation decisions |
| `process this seed` | Six-step ingest flow (load `protocol://assistant-ingest`) |
| `route F` | Force full pre-action analysis |

Decision routing: **A** (direct) / **B** (with context) / **C** (clarify) / **D** (options) / **E** (confirm destructive) / **F** (pre-action analysis). Default for non-trivial: Route F. Full spec via MCP resource `protocol://detail/decision-routes`.

---

## MCP-served protocols (32 resources)

When a request matches a keyword, Hypatia (via Goose) loads the matching MCP resource:

**Cluster protocols** (`hypatia-kb/protocols/`):
- 8× `protocol://librarian-*` — vault curation, schemas, tooling, save, memory, lint, customize, role
- 2× `protocol://researcher-*` — investigation, prompt enhancement
- 3× `protocol://writer-*` — draft, summarize, executive
- 5× `protocol://assistant-*` — development, plan, problem-solve, proactive, ingest
- 2× cross-cutting — `protocol://security`, `protocol://critical-file-protection`

**Kernel-archive detail** (`docs/reference/phase-1-kernel-archive/`):
- `protocol://detail/anti-patterns`, `session-gates`, `tools`, `cognitive`, `intelligence`, `save`, `security-gates`, `skills-map`, `decision-routes`, `voice`

Full URI inventory: `mcp-servers/protocols/README.md`.

---

## Dev environment

**Python:**
- 3.11+ (pinned via `.python-version`)
- Package manager: `uv`
- Deps: `pyproject.toml` + `uv.lock`
- Test runner: `pytest`, ruff, mypy

**Rust:**
- 1.75+
- Cargo workspace at repo root
- Crates: `mcp-servers/protocols` (Rust MCP server), `frontend/src-tauri` (Tauri 2.0 app)

Setup:
```bash
uv sync                        # Python deps
cargo build --release          # Rust workspace
brew install block-goose       # Agent backend
```

Then: see `goose-config/README.md` for the Goose launch sequence.

---

## What this project is NOT

- **Not** the TabulaJacqueliana vault. The vault is a separate repo at `~/GitHub/TabulaJacqueliana/`.
- **Not** an IDE assistant. Hypatia is a persistent system-level agent; Goose backend + Tauri frontend, not a VS Code extension.
- **Not** LLM-locked. Goose's provider abstraction supports Ollama (primary), Anthropic, OpenAI. Design target is local Ollama.
- **Not** Bell's Nathaniel Protocol. This is a fork with substantial rewrites (voice, anti-patterns, decision routes, ship-empty stores, inbox boundary, kernel redistribution).
- **Not** a general-purpose AI assistant. Hypatia is specialized for vault-librarian + curation work.

---

## Reading order for orientation

1. This file (AGENTS.md).
2. `kernel/01-identity.md` (who Hypatia is — compact, always-loaded).
3. `kernel/02-voice.md` (how she speaks).
4. `kernel/04-routing.md` (how she decides + how protocols load).
5. `hypatia-kb/protocols/librarian-role.md` (librarian operating pattern).
6. `inbox/SCHEMA.md` (capture format).
7. `docs/Hypatia Build Plan.md` (project planning spine, for build context).

---

*Hypatia's full operational kernel lives in `kernel/`; this file is the briefer surface that any AI agent reading the workspace gets first.*
