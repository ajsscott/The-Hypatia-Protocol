# Hypatia Build Plan — Addendum

**Status:** Layered corrections on `../Hypatia Build Plan.md`. Does not
supersede the plan; flags deltas found by the 2026-04-22
`/codebase-analysis` session and records the Q1–Q12 clarifications asked
and answered the same day.

**Reading order:** Read this file immediately after the Build Plan. Where
this file contradicts the plan, this file is correct.

---

## Plan-vs-reality delta matrix (verified 2026-04-22)

| # | Plan claim | Ground truth | Severity | Action |
|---|---|---|---|---|
| 1 | `Nathaniel.md` 2,576 L | ✓ 2,576 | — | No action |
| 2 | `Hypatia-Protocol.md` 2,070 L | ✓ 2,070 | — | No action |
| 3 | 13 protocols totaling ~7,000 L | ✓ 13 files, 7,150 L | — | No action |
| 4 | `save-session.py` 883 LOC | ✓ 883 | — | No action |
| 5 | Vectorstore ~1,200 LOC | ✓ 1,186 across 6 modules | — | No action |
| 6 | Script tests 1,843 LOC across 7 files | **573 LOC across 4 files, all vectorstore; ZERO script-level tests exist** | **HIGH** | Phase 1 Day 20-21 rescope: write from scratch, not port. See Q5 decision below. |
| 7 | `validate-schemas.py` 312 LOC | **163 LOC** | LOW | Less work than planned; still port verbatim. |
| 8 | ~40 `fs_read` occurrences | **35 total Kiro tool refs: 8 fs_read + 11 fs_write + 16 execute_bash** (0 fs_append/fs_edit/fs_list/fs_delete/search_file_content) | LOW | Plan's grep-pass holds; count is accurate at aggregate level. |
| 9 | `save-session.py` hardcodes `nate@pocket-hq.local` | **Not in `save-session.py`; it's in `scripts/setup.sh:463` (WSL branch) and `:484` (native branch)** | MED | Fix both in setup.sh during Phase 1 Week 3; make config-driven. |
| 10 | CSR + RRF both exist as Python to port | **CSR is BEHAVIORAL (kernel + index JSON), not Python. Only RRF is Python.** See §CSR clarification below. | HIGH | Phase 3 Python port is RRF only; CSR lives in Phase 1 `.clinerules/07-intelligence-layer.md`. Q4 deferred — AJ to verify. |
| 11 | `knowledge.json` 447 / `memory.json` 24 / `patterns.json` 211 / `reasoning.json` 126 entries | ✓ all confirmed | — | No action |
| 12 | Bell-personal refs ~"a few per store" / synonym-map ~5 | **689 Nate/Kiro/Nathaniel refs total across 4 JSON stores (438 in knowledge.json alone)** | HIGH | Per Q6 decision 2026-04-22: ship empty stores. No `reseed.py` review pass. |
| 13 | Sub-agent 4-file pattern, 729 L | 4 files / 709 L (55/51/425/178) | — | No action |
| 14 | `consciousness.md` 2026-02-26 snapshot drifts | ✓ confirmed; additionally hardcodes `"Sir"` user address (lines 12, 20) | — | Plan already mandates full rewrite. Flag "Sir" specifically. |
| 15 | macOS `stat -c` bug in `python-maintenance.sh` | ✓ confirmed at lines 43, 108 | — | Rewrite in Python during Phase 1 (cross-platform via `os.stat()`). |
| 16 | 8 portability gaps enumerated | ✓ all 8 confirmed | — | Per Q9: defer flash-drive work to Phase 1.5. |
| 17 | Bell has pyproject/uv | **Bell has NO dependency manifest at all. No pyproject, no requirements.txt, no lockfile.** | MED | Phase 1 Day 1 work is larger than implied. Author pyproject.toml from scratch per plan's prescription (uv confirmed Q3 2026-04-22). |
| 18 | CI has a "script-tests gap" | ✓ confirmed at `.github/workflows/validate.yml` | — | Phase 1 closes the gap for save-session.py + validate-schemas.py only (per Q5). |
| 19 | Bell's `.gitattributes` memory-sanitize filter is incomplete | **False. Pipeline is complete: `.gitattributes` + `scripts/setup-filters.sh` + `scripts/setup.sh:436-438` + `scripts/git-filter-clean.py` + `scripts/git-filter-smudge.py`.** | — | Plan can port verbatim; just replace Bell's PII regex template in `git-filter-clean.py` with AJ's (or ship empty). |

