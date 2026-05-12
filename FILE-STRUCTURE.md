# File Structure

Snapshot of the repo's directory layout. Verified against the working tree as of Phase 1 close (2026-05-12).

```
The-Hypatia-Protocol/
├── .github/
│   └── workflows/validate.yml        CI: JSON + schemas + keyword-drift + pytest
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
│       ├── 10-skills-loading.md      Single source of truth for keyword routing
│       └── 11-decision-routes.md
├── .roomodes                         Custom mode definition (slug: hypatia)
├── .gitattributes                    LF normalization + sanitization filter attribs
├── .gitignore                        Excludes secrets, venvs, exports, workspace
├── .editorconfig                     LF line endings, UTF-8, trim whitespace
├── .python-version                   3.11
├── pyproject.toml                    Project metadata + dependencies (uv)
├── uv.lock                           Locked dependency tree
├── hypatia.config.yaml               Vault path, git identity, paths, preferences
├── AGENTS.md                         Cross-tool workspace agent spec
├── CLAUDE.md                         Claude Code port-work notes (gitignored)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── FILE-STRUCTURE.md                 This file
├── LICENSE                           MIT, AJ Strauman-Scott 2026 + Bell attribution
├── POCKET-HQ.md                      Pattern reference (scaffold dirs removed)
├── README.md
├── SECURITY.md
│
├── hypatia-kb/                       Knowledge base
│   ├── README.md
│   ├── QUICKSTART.md                 Operating cheat sheet
│   ├── CUSTOMIZATION.md
│   ├── Hypatia-Protocol.md           FROZEN HISTORICAL (superseded by .roo/rules-hypatia/11)
│   ├── lexicon.md
│   │
│   ├── protocols/                    All lazy-loaded protocols (20 files)
│   │   ├── README.md
│   │   ├── CRITICAL-FILE-PROTECTION.md
│   │   ├── security.md
│   │   │
│   │   ├── # Librarian cluster (8)
│   │   ├── librarian-role.md
│   │   ├── librarian-vault-structure.md
│   │   ├── librarian-note-schemas.md
│   │   ├── librarian-tooling.md
│   │   ├── librarian-writing-rules.md
│   │   ├── librarian-memory.md
│   │   ├── librarian-lint.md
│   │   ├── librarian-customize.md
│   │   │
│   │   ├── # Researcher cluster (2)
│   │   ├── researcher-investigate.md
│   │   ├── researcher-prompt-enhance.md
│   │   │
│   │   ├── # Writer cluster (3)
│   │   ├── writer-draft.md
│   │   ├── writer-summarize.md
│   │   ├── writer-executive.md
│   │   │
│   │   └── # Assistant cluster (5)
│   │       ├── assistant-development.md
│   │       ├── assistant-plan.md
│   │       ├── assistant-problem-solve.md
│   │       ├── assistant-proactive.md
│   │       └── assistant-ingest.md
│   │
│   ├── Intelligence/                 Patterns, knowledge, reasoning stores
│   │   ├── README.md
│   │   ├── intelligence-operations.md
│   │   ├── learning-loop.md
│   │   ├── knowledge.json            Ships empty (Q-06)
│   │   ├── knowledge-index.json
│   │   ├── patterns.json             Ships empty
│   │   ├── patterns-index.json
│   │   ├── reasoning.json            Ships empty
│   │   ├── reasoning-index.json
│   │   ├── cross-references.json
│   │   └── synonym-map.json          Seeded (21 groups, Q-14)
│   │
│   ├── Memory/                       Session and entity memory
│   │   ├── README.md
│   │   ├── memory.json               Seeded (identity stanza)
│   │   ├── memory-index.json
│   │   ├── session-index.json
│   │   ├── archive/                  Archived session logs
│   │   └── cache/                    Session-local SQLite cache
│   │
│   ├── Benchmarks/                   24-test harness (re-baseline in Phase 3)
│   │   ├── README.md
│   │   ├── run-benchmark.py          Loads concat-kernel + stores; emits PASS/FAIL
│   │   ├── benchmark-candidates.md
│   │   ├── save-protocol-benchmark.md
│   │   └── img-gate-stress-test.md
│   │
│   ├── exports/                      Generated Dataview markdown (gitignored)
│   │
│   └── vectorstore/                  Hybrid semantic search (Phase 3)
│       ├── SETUP.md
│       ├── BENCHMARK.md
│       ├── concat.py                 Shared KB concatenation
│       ├── kb_vectorize.py           Build vector index from KB
│       ├── kb_query.py               Hybrid search (RRF: semantic + keyword)
│       ├── kb_sync.py                Sync vectorstore with KB changes
│       ├── kb_server.py              MCP server for semantic search
│       ├── kb_benchmark.py           Embedding-model benchmarking
│       ├── run-server.sh             MCP server launcher
│       └── tests/                    Hypothesis-based tests
│
├── inbox/                            Curation staging (Q-22 boundary)
│   ├── SCHEMA.md                     Capture frontmatter spec
│   └── preferences/                  Free-form markdown captures
│
├── workspace/                        Hypatia scratch (gitignored except README)
│   └── README.md
│
├── docs/                             Reference documentation
│   ├── Hypatia Build Plan.md         Locked planning spine
│   ├── hypatia-build-plan-addendum.md
│   ├── port-inventory.md             File-by-file Bell disposition
│   ├── open-questions.md             Durable decisions log (Q-01 .. Q-32)
│   ├── system-maintenance.md
│   ├── vault-librarian-reference.md  Frozen vault CLAUDE.md
│   ├── growth-spec-script-offload.md
│   ├── llm-wiki.md                   Geoff Huntley's pattern reference
│   ├── research/
│   └── reference/
│       ├── nathaniel/                Frozen Bell historical artifacts
│       └── bell-steering-files/      Archived Bell .steering-files content
│
├── scripts/                          Setup, validation, save-time persistence
│   ├── setup.sh                      First-run setup (filters, deps)
│   ├── setup-filters.sh              Git sanitization filter config only
│   ├── run-python.sh                 Python runner (venv-aware)
│   ├── save-session.py               Atomic save: JSON + index + inbox + export + commit-stage
│   ├── hypatia-git-commit.py         Wraps `git commit` with Hypatia identity from config
│   ├── check-keyword-drift.py        Kernel keyword-map vs protocol-declaration linter
│   ├── export-intelligence-to-markdown.py   Dataview-queryable markdown exports
│   ├── session-cache.py              Session-local SQLite cache (FTS5)
│   ├── cascade-correction.py         Scan stores for stale claims; apply fixes
│   ├── removal-cascade.py            Delete entries with full cascade
│   ├── maintenance.py                Health checks + safe auto-fixes
│   ├── reseed.py                     Golden seed verification and reseed
│   ├── secure-fetch.py               MCP fetch security proxy (URL filtering)
│   ├── full-maintenance.sh           Maintenance wrapper (Mac)
│   ├── python-maintenance.sh         Python cache cleanup
│   ├── harden-repo.sh                Pre-push confidential-pattern scan
│   ├── git-filter-clean.py           Git clean filter (sanitize on commit)
│   ├── git-filter-smudge.py          Git smudge filter (restore on checkout)
│   ├── normalize-schemas.py          JSON schema normalization
│   ├── validate-schemas.py           JSON schema validation
│   └── pre-commit-kb-validate.sh     Pre-commit hook for KB validation
│
└── tests/                            Script-level test suites
    ├── test_save_session.py          Includes TestInboxFlush + TestMarkdownExport
    ├── test_save_oob.py              End-to-end + out-of-bounds
    ├── test_schema_validation.py     Schema gate per Q-05 (NEW)
    ├── test_keyword_drift.py         Kernel-map linter gate per Q-05 (NEW)
    ├── test_session_cache.py
    ├── test_cascade_correction.py
    ├── test_removal_cascade.py
    ├── test_maintenance.py
    └── test_edge_cases.py
```

