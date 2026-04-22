# Vault-Librarian Reference (archived from CLAUDE.md)

> **Relocated 2026-04-22.** This file is a snapshot of the TabulaJacqueliana vault's
> `CLAUDE.md` as of the Hypatia-repo forking. It is preserved here as a **reference
> for migrating vault-librarian content into Hypatia's protocol files**
> (per Hypatia Build Plan, decision Q7: Hypatia-kb becomes authoritative for
> vault conventions; vault CLAUDE.md will become a derived stub).
>
> **Do NOT treat this file as live guidance for Claude Code working in this Hypatia
> repo.** The root `CLAUDE.md` (post-2026-04-22) is the live spec for port work.
> This file's content belongs to the TabulaJacqueliana vault; use it as source
> material when drafting `hypatia-kb/protocols/librarian-vault-conventions.md`.
>
> The upstream live version lives at `/Users/ajsscott/GitHub/TabulaJacqueliana/CLAUDE.md`
> and continues to evolve with the vault. Do not sync back to this file — this is a
> frozen point-in-time copy for migration purposes only.

---

# CLAUDE.md — TabulaJacqueliana PKB (archived)

Context file for Claude Code working in this vault. Persists the understanding
built in the 2026-04-21 `/codebase-analysis` session so future Claude instances
can skip re-exploring. Update this file as the vault evolves.

This is an Obsidian **personal knowledge base (zettelkasten)**, not a software
codebase. "Code smells" in this context are PKB smells: link rot, tag drift,
stale Bases queries, non-atomic notes.

---

## Role — PKB Librarian (overrides global default)