---

## CSR clarification

**Plan's § "Critical architectural insights" item 2** correctly distinguishes
RRF (the fusion algorithm) from CSR (the routing pattern). Good.

**Plan's § "Phase 3" port list** implicitly treats CSR as Python to port
("Port targets from Bell's `vectorstore/`"). That's wrong. CSR is not in
`vectorstore/`. Relevant file:line pointers for AJ's review:

- `hypatia-kb/Intelligence/README.md:119-127` — "CSR Pattern. All data stores
  use Context Signal Routing."
- `hypatia-kb/Intelligence/README.md:177` — "All `.json` files use the CSR
  (Context Signal Routing) pattern."
- `hypatia-kb/Intelligence/intelligence-operations.md:197-198` — "If signal
  matches, fetch the specific entry by ID (CSR pattern). ... CSR-only is
  the fallback when vectorstore is unavailable."
- `hypatia-kb/memory-protocol.md:22-24` — "Index Operations (CSR Pattern).
  The memory system uses Context Signal Routing for efficient retrieval.
  Load the lightweight index first, then selectively retrieve relevant
  memories."
- `hypatia-kb/Hypatia-Protocol.md:1184` — "PART 2: UPDATE SESSION INDEX (CSR
  Pattern)"
- `hypatia-kb/Hypatia-Protocol.md:2000` — "Task Execution: CSR retrieves
  relevant patterns/knowledge on-demand"
- `scripts/save-session.py:704` — comment "Intelligence stores grow
  indefinitely — CSR indexes keep query cost constant."
- `hypatia-kb/maintenance-protocol.md:90` — "If vectorstore missing: note as
  INFO, not error (system degrades gracefully to CSR-only)"

**Implication:** CSR is kernel behavior + JSON scaffolding, not code. The
Hypatia implementation lives in `.clinerules/07-intelligence-layer.md`
(instructing the LLM to consult `*-index.json` before loading `*.json`) and
in the empty-but-schema-valid index files we ship in Phase 1 Day 6-7.

**Phase 3's Python port target (final):** `concat.py`, `kb_vectorize.py`,
`kb_sync.py`, `kb_query.py`, `kb_server.py`, `kb_benchmark.py`,
`run-server.sh`. Total ~1,186 LOC. CSR adds zero lines to this.

---

## Decisions from Q1–Q12 (2026-04-22)

Decisions recorded during the Q&A session that followed the codebase analysis.
Each decision updates or clarifies a Build Plan entry.

### Q1 — Repo location
**Decision:** Rename in place. Keep
`/Users/ajsscott/GitHub/The-Hypatia-Protocol/`. No move to
`/Users/ajsscott/GitHub/Hypatia/`. Flash-drive primary deferred to Phase 1.5.
**Supersedes:** Build Plan § "Open questions" #1.

### Q2 — Substrate
**Decision:** Cline (plan decision #1 stands).
**Superseded 2026-05-11 by Q-21 (Roo Code).** Same tool-use protocol so the
port plan is unaffected; full Cline→Roo sweep deferred to Phase 1 start. See
`open-questions.md` Q-21 for rationale (better Ollama integration). Q-02
remains in the log as the historical answer.
**Reason (new):** Cline's multi-provider support is load-bearing. AJ's
Claude subscription may lapse; she plans to fall back to local Ollama
models. Claude Code is Anthropic-only; Cline supports Anthropic + OpenAI +
Ollama. See `/home/agent/.claude/projects/-Users-ajsscott-GitHub-The-Hypatia-Protocol/memory/constraint_llm_agnostic.md`.
**Implication for design:** Do NOT wire Hypatia protocols to assume
Claude-specific features (prompt caching, `<system-reminder>` semantics,
the Skill system, 200k context). Cline's lowest-common-denominator
(mid-size local model, ~14B params via Ollama) is the design target.

### Q3 — Dependency management
**Decision:** `uv` + `pyproject.toml` + `uv.lock`.
**Supersedes:** None (plan prescribed this; confirmed).

### Q4 — CSR port scope
**Decision:** Deferred. AJ to verify Bell's CSR implementation independently
using the file:line pointers listed in § CSR clarification above, then
confirm or reject the "CSR is behavioral" framing.
**Placeholder assumption:** CSR = behavioral; Phase 3 Python port is RRF +
MCP only. If AJ rejects after verification, revisit Phase 3 scope.

### Q5 — Test coverage for Phase 1
**Decision:** Critical-path only. Write new tests for `save-session.py` +
`validate-schemas.py`. Port `vectorstore/tests/*` 1:1. All other scripts
get tests in Phase 1.5.
**Supersedes:** Build Plan § Week 3 Day 20-21 "Port Bell's script-side
tests to `tests/` (1,843 LOC — substantial, but tests are mostly portable)."
**Corrected Phase 1 test scope:**
- `tests/test_save_session.py` (new, ~300-400 LOC budgeted)
- `tests/test_schema_validation.py` (new, ~150-200 LOC)
- `tests/test_keyword_drift.py` (new, ~80 LOC — Phase 1 prerequisite)
- `hypatia-kb/vectorstore/tests/test_*.py` (ported 1:1, 573 LOC, path renames only)
**Calendar impact:** +1 to 2 days net vs. plan's assumption (plan assumed
port-verbatim; reality is write-from-scratch, but scope is narrower).