## Path routing reference

| Domain | Path | Purpose |
|---|---|---|
| Kernel | `.roo/rules-hypatia/` | Always-loaded system-prompt rules (Roo mode = hypatia) |
| Mode definition | `.roomodes` | Hypatia custom mode (slug, role, tool groups) |
| Agent spec | `AGENTS.md` | Cross-tool workspace agent overview |
| Per-machine config | `hypatia.config.yaml` | Vault path, git identity, paths, preferences |
| Knowledge base | `hypatia-kb/` | All protocols, intelligence, memory, vectorstore |
| Protocols | `hypatia-kb/protocols/` | All 20 lazy-load protocols (4 clusters + cross-cutting) |
| Intelligence | `hypatia-kb/Intelligence/` | patterns / knowledge / reasoning / cross-refs / synonym-map |
| Memory | `hypatia-kb/Memory/` | memory.json + session logs + cache |
| Vectorstore | `hypatia-kb/vectorstore/` | fastembed + RRF semantic search |
| Generated exports | `hypatia-kb/exports/` | Dataview markdown (gitignored, regenerated on save) |
| Inbox | `inbox/preferences/` | Free-form captures awaiting Scholar consolidation |
| Workspace | `workspace/` | Per-machine scratch (gitignored except README) |
| Build docs | `docs/Hypatia Build Plan.md` + `docs/*-addendum.md` | Locked planning spine + corrections |
| Bell reference | `docs/reference/` | Frozen historical artifacts from upstream fork |
| Scripts | `scripts/` | Setup, save, validation, maintenance, git filters |
| Tests | `tests/` + `hypatia-kb/vectorstore/tests/` | Script + vectorstore test scaffolding |

## Notes on state

- **`hypatia-kb/protocols/` consolidates the entire protocol layer** (Phase 1 commit e18568b). Bell's `hypatia-kb/*-protocol.md` flat layout was relocated and cluster-prefixed.
- **`hypatia-kb/Benchmarks/`** holds the 24-test harness only. Bell's dated snapshots were removed in Phase 1; re-baseline in Phase 3 once stores accumulate.
- **`hypatia-kb/Hypatia-Protocol.md`** is frozen historical reference. Live decision routing is `.roo/rules-hypatia/11-decision-routes.md`.
- **`docs/reference/`** is the holding pen for frozen upstream content. Do not edit in place.
- **`tests/`** contains Bell's original scaffolding plus three new Hypatia-native tests (`test_schema_validation`, `test_keyword_drift`, the extended `test_save_session`).
