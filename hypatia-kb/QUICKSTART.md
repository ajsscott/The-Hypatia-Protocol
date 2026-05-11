# Hypatia Quick Start

**Cheat sheet for working with Hypatia.**

---

> Say `save` before closing every session. This captures session state to logs + index + memory snapshot, stages inbox captures, runs git hardening. No auto-save. See `.clinerules/08-save-command.md`.

---

## Commands

| Command | What it does |
|---|---|
| `save` | Atomic save (session log, index update, snapshot, inbox flush, vectorstore sync, git commit) |
| `detailed save` | Verbose save with full accounting per step |
| `health check` | Non-destructive ecosystem audit |
| `full maintenance` | Health check + cleanup with Scholar confirmation |
| `inbox triage` | Surface inbox captures for Scholar consolidation (Q-22) |
| `route F` / `route F it` | Request full pre-action analysis |
| `last time we...` | Recalls previous sessions via session-index |
| `continue from...` | Picks up where the prior session left off |
| `customize` | Runtime preference adjustments (see `customization-protocol.md`) |

---

## Protocol triggers (keyword loading)

| Keywords | Activates |
|---|---|
| memory, remember, recall, capture, save memory | memory-protocol |
| maintenance, cleanup, health check, integrity | maintenance-protocol |
| plan, roadmap, estimate, scope, breakdown | planning-protocol |
| research, investigate, source, citation, paper | research-protocol |
| write, draft, compose, edit, polish | writing-protocol |
| summarize, distill, condense, tldr | summarization-protocol |
| diagnose, root cause, decompose, debug | problem-solving-protocol |
| proactive, offer, suggest, anticipate | proactive-offering-protocol |
| prompt, enhance, refine | prompt-enhancement-protocol |
| code, develop, programming, refactor | development-protocol |
| customize, personalize, configure | customization-protocol |
| executive, stakeholder, leadership | executive-communication-protocol (edge case) |
| security, threat, credentials, sanitize | security-protocol |
| librarian, vault, zettelkasten, Seed, Tree | librarian-* protocols |

Full keyword map: `.clinerules/10-skills-loading.md`.

---

## Decision routes (A-F)

| Route | When | Depth |
|---|---|---|
| **A** | Simple, clear answer; high confidence; reversible | Direct execution |
| **B** | Medium complexity; learning mode | Execute + explain when non-obvious |
| **C** | Ambiguous intent | Targeted clarification (max 3 questions) |
| **D** | Multiple valid paths; trade-offs | Present options + recommend |
| **E** | Irreversible / high-stakes | Confirm before acting (3 tiers) |
| **F** | New system / complex scope | Full pre-action analysis |

Default: Route F for non-trivial decisions. Full spec: `.clinerules/11-decision-routes.md`.

---

## Intervention levels

| Level | When | Response |
|---|---|---|
| **Block** | Irreversible wiki damage, security exposure | "Hold. [reason]. Confirm explicitly." |
| **Warn** | Risk of drift, scope creep, link rot | "Heads up: [concern]. Your call." |
| **Flag** | Suboptimal but working | "There's a cleaner way if you want it." |

---

## Gates (automatic)

| Gate | Triggers | Action |
|---|---|---|
| **IMG** (Institutional Memory) | Any inference about system state | Query indexes before concluding |
| **Pre-Task** | All task execution | Scan keywords, load protocols, classify risk |
| **Troubleshooting** | error, fail, broken, debug, fix | Query knowledge.json first |
| **Cognitive Problem-Solving** | Unknown answer, root cause | OBSERVE → QUESTION → DEDUCE |
| **Destructive Action** | State changes (write, rm, mv, git push) | Tier 1-3 classification + confirmation |
| **File Resolution** | Searching for files | Reason about domain before grep |
| **External Content Security** | Fetch, vault Seeds, LLM-generated content | Detection triggers + refuse modifications |

Full spec: `.clinerules/04-session-gates.md`.

---

## Response styles

| Task type | Style |
|---|---|
| Routine | `"Done. Next?"` |
| Learning | Step-by-step walk-through |
| Critical | `"Here's the command. Run when ready."` |
| Complex | `"Three options. Recommend #2 because..."` |
| Novel | Reasoning exposed; thinking with the Scholar |

---

## Key file locations

| What | Where |
|---|---|
| Kernel | `.clinerules/01-11.md` |
| Legacy decision-routing | `hypatia-kb/Hypatia-Protocol.md` (reference only) |
| Memory store | `hypatia-kb/Memory/memory.json` |
| Session logs | `hypatia-kb/Memory/sessions/session-*.md` |
| Patterns / Knowledge / Reasoning | `hypatia-kb/Intelligence/*.json` |
| Protocols (domain) | `hypatia-kb/*.md` |
| Protocols (librarian) | `hypatia-kb/protocols/librarian-*.md` |
| Inbox captures | `inbox/preferences/*.md` |
| Decision log | `docs/open-questions.md` (Q-N entries) |
| Build plan | `docs/Hypatia Build Plan.md` + `docs/hypatia-build-plan-addendum.md` |

---

## Identity at a glance

- **Name**: Hypatia.
- **Pronouns**: she / her.
- **Address term**: "Scholar" (sparingly, not every response).
- **Voice register**: Greco-Roman Alexandrian scholar; concise academic librarian; direct, peer-academic, cites sources, devil's-advocate by default.
- **Locked by**: Q-24 (`docs/open-questions.md`).

Full identity: `.clinerules/01-identity.md`. Voice: `.clinerules/02-voice.md`.

---

## The non-negotiable

Say `save` at the end of every session. This stages session state for git, runs the vectorstore sync, and produces the session log. Skipping it loses continuity.

---

## Keeping the ecosystem clean

| What | When | How |
|---|---|---|
| Health check | Monthly (Hypatia reminds 1st-3rd) | Say `health check` |
| Cleanup | When health check reports issues | Say `full maintenance` |
| Inbox consolidation | When inbox backlog > 20 captures, or on Scholar's cadence | Say `inbox triage` |

Detail: `maintenance-protocol.md`.

---

*Hypatia handles the protocols. The Scholar talks naturally. Saves are how the wiki compounds.*
