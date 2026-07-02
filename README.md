# The Hypatia Protocol

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Substrate: Goose + Obsidian](https://img.shields.io/badge/substrate-Goose%20%2B%20Obsidian-blue)
![Platform: Mac](https://img.shields.io/badge/platform-Mac-lightgrey)

**A persistent AI partner-scholar for the TabulaJacqueliana zettelkasten vault.**

Hypatia is a curator, not a chatbot. She processes Seeds into Trees, maintains the citation graph, flags contradictions across sources, and refuses to silently let stale claims outlast the session that could have caught them.

This is a personal project (AJ Strauman-Scott's). It's open source under MIT in case the architecture is useful to others, but it is specifically tuned for the TabulaJacqueliana vault and AJ's working register. It's not a general-purpose framework.

**Phase 1.5 substrate pivot (2026-05-12):** Originally targeted Roo Code as the substrate; pivoted during Phase 1 empirical testing to Goose backend + Rust/Tauri custom frontend. See `docs/Hypatia Build Plan.md` for current phasing.

---

## What this is

A Rust + Python + markdown framework that ships:

- **A compact kernel** (`kernel/`, 4 files, ~4K tokens) — Hypatia's always-loaded identity / voice / critical gates / routing instinct. Loaded as Goose's system prompt.
- **A protocols MCP server** (`mcp-servers/protocols/`, Rust) — serves the 20 cluster protocols + 16 kernel-archive detail expansions (36 resources) and, critically, the `read_protocol` / `list_protocols` **tools** — Goose exposes only tools to the model, so the tools are the live loading path.
- **A knowledge base** (`hypatia-kb/`) with empty-at-launch JSON stores for memory, patterns, knowledge, reasoning; a hybrid vectorstore (`vault_search` — RRF-fused semantic + keyword search over the vault's notes, plus the KB stores); the 20 cluster protocols.
- **A capture pipeline** (`inbox/preferences/`) where Hypatia files free-form markdown observations during sessions. AJ consolidates manually during maintenance; no auto-promotion to canonical stores (Q-22 inbox boundary).
- **An Obsidian surface** — Hypatia lives in the vault via ACP (`goose acp` + the community Agent Client plugin; `docs/obsidian-setup.md`). The Tauri frontend (`frontend/`) is PARKED — Obsidian is the natural UI.
- **A Goose custom-distro layer** (`goose-config/`) — a generator that turns the kernel into Goose recipes + global goosehints, derived Ollama models (`hypatia-gemma4` 12B / `hypatia-gemma4-lite` E4B), and the think-shim that disables Gemma-4's latency-killing hidden thinking.
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
| Frontend | Obsidian (Agent Client plugin over ACP) + terminal launcher; Tauri app parked |
| LLM provider | Ollama (local), with Anthropic / OpenAI fallback via Goose |
| Local model target | `hypatia-gemma4` (Gemma-4 12B QAT, thinking disabled — Q-17 answered 2026-07-02, evidence in `docs/q17-eval/`); `hypatia-gemma4-lite` (E4B) for light bursts |
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

# Install Goose + configure the Ollama provider once
brew install block-goose-cli && goose configure

# Build the derived models (thinking-disabled, right ctx/samplers)
ollama create hypatia-gemma4 -f goose-config/hypatia-gemma4.Modelfile
ollama create hypatia-gemma4-lite -f goose-config/hypatia-gemma4-lite.Modelfile

# Keep the model resident between turns
launchctl setenv OLLAMA_KEEP_ALIVE 1h

# Alias the launcher, then launch her
echo "alias hypatia='\$HOME/GitHub/other/The-Hypatia-Protocol/scripts/launch-hypatia.sh'" >> ~/.zshrc
source ~/.zshrc
hypatia            # full model, interactive
hypatia lite       # light-burst tier
hypatia ask "..."  # one-shot, throwaway session
```

For Hypatia inside Obsidian (ACP + Agent Client plugin): [`docs/obsidian-setup.md`](docs/obsidian-setup.md).

Hypatia introduces herself with `"Hello, Scholar."` on session start. (More accurately: she greets with whatever the compact kernel + her register produce; the greeting is hers, not scripted.)

Full setup walk-through: [`goose-config/README.md`](goose-config/README.md) + [`docs/phase-1.5-launch-runbook.md`](docs/phase-1.5-launch-runbook.md).

---

## Operating

| Trigger | What happens |
|---|---|
| `Hello, Hypatia` (or any greeting) | She introduces herself in Alexandrian register; loads `protocol://librarian-role` via MCP if continuing a curation thread |
| `save` | Runs the 6-step save flow: session log + index update + memory snapshot + inbox flush + vectorstore sync + git commit (loads `protocol://detail/save`) |
| `health check` | Non-destructive ecosystem audit |
| `inbox triage` | Surface inbox captures for Scholar consolidation decisions |
| `grow this Seed` / `process this seed` | Invokes `protocol://assistant-ingest`; runs the six-step ingest flow (**growing**, in the vault's lexicon) |
| `how's the climb?` | PM progress through Mountains — bottom-up: Steps ascend Trails ascend Slopes summit Mountains (**climbing**) |
| `what do we have about X?` | `vault_search` — hybrid semantic search over the vault's 2,000+ notes |

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

frontend/                   Tauri desktop UI (PARKED — Obsidian is the UI)

goose-config/               Goose custom-distro layer
├── regen-system-prompt.sh  Generator: kernel → recipes + goosehints
├── hypatia-gemma4.Modelfile        Q-17 model (12B QAT, 32K ctx)
├── hypatia-gemma4-lite.Modelfile   E4B light tier (16K ctx)
└── com.hypatia.think-shim.plist    launchd agent for the think-shim

hypatia-kb/                 Knowledge base
├── protocols/              20 lazy-loaded protocols (librarian/researcher/writer/assistant + cross-cutting)
├── Intelligence/           patterns / knowledge / reasoning + indexes
├── Memory/                 memory.json + session logs
└── vectorstore/            fastembed + RRF hybrid search: KB stores + vault notes (vault_search MCP tool)

inbox/                      Curation staging (Q-22 inbox boundary)
└── preferences/            Free-form markdown captures

scripts/                    Python tooling (save-session, validation, launcher, think-shim, Q-17 eval)
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
