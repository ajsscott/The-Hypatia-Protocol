# Hypatia — Open Questions Log

Durable record of decisions made, decisions pending, and decisions
deferred during Hypatia's port and build. Append-only. Questions marked
**ANSWERED** carry the decision date and decider; questions marked **OPEN**
are pending.

Entry format:
```
## Q-<id> | <ANSWERED|OPEN|DEFERRED> — <short question>
Asked: YYYY-MM-DD  Status: <status>  Decided by: <name, if answered>
Context: <1-3 sentences of why the question arose>
Options considered: <numbered list>
Decision: <chosen option + rationale>
Supersedes: <references to plan sections or other questions>
```

---

## Q-01 | ANSWERED — Where should the Hypatia repo live?

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan left location open. Options spanned local-GitHub,
flash-drive primary, or rename-in-place of the existing fork.

**Options considered:**
1. Rename in place — keep `/Users/ajsscott/GitHub/The-Hypatia-Protocol/`
2. Move to `/Users/ajsscott/GitHub/Hypatia/` + private GitHub
3. Flash-drive primary, private GitHub mirror
4. Flash-drive primary, public GitHub mirror (Bell-style)

**Decision:** Option 1. No filesystem move. Flash-drive portability is
Phase 1.5+ work.

**Supersedes:** Build Plan § "Open questions" #1.

---