### Q6 — JSON store bootstrap
**Decision:** Ship empty.
**Supersedes:** Build Plan § Week 2 Day 6-7 sub-point "Populate
`hypatia-kb/Intelligence/synonym-map.json` with Hypatia-specific synonyms"
— keep the synonym-map seeding; wipe everything else.
**No reseed.py review pass in Phase 1.** Build Plan § "Risk register /
landmines" item 5 ("Intelligence store bootstrap — empty at ship → sparse
retrieval for first few weeks") is accepted.

### Q7 — Vault-convention authority (Hypatia-kb owns)
**Decision:** Hypatia-kb/protocols/ becomes authoritative for vault
conventions. Vault `CLAUDE.md` becomes a derived stub once Phase 1 ships.
**Implication — new Phase 0:** Before Phase 1 Day 1 starts, the 717-line
archived vault CLAUDE.md (at `docs/vault-librarian-reference.md`) must
migrate into draft `hypatia-kb/protocols/librarian-*.md` files. Split is
judgment-heavy (some content is librarian-generic, some is
vault-specific). Budget: ~1 week calendar.
**Phase 0 deliverables:**
- `hypatia-kb/protocols/librarian-vault-conventions.md` (vault-specific:
  Trees/Seeds/Mountains schema, canonical frontmatter, Bases load-bearing
  fields, Seed→Tree linkage contract, known drift register).
- `hypatia-kb/protocols/librarian-generic-zettelkasten.md` (atomic-note
  principle, block-ref embeds, graph-maintenance heuristics — vault-agnostic).
- Stub vault CLAUDE.md that points Claude Code sessions to Hypatia's
  authoritative docs (once they exist and are tested).
- **Don't replace vault CLAUDE.md until Phase 1 ships** — both must exist in
  parallel during development; vault CLAUDE.md becomes a stub only after
  Hypatia is loadable and Claude Code can successfully read the pointer.

### Q8 — Git commit identity
**Decision:** Distinct `Hypatia` identity for commits Hypatia herself
writes. Port-work commits (AJ + Claude Code collaborating) attribute to
AJ.
**Suggested config:**
```
[user "hypatia"]
    name = Hypatia
    email = hypatia@local
```
Used via `git commit --author="Hypatia <hypatia@local>"` from Hypatia's
save-session workflow, or via a dedicated `HYPATIA_GIT_*` env-var pair.
Final form to be decided during Phase 1 Week 3.

### Q9 — Flash-drive portability
**Decision:** Defer to Phase 1.5.
**Supersedes:** Build Plan § "Portability analysis" is preserved as Phase
1.5 spec but is NOT a Phase 1 deliverable. Phase 1 Week 3 Day 16-17 "Vault
integration layer" is simplified: `hypatia.config.yaml` still exists but
the first-run detection + per-machine venv bootstrap + flash-drive setup
story is deferred. Config is hand-written once on AJ's Mac.
**Calendar savings:** ~2 days.

