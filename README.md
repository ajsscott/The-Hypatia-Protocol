# The Hypatia Protocol

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Substrate: Roo Code](https://img.shields.io/badge/substrate-Roo%20Code-blue)
![Platform: Mac](https://img.shields.io/badge/platform-Mac-lightgrey)

**A persistent AI partner-scholar for the TabulaJacqueliana zettelkasten vault.**

Hypatia is a curator, not a chatbot. She processes Seeds into Trees, maintains the citation graph, flags contradictions across sources, and refuses to silently let stale claims outlast the session that could have caught them.

This is a personal project (AJ Strauman-Scott's). It's open source under MIT in case the architecture is useful to others, but it is specifically tuned for the TabulaJacqueliana vault and AJ's working register. It's not a general-purpose framework.

---

## What this is

A Python + markdown framework that ships:

- **A custom Roo Code mode** (`.roomodes`, slug: `hypatia`) defining the Hypatia persona: voice, role, tool access.
- **A kernel** (`.roo/rules-hypatia/`, 11 files) that Roo Code loads as Hypatia's system-prompt instructions: identity, voice, anti-patterns, gates, tools, cognitive layer, intelligence layer, save command, security, skills-loading, decision routes.
- **A knowledge base** (`hypatia-kb/`) with empty-at-launch JSON stores for memory, patterns, knowledge, reasoning; a vectorstore for semantic search; 13 domain protocols; 5 librarian-specific protocols for vault work.
- **A capture pipeline** (`inbox/preferences/`) where Hypatia files free-form markdown observations during sessions. AJ consolidates manually during maintenance; no auto-promotion to canonical stores.
- **Operational scripts** (`scripts/`) for setup, validation, save-time persistence, vectorstore sync, git filter chain.

---

## Lineage

Forked from Warner Bell's [Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (MIT). Bell's framework was a Kiro-targeted persistent AI personality system with a southern-urban AAVE voice register ("Nate, your cognitive consigliere"). The fork:

- **Replaces the voice** with a Greco-Roman Alexandrian scholar register (named for Hypatia of Alexandria).
- **Replaces the substrate** with Roo Code (multi-provider; runs against local Ollama for LLM-agnostic operation; Anthropic / OpenAI as alternatives).
- **Adds an inbox boundary** so the canonical stores grow only through deliberate curation, never silent accumulation.
- **Ships empty** so the wiki compounds through usage, not Bell's prior content.
- **Targets Mac only** (cross-platform deferred indefinitely; the Scholar's working surface is a single machine).

Bell's original is preserved under `docs/reference/` as historical reference. The decomposed `.roo/rules-hypatia/` kernel was distilled from Bell's 2,576-line `Nathaniel.md` source over the course of the Phase 1 port.

---

## Substrate and dependencies

| Layer | Choice |
|---|---|
| Editor | VS Code |
| AI extension | [Roo Code](https://docs.roocode.com/) |
| LLM provider | Ollama (local), Anthropic, or OpenAI (configurable per-task in Roo) |
| Recommended local models | `mistral-nemo:12b`, `qwen3:14b`, `deepseek-r1:14b` |
| Python | 3.11+ |
| Package manager | `uv` |
| Vault | [Obsidian](https://obsidian.md/) on the TabulaJacqueliana vault |

---

## Quick start (Mac)

```bash
# Clone
git clone https://github.com/<owner>/The-Hypatia-Protocol.git
cd The-Hypatia-Protocol

# Set up Python environment
uv sync

# Set up git filters and pre-commit hooks
./scripts/setup.sh

# Install Roo Code in VS Code
#   Open VS Code → Extensions → search "Roo Code" → install
#   Configure your LLM provider (Ollama recommended for local; Anthropic / OpenAI as alternatives)

# Open the repo in VS Code; Roo Code reads .roomodes + .roo/rules-hypatia/ on activation.
# Switch to Hypatia mode in Roo (mode picker → Hypatia).
```

Hypatia introduces herself with `"Hello, Scholar!"` on session start.

---

## Operating

| Command | Effect |
|---|---|
| `save` | Persist the session: log + index update + snapshot + inbox flush + vectorstore sync + git commit |
| `detailed save` | Verbose save with per-step accounting |
| `health check` | Non-destructive ecosystem audit |
| `full maintenance` | Health check + cleanup with Scholar confirmation |
| `inbox triage` | Surface inbox captures for Scholar consolidation decisions |
| `route F` | Request full pre-action analysis for non-trivial decisions |

Decision routing: **A** (direct) / **B** (with context) / **C** (clarify) / **D** (options) / **E** (confirm destructive) / **F** (pre-action analysis). Default for non-trivial tasks: Route F.

Full operating guide: [`hypatia-kb/QUICKSTART.md`](hypatia-kb/QUICKSTART.md).

---

## Architecture

```
.roo/
  rules-hypatia/          11-file kernel (loaded when Roo mode = hypatia)
.roomodes                 Custom mode definition (slug, roleDefinition, tool groups)
AGENTS.md                 Cross-tool workspace agent spec
hypatia-kb/               Knowledge base
  Memory/                 memory.json + indexes + session logs
  Intelligence/           patterns.json / knowledge.json / reasoning.json + indexes
  protocols/              librarian-* protocols for vault-specific behavior
  *-protocol.md           13 domain protocols (memory, research, writing, etc.)
  vectorstore/            Python + fastembed semantic search
inbox/
  preferences/            Free-form markdown captures awaiting Scholar consolidation
  SCHEMA.md               Capture frontmatter spec
docs/
  Hypatia Build Plan.md   Locked planning spine
  hypatia-build-plan-addendum.md
  open-questions.md       Decision log (build-process artifact)
  port-inventory.md       Bell file disposition
  reference/              Frozen Bell historical artifacts
scripts/                  Setup, validation, maintenance, save-time persistence
tests/                    Critical-path scaffolding (Phase 1+)
pyproject.toml + uv.lock  Python project + locked deps (uv)
.python-version           3.11 pin
```

Full directory layout: [`FILE-STRUCTURE.md`](FILE-STRUCTURE.md).

---

## Two load-bearing conventions

### Inbox boundary

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

Full identity: [`.roo/rules-hypatia/01-identity.md`](.roo/rules-hypatia/01-identity.md). Voice: [`.roo/rules-hypatia/02-voice.md`](.roo/rules-hypatia/02-voice.md).

---

## License

MIT, AJ Strauman-Scott 2026. Fork of Warner Bell's [Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (also MIT). See [`LICENSE`](LICENSE).

---

## Contributing

This is a personal-use project. Bug reports and design discussion welcome via issues. Pull requests for Hypatia herself are unlikely to be accepted since the persona is tuned for one user; PRs for substrate-agnostic improvements (vectorstore, save pipeline, schema validation, security filters) are open. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
