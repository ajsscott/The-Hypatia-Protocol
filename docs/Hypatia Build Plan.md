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
last_updated: 2026-05-12
complete: false
---

# Hypatia Build Plan

**Status:** Phase 1 substantially complete (2026-05-12). Substrate pivoted from Roo Code to Goose backend + Rust/Tauri frontend during Phase 1 close-out empirical testing. This document captures the post-pivot plan.

**Derived from:** [[Building a Persistent AI Partner A Context Engineering Case Study]] + [Warner Bell's Nathaniel Protocol](https://github.com/Warner-Bell/The-Nathaniel-Protocol) (forked under MIT).

**Companion Slope:** [[Hypatia Build]].

---

## Design decisions (current)

The original 8 decisions (2026-04-22) plus all subsequent revisions through Q-33 (2026-05-12).

| # | Area | Decision | Source |
|---|---|---|---|
| 1 | Substrate (host) | **Goose** (Block, Apache 2.0) as agent-loop / MCP / LLM-provider backend | Q-31 (2026-05-12) |
| 2 | Substrate (frontend) | **Custom Rust + Tauri** frontend talking to Goose as backend daemon | Q-32 (2026-05-12) |
| 3 | LLM provider | Ollama primary (LLM-agnostic; Q-02 + Q-21). Cloud APIs (Anthropic, OpenAI) supported via Goose's provider abstraction. | Q-02, Q-21 |
| 4 | Local model target | **TBD** — Q-17 revision pending. Original `qwen3:14b` failed empirical test (thinking-mode + kernel size). `qwen2.5-coder:14b` and `gemma4` evaluated; substrate-side bug masked model behavior. Final pick deferred until Phase 1.5 testing with compact kernel. | Q-17 (revision pending) |
| 5 | Scope | Bell's general-partner scope + zettelkasten PKB telos + persistent system-level agent behavior (popup on flash-drive plug-in, screen-aware, multi-MCP). | Q-original-2 + Q-31 |
| 6 | Architecture | **Compact kernel (~3-5K tokens) + protocols-as-MCP-resources.** The 40K-token monolithic kernel from Phase 1 redistributes: identity / voice / critical gates stay always-loaded; protocols / anti-patterns details / decision routes / intelligence layer migrate to MCP-served resources loaded on demand. | Q-33 (2026-05-12) |
| 7 | Skill clusters | One persona + four clusters (Librarian / Researcher / Writer / Assistant). Cluster organization preserved across substrate pivot. | Q-original-4 |
| 8 | Persona | "Hypatia" — Alexandrian scholar register, she/her, addresses user as "Scholar" sparingly. | Q-24 (2026-05-11) |
| 9 | Stores | JSON authoritative + markdown export layer (Dataview-queryable). Direct vault R/W via MCP. | Q-original-6 |
| 10 | Memory flow | Inbox boundary: free-form markdown captures during sessions; Scholar consolidates into JSON stores during scheduled maintenance. | Q-22 (2026-05-11) |
| 11 | Phasing | Phase 0 (DONE) → Phase 1 (DONE) → Phase 1.5 (substrate) → Phase 2 (persistent behaviors) → Phase 3 (retrieval) → Phase 4 (distribution). | Q-31 reframe |
| 12 | Repo location | `/Users/ajsscott/GitHub/The-Hypatia-Protocol/` (rename-in-place from Bell's fork). | Q-01 |
| 13 | Repo scope boundary | Hypatia's stores independent of TabulaJacqueliana's `_src/_meta/` for portability. | Q-original-8 |
| 14 | Vault-convention authority | `hypatia-kb/protocols/librarian-*.md` is authoritative. Vault CLAUDE.md becomes a derived stub once Phase 1.5 ships. | Q-07 (2026-04-22) |
| 15 | Substrate replaces vault YOLO | Hypatia replaces the Obsidian YOLO plugin as the vault's in-Obsidian LLM substrate. | Q-23 (2026-05-11) |
| 16 | Build identity | AJ Strauman-Scott authors port commits; distinct `Hypatia <hypatia@local>` identity for Hypatia's own commits. | Q-08 (2026-04-22) |
| 17 | Phase 1 test coverage | Critical-path only: save-session, schema-validation, keyword-drift. Other scripts deferred to Phase 1.5+. | Q-05 (2026-04-22) |
| 18 | JSON store bootstrap | Ship empty. Stores grow only through Scholar consolidation. | Q-06 (2026-04-22) |

Full decision history with rationale: `docs/open-questions.md`.

---

## Architecture (post-pivot)

```
┌─────────────────────────────────────────────────────────────┐
│  Hypatia Frontend (Rust + Tauri)                            │
│  - Menubar / popup window UI                                │
│  - USB-mount detection (Phase 2)                            │
│  - Screen-capture surface (Phase 2)                         │
│  - Bundle target: flash-drive (Phase 4)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │  HTTP / IPC (Goose daemon API)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Goose Backend (Apache 2.0, Rust core)                      │
│  - Agent loop (intake → plan → tool-use → response)         │
│  - MCP client (manages 70+ ext + custom Hypatia MCPs)       │
│  - LLM provider abstraction (Ollama / Anthropic / OpenAI)   │
│  - Session state, conversation history                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Ollama      │  │  MCP Servers     │  │  MCP Servers     │
│  (local)     │  │  (Hypatia-built) │  │  (community)     │
│              │  │                  │  │                  │
│  qwen3 /     │  │  - protocols-mcp │  │  - filesystem    │
│  gemma4 /    │  │  - vectorstore   │  │  - github        │
│  qwen2.5-c   │  │  - vault-rw      │  │  - obsidian      │
│              │  │  - screen-watch  │  │  - ...           │
│              │  │  - file-watcher  │  │                  │
│              │  │  - save-session  │  │                  │
└──────────────┘  └──────────────────┘  └──────────────────┘
```

**Key shift from Phase 1 design:** Hypatia's identity, protocols, intelligence layer, decision routes — these are no longer all in an always-loaded monolithic kernel. The compact always-loaded kernel carries only identity + voice + critical never-violate gates (~3-5K tokens). Everything else is MCP-served on demand, consistent with Goose's design model and with the original Build Plan's "Protocol-as-MCP" framing.

---

## Phase 0 — Vault-librarian content migration (DONE, 2026-05-11)

Migrated the 717-line vault `CLAUDE.md` into `hypatia-kb/protocols/librarian-*.md` (5 files + README). Per Q-07 decision, hypatia-kb becomes authoritative for vault conventions; vault CLAUDE.md will become a derived stub once Phase 1.5 ships (Q-18 demotion gate pending).

**Deliverables (complete):**
- `hypatia-kb/protocols/librarian-role.md`
- `hypatia-kb/protocols/librarian-vault-structure.md`
- `hypatia-kb/protocols/librarian-note-schemas.md`
- `hypatia-kb/protocols/librarian-tooling.md`
- `hypatia-kb/protocols/librarian-writing-rules.md`

Source preserved at `docs/vault-librarian-reference.md` as frozen historical reference.

---

## Phase 1 — Hypatia's brain (DONE, 2026-05-12; one carve-out)

Substrate-agnostic infrastructure. Travels intact across the Phase 1.5 substrate pivot.

**Complete:**

- **Kernel decomposition** — `.roo/rules-hypatia/01-11.md` (11 files, ~40K tokens). Note: this will be **redistributed** in Phase 1.5 per Q-33; current monolithic form is too big for Goose's design model.
- **20 protocols** in `hypatia-kb/protocols/`: 8 librarian-* + 2 researcher-* + 3 writer-* + 5 assistant-* + 2 cross-cutting (security, CRITICAL-FILE-PROTECTION). All cluster-prefixed per Q-25.
- **Scripts (24 files):** save-session, hypatia-git-commit, check-keyword-drift, export-intelligence-to-markdown, validate-schemas, plus inherited cascade/maintenance/removal/reseed/secure-fetch/git-filters/normalize/setup.
- **Tests:** 175 pytest passing. Q-05 critical-path coverage (save-session inbox + export wiring, schema validation, keyword drift) + Bell's inherited test scaffolding.
- **CI workflow:** uv-based, gates on JSON validity + schema validation + keyword drift + script pytest + vectorstore pytest.
- **Config:** `hypatia.config.yaml` (vault path, instance, git identity, paths, preferences). Real file, committed (not example template per Q-30).
- **Memory + Intelligence stores:** ship empty (Q-06). Schemas validated. synonym-map seeded with 21 zettelkasten groups (Q-14).
- **Inbox boundary:** `inbox/SCHEMA.md` + `inbox/preferences/` for free-form captures (Q-22).
- **LICENSE:** AJ MIT + Bell attribution.
- **Decision routes:** `.roo/rules-hypatia/11-decision-routes.md` (Q-13 four fixes resolved).
- **Voice + persona:** Q-24 (Scholar address, she/her, Alexandrian register).
- **All Bell refs** scrubbed except historical/credit contexts.

**Carve-out (deferred to Phase 1.5):**
- **Kernel architectural redistribution (Q-33).** Empirical Phase 1 testing showed the 40K-token monolithic kernel is too big for fast local inference + exceeds substrate (Goose) design limits. Redistribution requires Phase 1.5 work.

---

## Phase 1.5 — Substrate integration (current, ~3-6 weeks)

The Phase 1 brain plugs into the Goose backend + Rust/Tauri frontend body.

### Week 1 — Kernel architectural redistribution (Q-33)

Refactor the 11 always-loaded kernel files into:

- **Compact kernel** (~3-5K tokens, always-loaded): identity + voice + critical never-violate gates (security, file-protection, inbox boundary)
- **MCP-served resources** (~35K tokens, lazy-loaded by keyword/intent): full anti-patterns, decision routes A-F detail, intelligence-layer specifics, cluster protocols

Build `protocols-mcp-server` — a custom MCP server that exposes the protocols/ directory as MCP resources. Hypatia (via Goose) calls `read_resource(protocol://librarian-role)` on keyword match instead of having the full text pre-loaded.

**Deliverables:**
- New compact kernel files (or reorganized .roo/rules-hypatia/ → kernel/)
- `mcp-servers/protocols/` — Rust MCP server serving protocols as resources
- Updated keyword-drift linter to verify kernel + MCP resource consistency
- Pytest coverage for the MCP server

### Week 2 — Goose installation + Hypatia configuration

- Install Goose locally (CLI + daemon mode)
- Create custom Goose distro: branding + provider config + extension config for Hypatia
- Wire Ollama provider; pin model (TBD after Q-17 revision)
- Register Hypatia's MCP servers (protocols, vault-rw, save-session)
- Validate: Hypatia introduces herself in Alexandrian register; uses Scholar address sparingly; behavior matches Q-24 spec

### Week 3 — Rust + Tauri frontend scaffold

- New `frontend/` directory at repo root
- Tauri project: `cargo create-tauri-app`
- Basic UI: menubar icon, popup chat window, conversation rendering
- HTTP client → Goose daemon API
- Settings panel (provider, model, vault path — reads from hypatia.config.yaml)
- macOS app bundle build

### Week 4 — First end-to-end behaviors

- Save-session works end-to-end (Hypatia → save-session.py → JSON updates → markdown export → git commit via hypatia-git-commit.py)
- Read/write vault: drop a Seed → Hypatia ingests via assistant-ingest protocol → creates Tree drafts
- Conversation persistence across sessions
- Goose's session memory + Hypatia's inbox/Memory schemas coexist (Q-22 boundary holds)

**Phase 1.5 exit criteria:**

- [ ] Hypatia launches from the Tauri app, introduces herself correctly
- [ ] At least one full ingest cycle (Seed → Tree drafts → save-session → commit)
- [ ] 3+ inbox captures consolidated into Memory by Scholar
- [ ] Q-17 model decision finalized (which Ollama model is canonical)
- [ ] No regressions in pytest suite (175 → growing)

---

## Phase 2 — Persistent agent behaviors (~4-6 weeks after Phase 1.5)

The Tauri frontend grows from "manually launched chat window" to "always-present system-level agent."

**Capabilities to add:**

- **Menubar / tray persistence** — Hypatia lives in the menubar; popup window opens on click or hotkey
- **USB-mount detection** — `IOKit` (via `core-foundation` Rust crate) watches for flash-drive mount; auto-launches Hypatia if mount contains a `hypatia.config.yaml`
- **File watcher MCP server** — watches `Seeds/` in the vault; new file = ingest trigger queued for Hypatia review
- **Screen capture MCP server** — Hypatia can request screenshots when context warrants (Scholar reviews suggestion, approves capture)
- **Vision integration** — pair screen capture with vision-capable model (Gemma 4 has native vision; can route specific tasks to vision-enabled model)

**New MCP servers (built in Rust as Tauri sidecars or standalone):**
- `screen-watcher` — capture + describe + queue
- `mount-detector` — USB plug-in → notify-Hypatia
- `file-watcher` — vault Seeds + drop-zone

**Phase 2 exit criteria:**

- [ ] Hypatia auto-launches when flash-drive plugged into a new Mac
- [ ] Watcher runs continuously; ≥10 watcher-triggered ingests processed
- [ ] Screen capture used in ≥3 real curation sessions without workflow friction

---

## Phase 3 — Retrieval intelligence (~4-6 weeks after Phase 2)

Bell's RRF + Hypatia-specific CSR fusion + confidence calibration. Implemented as MCP servers (consistent with the architecture).

**MCP servers to build:**

- `vectorstore-mcp` — wraps Bell's Python vectorstore (port from `hypatia-kb/vectorstore/`). Exposes `hypatia_search`, `hypatia_sync`, `hypatia_rebuild` tools. Python sidecar invoked from Rust frontend or from Goose's MCP host.
- `csr-mcp` — Context Signal Routing: tag/category index lookup with synonym expansion. Likely Rust-native for speed.
- `calibration-mcp` — confidence calibration loop. Reads `memory.json confidence_events[]`, computes per-pattern calibration error, surfaces during save-session.

**Other Phase 3 work:**

- Fix `kb_query.py:268-290` tiebreak-by-distillation-level comment drift
- Fix `kb_benchmark.py:88,113` hardcoded `/tmp/` → `tempfile.gettempdir()`
- Port `vectorstore/tests/*.py` (573 LOC, hypothesis-based)
- Decide embedding model: `all-MiniLM-L6-v2` (faster) vs `all-mpnet-base-v2` (more accurate) vs newer 2026 options
- Resolve Q-04 — Scholar confirms/rejects "CSR is behavioral" framing

**Phase 3 exit criteria:**

- [ ] `hypatia_search` MCP tool returns sub-second results on populated stores
- [ ] Vectorstore rebuilds in <10s for a 500-entry store
- [ ] Confidence calibration adjusts at least one pattern's confidence automatically

---

## Phase 4 — Distribution (~2-4 weeks after Phase 3)

Flash-drive bundle: Hypatia + Goose + Ollama + chosen model + custom frontend, all on a single USB stick.

**Deliverables:**

- `dist/hypatia-flash/` bundle structure:
  ```
  hypatia-flash/
  ├── Hypatia.app/           Tauri app bundle (macOS)
  ├── goose                  Goose binary
  ├── ollama                 Ollama binary
  ├── models/                Pre-pulled model blobs (~10-15 GB)
  ├── hypatia.config.yaml    Per-machine config (vault path auto-detected)
  ├── hypatia-kb/            Knowledge base + protocols + Intelligence/Memory
  ├── mcp-servers/           Custom Rust MCP servers
  └── README.md              Setup instructions
  ```
- Auto-mount detection script
- First-run flow: detect new machine → prompt for vault path → bootstrap config → launch Hypatia
- macOS code-signing (likely ad-hoc; full notarization later)

**Phase 4 exit criteria:**

- [ ] Plug flash drive into a second Mac; Hypatia auto-launches; passes Phase 1.5 exit criteria on new machine
- [ ] Bundle size <30 GB (fits modern fast USB-C flash drives comfortably)
- [ ] Documented setup time per new machine: <10 minutes including model load

---

## Repo structure (target end of Phase 1.5)

```
The-Hypatia-Protocol/
├── kernel/                            Compact always-loaded kernel (~3-5K tokens, Q-33)
│   ├── 01-identity.md
│   ├── 02-voice.md
│   └── 03-critical-gates.md           (consolidates session-gates + security)
│
├── .roo/rules-hypatia/                LEGACY 11-file kernel (Phase 1) — kept during transition
│                                       Once kernel/ stabilizes, this becomes archival
│
├── hypatia-kb/
│   ├── protocols/                     20 protocol files (Phase 1 layout preserved)
│   ├── Intelligence/                  JSON stores + indexes (ship empty)
│   ├── Memory/                        memory.json + session-index + cache
│   ├── exports/                       Dataview markdown (gitignored)
│   ├── Benchmarks/                    24-test harness
│   └── vectorstore/                   Python (Phase 3 → vectorstore-mcp)
│
├── mcp-servers/                       NEW. Hypatia-specific MCP servers
│   ├── protocols/                     (Rust) Serves protocols/ as MCP resources
│   ├── vault-rw/                      (Rust) Vault read/write
│   ├── save-session/                  (Rust wrapper around scripts/save-session.py)
│   └── README.md
│
├── frontend/                          NEW. Rust + Tauri custom UI
│   ├── src-tauri/                     Tauri backend (Rust)
│   ├── src/                           Frontend code (HTML/CSS/JS or Yew)
│   ├── Cargo.toml
│   └── tauri.conf.json
│
├── goose-config/                      NEW. Goose custom distro
│   ├── Cargo.toml                     Distro Cargo config
│   ├── config.yaml                    Provider + extension defaults
│   └── README.md
│
├── inbox/                             Curation staging (Q-22)
├── workspace/                         Per-machine scratch (gitignored)
├── docs/                              Reference + planning + decisions log
├── scripts/                           Python tooling (save-session etc.)
├── tests/                             Pytest suites
├── .github/workflows/                 CI
├── hypatia.config.yaml                Per-machine config
├── pyproject.toml + uv.lock           Python deps
├── Cargo.toml + Cargo.lock            Rust workspace (frontend + mcp-servers)
├── LICENSE                            MIT, AJ + Bell attribution
├── README.md
├── AGENTS.md
└── CLAUDE.md                          Claude Code port notes (gitignored)
```

---

## Dependencies

**Python (Phase 1):** unchanged. `pyproject.toml` defines `fastembed`, `numpy`, `mcp`, `pyyaml`. uv-managed.

**Rust (new in Phase 1.5):** Cargo workspace at repo root.

```toml
# Cargo.toml (workspace)
[workspace]
members = [
    "frontend/src-tauri",
    "mcp-servers/protocols",
    "mcp-servers/vault-rw",
    "mcp-servers/save-session",
]
resolver = "2"

[workspace.dependencies]
tauri = "2.0"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
# MCP SDK (Rust):
rmcp = "0.x"  # version TBD when Phase 1.5 starts
```

**External binaries:** Goose (installed via brew or download), Ollama (already installed).

---

## Risk register / landmines

**HIGH**

1. **Compact-kernel redesign is design-heavy work, not mechanical refactor.** Deciding what stays always-loaded vs what becomes MCP resource is a real judgment call. Mitigation: validate with empirical "does Hypatia behave correctly?" tests after each redistribution pass.

2. **Goose has open Ollama context-handling issues** ([#1253](https://github.com/block/goose/issues/1253), [#7264](https://github.com/block/goose/issues/7264), [#4000](https://github.com/block/goose/issues/4000)). May hit similar truncation bugs we saw in Roo Code. Mitigation: aggressive kernel compaction reduces total prompt size; if still hitting limits, contribute upstream fix.

3. **Rust + Tauri learning curve.** Hypatia is the Scholar's first significant Rust project alongside ongoing CUNY-SPS work. Mitigation: start with simplest possible Tauri scaffold; iterate; lean on Tauri's docs + community.

**MEDIUM**

4. **MCP-server architecture proliferation.** Each capability becomes its own MCP server (protocols, vault-rw, save-session, screen-watch, file-watch, vectorstore, csr, calibration). 8+ servers by Phase 3. Mitigation: shared crate for common MCP plumbing; consolidate where possible.

5. **Flash-drive bundle size.** Ollama + qwen3:14b or gemma4 alone is 8-15 GB; Goose binary + Tauri app + Hypatia config adds modest overhead. Total likely 12-20 GB. Mitigation: pick smaller default model (qwen2.5-coder:7b or gemma4 8B variant) for the bundle; user can pull larger models on first machine setup.

6. **macOS code-signing for ad-hoc distribution.** First-run security prompts on each new Mac. Mitigation: document the right-click-open workaround; defer notarization to v2.

**LOW**

7. **Custom distro lock-in.** If Goose's API changes, custom distro requires updates. Mitigation: pin Goose version per release; track upstream changes.

8. **Tauri vs egui/Slint regret.** If Tauri proves limiting, swap UI framework. Mitigation: keep UI logic separable from Goose-client logic so swap is feasible.

---

## Open questions still pending

See `docs/open-questions.md` for full state. Highlights:

- **Q-04** — CSR Python port scope (deferred to Phase 3; Scholar to verify "CSR is behavioral" framing)
- **Q-17** — Final Ollama model pick. Reopened after Phase 1 empirical testing. Decide during Phase 1.5 Week 2.
- **Q-18** — Vault CLAUDE.md demotion gate (post-Phase 1.5)
- **Q-19** — Git history disposition (Bell's `ee34dfd` still in log)
- **Q-20** — `docs/Hypatia Build.md` Slope-note disposition

---

## Next action

1. Capture today's three decisions in `open-questions.md` as Q-31, Q-32, Q-33.
2. Persona validation via Continue.dev (with current 40K kernel — sees what truncation does, gives qualitative signal).
3. Start Phase 1.5 Week 1: kernel architectural redistribution.

**Phase 1.5 estimated calendar:** 4-6 weeks at 10-20 hours/week. **Phase 2:** +4-6 weeks. **Phase 3:** +4-6 weeks. **Phase 4:** +2-4 weeks. **Total to flash-drive Hypatia:** 14-22 weeks of focused work.
