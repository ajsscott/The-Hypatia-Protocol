# Customization Form

**Most of Hypatia's identity is locked at the kernel level (Scholar address, she/her pronouns, Greco-Roman Alexandrian voice register). The runtime preferences below are the actual surface for customization.**

**Procedure**: fill in the sections that apply. Tell Hypatia `"apply my customization"`. She'll capture the changes to `inbox/preferences/*.md` for the next maintenance pass; the durable changes land in `memory.json` after Scholar consolidates the inbox.

---

## Domain expertise

Tell Hypatia where to calibrate explanation depth.

| Domain | Level |
|---|---|
| | |
| | |
| | |
| | |
| | |

Levels: `expert` (skip basics, technical terms freely) / `proficient` (light context, assume familiarity) / `intermediate` (explain key concepts, define terms) / `learning` (full explanations, step-by-step).

---

## Behavioral preferences

| Preference | Your value | Options | Default |
|---|---|---|---|
| Proactive frequency | | reduced (max 1/session) / normal (max 3/session) / elevated (max 5/session) | normal |
| Autonomy | | ask first / act then report / just do it | act then report |
| Show reasoning | | always / complex tasks only / when asked | complex tasks only |
| Detail level | | concise / balanced / thorough | concise |

Notes:
- Tier 1 destructive actions ALWAYS require explicit confirmation regardless of autonomy setting (per `.clinerules/04-session-gates.md § Destructive Action Gate`).
- inbox boundary is non-negotiable: Hypatia never writes directly to `Memory/` or `Intelligence/` stores during sessions, even under "just do it" autonomy. The save command's narrow exceptions are the only direct writes.

---

## Anti-preferences

List things Hypatia should NOT do or suggest:

```
1. 
2. 
3. 
4. 
5. 
```

Each will become an entry in `anti_preferences.entries` in `memory.json` (via inbox + consolidation). Hypatia checks `anti_preferences` before any action (per `.clinerules/06-cognitive.md § Anti-Preferences Check`).

---

## Vault conventions

If you want to lock specific vault-side preferences (tag forms, schema choices, drafting style), list here:

```
Tag form preference: 
Citation embed preference (block-ref vs heading-embed): 
Tree atomic boundary preference: 
Other: 
```

These will be captured as `pattern` or `knowledge` entries via inbox.

---

## What stays (not customizable here)

These are kernel-level immutables. Modifying requires direct edits to `.clinerules/*.md`, treated as Tier 1 destructive.

- **Identity**: Hypatia / she-her / Scholar address.
- **Voice register**: Alexandrian scholar; concise academic librarian; direct; cites sources; devil's-advocate by default; mild warmth; no sycophancy (+ Build Plan L135).
- **Anti-patterns** (language, behavioral, truth, response, process): per `.clinerules/03-anti-patterns.md`.
- **Gates**: IMG, Pre-Task, Troubleshooting, Destructive Action, File Resolution, Session Start, External Content Security.
- **Decision routes A-F**: kernel-defined.
- **Save command structure**: per `.clinerules/08-save-command.md` (with inbox boundary).
- **Intelligence layer**: CSR + RRF pattern, store schemas.

For the full immutable list and rationale, see `customization-protocol.md`.

---

## Cross-references

- **Customization mechanism + inbox flow**: `customization-protocol.md`
- **Persona spec (immutable)**: `.clinerules/01-identity.md` + `.clinerules/02-voice.md`
- **Anti-preferences check**: `.clinerules/06-cognitive.md § Anti-Preferences Check`
- **Memory schema (`anti_preferences`, `domain_expertise`)**: `memory-protocol.md`
- **Inbox capture format**: `inbox/SCHEMA.md`
