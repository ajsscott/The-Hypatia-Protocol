# Hypatia Port Inventory — file-by-file disposition

**Status:** Verified 2026-04-22 against Bell's repo. Supersedes Build Plan
§ "File-by-file customization strategy" where they differ.

**Legend:**
- **P** — port verbatim (path renames only)
- **A** — adapt (content edits required)
- **R** — rewrite from scratch (Bell's content unusable as starting point)
- **D** — discard (not needed for Hypatia)
- **NEW** — write new file, no Bell analog

**Effort units:** eng-hours, assuming focused work. Not calendar days.

---

## Persona / kernel layer — `.steering-files/steering/` → `.clinerules/`

| Bell file | LOC | Disposition | Hypatia target | Effort | Notes |
|---|---:|:---:|---|---:|---|
| `Nathaniel.md` | 2,576 | **A** (decompose) | `.clinerules/01-10.md` | 16-20 | 36 `## ` headers. See table below. Voice section (L459-467) requires full rewrite. |
| `tool-inventory.md` | 119 | **R** | `.clinerules/05-tools.md` | 3-4 | Replace Kiro tool names with Cline equivalents. Map: fs_read→read_file, fs_write→write_to_file, fs_edit→replace_in_file, fs_append→write_to_file(append), execute_bash→execute_command. |

### `Nathaniel.md` decomposition (from 36 headers → 10 `.clinerules/` files)

| Target file | Bell kernel sections | ~LOC |
|---|---|---:|
| `01-identity.md` | Commitment, Identity, Super-Objective, Irreducible Self | ~110 |
| `02-voice.md` | The Voice (L459-467) — **REWRITE entirely**; Hypatia persona brief in Build Plan decision #5 | ~80 |
| `03-anti-patterns.md` | Language + Behavioral + Truth + Response + Process Anti-Patterns, Meta-Rules, Warning Signs | ~280 |
| `04-session-gates.md` | IMG, Pre-Task Protocol, Session Protocols, Context Priming, Greeting, Initialization Sequence | ~200 |
| `05-tools.md` | NEW (from tool-inventory.md, Cline tools) | ~120 |
| `06-cognitive.md` | OBSERVE>QUESTION>DEDUCE (from IMG), Cognitive Synchronization Pattern (CSP) | ~250 |
| `07-intelligence-layer.md` | KB Location Map + tiered surfacing + **CSR pattern description** (Q4 clarification) | ~150 |
| `08-save-command.md` | The 10-step atomic save workflow (from save-command section of kernel + memory-protocol) | ~200 |
| `09-security.md` | External Content Security gate (L168-187) + snippets from security-protocol.md | ~140 |
| `10-skills-loading.md` | Protocol Keyword Map (L319-347) — SINGLE SOURCE OF TRUTH for keyword triggers, enforced by check-keyword-drift.py | ~100 |
| `11-decision-routes.md` | From `Nate's-kb/Nate-Protocol.md` — see next table | ~600 |

`11-decision-routes.md` is loaded always (per plan decision). Bell's
2,070-line file compresses to ~600 lines after stripping Kiro examples.

---

## Sub-agent framework — `.steering-files/agents/analyst/`

Per Build Plan: defer to Phase 2+.

| Bell file | LOC | Disposition | Notes |
|---|---:|:---:|---|
| `README.md` | 55 | **A** (Phase 2) | Keep pattern; retarget to Hypatia sub-agents. |
| `analyst-prompt.md` | 51 | **A** (Phase 2) | Adapt to Hypatia's clusters. |
| `consciousness.md` | 425 | **D** + **NEW** | Bell's file drifts from kernel (2026-02-26 snapshot, 55 days stale; hardcodes "Sir"). Hypatia's pattern: **auto-extract from `.clinerules/` at build time, never hand-edit**. |
| `specialization.md` | 178 | **A** (Phase 2) | Adapt to Hypatia's research cluster. |

**Phase 2 architectural change:** `consciousness.md` per sub-agent becomes a
generated artifact. Build step reads `.clinerules/01-identity.md` +
`02-voice.md` + the sub-agent's manifest → writes `consciousness.md` on
every `save-session`. Bell's drift landmine becomes impossible by
construction.

---

## Settings / runtime wiring

| Bell file | Disposition | Hypatia target | Notes |
|---|:---:|---|---|
| `.steering-files/settings.json` | **R** | `.vscode/settings.json` (or Cline's config surface) | Kiro's `kiroAgent.trustedCommands` schema does not map to Cline. Full rewrite. |
| `.steering-files/settings/mcp.json` | **A** | `.vscode/mcp.json` (or Cline equivalent) | 3 servers (time, secure-fetch, hypatia-vectorstore). Rename paths; rename tool names (`kb_*` → `hypatia_*`). |

---

## Protocols — `Nate's-kb/*-protocol.md` → `hypatia-kb/protocols/`

Plan's 4-cluster remapping confirmed. Per Q7 decision, Phase 0 adds `librarian-vault-conventions.md` from migrated vault CLAUDE.md.

| Bell file | LOC | Hypatia cluster | Target file | Disposition | Effort |
|---|---:|---|---|:---:|---:|
| `research-protocol.md` | 248 | Researcher | `researcher-investigate.md` | **A** | 3 |
| `prompt-enhancement-protocol.md` | 317 | Researcher | `researcher-prompt-enhance.md` | **A** | 3 |
| `writing-protocol.md` | 770 | Writer | `writer-draft.md` | **A** | 6 |
| `summarization-protocol.md` | 582 | Writer | `writer-summarize.md` | **A** | 5 |
| `executive-communication-protocol.md` | 253 | Writer | `writer-executive.md` | **A** | 3 |
| `development-protocol.md` | 2,464 | Assistant | `assistant-development.md` | **A** (heavy strip) | 10-12 |
| `planning-protocol.md` | 407 | Assistant | `assistant-plan.md` | **A** | 4 |
| `problem-solving-protocol.md` | 195 | Assistant | `assistant-problem-solve.md` | **A** | 2 |
| `proactive-offering-protocol.md` | 151 | Kernel | (merged into `.clinerules/`) | **A** | 2 |
| `save-command.md` (in kernel) | — | Librarian | `librarian-save.md` | **A** | 4 |
| `maintenance-protocol.md` | 440 | Librarian | `librarian-lint.md` | **A** | 4 |
| `memory-protocol.md` | 491 | Librarian | `librarian-memory.md` | **A** | 4 |
| `customization-protocol.md` | 319 | Librarian | `librarian-customize.md` | **A** | 3 |
| `security-protocol.md` | 513 | Kernel | (merged into `.clinerules/09-security.md`) | **A** | 4 |
| — | — | Librarian | `librarian-vault-conventions.md` | **NEW** (Phase 0 from vault CLAUDE.md) | 16-20 |
| — | — | Librarian | `librarian-generic-zettelkasten.md` | **NEW** (Phase 0) | 8-10 |
| — | — | Assistant | `assistant-ingest.md` | **NEW** | 4-6 |

**Stripping targets during port** (find via grep before each protocol edit):
- `Nate`, `Nathaniel` → `Hypatia`
- `Kiro`, `.kiro/`, `Kiro IDE`, `kiro-cli` → (delete or replace with Cline equivalent)
- `fs_read` / `fs_write` / `fs_append` / `fs_edit` / `execute_bash` → Cline tool names
- `Sir` (as address term) → (delete stanza)
- `Pocket HQ` → (delete — Hypatia has no Pocket HQ)
- AWS-specific content (Strands, Bedrock, SDK) in `development-protocol.md` → strip to universal dev practices
- AAVE vocabulary ("Bet," "Deadass," etc.) → delete; rewrite voice

---

## Decision routes — `Nate's-kb/Nate-Protocol.md`

| Bell file | LOC | Disposition | Hypatia target | Effort |
|---|---:|:---:|---|---:|
| `Nate-Protocol.md` | 2,070 | **A** (compress) | `.clinerules/11-decision-routes.md` | 6-8 |

**Caution:** Routes A-F are referenced by tag (`#route-a` etc.) in the
Section Routing table (L24-29), NOT as level-3 headings like `### Route A:`.
Plan's "port Routes A-F verbatim" should locate them by tag. Routes are
embedded within `### Phase 3: Route Decision` (L319) and `### Route Quick
Reference` (L510).

Per Build Plan: "apply the 4 fixes" — restore Route E "just do it"
override language, restore Route B expertise-detection in skip-explanation,
tighten Route F verification-rule language, drop the CoV reference pointer.

---

## Intelligence stores — `Nate's-kb/Intelligence/` → `hypatia-kb/Intelligence/`

Per Q6 decision: ship empty. Carry schema, not content.

| Bell file | Entries | Disposition | Hypatia action |
|---|---:|:---:|---|
| `patterns.json` | 211 | **R** (empty) | Write empty `{}` or `[]` matching schema; validator accepts. |
| `patterns-index.json` | — | **R** (empty) | Empty indexes. |
| `knowledge.json` | 447 | **R** (empty) | Empty. 438 Nate/Kiro refs wiped. |
| `knowledge-index.json` | — | **R** (empty) | Empty. |
| `reasoning.json` | 126 | **R** (empty) | Empty. 19 Nate/Kiro refs wiped. |
| `reasoning-index.json` | — | **R** (empty) | Empty. |
| `cross-references.json` | 97 refs | **R** (empty) | Empty. |
| `synonym-map.json` | 40 groups | **R** with Hypatia seed | Write fresh with zettelkasten-relevant groups (Seed/Tree/Mountain taxonomy, Obsidian-verbs, AJ's workflow terms). ~10-20 initial groups. |

---

## Memory stores — `Nate's-kb/Memory/` → `hypatia-kb/Memory/`

| Bell file | Disposition | Hypatia action |
|---|:---:|---|
| `memory.json` | **R** with seed | Seed `instance_identity: { instance_name: "Hypatia", description: "zettelkasten PKB partner", created: "2026-04-22" }` + 5-7 preferences (peer register, devil's-advocate, atomic commits, ask-before-destructive, pre-verify-before-scripting). |
| `memory-index.json` | **R** (empty) | Regenerated from memory.json. |
| `session-index.json` | **R** (empty) | Empty. |

---

## Python backend — `scripts/`

| Bell file | LOC | Disposition | Hypatia target | Effort | Notes |
|---|---:|:---:|---|---:|---|
| `save-session.py` | 883 | **A** | `scripts/save-session.py` | 10-14 | Rename `Nate's-kb/` → `hypatia-kb/` (4 paths). Strip Windows/WSL fallback. |
| `validate-schemas.py` | 163 | **P** | `scripts/validate-schemas.py` | 1-2 | Pure schema validator; no content coupling. Path rename only. |
| `cascade-correction.py` | 227 | **P** | `scripts/cascade-correction.py` | 2 | Path rename. |
| `maintenance.py` | 223 | **P** | `scripts/maintenance.py` | 2 | Path rename. |
| `removal-cascade.py` | 258 | **P** | `scripts/removal-cascade.py` | 2 | Path rename. |
| `reseed.py` | 255 | **A** | `scripts/reseed.py` | 3 | Path rename. Strip Bell's PII blocklist (ship empty). |
| `session-cache.py` | 299 | **P** | `scripts/session-cache.py` | 2 | Path rename. |
| `normalize-schemas.py` | 509 | **P** | `scripts/normalize-schemas.py` | 2 | Path rename. |
| `secure-fetch.py` | 83 | **A** | `scripts/secure-fetch.py` | 1 | Path rename. Move `~/.kiro/security.log` to config. |
| `git-filter-clean.py` | 19 | **A** | `scripts/git-filter-clean.py` | 1 | Replace Bell's PII regex template with AJ's (or ship empty). |
| `git-filter-smudge.py` | 4 | **P** | `scripts/git-filter-smudge.py` | 0.2 | Verbatim. |
| — | — | **NEW** | `scripts/check-keyword-drift.py` | 4-6 | Phase 1 prerequisite. Enforces single-source-of-truth between `.clinerules/10-skills-loading.md` and each protocol's `**Keywords**:` line. |

---

## Vectorstore — `Nate's-kb/vectorstore/` → `hypatia-kb/vectorstore/` (Phase 3)

| Bell file | LOC | Disposition | Effort | Notes |
|---|---:|:---:|---:|---|
| `concat.py` | 83 | **P** | 0.5 | Verbatim. |
| `kb_vectorize.py` | 139 | **A** | 1-2 | Path rename; optionally swap embedding model. |
| `kb_sync.py` | 159 | **A** | 1-2 | Path rename. |
| `kb_query.py` | 481 | **A** | 3-4 | Path rename. Fix tiebreak-by-distillation-level comment drift. |
| `kb_server.py` | 85 | **A** | 1 | Path rename + `kb_` → `hypatia_` tool name prefix. |
| `kb_benchmark.py` | 239 | **A** | 1 | Path rename + `tempfile.gettempdir()` replacement for hardcoded `/tmp/`. |
| `run-server.sh` | 7 | **A** | 0.2 | Path rename. |

---

## Shell scripts

| Bell file | Disposition | Hypatia action | Notes |
|---|:---:|---|---|
| `scripts/setup.sh` | **A** (heavy edit) | Strip Kiro blocks (L195-228), Windows branches, hardcoded git identities (L463, L484) → config-driven | Mac/Linux only for Phase 1 per Q9. |
| `scripts/setup-filters.sh` | **P** | Verbatim. | Wires the sanitize-memory filter. |
| `scripts/pre-commit-kb-validate.sh` | **A** | Add `set -euo pipefail`, explicit error if `python3` absent | Fix silent-failure landmine. |
| `scripts/full-maintenance.sh` | **D** | — | Kiro-branded. |
| `scripts/python-maintenance.sh` | **R** | Rewrite in Python (cross-platform via `os.stat()`) | Bell's `stat -c` is Linux syntax; breaks on macOS. |
| `scripts/kiro-maintenance.sh` | **D** | — | Kiro-specific. |
| `scripts/wsl-maintenance.sh` | **D** | — | WSL-specific; Phase 1 is Mac/Linux native. |
| `scripts/harden-repo.sh` | **A** | Path renames; keep general pattern. | |
| `scripts/run-python.sh` | **NEW** | Write; referenced by pre-commit hook but file is missing in Bell's repo. | |

---

## Windows / PowerShell

All discarded per Build Plan + Q9.

| Bell file | Size | Disposition |
|---|---:|:---:|
| `scripts/setup.bat` | — | **D** |
| `scripts/bootstrap-windows.ps1` | 5.6 KB | **D** |
| `scripts/setup-wsl.ps1` | 3.4 KB | **D** |
| `scripts/teardown.ps1` | 3.3 KB | **D** |
| `scripts/wsl-compact.ps1` | 3.6 KB | **D** |

---

## Tests — `tests/` + `Nate's-kb/vectorstore/tests/`

Per Q5: critical-path only in Phase 1.

| Bell file | LOC | Disposition | Hypatia target | Effort | Notes |
|---|---:|:---:|---|---:|---|
| (script-level tests) | **0 exist** | — | — | — | Plan claimed 1,843 LOC / 7 files; reality is zero. |
| `Nate's-kb/vectorstore/tests/test_build.py` | 158 | **P** | `hypatia-kb/vectorstore/tests/test_build.py` | 1 | Path rename. |
| `Nate's-kb/vectorstore/tests/test_query.py` | 153 | **P** | `test_query.py` | 1 | Path rename. |
| `Nate's-kb/vectorstore/tests/test_sync.py` | 168 | **P** | `test_sync.py` | 1 | Path rename. |
| `Nate's-kb/vectorstore/tests/test_concat.py` | 94 | **P** | `test_concat.py` | 0.5 | Path rename. |
| — | — | **NEW** | `tests/test_save_session.py` | 8-12 | ~300-400 LOC. Covers: ops validation, entry add, index rebuild, cross-reference update, cascade, file-lock behavior. |
| — | — | **NEW** | `tests/test_schema_validation.py` | 4-6 | ~150-200 LOC. Covers the three store schemas + enum/length validation. |
| — | — | **NEW** | `tests/test_keyword_drift.py` | 2-3 | ~80 LOC. Asserts `.clinerules/10-skills-loading.md` keyword map matches each protocol's `**Keywords**:` line. |

---

## Root / docs / governance

| Bell file | Size | Disposition | Hypatia action |
|---|---:|:---:|---|
| `LICENSE` | — | **R** | MIT, AJ copyright 2026+. |
| `README.md` | 73 KB | **R** | Rewrite per Hypatia architecture + setup. |
| `POCKET-HQ.md` | 6.8 KB | **A** | Strip Bell branding; preserve 5-principle framing. Rename to `ARCHITECTURE.md` or `PRINCIPLES.md`. |
| `CRITICAL-FILE-PROTECTION.md` | — | **A** | Update paths to Hypatia's. |
| `FILE-STRUCTURE.md` | — | **R** | Regenerate for Hypatia. |
| `QUICKSTART.md` | — | **R** | Hypatia-specific setup walkthrough. |
| `CUSTOMIZATION.md` | — | **R** | Rewrite for Hypatia. |
| `CONTRIBUTING.md` | — | **D** | Private PKB, not OSS. |
| `CODE_OF_CONDUCT.md` | — | **D** | Private PKB. |
| `SECURITY.md` | — | **D** | Private PKB. |
| `docs/system-maintenance.md` | 12.9 KB | **P** | Generic ops; port as-is. |
| `docs/growth-spec-script-offload.md` | 30.1 KB | **D** | Bell-personal work. |
| `docs/research/` | — | Skimmed | TBD — quick audit needed before disposition. |
| `.gitignore` | — | **A** | Remove Kiro lines; add `.venv/`, `hypatia.config.yaml`, vectorstore cache, etc. |
| `.gitattributes` | — | **A** | Line 1 (LF normalize) keep; sanitize-memory filter lines keep (pipeline works). |
| `.editorconfig` | — | **P** | Verbatim. |

---

## Pocket HQ scaffold

| Folder | Current | Disposition |
|---|---|:---:|
| `Projects/` | empty (.gitkeep) | **D** |
| `Business/` | empty | **D** |
| `Brand/` | empty | **D** |
| `Life/` (+ 9 subfolders: Career, Education, Family, Finances, Goals, Health, Home, Journal) | empty | **D** |
| `Archive/` | empty | **D** |

Bell's Pocket HQ is personal project management. Hypatia's project
management lives in TabulaJacqueliana's Mountains/. Discard all.

---

## `.github/`

| Bell file | Disposition | Hypatia action |
|---|:---:|---|
| `.github/workflows/validate.yml` | **A** | Port with path renames + add new test steps for test_save_session/test_schema_validation/test_keyword_drift. |
| `.github/ISSUE_TEMPLATE/*` | **D** | Private PKB. |

---

## Effort rollup (Phase 1 only)

| Category | Hours |
|---|---:|
| Kernel decomposition (Nathaniel.md → .clinerules/01-11.md) | 16-20 |
| Decision routes (Nate-Protocol.md → 11-decision-routes.md) | 6-8 |
| Protocol ports (13 ported + 3 new) | 56-72 |
| Python backend (11 scripts + 1 new) | 24-34 |
| Tests (3 new + 4 ported) | 16-24 |
| Settings / mcp / Cline wiring | 6-8 |
| Shell scripts | 6-10 |
| JSON scaffolding + memory seed | 4-6 |
| Root / docs / governance | 12-16 |
| **Phase 1 total** | **146-198 hours** |

Plan estimated 40-60 hours, 10-20 hours/week, 2-3 weeks. Port-inventory
estimate is more pessimistic — **146-198 hours / 10-20 hours/week =
7-20 calendar weeks**. Realistic Phase 1 calendar is closer to **5-6
weeks**, not 2-3.

This is before Phase 0 (content migration, ~20-30 hours).

**Add Phase 3 (vectorstore port):** ~20-30 additional hours.
**Add Phase 2 (listener):** ~40-60 additional hours, per plan.

---

## Change log

- **2026-04-22** — initial inventory from codebase analysis.