## Q-02 | ANSWERED — Runtime substrate: keep Cline, or revisit?

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan locked Cline as decision #1. Devil's-advocate pushback
raised whether Claude Code (AJ's daily driver) was a better fit.

**Options considered:**
1. Switch to Claude Code — reuses existing harness patterns
2. Keep Cline — multi-provider substrate
3. Both — Claude Code primary, Cline parallel

**Decision:** Option 2 (Cline), with the load-bearing reason made
explicit: **Cline supports multiple LLM providers (Anthropic, OpenAI,
Ollama). Claude Code is Anthropic-only. AJ's Claude subscription may
lapse; she plans Ollama fallback (her vault already runs YOLO + Ollama
with mistral-nemo:12b / qwen3:14b / deepseek-r1:14b). Vendor lock is
unacceptable.**

**Implication for all downstream design:** Hypatia's kernel and protocols
must NOT assume Claude-specific features (prompt caching,
`<system-reminder>` semantics, the Skill system, 200k context). Design
target = Cline lowest-common-denominator, expected backend ≈ local 14B
model via Ollama.

**Supersedes:** Build Plan decision #1 (stands, with this rationale).
Also informs every subsequent protocol-writing decision.

---

## Q-03 | ANSWERED — Dependency management tool

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan prescribed `uv` + `pyproject.toml` + `uv.lock`. Bell
has no dependency manifest at all. Fresh choice required.

**Options considered:**
1. uv + pyproject.toml
2. pip-tools (pip-compile)
3. Plain requirements.txt
4. Poetry

**Decision:** Option 1.

**Supersedes:** Build Plan § "Dependencies (pyproject.toml baseline)" —
confirmed as written.

---

## Q-04 | DEFERRED — CSR port scope for Phase 3

Asked: 2026-04-22  Status: DEFERRED  Decision owner: AJ

**Context:** Initial survey-agent report claimed CSR was absent from
Bell's Python code, implying Phase 3's CSR port target was vaporware.
Deep-dive correction: CSR IS real but it's a **behavioral / architectural
pattern** (kernel-instructs-LLM to read `*-index.json` before loading
`*.json`), not a Python fusion algorithm. RRF is the Python fusion; CSR
is markdown-and-index-JSON. AJ wants to verify Bell's CSR implementation
independently before accepting the "CSR is behavioral" framing.

**File:line pointers for AJ's review:**
- `hypatia-kb/Intelligence/README.md:119-127` — CSR pattern overview
- `hypatia-kb/Intelligence/README.md:177` — "All `.json` files use CSR"
- `hypatia-kb/Intelligence/intelligence-operations.md:197-198` — fetch by ID
- `hypatia-kb/memory-protocol.md:22-24` — CSR for memory retrieval
- `hypatia-kb/Hypatia-Protocol.md:1184, 2000` — CSR integration points
- `scripts/save-session.py:704` — CSR indexes comment
- `hypatia-kb/maintenance-protocol.md:90` — "degrades gracefully to CSR-only"

**Placeholder assumption (until AJ confirms):** CSR is behavioral. Phase
3 Python port is RRF + MCP only. `.clinerules/07-intelligence-layer.md`
(Phase 1) carries the CSR kernel instructions. Phase 1 Day 6-7 ships
empty-but-schema-valid `*-index.json` scaffolds.

**Revisit trigger:** AJ reads the file:line pointers above, accepts or
rejects placeholder. If rejected, revisit Phase 3 scope.

---

## Q-05 | ANSWERED — Phase 1 test coverage

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan claimed 1,843 LOC of portable script tests across 7
files. Codebase analysis found 0 script-level tests — only 573 LOC of
vectorstore tests (4 files). Phase 1 Week 3 Day 20-21 needs rescoping.

**Options considered:**
1. Critical-path only — tests for save-session.py + validate-schemas.py;
   port vectorstore 1:1
2. Full coverage now — write script-level tests for all 10+ scripts
3. Ship without script tests — explicit Phase 1.5 sprint

**Decision:** Option 1.

**Concrete scope:**
- New: `tests/test_save_session.py` (~300-400 LOC)
- New: `tests/test_schema_validation.py` (~150-200 LOC)
- New: `tests/test_keyword_drift.py` (~80 LOC; Phase 1 prerequisite)
- Ported 1:1: `hypatia-kb/vectorstore/tests/test_*.py` (573 LOC, path renames)

**Supersedes:** Build Plan § Week 3 Day 20-21 "port Bell's script-side
tests (1,843 LOC — mostly portable)" — rescoped.

---

## Q-06 | ANSWERED — JSON store bootstrap

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan estimated "a few per store" of Bell-personal content.
Reality: 689 Nate/Kiro/Nathaniel references across 4 stores (438 in
knowledge.json alone). Cleanup scope 30× plan's estimate.

**Options considered:**
1. Ship empty stores — wipe all, seed memory.json identity only
2. reseed.py + manual review — flag and keep universal entries
3. Keep universal tech content — wipe identity only, keep AWS/Strands
   content as cloud-dev reference

**Decision:** Option 1. Empty JSON stores at Phase 1 ship. Seed
memory.json with `instance_identity` stanza + 5-7 preferences observed
from TabulaJacqueliana sessions (peer register, devil's-advocate,
atomic commits, ask-before-destructive, pre-verify-before-scripting).

**Supersedes:** Build Plan § Week 2 Day 6-7 — confirms the plan's
default. Build Plan § Week 1 subsection on knowledge.json cleanup
(implicit) is dropped.

---

## Q-07 | ANSWERED — Vault-convention authority

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** TabulaJacqueliana vault has a 717-line `CLAUDE.md` with
battle-tested librarian duties, schemas, drift guardrails. Question:
where should this knowledge live authoritatively in Hypatia's world?

**Options considered:**
1. Hypatia reads vault CLAUDE.md at session start — single SSoT in vault
2. Build step syncs vault → protocols — derived artifact
3. Duplicate into Hypatia protocols — two SSoTs, will drift
4. Hypatia-kb owns; vault CLAUDE.md becomes derived stub — single SSoT
   in Hypatia

**Decision:** Option 4. Hypatia-kb is authoritative. Vault CLAUDE.md
becomes a derived stub once Phase 1 ships.

**New implication — Phase 0:** Pre-Phase-1 content migration. Current
717 lines at `docs/vault-librarian-reference.md` must migrate into draft
`hypatia-kb/protocols/librarian-vault-conventions.md` +
`librarian-generic-zettelkasten.md`. Judgment-heavy split. ~1 week
calendar (20-30 hours).

**Supersedes:** None in Build Plan (plan was silent on this). Creates
Phase 0.

**Counter-argument considered:** Bell's kernel design assumes
self-contained authority. Extending lazy-load across the repo/vault
boundary is novel pattern-work, no precedent in Bell's repo. But Bell's
closest analog (`consciousness.md`) is the drift anti-pattern — repo's
implicit recommendation is Option 4 over Option 3.

---

## Q-08 | ANSWERED — Git commit identity for Hypatia

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Bell hardcodes `nate@pocket-hq.local` / `Nathaniel` as git
identity (at `scripts/setup.sh:463` WSL branch and `:484` native branch).
Question: who owns commits Hypatia writes?

**Options considered:**
1. AJ's identity — `aj.scott@renphil.org`, same as her config
2. Distinct `Hypatia` identity — e.g., `hypatia@local`
3. AJ identity + `Co-Authored-By: Hypatia` trailer

**Decision:** Option 2. Distinct Hypatia identity.

**Draft config** (to finalize during Phase 1 Week 3):
```
[user "hypatia"]
    name = Hypatia
    email = hypatia@local
```
Invoked via `git commit --author="Hypatia <hypatia@local>"` from
Hypatia's save-session workflow. Port-work commits (AJ + Claude Code
collaborating on the port itself) continue to attribute to AJ.

