# Librarian — Note Schemas

**Purpose**: Canonical schemas for every note type in TabulaJacqueliana: atomic Tree notes, Seed→Tree linkage contracts, naming conventions, tag taxonomy, the Mountains PM hierarchy, and per-note-type frontmatter fields. Hypatia uses this as the source of truth when drafting, refactoring, or validating any note.
**Last Updated**: 2026-05-11
**Trigger Keywords**: schema, atomic note, atomic, frontmatter, YAML, naming, tag, kind, content_type, citekey, cite, embed, topics, aliases, Tree, Seed, Mountain, Mountain hierarchy

---

## Canonical atomic Tree note (April 2026 style)

Produced by the user's April-2026 RAG-research push. Filename is Title Case with spaces; full name with acronym in `aliases`.

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

- **Body is typically embeds only, zero prose.** The note is a graph handle + a transclusion pane of source quotes.
- **Exception: parent-concept notes** (e.g. `Agentic AI.md`) carry rich prose with inline `[[wikilinks]]` and interleaved `![[Screenshot.png]]` + source embeds — that's the older/richer style, still valid.

**Seed examples of the new style:**
`Trees/Machine Learning/Deep Learning/{Adaptive RAG, Corrective RAG, Agent-G, Hierarchical Agentic RAG, Multi-Agent RAG, Agentic Document Workflows, Graph-Enhanced Agent for Retrieval-Augmented Generation}.md`.

**Parent-concept aggregator example:**
`Trees/Machine Learning/Deep Learning/Agentic Retrieval-Augmented Generation.md` (7 stacked `^cite-*` embeds, no prose).

**Prose-era example:** `Trees/Machine Learning/Deep Learning/Agentic AI.md`.

**User's stated philosophy:** `Trees/Learning Engineering/Zettelkasten Note-Taking.md`. Atomic = one concept, literature-note pattern.

---

## Seed → Tree linkage contract

Two patterns coexist. The first is the direction of travel.

### Pattern A — block-reference embeds (new, dominant for Research PDFs)

Seed side: `> [!quote] <callout>` + quote text + `^cite-<6chars>`. Example source: `Seeds/Sources/Research/singh_agenticRAGSurvey_2026.md` (54 anchors).
Tree side: `![[singh_agenticRAGSurvey_2026#^cite-9rynu4]]`.

Older variant (same pattern, pre-April): Annotator plugin's `> %%HIGHLIGHT%% <text>` + `^<random11>` block anchors, produced by `_src/_QuickAdd/wrapSelectionAsAnnotation.js`. ~20+ Research seeds use this. **No QuickAdd macro yet exists for the new `^cite-` callout style — it's hand-rolled.**

### Pattern B — section-heading embeds (older, fragile)

`![[<source>#<heading name>]]`. Works because Articles preserve the source site's structure and older Research notes have explicit outline headings. ~59 embeds across 50 Tree files. **Fragile to any heading rename or typo fix in the source.** Includes literal markdown formatting: `![[patro_llmorbit_2026#**Chain-of-Thought (CoT)**]]`.

**Direction of travel:** prefer Pattern A. When touching a Pattern-B Seed during refactor, convert the embeds to Pattern A `^cite-*` form.

---

## Naming conventions

- **Tree topics**: Title Case with spaces. Full name; acronym in `aliases`.
  `Graph-Enhanced Agent for Retrieval-Augmented Generation.md` + `aliases: [GeAR]`.
  Disambiguation with parenthetical: `Reflexion (agentic AI algorithm).md`.
- **Research seeds** (citation-plugin): `firstauthor_camelTitleSlug_year.md`.
  e.g. `singh_agenticRAGSurvey_2026.md`, `arevalillo-herraez_addingIntentionBasedSupport_2017.md`.
- **PDFs** (Zotero/BetterBibTeX default): `Author et al. - Year - Title.pdf`.
  Live in `_attachments/_pdfs/`. Linked from the Seed via `pdf: "![[Author et al. - Year - Title.pdf]]"` (embed wrapped in a string, not a rendered link).

---

## Tag taxonomy

**Flat, single-token, lowercase camelCase. NOT hierarchical.** No `ml/dl/rag` nesting; inline `#tags` effectively unused (all tagging is YAML).

Rough buckets:

- **Domain** (Trees): `deeplearning`, `learningEngineering`, `stats`, `linearalgebra`, `programming`, `library`, `python`, `c++`, `irt`, `astrology`, acronyms like `MoE`, `DKT`, `MCP`, `CoT`.
- **Source type** (Seeds): `source`, `article`, `research`, `book`, `quote`, `textbook`, `slidedeck`, `youtube`, `video`, `webClipping`, `BotChat`, `workNote`, `conversation`, `documentation`, `Webpage`.
- **Entity type**: `person`, `company`, `organization`, `initiative`, `tool`, `dataset`, `knowledgeGraph`, `fund`.
- **Project context**: `mountain`, `projectManagement`, `RenPhil`, `EngHub`, `AIED`, `eedi`, `project`, `check-in`, `adviceRequest`, `dailyNote`.
- **Identity/DEI** (Literature only, stored as booleans not tags): `woman_or_nb_author`, `disabled_author`, `lgbtqia_author`, `global_majority_author`, `own_physical_copy`.

---

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

- Folder placement is cosmetic. **`kind:` is truth** for `Meridian.base`.
- `parent:` and `project:` hold wikilink arrays — `parent` walks up one level, `project` pins to the top-level Mountain.
- Inheritance of `parent`/`project` is done by QuickAdd macros at `_src/_QuickAdd/qa_inherit_slope.js`, `qa_store_parent.js`, etc.
- **Status enum**: `Unprocessed, Backlog, Unstarted, In-Progress, Researching, Outlining, Drafting, Editing`. Ad-hoc `Completed` appears in the wild but isn't in the template dropdown.
- **Priority**: `High, Medium, Low`.

---

## Frontmatter schemas (quick reference)

### `kind:` vs `content_type:` — two fields, two roles (intentional)

Both are type-of-note fields that coexist on Seeds by design, not drift. Decision recorded 2026-04-22:

- **`kind:`** is the **project-management field**. Drives `Meridian.base` and every structural Base. Values span the full vocabulary: `Research`, `Article`, `Book`, `Quote`, `BotChat`, `Slide Deck`, `Textbook`, `Conversation`, `Mountain`, `Slope`, `Trail`, `Step`, `Idea`, `Bug`, `Document`, `Webpage`. **Always list form** (`kind:\n  - Research`) per the 2026-04-22 schema decision. List form supports both `== ["X"]` and `.contains("X")` Base queries.
- **`content_type:`** is a **general source-medium refinement** on Seeds. Narrower enum: `Article`, `Research`, `Book`, `Quote`, `BotChat`, `Slide Deck`, `Textbook`, `Conversation`. Scalar form (plain string). Used by content-specific Bases like `TBR Research.base`. Not PM-bearing.

For a Research Seed, both are set: `kind: [Research]` (structural) + `content_type: "Research"` (source medium). The duplication is intentional — the two fields serve different Bases and different queries.

### Fields per note type

**Universal (every note):** `aliases`, `tags`, `topics`, `created`, `last_updated`. (`topics` absent in Basic Template but present nearly everywhere in the wild.)

**Trees (concept notes):** universal + `reference_link` (often empty).

**Seeds/Sources/\***: universal + `icon`, `content_type` (`Article|Research|Book|Quote|BotChat|Slide Deck|Textbook|Conversation`), `reference_link`, `author: ["[[Firstname Lastname]]"]`, `title`, `subtitle`, `year`, `publisher_platform`, `processed: bool`, `read: bool`, `annotated: bool`.

**Research seeds add:** `journal`, `doi`, `zotero_link`, `in_zotero: bool`, `complete: bool`, `due`, `pdf: "![[Author - Year - Title.pdf]]"`, `annotation-target`.

**Articles add:** `cover_image`, `published`, `description`, `web_clipping: bool`, `word_count`, `kind`.

**Books (Literature) add:** `cover_image`, `genre-mood`, `description`, `isbn`, `page_count`, `publisher`, `source` (Kindle/Hardcover/Paperback), `woman_or_nb_author`, `disabled_author`, `lgbtqia_author`, `global_majority_author`, `own_physical_copy` (DEI metadata as booleans).

**Mountains hierarchy** (`Mountain|Slope|Trail|Step|Idea|Bug|Document`): universal + `icon`, `kind`, `status`, `priority`, `due`, `parent`, `project`, `complete: bool`. Mountain-only: `organization`, `description`. **No `cover_image:` field** on PM-hierarchy items (decision 2026-04-22 — PM items don't need covers; field removed from 45 notes that had it empty).

---

## Cross-references

- **Librarian role, operations, duties** — `librarian-role.md`
- **Vault identity, folder layout, entry points** — `librarian-vault-structure.md`
- **Bases, plugins, YOLO config** — `librarian-tooling.md`
- **Drift, writing rules, lessons learned** — `librarian-writing-rules.md`
