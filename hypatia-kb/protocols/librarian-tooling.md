# Librarian — Tooling

**Purpose**: Inventory of vault tooling — Bases (what's load-bearing), the Obsidian plugin stack, and the YOLO plugin's current state. Hypatia uses this when reasoning about query side-effects, schema changes, plugin behavior, or when the user asks "what's running in the vault?"
**Last Updated**: 2026-05-11
**Trigger Keywords**: Bases, plugin, plugin stack, YOLO, Obsidian, Meridian, Templater, QuickAdd, Dataview, citation, citation plugin, web clipper, RAG, embedding, vector, vector DB

---

## Bases — what's load-bearing

### Inventory (7 files)

| Path | Filter | Purpose |
|---|---|---|
| `Bases/Meridian.base` | `!kind.isEmpty` | 25 views — PM spine |
| `Bases/Articles Base.base` | `file.tags.contains("article")` | Articles cards |
| `Bases/Books Base.base` | `file.tags.contains("book")` | Books TBR + all |
| `Bases/Code Libraries.base` | `file.hasTag("library")` | Python + all libs |
| `Bases/TBR Research.base` | `content_type == "Research"` | Unread/Read papers |
| `Seeds/Sources/Research/Research Base.base` | `file.hasTag("research")` | (duplicate-ish) |
| `Trees/Programming/Libraries/pytest documentation.base` | `file.hasTag("pytest")` | pytest index |

### Load-bearing fields — never rename without grepping

- **`Meridian.base`**: `kind, parent, project, due, complete, priority, status`
- **Content bases**: `cover_image, is_read, processed, annotated, title, author, year, content_type, read, created, last_updated, topics`
- **Tag membership**: `article, book, library, python, pytest, research`

`Meridian.base` has formulas `days_until_due` and `due_status` (🔥 Overdue / 🧊 Later etc). 25 views grouped as Project-scoped (`list(project).contains(this)`), Parent-scoped (`list(parent).contains(this)`), and Global (`All Mountains`, `Today`, `This Week`, `Cleanup`).

---

## Obsidian plugin stack (enabled community plugins)

| Plugin | Role | Key config |
|---|---|---|
| `yolo` v1.5.5.7 | Local-LLM assistant (main tuning target — see § YOLO below) | `.obsidian/plugins/yolo/data.json` |
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

**Core plugins enabled**: file-explorer, search, switcher, backlink, tag-pane, properties, daily-notes, templates, note-composer, command-palette, editor-status, file-recovery, **bases**. Disabled: graph, canvas, outgoing-link, page-preview, bookmarks, outline, sync, publish, webviewer.

**Web Clipper** (browser extension, templates live in `_src/_webclipper/`):
- `article-template-clipper.json` → `Seeds/Sources/Articles`
- `guardian-template-clipper.json`
- `website-template-clipper.json`
- `youtube-template-clipper.json` → `Sources/YouTube` (⚠ path drift — should be `Seeds/Sources/YouTube`)

---

## YOLO — being replaced by Hypatia

Per (2026-05-11), Hypatia replaces the Obsidian YOLO plugin as the vault's in-Obsidian LLM substrate. YOLO operates primarily as a SQL/vector-query generator over the vault DB — not as a librarian. Hypatia (running in Roo Code against local Ollama models) takes over curation, ingest, query, and lint.

**Artifacts in the vault during transition** — present today, deprecating:

- `_src/_YOLO/` — plugin runtime + skill definitions + 1.28 GB vector DB (gitignored). Inherit what's useful (skill prompts, system instructions) into Hypatia's protocol stack; let the rest decay.
- `_src/_meta/{anti-patterns, preferences, patterns, reasoning}.md` — Nathaniel-mimicry intelligence stores from the YOLO experiment. **Not authoritative for Hypatia.** Hypatia's stores live in `hypatia-kb/Intelligence/` (and the inbox-capture pipeline feeds them).
- `.obsidian/plugins/yolo/` — plugin config (4 agents, RAG, embeddings). Safe to leave installed during transition; safe to remove once Hypatia is fully wired.

**Implication for librarian work**: don't tune YOLO config. Don't propose YOLO-side fixes (dormant skills, unscoped RAG indexing, `chatModels[].toolType: "none"` clamp). If a vault task surfaces a YOLO issue, note it for the transition rather than treating it as a bug to fix.

---

## Cross-references

- **Librarian role, operations, duties** — `librarian-role.md`
- **Vault identity, folder layout, entry points** — `librarian-vault-structure.md`
- **Note schemas, naming, tags, Mountains hierarchy** — `librarian-note-schemas.md`
- **Drift, writing rules, lessons learned** — `librarian-writing-rules.md`
