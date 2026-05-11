# Librarian — Vault Structure

**Purpose**: Orients Hypatia to TabulaJacqueliana's identity, folder layout, and parallel organizing schemes. Lists the canonical entry points to read first when entering the vault for context.
**Last Updated**: 2026-05-11
**Trigger Keywords**: vault, Tabula, TabulaJacqueliana, structure, folder, Seeds, Trees, Mountains, Bases, Meridian, orientation, onboarding

---

## Vault identity

- **Owner**: AJ Strauman-Scott (`aj.scott@renphil.org`).
- **Origin**: CUNY-SPS Data Science MS notebase, expanded to cover all her interests and reading.
- **Current phase**: converting to atomic-zettelkasten style, heavily leaning on Obsidian properties, tags, and Bases.
- **Branches**: `main` has everything. `work-safe` excludes personal writing (daily journal `Seedlings/` and creative writing `Forests/`). Work on `work-safe` unless the user is on `main`.
- **Vault metaphor**: plants growing — Seeds germinate Seedlings into Trees which aggregate into Forests; Mountains are the climb (projects).

---

## Top-level folder reference

```
Seeds/          source clippings & lit notes (web, PDF, book, quote)
  Sources/{Articles,Research,Literature,Books,Films,YouTube,Textbooks,
           Slide Decks,Quotes,BotChats,Conversations,Podcasts}/
  People/       person notes
Seedlings/      daily journal + raw notes (main branch only)
Trees/          atomic concept notes, organized by domain
  Unprocessed/  pre-zettelkasten notes awaiting refactor (MS + Job Search era)
Forests/        creative writing (main branch only)
Mountains/      project management (see librarian-note-schemas.md § Mountains PM hierarchy)
Bases/          Obsidian Bases dashboards
_attachments/   binary assets; subfolder _pdfs/ holds PDFs
  (userIgnoreFilters in app.json hides this from search)
_templates/     20 Templater templates — one per kind/source type
_src/           non-note vault-local source
  _YOLO/        YOLO plugin runtime + skill definitions + vector DB (gitignored)
  _QuickAdd/    JS macros for Mountains inheritance
  _webclipper/  Obsidian Web Clipper (browser ext) templates
Meridian.md     root dashboard, embeds Meridian.base global views
```

---

## Architecture at a glance — three parallel organizing schemes

The vault has **three parallel organizing schemes**, each load-bearing in a different way. Don't treat them as interchangeable.

1. **Folder placement** — cosmetic + `auto-note-mover` uses tags to place new notes. Bases do not key on paths.
2. **`kind:` frontmatter** — the project-management truth. `Meridian.base` is filtered on `!kind.isEmpty()`. Values: `Mountain`, `Slope`, `Trail`, `Step`, `Idea`, `Bug`, `Document`, plus source kinds `Research`, `Article`, `Book`, etc.
3. **Tags + `topics:` wikilinks** — `tags` are flat membership labels that other Bases key on. `topics: - "[[Parent]]"` carries the concept graph (a DAG of parent/sibling concepts without explicit MOCs).

---

## Files to read first — vault entry points

When entering the vault for any non-trivial task, orient via these files in order:

1. **The vault's `CLAUDE.md`** — derived stub once Phase 1 ships; for now, the canonical orientation doc for vault-internal context. (Hypatia's authoritative librarian protocol is this directory: `hypatia-kb/protocols/librarian-*.md`.)
2. **`llm-wiki.md`** (vault root) — the operating pattern. Read before any generative work.
3. **`Trees/index.md`** — first stop for any query against the wiki.
4. **`Trees/log.md`** — chronology of wiki operations (grep-parseable).
5. **`_src/_meta/{anti-patterns, preferences, patterns, reasoning}.md`** — vault-side intelligence stores from an earlier Nathaniel-mimicry experiment. Treat as vault-internal artifact; Hypatia's authoritative stores live in `hypatia-kb/Intelligence/`.
6. **`_src/_YOLO/skills/*/SKILL.md`** — 9 skills (4 vault-operational: `process-seed`, `fill-metadata`, `find-unprocessed`, `link-audit`; 5 Nate-mimicry: `decision-routes`, `save-session`, `summarize`, `session-start`, `proactive-offer`).
7. **`Meridian.md`** — PM dashboard (what's active).
8. **Active initiative Slopes** — `Mountains/Slopes/{Trees Unprocessed Refactor, YOLO Nathaniel Mimicry}.md` + their linked Documents in `Mountains/Documents/`. Current initiatives with planning detail.
9. **`Trees/Learning Engineering/Zettelkasten Note-Taking.md`** — the user's stated zettelkasten philosophy.
10. **Canonical note examples:**
    - `Trees/Machine Learning/Deep Learning/Adaptive RAG.md` — minimal atomic
    - `Trees/Machine Learning/Deep Learning/Agentic Retrieval-Augmented Generation.md` — aggregator
    - `Trees/Machine Learning/Deep Learning/Agentic AI.md` — older prose style
    - `Seeds/Sources/Research/singh_agenticRAGSurvey_2026.md` — canonical `^cite-` Seed
11. **`_templates/{Mountain, Research, Basic} Template.md`** — the schemas.
12. **`Bases/Meridian.base`** — the PM spine.
13. **`Seeds/Sources/Articles/Building a Persistent AI Partner A Context Engineering Case Study.md`** — north-star for YOLO mimicry, read critically (n=1, unrigorous metrics).

---

## Cross-references

- **Librarian role, operations, duties** — `librarian-role.md`
- **Note schemas, naming, tags, Mountains hierarchy** — `librarian-note-schemas.md`
- **Bases, plugins, YOLO config** — `librarian-tooling.md`
- **Drift, writing rules, lessons learned** — `librarian-writing-rules.md`
