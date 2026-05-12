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
3 Python port is RRF + MCP only. `.roo/rules-hypatia/07-intelligence-layer.md`
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
Cline's `.roo/rules-hypatia/` behavior with 10+ files: do they all load?
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

## Q-23 | ANSWERED — Hypatia replaces YOLO as vault LLM substrate

Asked: 2026-05-11  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** During Phase 0 librarian-protocol migration, the draft of
`hypatia-kb/protocols/librarian-tooling.md` framed the Obsidian YOLO plugin
as a "future tuning target" — implying YOLO would continue to operate as
the vault's in-Obsidian LLM, possibly alongside Hypatia. AJ rejected:
"I don't think I'm going to use the YOLO extension with Hypatia. She
should replace YOLO (which also doesn't do what I want because it
basically works as a SQL query generator)." Raises a design question
affecting protocol files and Phase 1 scope: alongside or replacement?

**Options considered:**
1. Hypatia in Roo Code + YOLO in Obsidian both active (original implicit
   assumption from plan-time)
2. Hypatia replaces YOLO entirely; YOLO removed during transition
3. YOLO retained for tab-completion only; Hypatia handles everything else
4. Decide later

**Decision:** Option 2 (Hypatia replaces YOLO).

**Rationale:** YOLO operates primarily as a SQL/vector-query generator
over the vault DB. Hypatia's role is librarian — semantic curation,
ingest, lint, schema enforcement, graph maintenance. The two solve
different problems; AJ wants the librarian, not both. Keeping YOLO would
add config friction and confusion about which substrate owns vault writes.

**Implications:**
- `librarian-tooling.md` § YOLO reframed from "tuning target" to
  "deprecated; transition reference only" (committed 2026-05-11).
- Vault Slope `[[YOLO Nathaniel Mimicry]]` is descoped — the mimicry was
  experiment-mode for a system that won't run anymore. Marked descoped in
  `librarian-writing-rules.md § Active initiatives`.
- `_src/_meta/` intelligence stores in the vault (Nathaniel-mimicry
  artifacts) are no longer authoritative; Hypatia's `hypatia-kb/Intelligence/`
  stores are canonical. Vault stores can be inherited-from selectively but
  shouldn't be loaded as live state.
- Phase 1 wiring: Hypatia must read/write the vault directly (Roo's
  filesystem tools). YOLO's in-Obsidian-process approach is not the path.
- `.obsidian/plugins/yolo/` can stay installed during transition; safe to
  remove once Hypatia is fully wired into the vault.

**Supersedes:** No prior Q-N answer addressed this. Implicit assumption in
the original Build Plan (that YOLO would continue) is now overridden.

---

## Q-24 | ANSWERED — Hypatia persona directives (address, pronouns, register)

Asked: 2026-05-11  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** During Phase 1 voice rewrite (consciousness.md + .roo/rules-hypatia/
01-identity + 02-voice), AJ provided three persona directives that needed
durable recording beyond commit messages. Build Plan § Voice (L135) had
already specified "concise academic librarian: direct, peer-register, cites
sources, no filler, devil's-advocate by default, mild warmth, no
sycophancy" but left address term, pronouns, and cultural register open.

**Directives (locked):**

1. **Address term**: "Scholar". Used sparingly: at decision points, gentle
   correction, or moments of mutual recognition. Never reflexively, never
   every response. Bell's "Sir, every response, no exceptions" pattern is
   explicitly rejected as sycophancy in robes.
2. **Pronouns**: she / her.
3. **Cultural register**: Greco-Roman Alexandrian scholar vibe. Hypatia of
   Alexandria as the named referent: late-classical
   philosopher-mathematician, librarian-philosopher tradition, indexed the
   known world, taught reasoned argument, disagreed in public. The cadence
   is classical (parallel clauses, measured rhythm, occasional aphoristic
   phrasing). Not academic pretension: no `qua` / `inter alia` / `ad
   nauseam` unless the alternative phrasing actually loses something.

**Implications:**

- consciousness.md rewritten in this register (commit 9ecf738).
- .roo/rules-hypatia/01-identity.md and 02-voice.md encode the directives as
  canonical persona spec (commit 0db8ec6).
