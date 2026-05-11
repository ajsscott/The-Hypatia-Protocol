# File Structure

Snapshot of the repo's directory layout. Verified against the working tree, not aspirational.

```
The-Hypatia-Protocol/
├── .github/                          GitHub community files
│   ├── ISSUE_TEMPLATE/
│   └── workflows/validate.yml        CI: JSON validity + vectorstore tests
├── .vscode/                          Editor config (Roo Code lives here)
├── .roo/
│   └── rules-hypatia/                The kernel (11 files, ~111 KB)
│       ├── 01-identity.md
│       ├── 02-voice.md
│       ├── 03-anti-patterns.md
│       ├── 04-session-gates.md
│       ├── 05-tools.md
│       ├── 06-cognitive.md
│       ├── 07-intelligence-layer.md
│       ├── 08-save-command.md
│       ├── 09-security.md
│       ├── 10-skills-loading.md
│       └── 11-decision-routes.md
├── .roomodes                         Custom mode definition (slug: hypatia)
├── .gitattributes                    LF normalization + sanitization filter attribs
├── .gitignore                        Excludes secrets, generated artifacts, venvs
├── .editorconfig                     LF line endings, UTF-8, trim whitespace
├── .python-version                   3.11
├── pyproject.toml                    Project metadata + dependencies (uv)
├── uv.lock                           Locked dependency tree
├── AGENTS.md                         Cross-tool workspace agent spec
├── CLAUDE.md                         Claude Code port-work notes (gitignored)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── FILE-STRUCTURE.md                 This file
├── LICENSE                           MIT, AJ Strauman-Scott 2026
├── POCKET-HQ.md                      Inherited pattern from Bell (see file for caveats)
├── README.md
├── SECURITY.md
│
├── hypatia-kb/                       Knowledge base
│   ├── README.md
│   ├── QUICKSTART.md                 Operating cheat sheet (save, health check, etc.)
│   ├── CUSTOMIZATION.md
│   ├── CRITICAL-FILE-PROTECTION.md   Protected paths + inbox boundary enforcement
│   ├── Hypatia-Protocol.md           Decision Routes A-F (content rewrite pending)
│   ├── lexicon.md
│   │
│   ├── # Domain protocols (13)
│   ├── customization-protocol.md
│   ├── development-protocol.md
│   ├── executive-communication-protocol.md
│   ├── maintenance-protocol.md
│   ├── memory-protocol.md
│   ├── planning-protocol.md
│   ├── proactive-offering-protocol.md
│   ├── problem-solving-protocol.md
│   ├── prompt-enhancement-protocol.md
│   ├── research-protocol.md
│   ├── security-protocol.md
│   ├── summarization-protocol.md
│   ├── writing-protocol.md
│   │
│   ├── protocols/                    Librarian protocols (vault-specific)
│   │   ├── README.md
│   │   ├── librarian-role.md
│   │   ├── librarian-vault-structure.md
│   │   ├── librarian-note-schemas.md
│   │   ├── librarian-tooling.md
│   │   └── librarian-writing-rules.md
│   │
│   ├── Intelligence/                 Patterns, knowledge, reasoning stores
│   │   ├── README.md
│   │   ├── intelligence-operations.md
│   │   ├── learning-loop.md
│   │   ├── knowledge.json            Ships empty
│   │   ├── knowledge-index.json
│   │   ├── patterns.json             Ships empty
│   │   ├── patterns-index.json
│   │   ├── reasoning.json            Ships empty
│   │   ├── reasoning-index.json
│   │   ├── cross-references.json
│   │   └── synonym-map.json
│   │
│   ├── Memory/                       Session and entity memory
│   │   ├── README.md
│   │   ├── memory.json               Starter (identity + preferences)
│   │   ├── memory-index.json
│   │   ├── session-index.json
│   │   ├── archive/                  Archived session logs
│   │   └── cache/                    Session-local SQLite cache
│   │
│   ├── Benchmarks/                   Frozen Bell-era benchmark snapshots
│   │
│   └── vectorstore/                  Hybrid semantic search
│       ├── SETUP.md
│       ├── BENCHMARK.md
│       ├── concat.py                 Shared KB concatenation
│       ├── kb_vectorize.py           Build vector index from KB
│       ├── kb_query.py               Hybrid search (RRF: semantic + keyword)
│       ├── kb_sync.py                Sync vectorstore with KB changes
│       ├── kb_server.py              MCP server for semantic search
│       ├── kb_benchmark.py           Embedding model benchmarking
│       ├── run-server.sh             MCP server launcher
│       └── tests/                    Hypothesis-based tests
│
├── inbox/                            Curation staging
│   ├── SCHEMA.md                     Capture frontmatter spec
│   └── preferences/                  Free-form markdown captures
│
├── docs/                             Reference documentation
│   ├── Hypatia Build Plan.md         Locked planning spine
│   ├── hypatia-build-plan-addendum.md
│   ├── port-inventory.md             File-by-file Bell disposition
│   ├── open-questions.md             Durable decisions log
│   ├── system-maintenance.md
│   ├── vault-librarian-reference.md  Frozen vault CLAUDE.md (source of librarian-* protocols)
│   ├── growth-spec-script-offload.md
│   ├── llm-wiki.md                   Geoff Huntley's pattern reference
│   ├── research/
│   └── reference/
│       ├── nathaniel/                Frozen Bell historical artifacts
│       └── bell-steering-files/      Archived Bell .steering-files content
│
├── scripts/                          Setup, validation, save-time persistence
│   ├── setup.sh                      First-run setup (filters, deps, vectorstore)
│   ├── setup-filters.sh              Git sanitization filter config only
│   ├── run-python.sh                 Python runner (venv-aware)
│   ├── save-session.py               Atomic save: JSON mutations + index + vectorstore + commit
│   ├── session-cache.py              Session-local SQLite cache (FTS5)
│   ├── cascade-correction.py         Scan stores for stale claims; apply fixes
│   ├── removal-cascade.py            Delete entries with full cascade
│   ├── maintenance.py                Health checks + safe auto-fixes
│   ├── reseed.py                     Golden seed verification and reseed
│   ├── secure-fetch.py               MCP fetch security proxy (URL filtering)
│   ├── full-maintenance.sh           Maintenance wrapper (Mac, single phase)
│   ├── python-maintenance.sh         Python cache cleanup
│   ├── harden-repo.sh                Pre-push confidential-pattern scan
│   ├── git-filter-clean.py           Git clean filter (sanitize on commit)
│   ├── git-filter-smudge.py          Git smudge filter (restore on checkout)
│   ├── normalize-schemas.py          JSON schema normalization
│   ├── validate-schemas.py           JSON schema validation
│   └── pre-commit-kb-validate.sh     Pre-commit hook for KB validation
│
├── tests/                            Script test suites (scaffold; gaps tracked in Build Plan)
│   ├── test_save_session.py
│   ├── test_session_cache.py
│   ├── test_cascade_correction.py
│   ├── test_removal_cascade.py
│   ├── test_maintenance.py
│   ├── test_edge_cases.py
│   └── test_columbo_oob.py
│
└── # Pocket HQ scaffold (inherited from Bell; empty .gitkeep at present)
    ├── Projects/
    ├── Business/
    ├── Brand/
    ├── Life/
    │   ├── Career/  Education/  Family/  Finances/
    │   └── Goals/   Health/     Home/    Journal/
    └── Archive/
```

