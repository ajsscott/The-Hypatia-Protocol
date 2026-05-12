# Phase 1.5 Week 1 — Kernel Redistribution Design

**Status:** Design doc, 2026-05-12. Inputs Q-33 architectural decision into concrete file layout + content split.

**Goal:** Reduce the always-loaded system prompt from ~20K tokens (the current 11-file kernel) to ~3-5K tokens, with the bulk migrated to MCP-served resources that load on demand.

---

## Current state (Phase 1, to be refactored)

11 files at `.roo/rules-hypatia/`, total ~20K tokens (~15,837 words):

| File | Tokens (est.) | Disposition |
|---|---:|---|
| 01-identity.md | ~1,100 | Keep in compact kernel |
| 02-voice.md | ~1,650 | Mostly keep in compact kernel; trim examples |
| 03-anti-patterns.md | ~3,000 | Split: short summary in kernel, full → MCP |
| 04-session-gates.md | ~1,770 | Split: rules summary in kernel, full → MCP |
| 05-tools.md | ~1,270 | Full migrate → MCP. Goose handles tool inventory natively. |
| 06-cognitive.md | ~2,720 | Full migrate → MCP. Cognitive loop is reasoning detail, lazy-load. |
| 07-intelligence-layer.md | ~1,380 | Split: routing summary in kernel, full → MCP |
| 08-save-command.md | ~1,650 | Full migrate → MCP. Trigger via `save` keyword. |
| 09-security.md | ~1,560 | Split: critical never-violates in kernel, operational detail → MCP |
| 10-skills-loading.md | ~1,070 | Full migrate → MCP. Goose's MCP host handles routing natively. |
| 11-decision-routes.md | ~3,370 | Split: Routes A-F one-liners in kernel, per-route detail → MCP |

---

## Target state — compact kernel (~4,200 tokens)

Four files at `kernel/`:

```
kernel/
├── 01-identity.md              ~1,100 tokens
├── 02-voice.md                 ~1,500 tokens (trimmed)
├── 03-critical-gates.md        ~800 tokens (NEW)
└── 04-routing.md               ~800 tokens (NEW)
```

### `kernel/01-identity.md`
- Hypatia named for Hypatia of Alexandria
- Pronouns she/her
- Address term "Scholar" (sparingly, never reflexively)
- Super-objective: make the Scholar's knowledge compound; never let stale claims outlast a session
- Role: librarian + philosopher + mathematician
- Vault context: TabulaJacqueliana zettelkasten (entry point; details via MCP librarian-vault-structure)
- Source acknowledgment: forked from Bell's Nathaniel; not Bell's Nate

**Content:** lifted near-verbatim from current `01-identity.md`, condensed where redundant.

### `kernel/02-voice.md`
- Greco-Roman Alexandrian register: classical cadence, parallel clauses, occasional aphoristic phrasing
- Direct, peer-academic, devil's-advocate by default, mild warmth, no sycophancy
- Non-negotiables: accuracy over agreeableness, brevity over completeness, cite the source
- Hard prohibitions: no em-dashes, no filler openings ("Great question!", "So,", "Well,"), no AAVE markers, no "I'm just an AI"
- Reference to: full anti-pattern enumeration via MCP `protocol://anti-patterns-full`

**Content:** voice essentials + non-negotiables only. The full examples + register-comparison content in current `02-voice.md` migrates to MCP `protocol://voice-examples`.

### `kernel/03-critical-gates.md` (NEW)
Distilled from `04-session-gates.md` + `09-security.md` + the inbox-boundary content scattered across files.

- **Inbox boundary (Q-22):** Hypatia writes free-form captures to `inbox/preferences/`; does NOT write to canonical Memory/Intelligence stores. Scholar consolidates during maintenance.
- **Destructive Action Gate (tiers):**
  - Tier 1 (ALWAYS BLOCK): credentials, force-push, production data deletion, security bypass. No override.
  - Tier 2 (CONFIRM): file/Tree deletion, schema changes, external comms, git history rewrites. Confirm before proceeding.
  - Tier 3 (WARN AND PROCEED): overwriting files, large refactors, dependency updates. "Just do it" can skip.
- **Security never-violates:** no credential exfiltration, no exposing protected paths in URLs, no PII in outbound, no executing destructive commands without classification.
- **File protection (Tier-1 paths):** `inbox/`, `hypatia-kb/Memory/`, `hypatia-kb/Intelligence/` write via narrow flow only.
- Pointer: full details via MCP `protocol://session-gates-full`, `protocol://security-operational`, `protocol://critical-file-protection`.

### `kernel/04-routing.md` (NEW)
Distilled from `10-skills-loading.md` + `11-decision-routes.md` headers + `07-intelligence-layer.md` routing summary.

- **Always classify the request before acting.** Score complexity/stakes/reversibility/confidence/continuity.
- **Decision Routes A-F (one-liners):**
  - A: Direct — low complexity, high confidence, full reversibility. Execute.
  - B: With Context — medium complexity OR Scholar in learning mode. Execute + brief explanation.
  - C: Clarify — confidence below threshold. Ask one question, then proceed.
  - D: Options — multiple viable approaches. Surface options, await Scholar pick.
  - E: Confirm Destructive — Tier 1/2 gates (see 03-critical-gates).
  - F: Pre-Action Analysis — non-trivial scope. Frame, explore, interrogate, evaluate, ROI, reason, verify.
- **Default for non-trivial tasks:** Route F.
- **Scholar overrides** ("just do it" / "route F it") respected per Tier rules.
- **Load lazy-loadable protocols on demand** via Goose's MCP host. Keyword map at MCP `protocol://skills-loading-map`. Always-load gates (above) need no MCP fetch.
- Pointer: full per-route detail at MCP `protocol://decision-route-{a,b,c,d,e,f}`.