### Q10 — Phase 2 listener target
**Decision:** Claude Code session captures.
**Workflow:** When a Claude Code conversation produces useful synthesis, AJ
manually saves a markdown export to `~/Desktop/claude-captures/` (or
equivalent). Hypatia's watcher picks up new files in that folder, invokes
`assistant-ingest` with `source_type=claude_capture`, proposes a Seed in
the vault.
**Supersedes:** Build Plan § Phase 2 "Likely candidates" ranking. #3 in
the plan list (terminal/shell capture) is effectively the chosen target,
not #1 (Web Clipper) as plan recommended.
**Note:** This requires AJ to develop the capture habit. Web Clipper (plan's
#1) is a "free" capture that happens via existing browser ext; Claude
captures require manual save. Higher-value but higher-activation-energy.
AJ's call.

### Q11 — CLAUDE.md disposition
**Decision:** Move current CLAUDE.md to `docs/vault-librarian-reference.md`.
Write fresh root CLAUDE.md for port work. Done 2026-04-22.

### Q12 — Supplementary doc set
**Decision:** Write Build Plan Addendum (this file), Port Inventory
(`port-inventory.md`), Open Questions log (`open-questions.md`). Skip
explicit Phase 0 spec (Phase 0 is covered in this file's Q7 decision).

---

## Corrected Phase 1 calendar

With Q5 + Q7 + Q9 deltas applied:

| Phase | Calendar | Notes |
|---|---|---|
| **Phase 0 — Content migration** | ~1 week (5-7 working days) | NEW. Vault CLAUDE.md → draft Hypatia protocols. Judgment-heavy. |
| **Phase 1 Week 1 — Repo scaffold + runtime** | 5 days | Unchanged from plan. |
| **Phase 1 Week 2 — Intelligence + protocols** | 5 days | Per Q7: librarian-* protocols already drafted in Phase 0; Week 2 integrates + polishes. |
| **Phase 1 Week 3 — Save-session + tooling** | 5 days | -2 days from plan (Q9 defer) +1 day (Q5 test write from scratch) = net -1 day. |
| **Total Phase 1** | ~3 weeks (15-18 working days) | Plan said 2-3 weeks / 12-18 days. |

**Total to usable Hypatia (Phase 0 + Phase 1):** ~4 weeks (22-25 working
days), assuming 10-20 hours/week. Plan's "2-3 weeks" was Phase 1 only;
this is the full pre-Phase-2 timeline.

---

## New landmines surfaced by analysis (not in plan's risk register)

**HIGH**

12. **Keyword-map drift affects 8-10 of 13 protocols, not 3.** Plan's §
    landmine #1 understates. `scripts/check-keyword-drift.py` must be a
    Phase 1 Week 2 Day 8 deliverable, not Day 10. Run it on Bell's files
    FIRST (surfaces the existing drift), resolve the canonical keyword
    set, then use it as the pre-commit gate going forward.

13. **`pre-commit-kb-validate.sh` silent-failure.** If `python3` absent,
    the hook references `scripts/run-python.sh` which does not exist.
    Hook returns 0 (passes). Silent. Port must add `set -euo pipefail` +
    explicit error if `command -v python3` fails.

**MEDIUM**

14. **Consciousness.md's "Sir" address.** `consciousness.md:12,20`
    hardcodes user address as "Sir" with explicit non-negotiable
    language. Bell's voice feature; Hypatia has none. Voice-rewrite work
    must not just replace vocabulary — must delete the
    `User Address: "Sir"` stanza entirely.

15. **`kb_benchmark.py:88,113`** hardcodes `/tmp/kb_bench_ids.json`. Not
    Windows-portable; breaks on any OS using different temp dir. Fix:
    use `tempfile.gettempdir()`.

16. **`secure-fetch.py:17`** hardcodes `~/.kiro/security.log`. Move to
    `hypatia.config.yaml` log_path; default `~/.hypatia/security.log`.

**LOW**

17. **`hypothesis` is a Phase 1 test dep** the plan's pyproject.toml
    baseline omits. Add to `[project.optional-dependencies] dev`.

---

## Files this addendum does NOT change

- Build Plan § Phase 1 architecture decomposition (`.clinerules/01-11.md`
  layout — still correct)
- Build Plan § "Terminology reset" (RRF / CSR / IMG / CSP definitions — all
  correct except for the CSR-is-Python implication elsewhere in plan)
- Build Plan § "File-by-file customization strategy" — superseded by
  `port-inventory.md` but not contradicted
- Build Plan § "Deliverables" (final exit criteria unchanged)

---

## Change log

- **2026-04-22** — initial addendum written after codebase-analysis and
  Q1-Q12 session. All 19 delta matrix items verified.
- **2026-05-11** — Q-21 supersedes Q-02 (Roo Code over Cline). Note added
  inline to Q2 entry; full Cline→Roo terminology sweep deferred to Phase 1.
