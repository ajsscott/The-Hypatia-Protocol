# Hypatia Inbox — Capture Schema

Captures land here from Claude Code sessions. They are **free-form markdown with structured
frontmatter** — not validated JSON. AJ consolidates them into
`hypatia-kb/Memory/*.json` and `hypatia-kb/Intelligence/*.json` during
scheduled maintenance sessions.

Format-light by design: capture-time friction matters more than
schema-perfection. Anything unclear can be fixed at consolidation time.

---

## File location

```
inbox/preferences/<topic-slug>.md
```

- `<topic-slug>` — kebab-case, descriptive. `tab-indent-preference.md`,
 not `pref-1.md`. If the same topic gets multiple captures, append
 `-NN`: `tab-indent-preference-02.md`.
- One observation per file. Don't append to an existing file unless the
 new observation is genuinely the same data point reinforced — in which
 case bump confidence and note the second source-session.

---

## Frontmatter (required)

```yaml
---
observed: 2026-05-11 # ISO date, capture time
source-session: sandboxed_claude — Hypatia Phase 0 # repo + brief context
candidate-type: preference # see types below
confidence: high # high | medium | low
status: new # new | consolidated | rejected
---
```

### Field semantics

- **`observed`** — date the observation was made, ISO 8601 (`YYYY-MM-DD`).
 Time-of-day not required.
- **`source-session`** — what kind of session this came from. Examples:
 `sandboxed_claude — Hypatia Phase 0 port`,
 `sandboxed_claude — TabulaJacqueliana note triage`,
 `host Claude Code — exploratory query`. Enough that AJ can reconstruct
 context at consolidation time.
- **`candidate-type`** — which Hypatia store this *would* target if accepted:
 - `preference` → `hypatia-kb/Memory/memory.json` (AJ's preferences entity)
 - `pattern` → `hypatia-kb/Intelligence/patterns.json` (behavioral patterns)
 - `knowledge` → `hypatia-kb/Intelligence/knowledge.json` (factual claims)
 - `reasoning` → `hypatia-kb/Intelligence/reasoning.json` (derived
 conclusions, multi-step inferences)
 - `unsure` → AJ decides at consolidation. Don't overthink; use this when
 the type is genuinely ambiguous.
- **`confidence`**:
 - `high` — explicit AJ statement, or recurring across 3+ exchanges in
 the session
 - `medium` — single observation but consistent with prior captures
 - `low` — single observation, possibly situational, worth flagging
 but probably won't survive consolidation
- **`status`** — initialized to `new` by Claude. AJ flips to
 `consolidated` after porting into the target JSON store, or `rejected`
 with a `rejection-reason:` field if dropped.

---

## Body structure (recommended, not enforced)

```markdown
## What I observed

<1-3 sentences. Be specific. "AJ rejected X because Y" not "AJ has
preferences." Quote her words if she made an explicit statement.>

## How I'd codify it

<How this would appear in the target JSON store. For preference:
"User prefers tabs over spaces for indentation in Python." For pattern:
"Loud-fail over silent-recovery on schema validation errors."
For knowledge: "Hypatia targets Roo Code substrate as of."
This section is the candidate consolidated form.>

## Confidence rationale

<Why high/medium/low. What evidence backs it. Where it could be wrong.>

## Related captures

<Optional. Wikilinks to prior captures on the same topic, if any.>
```

---

## What NOT to capture

- **Persona / behavior rules** for Hypatia (e.g., "always cite sources").
 Those belong in the protocol markdown files, not in memory stores.
 Direct AJ to edit `hypatia-kb/<topic>-protocol.md`.
- **Project-specific notes.** Use the project's `CLAUDE.md` instead.
- **Tabula-vault material.** Use `~/GitHub/TabulaJacqueliana/Seeds/from-claude/`.
- **Speculation about what AJ *might* prefer.** Confidence-low captures
 about hypotheticals waste consolidation time. Wait until you've
 observed the actual signal.

---

## Consolidation lifecycle

```
new → AJ reviews → consolidated → entry exists in target JSON store
 ↘ rejected → kept in inbox/ with rejection-reason: field
```

Consolidated captures move to `inbox/preferences/_consolidated/` (or get
deleted, AJ's call). Rejected ones stay where they are — pattern
recognition for "Claude over-infers in X situation" is valuable.

---

## Example capture

```markdown
---
observed: 2026-05-11
source-session: sandboxed_claude — Hypatia Phase 0 setup
candidate-type: preference
confidence: high
status: new
---

## What I observed

AJ explicitly said "I want the memories claude learns within the sandbox
to be kept at the template or user level" during a session about wiring
up the sandbox. She also said "I'm trying to develop a personal
assistant. that I can have interact with any computer I'm on by living
on a fast USB stick."

## How I'd codify it

User preference for portable, cross-machine assistant state:
- Memory should live in files synced via portable storage, not in
 any tool's local config dir
- Decision criteria for new tooling: must support file-system-resident
 state, not OS keychain / cloud-only / app-local DB

## Confidence rationale

High. Explicit goal-statement, restated across multiple exchanges in
the same session, consistent with + substrate decisions and
POCKET-HQ.md design.

## Related captures

(First on this topic.)
```
