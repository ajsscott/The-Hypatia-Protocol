# The Hypatia Protocol

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Substrate: Goose + Tauri](https://img.shields.io/badge/substrate-Goose%20%2B%20Tauri-blue)
![Platform: Mac](https://img.shields.io/badge/platform-Mac-lightgrey)

**A persistent AI partner-scholar for the TabulaJacqueliana zettelkasten vault.**

Hypatia is a curator, not a chatbot. She processes Seeds into Trees, maintains the citation graph, flags contradictions across sources, and refuses to silently let stale claims outlast the session that could have caught them.

This is a personal project (AJ Strauman-Scott's). It's open source under MIT in case the architecture is useful to others, but it is specifically tuned for the TabulaJacqueliana vault and AJ's working register. It's not a general-purpose framework.

**Phase 1.5 substrate pivot (2026-05-12):** Originally targeted Roo Code as the substrate; pivoted during Phase 1 empirical testing to Goose backend + Rust/Tauri custom frontend. See `docs/Hypatia Build Plan.md` for current phasing.

---

## What this is

A Rust + Python + markdown framework that ships:

- **A compact kernel** (`kernel/`, 4 files, ~4K tokens) — Hypatia's always-loaded identity / voice / critical gates / routing instinct. Loaded as Goose's system prompt.
- **A protocols MCP server** (`mcp-servers/protocols/`, Rust) — serves the 20 cluster protocols + 10 kernel-archive detail expansions as MCP resources, lazy-loaded by Goose on keyword match.
- **A knowledge base** (`hypatia-kb/`) with empty-at-launch JSON stores for memory, patterns, knowledge, reasoning; a vectorstore for semantic search; the 20 cluster protocols.
- **A capture pipeline** (`inbox/preferences/`) where Hypatia files free-form markdown observations during sessions. AJ consolidates manually during maintenance; no auto-promotion to canonical stores (Q-22 inbox boundary).
- **A custom Tauri frontend** (`frontend/`, Rust + Tauri 2.0) — Hypatia's desktop UI, talks to Goose daemon over HTTP.
- **A Goose custom-distro config** (`goose-config/`) — preconfigured providers, extensions, system prompt, hints.
- **Operational scripts** (`scripts/`, Python) for setup, validation, save-time persistence, vectorstore sync, git filter chain.

---

## Lineage

Forked from Warner Bell's [Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (MIT). Bell's framework was a Kiro-targeted persistent AI personality system with a southern-urban AAVE voice register ("Nate, your cognitive consigliere"). The fork:

- **Replaces the voice** with a Greco-Roman Alexandrian scholar register (named for Hypatia of Alexandria).
- **Replaces the substrate** with Goose backend (Apache 2.0, MCP-first, Rust core) + a custom Rust/Tauri frontend for persistent system-level integration.
- **Adds an inbox boundary** so the canonical stores grow only through deliberate curation, never silent accumulation.
- **Ships empty** so the wiki compounds through usage, not Bell's prior content.
- **Architecturally redistributes** the original monolithic kernel into compact-always-loaded + protocols-as-MCP-resources (Q-33).
- **Targets Mac only** (cross-platform deferred indefinitely; the Scholar's working surface is a single machine).

Bell's original is preserved under `docs/reference/` as historical reference. The 11-file Phase 1 kernel (Roo Code-targeted) is archived at `docs/reference/phase-1-kernel-archive/` and now serves as MCP-resource source material for Hypatia's Goose backend.

---

## Substrate and dependencies

| Layer | Choice |
|---|---|
| Agent backend | [Goose](https://block.github.io/goose/) (Block, Apache 2.0) |
| Frontend | Custom Tauri 2.0 app (Rust) |
| LLM provider | Ollama (local), with Anthropic / OpenAI fallback via Goose |
| Local model target | TBD per Q-17 re-evaluation; candidates: `gemma4`, `qwen2.5-coder:14b`, `qwen3-coder:30b`, `devstral:24b` |
| Python | 3.11+ (for scripts and tests) |
| Rust | 1.75+ |
| Package managers | `uv` (Python) + `cargo` (Rust) |
| Vault | [Obsidian](https://obsidian.md/) on the TabulaJacqueliana vault |

---

## Quick start (Mac)

```bash
# Clone
git clone https://github.com/<owner>/The-Hypatia-Protocol.git
cd The-Hypatia-Protocol

# Python environment
uv sync

# Rust build (compiles MCP servers + Tauri frontend)
cargo build --release

# Install Goose
brew install block-goose

# Pull a model (start with gemma4 for native large context)
ollama pull gemma4

# Configure Goose with Hypatia distro
export HYPATIA_REPO_ROOT="$PWD"
export GOOSE_CONFIG_PATH="$PWD/goose-config/config.yaml"
./goose-config/regen-system-prompt.sh     # builds system-prompt.md from kernel/

# Launch Goose daemon (terminal 1)
goose serve --port 8765

# Launch Hypatia frontend (terminal 2)
cd frontend && cargo tauri dev
```

Hypatia introduces herself with `"Hello, Scholar."` on session start. (More accurately: she greets with whatever the compact kernel + her register produce; the greeting is hers, not scripted.)

Full setup walk-through: [`goose-config/README.md`](goose-config/README.md) + [`frontend/README.md`](frontend/README.md).

---

## Operating

| Trigger | What happens |
|---|---|
| `Hello, Hypatia` (or any greeting) | She introduces herself in Alexandrian register; loads `protocol://librarian-role` via MCP if continuing a curation thread |
| `save` | Runs the 6-step save flow: session log + index update + memory snapshot + inbox flush + vectorstore sync + git commit (loads `protocol://detail/save`) |
| `health check` | Non-destructive ecosystem audit |
| `inbox triage` | Surface inbox captures for Scholar consolidation decisions |
| `process this seed` | Invokes `protocol://assistant-ingest`; runs the six-step ingest flow |

Decision routing: **A** (direct) / **B** (with context) / **C** (clarify) / **D** (options) / **E** (confirm destructive) / **F** (pre-action analysis). Default for non-trivial tasks: Route F.

Full kernel content (always-loaded): [`kernel/`](kernel/). Protocol resources (lazy-loaded via MCP): [`hypatia-kb/protocols/`](hypatia-kb/protocols/) + [`docs/reference/phase-1-kernel-archive/`](docs/reference/phase-1-kernel-archive/).

---

## Architecture

```
kernel/                     Compact always-loaded kernel (~4K tokens)
├── 01-identity.md
├── 02-voice.md
├── 03-critical-gates.md
└── 04-routing.md

mcp-servers/                Custom Rust MCP servers
├── protocols/              Serves protocols + kernel-archive as MCP resources

frontend/                   Custom Tauri desktop UI
├── src-tauri/              Rust backend (window, commands, Goose client)
└── src/                    HTML/CSS/JS frontend

goose-config/               Goose custom-distro config
├── config.yaml             Provider + extensions + system prompt source
├── extensions.yaml         MCP server registrations
└── regen-system-prompt.sh  Concatenates kernel/ for Goose

hypatia-kb/                 Knowledge base
├── protocols/              20 lazy-loaded protocols (librarian/researcher/writer/assistant + cross-cutting)
├── Intelligence/           patterns / knowledge / reasoning + indexes
├── Memory/                 memory.json + session logs
└── vectorstore/            fastembed + RRF semantic search (Phase 3)

inbox/                      Curation staging (Q-22 inbox boundary)
└── preferences/            Free-form markdown captures

scripts/                    Python tooling (save-session, validation, maintenance)
tests/                      Pytest suites
docs/                       Build Plan, decisions log, reference archive
hypatia.config.yaml         Per-machine config (vault path, git identity)
```

Full directory layout: [`FILE-STRUCTURE.md`](FILE-STRUCTURE.md).

---

## Two load-bearing conventions

### Inbox boundary (Q-22)

Hypatia does NOT write directly to `hypatia-kb/Memory/*.json` or `hypatia-kb/Intelligence/*.json` during sessions. New observations (preferences, decisions, patterns, knowledge, reasoning) get captured to `inbox/preferences/*.md` as free-form markdown. The Scholar consolidates inbox captures into canonical JSON stores during scheduled maintenance.

Narrow exceptions where the save command writes to `memory.json` directly: `last_session_snapshot`, `session-index.json` append, session log file creation. Mechanical metadata, not content curation.

### Ship empty, grow through curation

The intelligence and memory stores ship empty. They grow only through deliberate Scholar consolidation of inbox captures. CSR queries return zero matches until usage accumulates entries.

---

## Identity

- **Name**: Hypatia.
- **Pronouns**: she / her.
- **User address**: "Scholar" (used sparingly, not every response).
- **Voice register**: Greco-Roman Alexandrian scholar. Direct, peer-academic, cites sources, devil's-advocate by default, mild warmth, no sycophancy.
- **Non-negotiables**: accuracy over agreeableness, brevity over completeness, cite the source.

Full identity: [`kernel/01-identity.md`](kernel/01-identity.md). Voice: [`kernel/02-voice.md`](kernel/02-voice.md).

---

## License

MIT, AJ Strauman-Scott 2026. Fork of Warner Bell's [Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (also MIT). See [`LICENSE`](LICENSE).

---

## Contributing

This is a personal-use project. Bug reports and design discussion welcome via issues. Pull requests for Hypatia herself are unlikely to be accepted since the persona is tuned for one user; PRs for substrate-agnostic improvements (vectorstore, save pipeline, schema validation, security filters, protocols MCP server, Tauri frontend ergonomics) are open. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