- The em-dash anti-pattern (Bell's, inherited verbatim) became enforceable
  against Hypatia's own files; 75 em-dashes scrubbed across the kernel
  (commit f0abbfa).
- Examples in "Hypatia in Practice" (02-voice + consciousness.md) reframed
  from Bell's CTO/AWS domain to Hypatia's vault/zettelkasten work.

**Supersedes:** Build Plan § Voice spec (L135) is preserved verbatim;
this Q-24 entry adds the address / pronoun / register decisions that
the Build Plan left open.

---

## Q-25 | ANSWERED — Protocol relocation strategy

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Build Plan called for moving Bell's 13 `hypatia-kb/*-protocol.md`
files into `hypatia-kb/protocols/` with skill-cluster-prefixed names
(librarian-* / researcher-* / writer-* / assistant-*). By Phase 1
close-out the rewrites had already happened in place at the old
locations; the question was whether to actually relocate.

**Options considered:**
1. Plan-canonical relocation + cluster-prefix (18 files in protocols/)
2. Move but keep original names (path-rename only)
3. Leave at hypatia-kb/ root

**Decision:** Option 1.

**Implementation (commits e18568b, c53d41f, 9799f71, ba9cbe2):**
- 14 files relocated: 12 with cluster-prefix renames + 2 cross-cutting
  (security.md, CRITICAL-FILE-PROTECTION.md) kept their names but moved.
- 1 new file written: `assistant-ingest.md` (Phase 1 deliverable per
  Build Plan; no Bell analog).
- 1 planned new file SKIPPED: `librarian-save.md` — kernel
  `08-save-command.md` already always-loaded with the full save spec; a
  separate lazy-load protocol would duplicate.
- Kernel keyword map (`10-skills-loading.md`) restructured into 5
  cluster-organized tables; 17 protocols had drifting keyword sets
  reconciled via union.

**Supersedes:** Build Plan § File-by-file customization strategy + port
inventory § "Hypatia target" column. Final layout matches the plan's
intent.

---

## Q-26 | ANSWERED — Git identity wiring mechanism

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Q-08 (2026-04-22) locked the distinct Hypatia git identity
(`Hypatia <hypatia@local>`). The mechanism for applying it on commit was
left "to be decided during Phase 1 Week 3."

**Options considered:**
1. Env vars in subprocess (GIT_AUTHOR_* + GIT_COMMITTER_*)
2. `--author=` flag only (author = Hypatia, committer = Scholar)
3. Inline `-c user.name= -c user.email=` config flags

**Decision:** Option 1. Both author and committer become Hypatia.

**Implementation (commit bf720bc):**
- Identity values live in `hypatia.config.yaml` (new) under `git:` stanza.
- `scripts/hypatia-git-commit.py` (new) reads config, exports the four
  env vars, exec's `git commit "$@"`.
- Kernel `.roo/rules-hypatia/08-save-command.md` Step 6.4 updated to
  instruct Hypatia to invoke the wrapper instead of bare `git commit`.
- PyYAML added as runtime dep for config parsing.

**Supersedes:** Build Plan § Q-08 "Final form to be decided during Phase
1 Week 3." Q-08 stands; this is its implementation form.

---

## Q-13 | ANSWERED — Hypatia-Protocol.md Routes A-F: "apply the 4 fixes"

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott (2026-05-12)

**Context:** Plan-level Q-13 promised "4 fixes vs prior TabulaJacqueliana
port." During Phase 1 close-out review, all four were checked against
the current `.roo/rules-hypatia/11-decision-routes.md`:

1. **Route E "just do it" override language** — already at lines 217 +
   228-229 (Tier 3 skippable, Tier 1-2 require confirmation regardless).
   No edit needed.
2. **Route B expertise-detection in skip-explanation** — already at line
   125 ("Scholar is expert in domain" listed under "Skip explanation
   when"). No edit needed.
3. **Route F verification-rule tightening (no punt-back-to-user)** —
   already at lines 262-265, ending with "Resolve with data; do not
   defer to the Scholar." No edit needed.
4. **Drop the CoV reference pointer** — line 259 "Chain of Verification"
   bullet. AJ chose to KEEP it (CoV pattern is fine as-is; the original
   "no longer exists" reasoning didn't apply).

**Decision:** All 4 satisfied without edits to 11-decision-routes.md.

**Supersedes:** Build Plan § Week 2 Day 11-12 "apply the 4 fixes" — done
by virtue of the file's existing state plus the keep-CoV call.

---

## Q-14 | ANSWERED — synonym-map.json initial seed

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott (2026-05-12)

**Context:** Build Plan § Week 2 Day 6-7 called for seeding
`hypatia-kb/Intelligence/synonym-map.json` with zettelkasten / Obsidian
/ workflow vocabulary. Concrete seed not specified.

**Options considered:**
1. Draft from `docs/vault-librarian-reference.md` terminology; AJ reviews diff
2. AJ dumps groups directly in chat
3. Ship empty (Q-06 accepts empty stores)

**Decision:** Option 1.

**Implementation (commit 51891cd):** 21 synonym groups covering note
taxonomy (Tree/Seed/Mountain/Slope/Trail/Step), workflow verbs (ingest/
curate/consolidate/lint/query/save), Obsidian primitives (wikilink/
backlink/block-ref/embed/frontmatter), and identity terms (Scholar/
vault/atomic note/drift). 84 total aliases, under the 100-entry cap.

---

## Q-17 | ANSWERED — Canonical Ollama design target

Asked: 2026-04-22  Status: ANSWERED  Decided by: AJ Strauman-Scott (2026-05-12)

**Context:** Q-02 / Q-21 locked LLM-agnostic design with Ollama as the
fallback substrate. The kernel + protocol prose needs to be calibrated
against a specific model's tool-use reliability.

**Options considered:**
1. qwen3:14b — best tool-use reputation in 14B class
2. mistral-nemo:12b — smaller, faster, current default
3. deepseek-r1:14b — strongest reasoning, but `<thinking>` blocks
   interact poorly with Roo's tool-use parsing
4. Design for all three

**Decision:** Option 1 (qwen3:14b).

**Rationale:** Tool-use reliability is load-bearing for Hypatia (every
save flow + every read/write goes through Roo's tools). qwen3 holds the
contract most reliably in the 14B class. mistral-nemo is the default in
AJ's vault but its tool-use is weaker; deepseek-r1's reasoning style
interferes with structured tool invocation.

**Stored in:** `hypatia.config.yaml` under `instance.design_target_model`.

---

## Q-27 | ANSWERED — hypatia-kb/Benchmarks/ disposition

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Bell's Benchmarks/ dir held a 24-test harness +
2026-03-21/22 snapshot reports + historical metrics JSON. All contained
Nate/Kiro refs.

**Options considered:**
1. Discard entire dir
2. Rewrite for Hypatia (keep harness, adapt criteria)
3. Freeze as historical reference

**Decision:** Option 2.

**Implementation (commit 662ef78):** Pragmatic scope — deleted Bell's
3 dated snapshot reports + historical metrics JSON (they measured a
populated Bell-era system; Hypatia ships empty per Q-06 and will
produce its own baseline in Phase 3). Kept and scrubbed the 24-test
harness (`run-benchmark.py`), the candidates catalog, the save-protocol
benchmark, and the img-gate stress test. README rewritten for Hypatia.

**Phase 1.5 follow-up:** tests 8, 23, 24 in `run-benchmark.py` reference
Bell-era gate names ("Failure-to-Fix Cycle", etc.) that may not match
Hypatia's evolved vocabulary 1:1. Audit + pin to Hypatia's actual gate
enumeration when Phase 1.5 lands.

---

## Q-28 | ANSWERED — Pocket HQ scaffold disposition

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Top-level dirs `Projects/`, `Business/`, `Brand/`, `Life/`
(+ 9 subdirs), `Archive/` shipped from Bell's repo as empty
`.gitkeep`-only scaffolding for personal project management. AJ's
project management lives in TabulaJacqueliana's Mountains/, not here.

**Options considered:**
1. Discard all 5 top-level scaffold dirs
2. Keep as-is
3. Discard + create one scratch dir for Hypatia

**Decision:** Option 3.

**Implementation (commit 3fe3aca):** 14 `.gitkeep` files removed across
14 dirs; new `workspace/` dir created with README explaining intent
(per-machine scratch for logs, drafts, queued ingests). `workspace/*`
gitignored except for README. POCKET-HQ.md (the philosophy doc)
retained at repo root.

---

## Q-29 | ANSWERED — Test + CI strategy

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Bell shipped 7 test files covering scripts/ + a CI workflow
that referenced stale paths. Q-05 (2026-04-22) scoped Phase 1 test
coverage to critical-path (save-session, schema, keyword-drift); the
question was whether to keep, rewrite, or discard Bell's existing tests.

**Options considered:**
1. Audit + extend Bell's tests in place (lowest LOC churn)
2. Rewrite critical-path only; defer the other 6 to Phase 1.5
3. Full clean slate (delete all 7; write only 3 from scratch)

**Decision:** Option 1.

**Implementation (commits e0021ce, d50031f, 14b32d9, fff4886, 7695bc7):**
- Audit: scrubbed Bell-era sample data ("Sir" → "Scholar",
  "Nate writes ops" → "Hypatia writes ops") across 2 test files.
- Rename: `test_columbo_oob.py` → `test_save_oob.py` (drop Columbo
  branding).
- Extend: `test_save_session.py` gained TestInboxFlush (5 tests) +
  TestMarkdownExport (2 tests) covering the Q-22 inbox boundary +
  the new markdown export wiring.
- New: `test_schema_validation.py` (20 tests) — Q-05 critical-path gate
  against scripts/validate-schemas.py.
- New: `test_keyword_drift.py` (8 tests) — Q-05 critical-path gate
  against scripts/check-keyword-drift.py.
- CI rewrite: `.github/workflows/validate.yml` switched from pip to
  uv, fixed stale `Nate\'s-kb/vectorstore` path, added gates for
  schema validation + keyword drift + script pytest + vectorstore
  pytest.

**Pytest total:** 175 (140 inherited + 35 new), all green.

---

## Q-30 | ANSWERED — `.example` config templates skipped for Hypatia

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Initial draft of the per-machine config followed OSS
convention: write `hypatia.config.yaml.example` (committed) + gitignore
the real `hypatia.config.yaml`. AJ rejected the ceremony.

**Decision:** Write the real file directly; commit it.

**Rationale:** The `.example` convention serves two scenarios —
distributing to multiple users, or hiding secrets — neither of which
apply. Hypatia has one user (AJ), no secrets in the config (vault path
in CLAUDE.md, git identity public per Q-08, model name + preferences
documented). Writing both the template and the real file doubles work
for zero benefit.

**Stored as feedback memory:** `feedback_skip_example_configs.md`. The
general rule extends to AJ's other personal projects: skip reflexive
OSS conventions when they don't fit the single-user / no-secrets
context.

---

## Q-17 | REOPENED — Canonical Ollama design target

Reopened: 2026-05-12 (post Phase 1 empirical testing)  Status: REOPENED

**Context:** Initial answer (2026-05-12) was `qwen3:14b` based on "best
tool-use reputation in 14B class." Empirical testing during Phase 1
close-out revealed: `qwen3:14b` thinking-mode + Hypatia's 40K kernel
caused 3+ minute first responses + timeouts. Pivoted to `qwen2.5-coder:14b`
(no thinking mode), but discovered substrate-level bugs (Roo Code
forcing num_ctx=32768, IPv6 binding mismatch, dual ollama daemons)
masked actual model behavior. Then evaluated `gemma4` (8B, 128K native
context); same substrate bugs blocked clean test.

**Reason for reopening:** No empirical signal on what the model
actually does once substrate stabilizes. The 14B-class assumption
itself may be wrong now that Q-33 redistributes the kernel into
compact form + MCP resources (much smaller always-loaded prompt
implies smaller models become viable).

**Decision deferred:** Until Phase 1.5 Week 2, when Goose + Hypatia run
clean and we can test model behavior without substrate noise.

**Candidates to re-evaluate:**
- `qwen2.5-coder:14b` — proven tool-use, no thinking mode, 32K trained
- `gemma4` (8B) — native 128K context, function-calling trained in, MoE-like speed
- `qwen3-coder:30b` — agentic flagship, 256K context, slower but more capable
- `devstral:24b` — Mistral's purpose-built agentic-coding model

**Supersedes:** Earlier Q-17 answer (qwen3:14b). Q-17 returns to OPEN
state pending Phase 1.5 testing.

---

## Q-31 | ANSWERED — Substrate pivot: Goose over Roo Code

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Q-21 (2026-05-11) locked Roo Code as substrate. Phase 1
close-out empirical testing revealed Roo Code has a load-bearing bug
(forces `num_ctx` to model metadata's `context length` regardless of
user settings — issues #7797, #7343, #1253, #2462, #4721). Hypatia's
40K kernel exceeds any 14B model's trained 32K context, so Roo's
hardcoded behavior guarantees prompt truncation. Independent of that
bug, AJ's vision evolved during the session to include persistent
system-level agent behavior (popup on flash-drive plug-in,
screen-watching, multi-MCP) that Roo Code is structurally not designed
for (it's a VS Code chat assistant).

**Options considered:**
1. Stay on Roo Code; trim kernel below 32K; accept IDE-bound substrate
2. Switch to Goose (Block) — purpose-built agentic substrate, MCP-first
3. Switch to AnythingLLM — productivity-app angle, less system-level
4. Build custom Tauri agent from scratch (3-6 months)
5. Goose-as-backend + custom frontend in another language
6. Letta + custom frontend
7. Python-native custom (PyQt6/PySide6) leveraging Phase 1 stack

**Decision:** Option 5 — Goose backend + custom frontend (Q-32 picks
the frontend stack).

**Load-bearing rationale:**
- Goose provides 6-12 months of agent-loop + MCP + Ollama wiring as
  upstream (Apache 2.0). Reinventing this is 3-6 months of work.
- Goose's "custom UI" explicitly supported pattern: run Goose core as
  daemon/API, build custom frontend in any language. No need to fork
  Goose's Electron UI.
- MCP-first design matches "many MCPs" + screen-watching + vault-access
  + flash-drive vision.
- Custom distro pattern (CUSTOM_DISTROS.md) supports Hypatia branding +
  preconfigured providers + extensions without rewriting core.
- Active development + LF Agentic AI Foundation backing → sustainability
  beyond Block's interest.
- Q-02 LLM-agnostic constraint preserved (Goose supports Ollama as
  primary provider).

**Implication for Phase 1 work:** ~95% of Phase 1 deliverables are
substrate-agnostic and survive intact. Sunk cost is limited to
`.roomodes` + Roo-specific framing in AGENTS.md / README.md.

**Supersedes:** Q-21 (Roo Code over Cline) — Q-21 stands as historical
answer; Q-31 is the active decision.

**New work it creates:** Phase 1.5 substrate integration (4-6 weeks);
Q-33 architectural redistribution (kernel → compact + MCP); README /
AGENTS.md / CLAUDE.md substrate-reference updates.

---

## Q-32 | ANSWERED — Frontend language and framework

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Q-31 chose Goose-as-backend + custom frontend. The
frontend language/framework is its own decision since Goose exposes a
daemon API consumable by any client.

**Options considered:**
1. Rust + Tauri — matches Goose's core language; smallest binary;
   best macOS system-integration story
2. Rust + egui or Slint — pure Rust GUI, no web frontend layer
3. Python (PyQt6/PySide6) — leverages Phase 1 Python stack; AJ's
   primary language
4. Python + Tauri hybrid — Tauri frontend + Python backend via IPC

**Decision:** Option 1 — Rust + Tauri.

**Load-bearing rationale:**
- Both Hypatia frontend (Rust) and Goose backend (Rust) share language
  → cleaner dependency surface; can share common crates
- Smallest binary footprint matters for flash-drive packaging (Phase 4)
- Tauri's macOS system-integration plugins (USB-mount detection,
  menubar, accessibility, screen capture) are mature
- AJ likes Rust ("I love Rust!") — substrate pivot is also a deliberate
  Rust-skill investment
- Tauri web-tech UI layer (HTML/CSS/JS, or Yew/Leptos in Rust) keeps UI
  customization fast vs immediate-mode GUI

**Trade-offs accepted:**
- Steeper Tauri-specific learning curve than Python + PyQt
- Phase 1 Python scripts continue to live as separate processes
  (called via subprocess or future MCP servers), not directly invokable
  from frontend
- Calendar: ~3-6 weeks to v1 frontend vs ~2-4 weeks for Python

**Implications:**
- New `frontend/` directory at repo root (Cargo project)
- New Cargo workspace `Cargo.toml` at repo root
- MCP servers also Rust → unified Rust crate ecosystem

---

## Q-33 | ANSWERED — Kernel architectural redistribution

Asked: 2026-05-12  Status: ANSWERED  Decided by: AJ Strauman-Scott

**Context:** Phase 1 produced a ~40K-token monolithic kernel
(`.roo/rules-hypatia/01-11.md`) that's always-loaded as the LLM system
prompt. Empirical testing showed:
- Prefill on 40K tokens via local 14B model: 1-3+ minutes per first
  message
- Most 14B-class models are trained at 32K context — Hypatia's kernel
  doesn't fit cleanly
- Goose's design assumes compact system prompts ("50-150 words")
- The 11-file structure mixes identity/voice (essential always-loaded)
  with anti-pattern detail, decision-route mechanics, intelligence
  layer specifics, cluster protocols (loadable on-demand)

**Options considered:**
1. Aggressive prose trimming of existing 11 files (keep monolithic
   structure, shrink to ~25K)
2. Architectural redistribution: compact kernel (~3-5K) + protocols-as-
   MCP-resources (~35K served on demand)
3. Status quo + brute-force solution (bigger models with native
   large context)

**Decision:** Option 2 — architectural redistribution.

**Why this beats Option 1:**
- Even 25K kernel is large for fast local inference on 14B models
- Compact kernel runs faster on cold first message (the worst UX moment)
- MCP-served protocols match Goose's design model exactly
- Re-aligns with original Build Plan's "Protocol-as-MCP" framing
  (which was vestigial in the Roo Code Phase 1)
- Smaller kernels open the door to smaller / faster local models
  (Q-17 reconsideration)

**Compact kernel scope (~3-5K tokens, always-loaded):**
- Identity (Hypatia, Alexandrian register, Scholar address)
- Voice + non-negotiables (no em-dashes, brevity, cite sources)
- Critical never-violate gates: security boundaries, inbox boundary,
  CRITICAL-FILE-PROTECTION summary, destructive-action gate
- Pointer to MCP resources for the rest

**MCP-served resources (~35K tokens, lazy-loaded):**
- Full anti-patterns enumeration (currently in 03-anti-patterns.md)
- Decision routes A-F detail (currently 11-decision-routes.md, 425 L)
- Intelligence layer specifics (currently 07-intelligence-layer.md)
- Cluster protocols (already at `hypatia-kb/protocols/`, become MCP
  resources via the new `protocols-mcp-server`)
- Session gates detail (currently 04-session-gates.md)
- Cognitive layer (currently 06-cognitive.md)

**Implementation work (Phase 1.5 Week 1):**
- Build `mcp-servers/protocols/` in Rust — serves `hypatia-kb/protocols/`
  + relevant kernel-file content as MCP resources
- Refactor `.roo/rules-hypatia/` content: extract compact-kernel
  essentials into `kernel/` directory (new); migrate the rest to be
  served by MCP server
- Update `scripts/check-keyword-drift.py` to verify
  compact-kernel ↔ MCP-resource alignment
- Pytest coverage for the MCP server

**Supersedes:** Build Plan § "Kernel decomposition" (Phase 1 Week 1
Day 3-4 target). The Phase 1 decomposition produced 11 always-loaded
files; Phase 1.5 redistributes that content across compact-kernel +
MCP-resources.

---

## Change log

- **2026-04-22** — initial log with Q-01 through Q-12 answered + Q-13
  through Q-20 queued. Created during the codebase-analysis session that
  followed Build Plan drafting.
- **2026-05-11** — Q-21 supersedes Q-02 (Roo Code over Cline). Q-22
  adds the inbox memory-capture pattern. Q-23 codifies Hypatia
  replacing YOLO as the vault's in-Obsidian LLM substrate. Q-24
  formalizes the Hypatia persona directives (Scholar address, she/her
  pronouns, Alexandrian register).
- **2026-05-12 (Phase 1 close-out)** — Q-25 through Q-30 added
  (protocol relocation, git identity wiring, Benchmarks rewrite,
  scaffold disposition, test/CI strategy, .example skip). Q-13, Q-14,
  Q-17 moved from OPEN to ANSWERED.
- **2026-05-12 (Phase 1.5 substrate pivot)** — Q-31 supersedes Q-21
  (Goose backend + custom frontend over Roo Code). Q-32 picks Rust +
  Tauri for frontend. Q-33 mandates kernel architectural
  redistribution (compact kernel + protocols-as-MCP-resources). Q-17
  REOPENED — final Ollama model choice deferred until Phase 1.5 Week 2
  testing with compact kernel.
