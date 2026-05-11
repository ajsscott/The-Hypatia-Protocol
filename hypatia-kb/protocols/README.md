# `hypatia-kb/protocols/` — Librarian Protocol Index

This directory holds Hypatia's protocols for vault-librarian work on
TabulaJacqueliana. They were migrated from the vault's CLAUDE.md
during Phase 0 (2026-05-11).

## Files

| File | Purpose | When to load |
|---|---|---|
| `librarian-role.md` | Operating pattern (llm-wiki), three operations (ingest/query/lint), librarian duties, what stays with the user, devil's advocate, what NOT to do proactively | First — orientation to the role. Read before any vault work. |
| `librarian-vault-structure.md` | Vault identity, top-level folder reference, three parallel organizing schemes, files-to-read-first entry points | Second — orientation to the vault layout. |
| `librarian-note-schemas.md` | Canonical atomic Tree schema, Seed→Tree linkage contract, naming conventions, tag taxonomy, Mountains PM hierarchy, frontmatter schemas per note type | Before drafting, refactoring, or validating any note. |
| `librarian-tooling.md` | Bases (load-bearing fields), Obsidian plugin stack, YOLO transition note (: replaced by Hypatia) | Before reasoning about plugin behavior, schema-rename blast radius, or transition state. |
| `librarian-writing-rules.md` | Known drift/landmines, active initiatives, writing rules (drafting, approval granularity, atomic commits), lessons learned, update protocol | Before any write that touches multiple files, any rename, any frontmatter-field change. |

## Recommended reading order

1. `librarian-role.md` — what Hypatia does as librarian
2. `librarian-vault-structure.md` — where everything lives
3. `librarian-note-schemas.md` — what schemas are load-bearing
4. `librarian-writing-rules.md` — operational guardrails (drift, rules, lessons)
5. `librarian-tooling.md` — secondary reference for plugin/YOLO context

## Source

Migrated from `docs/vault-librarian-reference.md` (frozen 2026-04-22 snapshot
of the vault's `CLAUDE.md`). That file remains as historical archaeology;
this directory is the live spec.

## Update protocol

When vault conventions change meaningfully, update the relevant file in
this directory (see `librarian-writing-rules.md § Update protocol for
this directory`). Resolved landmines come out of
`librarian-writing-rules.md § Known drift`; new schemas go into
`librarian-note-schemas.md`; new tooling state goes into
`librarian-tooling.md`.

When a new librarian-concern emerges that doesn't fit any existing file,
add a new `librarian-<concern>.md` file rather than over-stuffing an
existing one. Update this README and the cross-references at the bottom
of each existing file.