---

## Target state — MCP-served resources

### Resources from kernel split

Migrated content from `.roo/rules-hypatia/` (full bodies become MCP resources):

| MCP URI | Source file | Notes |
|---|---|---|
| `protocol://anti-patterns-full` | 03-anti-patterns.md | Full enumeration |
| `protocol://voice-examples` | 02-voice.md (example sections) | Cadence patterns + examples |
| `protocol://session-gates-full` | 04-session-gates.md | Full gate spec |
| `protocol://tools-detail` | 05-tools.md | Tool inventory; mostly archival once Goose tool system live |
| `protocol://cognitive-loop` | 06-cognitive.md | OBSERVE>QUESTION>DEDUCE + CSP detail |
| `protocol://intelligence-layer-full` | 07-intelligence-layer.md | Full tiered surfacing + claim-match verification |
| `protocol://save-command-full` | 08-save-command.md | Full 6-step save flow |
| `protocol://security-operational` | 09-security.md | Credential patterns, sanitization filter, communication security |
| `protocol://skills-loading-map` | 10-skills-loading.md | Keyword routing map (becomes documentation; Goose MCP host does live routing) |
| `protocol://decision-route-a` ... `f` | 11-decision-routes.md (per Route section) | One resource per route |

### Resources from existing protocols/

Already aligned. All 20 files at `hypatia-kb/protocols/` become MCP resources without content change:

```
protocol://librarian-role
protocol://librarian-vault-structure
protocol://librarian-note-schemas
protocol://librarian-tooling
protocol://librarian-writing-rules
protocol://librarian-memory
protocol://librarian-lint
protocol://librarian-customize
protocol://researcher-investigate
protocol://researcher-prompt-enhance
protocol://writer-draft
protocol://writer-summarize
protocol://writer-executive
protocol://assistant-development
protocol://assistant-plan
protocol://assistant-problem-solve
protocol://assistant-proactive
protocol://assistant-ingest
protocol://security
protocol://critical-file-protection
```

Total MCP resources: 12 from kernel split + 20 from protocols = **32 resources** served by `mcp-servers/protocols/`.

---

## Routing logic at runtime

The compact kernel is *always* loaded. When a user request arrives, Hypatia:

1. Reads compact kernel content (in context already).
2. Classifies request per `kernel/04-routing.md`.
3. If the request matches a known keyword from the skills-loading map (kept as documentation), Hypatia tells Goose to load the matching MCP resource. Goose's MCP host fetches the resource content and adds it to context.
4. Hypatia then operates with: compact kernel + relevant MCP resources + user message + tool definitions.

For a typical librarian task ("ingest this Seed"), the effective system prompt becomes:
- compact kernel: ~4,200 tokens (always)
- `protocol://librarian-role`: ~1,000 tokens (loaded on keyword match)
- `protocol://librarian-note-schemas`: ~1,500 tokens (loaded on keyword match)
- `protocol://assistant-ingest`: ~1,800 tokens (loaded on keyword match)

Total per-task context: ~8,500 tokens. Well under any local model's trained context. Fast prefill.

For a save flow, the effective system prompt becomes:
- compact kernel: ~4,200 tokens
- `protocol://save-command-full`: ~1,650 tokens

Total: ~5,850 tokens. Tiny.

---

## Implementation plan (Week 1 work)

1. **Create `kernel/` directory** with 4 new compact files.
2. **Move `.roo/rules-hypatia/`** to `docs/reference/phase-1-kernel-archive/` (preserves historical full-text). Update README + AGENTS.md references.
3. **Build `mcp-servers/protocols/`** Rust MCP server: reads from `kernel-archive/` + `hypatia-kb/protocols/`, serves as resources. URI scheme above.
4. **Update `scripts/check-keyword-drift.py`** to verify the compact kernel's routing keywords align with what the MCP server actually serves.
5. **Pytest** for the MCP server (test resource list, content retrieval, missing-resource handling).
6. **Update `hypatia.config.yaml`** with MCP server registration (Goose will read this in Week 2).

---

## Outstanding questions for Week 2

- **Where does `kernel-archive/` live?** Options: `docs/reference/`, `kernel/_archive/`, deleted (since git history preserves it). Recommend `docs/reference/phase-1-kernel-archive/` to keep frontend-visible state clean.
- **How does Hypatia know which MCP resource to load on a given keyword?** Two paths:
  - (a) Compact kernel includes the keyword map (~1K tokens). Hypatia behaviorally decides to fetch.
  - (b) Goose's MCP host auto-routes based on resource metadata + Hypatia's tool calls. More native to Goose.
  Recommend (a) for v1 (Phase 1 worked this way; minimal change), migrate to (b) when Goose's routing patterns are clearer.
- **Persona drift risk:** by removing voice examples from always-loaded kernel, Hypatia might drift toward generic-assistant voice. Mitigation: keep `protocol://voice-examples` keyword-triggered on any sustained conversation; verify in persona validation (Phase 1.5 Week 2).

---

## Acceptance criteria for Week 1

- [ ] `kernel/` directory with 4 files totaling <5K tokens
- [ ] `mcp-servers/protocols/` Rust crate compiling
- [ ] All 32 MCP resources retrievable by URI
- [ ] `check-keyword-drift.py` passes against new layout
- [ ] Pytest passes (existing 175 tests + new MCP server tests)
- [ ] `docs/reference/phase-1-kernel-archive/` contains preserved full-text versions of the 11 original kernel files
- [ ] `.roo/rules-hypatia/` empty or removed (after archival)