**Supersedes:** Build Plan § "Open questions" #6.

---

## Q-09 | ANSWERED — Flash-drive portability timing

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan described flash-drive portability as a core Phase 1
requirement (~2-3 days of per-machine config work). AJ has one primary
Mac; multi-machine is Phase 2+ at earliest.

**Options considered:**
1. Defer to Phase 1.5 — Phase 1 targets AJ's Mac only
2. Full portability in Phase 1 — keep plan as-is (+2-3 days)
3. Config boundary only — `hypatia.config.yaml` exists but no
   bootstrap-on-different-machine story

**Decision:** Option 1.

**Supersedes:** Build Plan § "Portability analysis" (retained as Phase
1.5 spec) and § Week 3 Day 16-17 (simplified — `hypatia.config.yaml`
hand-written once on AJ's Mac).

---

## Q-10 | ANSWERED — Phase 2 first listener target

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Plan listed 6 candidate surfaces for autonomous listening,
ranked by ease × value. AJ's highest-friction workflow needed to drive
the Phase 2 priority.

**Options considered:**
1. Obsidian Web Clipper articles (plan's #1)
2. Research PDFs (Zotero → vault)
3. Claude Code session captures
4. Everything in Seeds/ (generic watcher)

**Decision:** Option 3. Claude Code session captures.

**Workflow:** AJ manually exports conversation synthesis to
`~/Desktop/claude-captures/` (or equivalent); Hypatia watcher picks up
new files, invokes `assistant-ingest` with
`source_type=claude_capture`, proposes a Seed.

**Trade-off accepted:** Higher activation energy than Web Clipper (which
is free capture via existing browser ext) but higher-value synthesis per
capture. Requires AJ to develop save-habit.

**Supersedes:** Build Plan § Phase 2 "My Phase 2 recommendation"
(changed target).

---

## Q-11 | ANSWERED — CLAUDE.md disposition in this repo

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Repo inherited the TabulaJacqueliana vault's 717-line
CLAUDE.md (not applicable to the port-engineering context).

**Options considered:**
1. Full replacement — write port-focused CLAUDE.md, drop vault content
2. Move old to `docs/` as reference — write fresh CLAUDE.md at root
3. Delete old, rely on Build Plan for context

**Decision:** Option 2. Done 2026-04-22.

**Artifacts:**
- `CLAUDE.md` — new port-focused spec for Claude Code sessions
- `docs/vault-librarian-reference.md` — archived vault CLAUDE.md for Phase
  0 migration source material

---

## Q-12 | ANSWERED — Supplementary planning doc set

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Build Plan is thorough but overlong (588 lines) and
contains errors the analysis surfaced. Consider layering corrections in
separate docs rather than editing plan in place.

**Options considered (multi-select):**
1. Build Plan Addendum
2. Port Inventory
3. Open Questions log (this file)
4. Phase 0 spec

**Decision:** Write 1 + 2 + 3. Skip explicit Phase 0 spec (Phase 0 is
documented in the Addendum's Q-07 decision notes).

**Artifacts (written 2026-04-22):**
- `docs/hypatia-build-plan-addendum.md`
- `docs/port-inventory.md`
- `docs/open-questions.md` (this file)

---

## Still open — queued for future sessions

### Q-13 | OPEN — Hypatia-Protocol.md Routes A-F: "apply the 4 fixes"

Asked: Build Plan § Week 2 Day 11-12. Still open.

**Context:** Plan mentions 4 fixes to apply vs a prior TabulaJacqueliana
port: restore Route E "just do it" override language, restore Route B
expertise-detection in skip-explanation, tighten Route F verification-rule
language (don't punt back to user), drop CoV reference pointer that no
longer exists. Fixes are referenced but not enumerated with file:line
specificity.

**Needs:** AJ dump the exact 4 fixes (or the vault location of the prior
port where they were applied) so they can be reproduced verbatim. Phase
1 Week 2 Day 11-12 prerequisite.

### Q-14 | OPEN — Hypatia-specific synonym-map initial seed

Asked: 2026-04-22 during port-inventory drafting.

**Context:** Build Plan § Week 2 Day 6-7 says populate
synonym-map.json with "zettelkasten vocabulary (Seed/Tree/Mountain/
atomic-note/block-ref/backlink), Obsidian concepts, AJ's workflow verbs."
Concrete initial seed not yet specified.

**Needs:** 10-20 synonym groups with canonical→aliases mapping. Ideally
seeded from AJ's 2+ months of vault work. Could auto-derive from vault
CLAUDE.md terminology + observed tag taxonomy.

### Q-15 | OPEN — Cline's MCP server config surface

Asked: 2026-04-22 during settings disposition.

**Context:** Bell's `mcp.json` targets Kiro's MCP schema. Cline's equivalent
MCP server registration may differ. Haven't verified Cline's schema.

**Needs:** Install Cline first; inspect its settings UI + config files;
confirm `hypatia-vectorstore` server wiring works before Phase 1 kickoff.
Phase 1 Week 1 Day 5 prerequisite.

### Q-16 | OPEN — Installed agent behavior when kernel fragments load

Asked: 2026-04-22 during kernel decomposition planning.

**Context:** Bell's 2,576-line monolithic kernel is always loaded in Kiro.
Cline's `.clinerules/` behavior with 10+ files: do they all load?
Concatenated in order? Any size cap? Unknown without testing.

**Needs:** Empirical test with Cline installed. Phase 1 Week 1 Day 5
task.

### Q-17 | OPEN — Which local Ollama model is the design target?

Asked: 2026-04-22 after Q2 LLM-agnostic constraint was surfaced.

**Context:** AJ's vault runs mistral-nemo:12b (default), qwen3:14b (agents),
deepseek-r1:14b (idle). Hypatia's lowest-common-denominator design target
needs to be concretely named so kernel prose can be tested against it.

**Needs:** AJ pick the canonical local-fallback model. Affects kernel
prose length, protocol structure, expected context window, reliability
of tool-use instructions. My suggestion: `qwen3:14b` — best tool-use
reputation in the 14B class.

### Q-18 | OPEN — Hypatia-kb migration timing for vault CLAUDE.md

Asked: 2026-04-22 after Q7 decision.

**Context:** Phase 0 migrates vault CLAUDE.md INTO Hypatia. Until that
migration ships + is tested, the vault CLAUDE.md must remain the live
authority for Claude Code vault sessions. Question: at what point does
the vault CLAUDE.md get demoted to a stub?

**Candidate gate:** Phase 1 ship + 2 weeks of Hypatia daily use without
protocol bugs → then demote vault CLAUDE.md. Until then, both files are
live (risk: they drift during the overlap window).

**Needs:** AJ confirm the demotion gate, and commit to not editing vault
CLAUDE.md during the overlap window (write new conventions directly into
Hypatia protocols, mirror back manually if vault CLAUDE.md needs a same-session
update for Claude Code's benefit).

### Q-19 | OPEN — Git history disposition for this repo

Asked: 2026-04-22 during docs/Hypatia Build.md review.

**Context:** `git log` currently shows Bell's commit `ee34dfd The
Nathaniel Protocol v3.2 ...`. Q1 decision "rename in place" + Decision
#3 "Repo: fresh (not forked)" are ambiguous about git history. Options:
1. Keep Bell's history + add Hypatia commits on top (honest attribution,
   noisy log)
2. Squash Bell's history to a single "Initial import from Nathaniel
   Protocol" commit (clean log, preserves attribution)
3. `git checkout --orphan` + fresh init (clean break, loses attribution
   in log — but LICENSE still credits Bell)

**Needs:** AJ decision. Affects how future Claude Code sessions read
history + how attribution reads in public.

### Q-20 | OPEN — docs/Hypatia Build.md (Slope note) disposition

Asked: 2026-04-22 when AJ added the file.

**Context:** File has `kind: Slope` + vault-native wikilinks (`parent:
"[[Obsidian Processing]]"`) that only resolve in TabulaJacqueliana. Its
effort estimate (2-3 weeks / 40-60h) is stale vs. port-inventory's
146-198h projection.

**Options:**
1. Keep as vault snapshot — frozen, stale-risk
2. Strip vault frontmatter, convert to regular markdown planning doc;
   update effort estimate
3. Delete from this repo — keep only in vault

**Needs:** AJ call. Reasonable to defer until the vault stub rewrite
(Q-18) anyway.

---

## Q-21 | ANSWERED — Substrate revisit: Cline vs. Roo Code

Asked: 2026-05-11  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Q-02 (2026-04-22) locked Cline as the runtime substrate for
multi-provider support (Anthropic / OpenAI / Ollama). Three weeks later,
revisit prompted by AJ's commitment to Ollama-primary deployment and the
plan to put Hypatia on a USB stick. Roo Code (Cline fork) has been
shipping faster on local-model ergonomics and uses the same tool-use
protocol as Cline, so the Phase 1 port plan doesn't change.

**Options considered:**
1. Stay on Cline — original decision, slower Ollama velocity
2. Switch to Roo Code — better Ollama, same tool names as Cline
3. Build a custom Python+Ollama agent loop — full control, months of work
4. Switch to Goose (Block) — Ollama-native, newer, less proven
5. Stay on Claude Code with LiteLLM proxy — hacky, breaks LLM-agnostic
   principle

**Decision:** Option 2 (Roo Code).

**Load-bearing rationale:**
- Same tool-use protocol as Cline → Phase 0/1 port work unaffected.
  `fs_read`/`fs_write` rewiring plan stands.
- Strictly better Ollama integration than upstream Cline as of 2026-05.
- Same LLM-agnostic principle from Q-02 preserved.

**Implication:** Phase 1 port targets Roo Code conventions where they
differ from Cline. Suspected scope: `.roorules` directory naming,
provider config format. Verify before Phase 1 starts.

**Supersedes:** Q-02 decision (Cline). Q-02 remains in the log as the
historical answer; this entry is the active decision.

---

## Q-22 | ANSWERED — Memory capture flow during Claude-Code-port sessions

Asked: 2026-05-11  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** While building Hypatia in Claude Code (sandboxed_claude
template), Claude will observe AJ's preferences, decision patterns, and
recurring concepts. The question: how do those observations flow into
Hypatia's Memory/ and Intelligence/ JSON stores, given that (a) those
stores have schemas (validate-schemas.py exists), (b) "Save Discipline"
from POCKET-HQ.md mandates consolidation as the heartbeat, and (c) AJ
wants review-before-canon.

**Options considered:**
1. Claude writes directly to Memory/*.json and Intelligence/*.json
   during sessions
2. Claude writes free-form markdown to an inbox; AJ consolidates into
   JSON stores during Hypatia maintenance
3. Claude writes to a structured pre-store (JSON) that mirrors final
   schema; AJ promotes entries via a script
4. Disable mid-session capture entirely; AJ writes preferences herself

**Decision:** Option 2 (inbox pattern).

**Mechanism:**
- New dir: `<hypatia>/inbox/preferences/` (created with this decision)
- Schema: `<hypatia>/inbox/SCHEMA.md` (defines frontmatter)
- Claude writes captures here during sandboxed_claude sessions
- AJ reviews + consolidates into Memory/Intelligence JSON during
  scheduled Hypatia maintenance sessions
- `validate-schemas.py` in CI prevents broken JSON from shipping
- Sandbox enforces this via Dippy: writes outside inbox/ are denied

**Rationale:**
- Aligns with POCKET-HQ.md "Save Discipline" pattern — consolidation
  is the heartbeat, not real-time accumulation.
- Preserves Q-06 (empty JSON stores at ship) by not letting ad-hoc
  Claude writes bypass curation.
- AJ retains review-before-canon — wrong inferences caught before they
  become Hypatia's beliefs.
- Schema separation: markdown captures need no validation (free-form);
  JSON stores have validation (Hypatia's contract).

**Implications for sandboxed_claude template:**
- `sandbox.sh` mounts Hypatia and Tabula repos :rw
- `.claude/CLAUDE.md` carries a Memory Capture Protocol section
- `.dippy/config` restricts writes to `inbox/` (Hypatia) and
  `Seeds/from-claude/` (Tabula)

**Supersedes:** None directly. Codifies an absence-of-spec from Phase 1.

---

## Change log

- **2026-04-22** — initial log with Q-01 through Q-12 answered + Q-13
  through Q-20 queued. Created during the codebase-analysis session that
  followed Build Plan drafting.
- **2026-05-11** — Q-21 supersedes Q-02 (Roo Code over Cline). Q-22
  adds the inbox memory-capture pattern.