## Path routing reference

| Domain | Path | Purpose |
|---|---|---|
| Kernel | `.roo/rules-hypatia/` | Always-loaded system-prompt rules (Roo mode = hypatia) |
| Mode definition | `.roomodes` | Hypatia custom mode (slug, role, tool groups) |
| Agent spec | `AGENTS.md` | Cross-tool workspace agent overview |
| Knowledge base | `hypatia-kb/` | All protocols, intelligence, memory, vectorstore |
| Domain protocols | `hypatia-kb/*-protocol.md` | Substrate-agnostic protocols (memory, research, etc.) |
| Librarian protocols | `hypatia-kb/protocols/librarian-*.md` | Vault-specific behavior (TabulaJacqueliana) |
| Intelligence | `hypatia-kb/Intelligence/` | patterns / knowledge / reasoning + indexes |
| Memory | `hypatia-kb/Memory/` | memory.json + session logs + cache |
| Vectorstore | `hypatia-kb/vectorstore/` | fastembed + RRF semantic search |
| Inbox | `inbox/preferences/` | Free-form captures awaiting Scholar consolidation |
| Build docs | `docs/Hypatia Build Plan.md` + `docs/*-addendum.md` | Locked planning spine + corrections |
| Bell reference | `docs/reference/` | Frozen historical artifacts from upstream fork |
| Scripts | `scripts/` | Setup, save, validation, maintenance, git filters |
| Tests | `tests/` + `hypatia-kb/vectorstore/tests/` | Script + vectorstore test scaffolding |

## Notes on inherited state

- **Pocket HQ scaffold** (`Projects/`, `Business/`, `Brand/`, `Life/`, `Archive/`) ships from the upstream fork. See `POCKET-HQ.md` for the pattern's origins and how Hypatia diverges from it (the TabulaJacqueliana vault is intentionally external, not consolidated here).
- **`hypatia-kb/Benchmarks/`** retains Bell-era benchmark snapshots as historical reference. Hypatia-specific benchmarks will replace them as the framework accumulates usage.
- **`docs/reference/`** is the holding pen for frozen upstream content. Do not edit in place; treat as read-only history.
- **`tests/` at repo root** contains Bell's original test scaffolding. Phase 1 of the port writes new tests for Hypatia's adapted scripts.