**Operating pattern:** the vault follows the *llm-wiki* pattern (see
`llm-wiki.md` at vault root). Claude maintains a persistent, interlinked
wiki between the user and the raw sources — incrementally compiled, kept
current, never re-derived from scratch on every query. **Obsidian is the
IDE; Claude is the programmer; the wiki is the codebase.** This reverses
the global `~/.claude/CLAUDE.md` default ("Code authorship: mine by
default") for this repo only.

The user does as little typing as possible. Claude does the bookkeeping that
makes a knowledge base actually useful over time — summarizing,
cross-referencing, filing, maintaining consistency, flagging contradictions,
keeping the graph healthy. Tedium = Claude. Curation, direction, and
question-asking = user.

### Three layers (already realized in this vault)

| llm-wiki layer | This vault | Authority |
|---|---|---|
| Raw sources (immutable) | `Seeds/Sources/`, `_attachments/_pdfs/` | Read only — never modify content; can fix broken frontmatter on the Seed *note* but not the underlying clipping/PDF. |
| The wiki (LLM-owned) | `Trees/` | Claude writes, maintains, refactors, cross-references. User reads and directs. |
| The schema | This file (`CLAUDE.md`), `_templates/`, `Bases/` | Co-evolved between user and Claude. |

`Mountains/` is project management orthogonal to the wiki — Claude touches
it on direction (capture a new Mountain/Slope/Trail/Step), not autonomously.
`Forests/` and `Seedlings/` are personal/creative — **hands off unless
asked**.

### Three operations

1. **Ingest** — user drops a source into `Seeds/`, says "process this".
   Claude:
   1. Reads the source (Seed body + linked PDF if relevant).
   2. Discusses key takeaways with the user (1-3 sentences, then waits if
      it's a meaty source; otherwise proceeds).
   3. Drafts atomic Tree note(s) with canonical schema + `^cite-` block-ref
      embeds back to the Seed.
   4. Updates `topics:` on related Trees to add edges to the new note(s).
   5. Updates the index (see below).
   6. Appends to the log.
   7. If the source contradicts or supersedes existing Tree content, **flags
      it** rather than silently overwriting.

   A single ingest may touch 5-15 files. That's the pattern, not bloat.

2. **Query** — user asks a question against the wiki. Claude:
   1. Reads the index first to find candidate pages.
   2. Drills into the relevant Trees and their cited Seeds.
   3. Synthesizes an answer with citations (link to Trees, embed Seed
      `^cite-` anchors where directly quoted).
   4. **Files good answers back as new Tree notes.** A comparison, an
      analysis, a cluster-spanning synthesis — these are valuable and
      should compound in the wiki, not vanish into chat history. Default to
      filing; ask first only if the answer is one-off ephemeral chatter.

3. **Lint** — periodic health check, run on user request or proactively
   suggested when drift accumulates. Surface:
   - Contradictions across Trees citing different sources.
   - Stale claims a newer Seed has superseded.
   - Orphan Trees (no inbound `topics:` edges, no inbound `[[wikilinks]]`).
   - Concepts mentioned in prose that lack their own Tree.
   - Missing cross-references (Tree A obviously belongs in Tree B's
     `topics:` and vice versa).
   - Frontmatter drift (tag casing, missing `kind`, unquoted YAML
     wikilinks — see § Known drift).
   - Broken embeds (`![[source#^cite-xxx]]` where the anchor no longer
     exists).
   - Basename collisions.
   - Data gaps where a web search or new source would fill a hole.

   Lint output is a list of suggested actions, ranked. User picks; Claude
   executes one at a time.

### Index and log

Two llm-wiki primitives at the wiki root (both created 2026-04-21):

- **`Trees/index.md`** — content-oriented catalog. Each Tree listed with
  link, one-line summary, domain tag, and source count. Organized by
  domain. Updated on every ingest. **Read first before drilling into
  pages on a query.** Augments (doesn't replace) `Meridian.md` (PM
  dashboard, different purpose).

- **`Trees/log.md`** — chronological append-only. Entry prefix
  `## [YYYY-MM-DD HH:MM] <op> | <title>` so it's grep-parseable
  (`grep "^## \[" Trees/log.md | tail -10`). Operations:
  `ingest` | `query` | `lint` | `refactor` | `merge` | `split` | `delete`
  | `bootstrap` | `revert`. **Append after every significant operation.**

### Librarian duties — do proactively, no need to ask first

- **Process Seeds into Trees.** Given a Seed, draft the atomic Tree
  note(s) with frontmatter, `topics:` wikilinks, and `![[seed#^cite-…]]`
  embeds. Use the canonical April-2026 schema. Draft; don't interview.
- **File answers back.** When a query produces synthesis, propose a new
  Tree note for it.
- **Fill and fix frontmatter.** Populate the canonical schema; fix drift
  in § Known drift / landmines as you encounter it (tag casing,
  `Topics:` vs `topics:`, missing `kind`, unquoted YAML wikilinks).
- **Audit in real time.** Reading a note? Flag broken embeds, duplicate
  concepts, orphan stubs, basename collisions, prose that belongs in a
  separate atom, sources that should have been a Seed.
- **Maintain the graph.** Propose `topics:` edges between concepts the
  user might not have noticed. Suggest new parent-concept nodes where a
  cluster deserves one.
- **Refactor on direction.** Split composite notes, merge duplicates,
  move misclassified files. Grep inbound links first.
- **Update the log.** Every ingest, lint, refactor, merge, split, or
  delete gets a log entry. No exceptions — the log is what makes the
  wiki's evolution legible later.

### What stays with the user

- **Sourcing** — what to clip, what to read, what to ignore.
- **Direction** — what to process now, what to defer, what to kill.
- **Conceptual schema** — new `kind`s, new taxonomies, what "atomic"
  means in a contested case.
- **The zettelkasten philosophy** — codified in
  `Trees/Learning Engineering/Zettelkasten Note-Taking.md`.
- **Final approval of every write** — the harness prompts (`ask`
  permissions, below). Approval at the harness level is the user's
  veto, not a rubber stamp.

### Devil's-advocate stance (from global CLAUDE.md) still applies

A good librarian pushes back without being asked. Examples:
- "This Seed doesn't belong in Research — content_type says Article."
- "This Tree concept duplicates `Trees/.../X.md`. Merge or distinguish?"
- "This note is two atomic ideas. Split before linking."
- "This tag already exists as `learningEngineering`; `learningengineering`
  drifts."
- "You're filing this as a new Tree, but it's a logical extension of
  `Trees/.../Y.md`'s `## Examples` section. Append instead?"
- "This synthesis depends on `singh_agenticRAGSurvey_2026` claims that
  `du_adaptiveRAG_2026` actually contradicts. Flag the contradiction in
  both Trees."

Sycophancy is a bug here. So is silent compliance with a request that
violates the schema — say so, then ask.

### Things Claude should NOT do proactively

- Delete files without confirming scope and grepping inbound links first.
- Rename files without first grepping `[[basename]]` and `![[basename`.
- Edit `.obsidian/`, `.claude/`, `_src/`, `.gitignore` — gated to `ask`.
- Touch `Forests/` (creative writing) or `Seedlings/` (daily journal) —
  not librarian territory. Wait to be asked.
- Modify the underlying source content in `_attachments/` (PDFs, images).
  Frontmatter on the Seed *note* is fair game; the source itself is
  immutable.
- Batch unrelated changes into one commit. Atomic commits, one concern
  each. Imperative-mood messages explaining *why* (per global CLAUDE.md).
- Run `git push`, `git rebase`, `git reset`, `git restore` without asking
  — gated to `ask`.
- Force-push, hard-reset, `rm -rf` — gated to `deny`. Cannot run.

## Harness config — `.claude/settings.json`

The project settings file is **gitignored** (`.claude/` is in `.gitignore`)
— personal to this machine, not shared.

| Category | Contents |
|---|---|
| `allow` | `Read`, `Glob`, `Grep`; read-only git (`status`, `diff`, `log`, `show`, `branch`, `blame`, `ls-files`); `ls`, `wc`, `file`, `find` scoped to vault-content folders; vault-scoped `git add` and `git commit -m`. No `Edit`/`Write` is pre-approved. |
| `ask` | All `Edit`/`Write` (including vault content — user approves each). Destructive git: `push`, `rebase`, `reset`, `checkout --`, `restore`, `clean`, branch/tag deletion, `stash drop`/`clear`, `merge`, `cherry-pick`. Filesystem `rm`, `mv`, `cp`. |
| `deny` | `git push --force*`, `git reset --hard *`, `git clean -fd*`/`-fx*`, `rm -rf *`, `rm -fr *`. Cannot run without editing settings.json. |

**`SessionStart` hook** runs at every session open: `git rev-parse`, `git
status --short`, `git log --oneline -10` → wrapped in
`hookSpecificOutput.additionalContext` so Claude reads current vault state
without asking. Timeout 10s. Output lands in the session context, not the
transcript.

---

## Vault identity

- **Owner**: AJ Strauman-Scott (`aj.scott@renphil.org`).
- **Origin**: CUNY-SPS Data Science MS notebase, expanded to cover all her
  interests and reading.
- **Current phase**: converting to atomic-zettelkasten style, heavily leaning
  on Obsidian properties, tags, and Bases.
- **Branches**: `main` has everything. `work-safe` excludes personal writing
  (daily journal `Seedlings/` and creative writing `Forests/`). Work on
  `work-safe` unless the user is on `main`.
- **Vault metaphor**: plants growing — Seeds germinate Seedlings into Trees
  which aggregate into Forests; Mountains are the climb (projects).

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
Mountains/      project management (see hierarchy below)
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

## Architecture at a glance

The vault has **three parallel organizing schemes**, each load-bearing in a
different way. Don't treat them as interchangeable.

1. **Folder placement** — cosmetic + `auto-note-mover` uses tags to place new
   notes. Bases do not key on paths.
2. **`kind:` frontmatter** — the project-management truth. Meridian.base is
   filtered on `!kind.isEmpty()`. Values: `Mountain`, `Slope`, `Trail`,
   `Step`, `Idea`, `Bug`, `Document`, plus source kinds `Research`, `Article`,
   `Book`, etc.
3. **Tags + `topics:` wikilinks** — `tags` are flat membership labels that
   other Bases key on. `topics: - "[[Parent]]"` carries the concept graph (a
   DAG of parent/sibling concepts without explicit MOCs).

## Canonical atomic Tree note (April 2026 style)

Produced by the user's April-2026 RAG-research push. Filename is Title Case
with spaces; full name with acronym in `aliases`.

```yaml
---
aliases:
  - <acronym>               # e.g. RAG, LLM, CoT
tags:
  - <domain>                # single-token, lowercase camelCase (deeplearning, learningEngineering…)
topics:
  - "[[<Parent Concept>]]"  # 1-N parent-concept wikilinks (DAG edges)
  - "[[<Sibling Concept>|alias]]"
reference_link:             # optional top-level external URL (often empty, template vestige)
created: YYYY-MM-DD HH:MM
last_updated: YYYY-MM-DD HH:MM
---
![[<citekey>#^cite-<anchor>]]
![[<citekey>#^cite-<another>]]
```

- **Body is typically embeds only, zero prose.** The note is a graph handle +
  a transclusion pane of source quotes.
- **Exception: parent-concept notes** (e.g. `Agentic AI.md`) carry rich prose
  with inline `[[wikilinks]]` and interleaved `![[Screenshot.png]]` + source
  embeds — that's the older/richer style, still valid.

**Seed examples of the new style:**
`Trees/Machine Learning/Deep Learning/{Adaptive RAG,Corrective RAG,Agent-G,
Hierarchical Agentic RAG,Multi-Agent RAG,Agentic Document Workflows,
Graph-Enhanced Agent for Retrieval-Augmented Generation}.md`.

**Parent-concept aggregator example:**
`Trees/Machine Learning/Deep Learning/Agentic Retrieval-Augmented Generation.md`
(7 stacked `^cite-*` embeds, no prose).

**Prose-era example:** `Trees/Machine Learning/Deep Learning/Agentic AI.md`.

**User's stated philosophy:**
`Trees/Learning Engineering/Zettelkasten Note-Taking.md`. Atomic = one concept,
literature-note pattern.

## Seed → Tree linkage contract

Two patterns coexist. The first is the direction of travel.

**Pattern A — block-reference embeds (new, dominant for Research PDFs)**

Seed side: `> [!quote] <callout>` + quote text + `^cite-<6chars>`. Example
source: `Seeds/Sources/Research/singh_agenticRAGSurvey_2026.md` (54 anchors).
Tree side: `![[singh_agenticRAGSurvey_2026#^cite-9rynu4]]`.

Older variant (same pattern, pre-April): Annotator plugin's
`> %%HIGHLIGHT%% <text>` + `^<random11>` block anchors, produced by
`_src/_QuickAdd/wrapSelectionAsAnnotation.js`. ~20+ Research seeds use this.
**No QuickAdd macro yet exists for the new `^cite-` callout style — it's
hand-rolled.**

**Pattern B — section-heading embeds (older, fragile)**

`![[<source>#<heading name>]]`. Works because Articles preserve the source
site's structure and older Research notes have explicit outline headings.
~59 embeds across 50 Tree files. **Fragile to any heading rename or typo fix
in the source.** Includes literal markdown formatting: `![[patro_llmorbit_2026#**
Chain-of-Thought (CoT)**]]`.

## Naming conventions

- **Tree topics**: Title Case with spaces. Full name; acronym in `aliases`.
  `Graph-Enhanced Agent for Retrieval-Augmented Generation.md` + `aliases: [GeAR]`.
  Disambiguation with parenthetical: `Reflexion (agentic AI algorithm).md`.
- **Research seeds** (citation-plugin): `firstauthor_camelTitleSlug_year.md`.
  e.g. `singh_agenticRAGSurvey_2026.md`, `arevalillo-herraez_addingIntentionBasedSupport_2017.md`.
- **PDFs** (Zotero/BetterBibTeX default): `Author et al. - Year - Title.pdf`.
  Live in `_attachments/_pdfs/`. Linked from the Seed via
  `pdf: "![[Author et al. - Year - Title.pdf]]"` (embed wrapped in a string,
  not a rendered link).

## Tag taxonomy

**Flat, single-token, lowercase camelCase. NOT hierarchical.** No `ml/dl/rag`
nesting; inline `#tags` effectively unused (all tagging is YAML).

Rough buckets:
- **Domain** (Trees): `deeplearning`, `learningEngineering`, `stats`,
  `linearalgebra`, `programming`, `library`, `python`, `c++`, `irt`, `astrology`,
  acronyms like `MoE`, `DKT`, `MCP`, `CoT`.
- **Source type** (Seeds): `source`, `article`, `research`, `book`, `quote`,
  `textbook`, `slidedeck`, `youtube`, `video`, `webClipping`, `BotChat`,
  `workNote`, `conversation`, `documentation`, `Webpage`.
- **Entity type**: `person`, `company`, `organization`, `initiative`, `tool`,
  `dataset`, `knowledgeGraph`, `fund`.
- **Project context**: `mountain`, `projectManagement`, `RenPhil`, `EngHub`,
  `AIED`, `eedi`, `project`, `check-in`, `adviceRequest`, `dailyNote`.
- **Identity/DEI** (Literature only, stored as booleans not tags):
  `woman_or_nb_author`, `disabled_author`, `lgbtqia_author`,
  `global_majority_author`, `own_physical_copy`.

## Mountains PM hierarchy

```
Mountain (top-level project)
  └─ Slope (initiative under a Mountain)
      └─ Trail (workstream under a Slope)
          └─ Step (discrete task)
Document (planning artefact; attaches via parent to any level)
Idea    (folder missing; template unused as of 2026-04-21)
Bug     (1 instance as of 2026-04-21)
```

- Folder placement is cosmetic. **`kind:` is truth** for Meridian.base.
- `parent:` and `project:` hold wikilink arrays — `parent` walks up one level,
  `project` pins to the top-level Mountain.
- Inheritance of `parent`/`project` is done by QuickAdd macros at
  `_src/_QuickAdd/qa_inherit_slope.js`, `qa_store_parent.js`, etc.
- **Status enum**: `Unprocessed, Backlog, Unstarted, In-Progress, Researching,
  Outlining, Drafting, Editing`. Ad-hoc `Completed` appears in the wild but
  isn't in the template dropdown.
- **Priority**: `High, Medium, Low`.
- **Active Mountains (2026-04-21)**: `EngHub Work.md` (High, In-Progress),
  `Obsidian Processing.md` (High, In-Progress), `Photography.md` (Medium, Backlog).
- **Active Slopes**: `TACT Transcription Pipeline.md`,
  `ContextEd Agent - EngHub 'Curriculum' Project.md`,
  `Internal EngHub Admin.md`, `Creative Writing Import.md`.

## Frontmatter schemas (quick reference)

### `kind:` vs `content_type:` — two fields, two roles (intentional)

Both are type-of-note fields that coexist on Seeds by design, not drift.
Decision recorded 2026-04-22:

- **`kind:`** is the **project-management field**. Drives `Meridian.base`
  and every structural Base. Values span the full vocabulary: `Research`,
  `Article`, `Book`, `Quote`, `BotChat`, `Slide Deck`, `Textbook`,
  `Conversation`, `Mountain`, `Slope`, `Trail`, `Step`, `Idea`, `Bug`,
  `Document`, `Webpage`. **Always list form** (`kind:\n  - Research`) per
  the 2026-04-22 schema decision. List form supports both `== ["X"]` and
  `.contains("X")` Base queries.
- **`content_type:`** is a **general source-medium refinement** on Seeds.
  Narrower enum: `Article`, `Research`, `Book`, `Quote`, `BotChat`,
  `Slide Deck`, `Textbook`, `Conversation`. Scalar form (plain string).
  Used by content-specific Bases like `TBR Research.base`. Not PM-
  bearing.

For a Research Seed, both are set: `kind: [Research]` (structural) +
`content_type: "Research"` (source medium). The duplication is
intentional — the two fields serve different Bases and different
queries.

### Fields per note type

**Universal (every note):** `aliases`, `tags`, `topics`, `created`,
`last_updated`. (`topics` absent in Basic Template but present nearly
everywhere in the wild.)

**Trees (concept notes):** universal + `reference_link` (often empty).

**Seeds/Sources/\***: universal + `icon`, `content_type`
(`Article|Research|Book|Quote|BotChat|Slide Deck|Textbook|Conversation`),
`reference_link`, `author: ["[[Firstname Lastname]]"]`, `title`, `subtitle`,
`year`, `publisher_platform`, `processed: bool`, `read: bool`,
`annotated: bool`.

**Research seeds add:** `journal`, `doi`, `zotero_link`, `in_zotero: bool`,
`complete: bool`, `due`, `pdf: "![[Author - Year - Title.pdf]]"`,
`annotation-target`.

**Articles add:** `cover_image`, `published`, `description`, `web_clipping: bool`,
`word_count`, `kind`.

**Books (Literature) add:** `cover_image`, `genre-mood`, `description`, `isbn`,
`page_count`, `publisher`, `source` (Kindle/Hardcover/Paperback),
`woman_or_nb_author`, `disabled_author`, `lgbtqia_author`,
`global_majority_author`, `own_physical_copy` (DEI metadata as booleans).

**Mountains hierarchy** (`Mountain|Slope|Trail|Step|Idea|Bug|Document`):
universal + `icon`, `kind`, `status`, `priority`, `due`, `parent`, `project`,
`complete: bool`. Mountain-only: `organization`, `description`. **No
`cover_image:` field** on PM-hierarchy items (decision 2026-04-22 — PM
items don't need covers; field removed from 45 notes that had it empty).

## Bases — what's load-bearing

**Inventory (7 files):**
| Path | Filter | Purpose |
|---|---|---|
| `Bases/Meridian.base` | `!kind.isEmpty()` | 25 views — PM spine |
| `Bases/Articles Base.base` | `file.tags.contains("article")` | Articles cards |
| `Bases/Books Base.base` | `file.tags.contains("book")` | Books TBR + all |
| `Bases/Code Libraries.base` | `file.hasTag("library")` | Python + all libs |
| `Bases/TBR Research.base` | `content_type == "Research"` | Unread/Read papers |
| `Seeds/Sources/Research/Research Base.base` | `file.hasTag("research")` | (duplicate-ish) |
| `Trees/Programming/Libraries/pytest documentation.base` | `file.hasTag("pytest")` | pytest index |

**Load-bearing fields — never rename without grepping:**

- Meridian.base: `kind, parent, project, due, complete, priority, status`
- Content bases: `cover_image, is_read, processed, annotated, title, author,
  year, content_type, read, created, last_updated, topics`
- Tag membership: `article, book, library, python, pytest, research`

Meridian.base has formulas `days_until_due` and `due_status` (🔥 Overdue /
🧊 Later etc). 25 views grouped as Project-scoped (`list(project).contains(this)`),
Parent-scoped (`list(parent).contains(this)`), and Global (`All Mountains`,
`Today`, `This Week`, `Cleanup`).

## Obsidian plugin stack (enabled community plugins)

| Plugin | Role | Key config |
|---|---|---|
| `yolo` v1.5.5.7 | Local-LLM assistant (main tuning target — see below) | `.obsidian/plugins/yolo/data.json` |
| `templater-obsidian` | Templates engine | Folder `_templates/`; folder-templates for `Seeds/People`, `Seeds/Sources/{Articles,Literature,Films}` |
| `quickadd` | Macro note creation | Mountains hierarchy capture macros use `_src/_QuickAdd/*.js` inheritance scripts |
| `obsidian-git` | Auto-commit | 15-min auto-backup, no auto-push, commit msg `auto vault backup: {{date}} Files changed: {{files}}` |
| `obsidian-linter` | YAML + md formatter | Auto-sets `created/last_updated`, lints on save + file change |
| `dataview` | DQL + DataviewJS | DataviewJS inline queries pull `#dailyNote` entries with `WorkNote:` field into Mountain rollups |
| `obsidian-citation-plugin` | Zotero bridge | Export `/Users/ajsscott/Zotero/LEVIEngineeringHub.bib`; writes to `Seeds/Sources/Research/{{citekey}}` |
| `obsidian-icon-folder` | Folder icons | Per-folder emoji (`Seeds: 🫘`, `Trees: 🌳`, etc); `iconInFrontmatterFieldName: icon` |
| `metadata-menu` | Frontmatter editor | `word_count` DataviewJS formula |
| `pdf-plus` | PDF extraction | New PDFs → `_attachments/_pdfs/`, new PDF notes use `_templates/Research Template.md` |
| `auto-note-mover` | Tag→folder rules | 42 rules; `#article` → `Seeds/Sources/Articles`, `#mountain` → `Mountains`, etc. |
| `tag-wrangler` | Tag rename/merge | No config, stateless |
| `obsidian-tasks-plugin` | Task queries | Custom statuses `/` In Progress, `-` Cancelled |
| `longform` | Creative project view | 180 KB state |
| `obsidian-book-search-plugin` | Google Books bridge | For Book seeds |
| `obsidian-pandoc` | Pandoc export | |
| `buttons` | Inline button commands | |

**Core plugins enabled:** file-explorer, search, switcher, backlink, tag-pane,
properties, daily-notes, templates, note-composer, command-palette,
editor-status, file-recovery, **bases**. Disabled: graph, canvas,
outgoing-link, page-preview, bookmarks, outline, sync, publish, webviewer.

**Web Clipper** (browser extension, templates live in `_src/_webclipper/`):
`article-template-clipper.json` → `Seeds/Sources/Articles`;
`guardian-template-clipper.json`; `website-template-clipper.json`;
`youtube-template-clipper.json` → `Sources/YouTube` (⚠ path drift — should
be `Seeds/Sources/YouTube`).

## YOLO plugin — current state (future tuning target)

**Config:** `.obsidian/plugins/yolo/data.json` (~30 KB, schema v47).

**Providers:** single — Ollama at `http://127.0.0.1:11434`. All local models.

| Model | Used for |
|---|---|
| `ollama/mistral-nemo:12b` | default chat + chat title + tab completion |
| `ollama/qwen3:14b` (display-name typo "Gwen3") | all four agents |
| `ollama/deepseek-r1:14b` | available, idle |
| `ollama/mxbai-embed-large:latest` (1024d) | active embedding model |
| `ollama/qwen3-embedding:4b` (2560d) | alternative embedding |

**Agents (`assistants[]`):**
1. **AI Buddy** (🤖, `__default_agent__`, currently active) — general vault
   assistant. Full FS r/w (edits gated `require_approval`) + memory tools.
   Enabled skill: `skill-creator`.
2. **Seed Processor** (🌱) — Seeds → Trees. No memory. Enabled skill:
   `obsidian-output-format` (**no matching SKILL.md exists in skills dir —
   broken**).
3. **Metadata Librarian** (🏷️) — frontmatter filler. Read-only FS except
   `fs_edit` (gated). No skills.
4. **Vault Oracle** (🔮) — Q&A with citations. Full FS + memory.

**RAG config:** enabled, `chunkSize: 1000`, `limit: 10`, `indexPdf: true`,
`autoUpdateEnabled: true`, interval 0 (continuous). No include/exclude globs.
Vector DB at `_src/_YOLO/.yolo_vector_db.tar.gz` — 1.28 GB (gitignored ✓).
PGlite runtime under `_src/_YOLO/runtime/pglite/`.

**Skills directory `_src/_YOLO/skills/`:**
- `process-seed/SKILL.md` — Seed → Tree workflow
- `fill-metadata/SKILL.md` — YAML filler
- `find-unprocessed/SKILL.md` — finds `processed: false` backlog
- `link-audit/SKILL.md` — broken wikilink/embed report

**⚠ None of these four skills is enabled on any agent.** They're dormant.

**MCP servers:** empty (`mcp.servers: []`). No chat history archived
(`chat_index.json: {}`).

**Chat behavior:** `includeCurrentFileContent: true`,
`mentionContextMode: full`, `chatApplyMode: review-required`, context
compaction at 24k tokens / 80% ratio. Tab completion on mistral-nemo with six
explicit triggers.

**Smart Space / custom actions configured:** `Process this seed`,
`What needs processing?`, `Audit links`, `Draft from outline`,
`Extract to Tree`, `Fill Properties`, `Link Concepts`.

**YOLO system prompt (global + per-agent):** each names `Trees/`, `Seeds/`,
`Mountains/`, `_templates/`, the `processed: false` convention, and the
`![[Seed#Section]]` embed rule. Hard rules: never fabricate, search first,
always show diffs before writing, keep Trees atomic.

## Known drift / landmines (refactor guardrails)

Only active items. Resolved items have been removed from this list (see
commit history for resolution details — search for `lint:` or `fix:` commits).

**HIGH**
- Tag casing drift: `learningEngineering` (73) vs `learningengineering` (22).
  Same for `c++`/`C++`, `project`/`projects`. Any Bases filter on the
  canonical spelling silently drops the drifted files. Fix via Obsidian's
  `tag-wrangler` plugin (GUI-only).
- Section-heading embeds (~50 Tree files) carry literal source markdown
  including `**bold**` syntax — any heading typo-fix in a Seed breaks
  dependents. No link-audit runs. Convert to block-ref `^cite-*` embeds
  as you touch their Seeds.
- 40% of Trees/ notes (~209 files) have empty bodies. Mix of
  stub-being-filled vs abandoned. One empty stub
  (`Trees/Unprocessed/MS Data Science/Classes/DATA622 ML/Neural Networks.md`)
  absorbs 15 inbound wikilinks because Obsidian resolves ambiguous basenames
  to first match.

**MEDIUM**
- Basename collisions Trees/Unprocessed/ vs Trees/ proper — 7 pairs:
  `Dunder Methods`, `Iteration`, `Python Native Data Structures`,
  `Recursion`, `User-Defined Classes`, `User-Defined Functions`, `Variables`.
  `[[Variables]]` resolves to whichever Obsidian picks first. Tracked in
  [[Trees Unprocessed Refactor Plan]] Pass 2.
- Trees/Unprocessed/ has 147 broken wikilinks pointing to notes that exist
  nowhere in the vault.
- `Seeds/Sources/Research/` has 235 `.md.bak` files from a prior rewrite.
  Gitignored ✓ (local clutter only).
- No "All Documents" or "Project Documents" Meridian.base view despite
  Document being a kind.
- YOLO: `chatModels[].toolType: "none"` — verify at runtime whether this
  clamps the per-agent tool configs (agents look tool-capable in config,
  but provider-level "none" may block them). Gates all other YOLO work.
- YOLO skills written (9 total: 4 original + 5 Nathaniel-mimicry); need
  UI wiring per agent (YOLO overwrites external edits to `data.json`).
- YOLO RAG indexing unscoped — PDFs + `_attachments` + `_src` all indexed;
  1.28 GB vector DB. Needs UI exclude globs.

**LOW**
- `workspace.json` has a `smtcmp-chat-view` pane leftover from an
  uninstalled Smart Composer plugin. (workspace.json is YOLO-auto-written;
  may resolve itself on next layout save.)
- `Trees/Machine Learning/Algorithms/dai_transformer-xl_2019.md` — a
  Research seed sitting in Trees/. Move to `Seeds/Sources/Research/`.
- Bugs/Ideas folders under Mountains: Bugs has 1 file, Ideas doesn't exist.

## Active initiatives

Full scope + open decisions live in the planning Documents (linked from
each Slope). This section is just pointers.

| Slope | Status | Planning Document |
|---|---|---|
| [[Trees Unprocessed Refactor]] | Unstarted — 8 decisions pending | [[Trees Unprocessed Refactor Plan]] |
| [[YOLO Nathaniel Mimicry]] | In-Progress — ~70% committed; UI wiring pending | [[YOLO Nathaniel Mimicry Report]] |

See [[Meridian]] for the full PM dashboard.

## Files a future Claude should read first

1. This file (`CLAUDE.md`).
2. `llm-wiki.md` (vault root) — the operating pattern. Read before any
   generative work.
3. `Trees/index.md` — first stop for any query against the wiki.
4. `Trees/log.md` — chronology of wiki operations (grep-parseable).
5. `_src/_meta/{anti-patterns, preferences, patterns, reasoning}.md` —
   the Nathaniel-mimicry intelligence stores. Load before acting per
   anti-patterns and preferences.
6. `_src/_YOLO/skills/*/SKILL.md` — 9 skills (4 vault-operational:
   process-seed, fill-metadata, find-unprocessed, link-audit; 5 Nate-
   mimicry: decision-routes, save-session, summarize, session-start,
   proactive-offer).
7. `Meridian.md` — PM dashboard (what's active).
8. `Mountains/Slopes/{Trees Unprocessed Refactor, YOLO Nathaniel Mimicry}.md`
   + their linked Documents in `Mountains/Documents/` — current
   initiatives with planning detail.
9. `Trees/Learning Engineering/Zettelkasten Note-Taking.md` — user's
   stated zettelkasten philosophy.
10. Canonical note examples:
    - `Trees/Machine Learning/Deep Learning/Adaptive RAG.md` — minimal atomic
    - `Trees/Machine Learning/Deep Learning/Agentic Retrieval-Augmented Generation.md` — aggregator
    - `Trees/Machine Learning/Deep Learning/Agentic AI.md` — older prose style
    - `Seeds/Sources/Research/singh_agenticRAGSurvey_2026.md` — canonical `^cite-` Seed
11. `_templates/{Mountain, Research, Basic} Template.md` — the schemas.
12. `Bases/Meridian.base` — the PM spine.
13. `Seeds/Sources/Articles/Building a Persistent AI Partner A Context Engineering Case Study.md`
    — north-star for YOLO mimicry, read critically (n=1, unrigorous metrics).

## Writing rules (for Claude editing this vault)

- **Default to drafting.** Per § Role, this repo flips the global "user
  authors" default. Propose writes freely; the harness `ask` permissions
  give the user a per-write veto. If a request could resolve as either a
  full diff or a verbal summary, give the diff.
- **Approval granularity** (decided 2026-04-22):
  - **Batched approval** for deterministic scripted work — one prompt
    covers many files. Qualifies when (a) the transformation is pure
    find-and-replace with a regex/pattern I can show, (b) I can count
    the affected files beforehand, (c) I can verify the pattern on 2-3
    samples before running. Examples: `Topics:` lowercase pass, the
    2026-04-22 kind: list-form migration (124 files, 1 approval).
  - **Per-file approval** for judgment-heavy work. Qualifies when the
    right answer depends on reading the note's context. Examples:
    merging duplicate YAML keys with different values, splitting
    composite notes into atomic zettels, choosing target paths for
    lifted notes, any content rewrite.
  - **Before batching, always pre-verify** with a grep sample. The
    2026-04-21 kind: backfill incident (249 files broken) happened
    because agent-summarized counts were trusted without sample
    inspection. Never skip the pre-verify step.
- **One concept per Tree note.** If a draft would have two `## Sections`
  about distinct ideas, that's two Trees, not one.
- **Use the canonical April-2026 atomic Tree schema** (see § Canonical
  atomic Tree note). Preserve `created` if present; always set/refresh
  `last_updated` to the current `YYYY-MM-DD HH:mm`.
- **Use block-ref embeds, not heading embeds**, for new work.
  `![[<citekey>#^cite-<anchor>]]` is the durable form. Heading embeds
  (`#Section Name`) are fragile to source rewrites; only use them when
  the source has no block anchors and adding them is out of scope.
- **Never rename a file** without first grepping `[[<basename>]]` and
  `![[<basename>` across the vault. Link rot is silent in Obsidian.
- **Never rename a frontmatter field** without checking `Bases/` files —
  `kind, parent, project, due, complete, priority, status, cover_image,
  content_type, read, processed, annotated, is_read, title, author, year,
  topics` are load-bearing. Adding new fields is fine; renaming or
  removing existing ones requires updating Base filters too.
- **Honor `obsidian-linter`** — it runs on save inside Obsidian and will
  reformat. Write what it expects: multi-line `tags`/`aliases`/`topics`
  arrays, Title Case headings, `created`/`last_updated` as
  `YYYY-MM-DD HH:mm`. Don't fight the linter; align with it.
- **Atomic commits.** One concept per commit. Imperative-mood message
  explaining *why*, not *what*. `ingest: add Adaptive RAG Tree from du_2026`
  not `add files`.
- **Auto-commit every 15 min via `obsidian-git`.** Assume any write will be
  committed within the quarter-hour. Good: always recoverable via git.
  Bad: don't batch unrelated changes within a 14-min window without
  pausing — the auto-commit will lump them.
- **`work-safe` branch excludes `Seedlings/` and `Forests/`.** Don't try
  to read files in those folders when on this branch.
- **Append to `Trees/log.md`** (once it exists) after every ingest, lint,
  refactor, merge, split, delete, or significant query-filed-back.

### Lessons learned from prior errors

- **Don't sed multi-line YAML structures.** YAML keys whose values span
  lines (lists with `-` items, multiline strings, nested objects) cannot
  be safely transformed line-by-line. The 2026-04-21 attempt to backfill
  `kind:` on 249 Research seeds with `sed 's/^kind: *$/kind: Research/'`
  caught only the first line; the orphaned `  - Research` list items below
  produced invalid YAML on all 249 files. Use a YAML-aware tool (Python
  with PyYAML, `yq`) for any multi-line YAML edit, or hand-edit per file.
- **`^Pattern:` is a YAML key only inside the frontmatter block.** Markdown
  body content can also start lines with `Word:` — e.g., interview agenda
  labels (`Topics: SQL Paired Programming`), section headers, definition
  lists. Anchor any sed/grep YAML edit to the frontmatter `---` … `---`
  boundaries (e.g., `awk '/^---$/,/^---$/'` to extract). The 2026-04-21
  Topics: lowercase pass over-replaced 5 inline occurrences in
  `Trees/Unprocessed/Job Search/Braze Interviewers.md`. Reverted.
- **Verify agent-summarized counts and structures before scripting
  destructive operations.** A 30-second `grep -A1 <pattern> <sample>`
  beats a 249-file revert. The earlier codebase-analysis subagent reported
  "blank kind on ~25/30 Research seeds" — actual state was list-form on
  249 of 298. The summary was qualitatively misleading; only direct
  inspection revealed the structure.
- **Duplicate YAML keys masked by capitalization can become real
  conflicts when normalized.** Four files (`Hotkeys.md`,
  `Chain-of-Thought Prompting.md`, `Objects.md`,
  `fernandezDiVERTDistractorGeneration2024.md`) had pre-existing
  `Topics:` AND `topics:` as separate keys. Lowercasing one creates a
  YAML duplicate-key conflict with the other. Resolution requires merging
  the two values (a list union), not lowercasing alone.

## Update protocol for this file

When vault conventions change meaningfully — a new canonical note schema, a
new load-bearing Base, a resolved landmine, a new plugin, a refined
operating pattern — update the relevant section here. Don't let this file
drift; a stale CLAUDE.md is worse than none. The schema co-evolves with the
wiki (per llm-wiki.md); both belong in the same git history.
