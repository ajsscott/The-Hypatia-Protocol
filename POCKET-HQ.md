# Pocket HQ

**An inherited pattern from the upstream fork. Hypatia adopts parts of it and diverges from others.**

---

## What Pocket HQ is

Pocket HQ is a work-organization pattern, not a product. The premise: consolidate your digital operational world (projects, business, learning, personal planning, and your AI partner's intelligence layer) into one local repository, so an AI agent can see it, reason across it, and remember it.

The pattern formalizes five architectural principles:

1. **Single-repo consolidation.** One tree, one disk, one machine. The AI can only connect dots it can see.
2. **AI-first directory design.** The folder structure is itself part of the prompt. Predictable paths, domain-based routing.
3. **Persistent intelligence layer.** A dedicated knowledge base where the AI accumulates preferences, patterns, knowledge, reasoning, session history. Compounds over time.
4. **Portability.** The entire workspace runs from a flash drive. Plug in, work, unplug.
5. **Save discipline.** End-of-session save is non-negotiable. It is the heartbeat that turns ephemeral conversation into persistent memory.

The full original framing is preserved at `docs/reference/nathaniel/` for historical reference.

---

## How Hypatia adopts and diverges

| Principle | Hypatia status |
|---|---|
| Single-repo consolidation | **Partial.** The framework (kernel + protocols + intelligence) consolidates here. The TabulaJacqueliana vault stays external by design. |
| AI-first directory design | **Adopted.** `.roo/rules-hypatia/` + `hypatia-kb/` + `inbox/` are structured for Roo Code to navigate without explanation. |
| Persistent intelligence layer | **Adopted with inbox boundary.** Hypatia captures to `inbox/preferences/*.md`; the Scholar consolidates into canonical stores. No auto-promotion. |
| Portability | **Deferred to Phase 1.5.** Phase 1 targets the Scholar's Mac. Flash-drive bootstrap (`hypatia.config.yaml` + cross-platform setup) is not implemented. |
| Save discipline | **Adopted.** `save` triggers session log + index + snapshot + inbox flush + vectorstore sync + git commit, in that order, atomically. |

### Why the vault stays external

The upstream pattern colocates everything. Hypatia's working context is a zettelkasten vault (Obsidian on TabulaJacqueliana) that predates the framework and has its own lifecycle, sync, and tooling. Forcing it into this repo would break Obsidian, force git-LFS for media, and entangle vault history with framework history. Hypatia reads and writes the vault as an external sense. The framework knows the vault's structure (`hypatia-kb/protocols/librarian-vault-structure.md`); it does not own it.

### Why portability is deferred

The flash-drive use case is real but secondary. Phase 1's goal is a working Hypatia on the Scholar's Mac. Per-machine bootstrap, path abstraction, and POSIX/Windows polyfill (the `save-session.py:53-55` `fcntl` exit, for instance) are tracked for Phase 1.5.

---

## The scaffold

Five empty directories ship at the repo root from the upstream fork:

```
Projects/   Active project work
Business/   Business operations
Brand/      Personal brand, content, social
Life/       Personal planning (Career/, Education/, Family/, Finances/, Goals/, Health/, Home/, Journal/)
Archive/    Completed or historical materials
```

These currently hold only `.gitkeep` markers. The Scholar may populate them, rename them, or remove them. They are not load-bearing for Hypatia's vault-librarian work, which routes through `hypatia-kb/` and the external vault.

The intelligence system (`hypatia-kb/`) sits alongside these as a peer, not above them. That is the part of the pattern Hypatia retains: the framework lives at the same level as the work it observes, not in a hidden config tree.

---

## The connection to Hypatia

The structural lesson worth keeping: a persistent AI partner needs a stable, navigable file substrate, and a save mechanism that turns each session into durable state. Without those, every session starts cold.

Hypatia's instantiation of the pattern:

- **Kernel** at `.roo/rules-hypatia/` (always loaded; Roo Code reads on mode switch).
- **Intelligence layer** at `hypatia-kb/Intelligence/` (curated; ships empty; grows through Scholar consolidation).
- **Memory** at `hypatia-kb/Memory/` (session logs + entity memory + cache).
- **Inbox** at `inbox/preferences/` (free-form captures awaiting curation; no auto-promotion to stores).
- **Save command** wired through `scripts/save-session.py` (atomic, idempotent, git-committed).

The phrase "the workspace is the prompt" still holds. The structure carries context the kernel does not have to restate.

---

## What this file is not

- Not a marketing document. The "compounding effect" framing in the upstream version assumed a productivity-tool audience. Hypatia is a personal-use research partner; the value compounds because the vault grows, not because of session counts.
- Not a deployment guide. See `README.md` for setup and `hypatia-kb/QUICKSTART.md` for operating.
- Not a contract. The five principles are a useful shorthand. The Scholar reserves the right to break any of them when the work demands it.
