# Librarian — Writing Rules, Drift, and Lessons

**Purpose**: The operational guardrails for Hypatia when editing the vault. Covers known drift/landmines that bound refactors, active initiatives, the rules for drafting + approval + commits, lessons learned from prior errors, and the update protocol for this directory itself.
**Last Updated**: 2026-05-11
**Trigger Keywords**: drift, landmine, refactor, guardrail, write, edit, commit, approval, batch, sample, verify, lesson, error, prior incident, atomic commit, link rot

---

## Known drift / landmines (refactor guardrails)

Only active items. Resolved items have been removed from this list (see vault commit history for resolution details — search for `lint:` or `fix:` commits).

### HIGH

- **Tag casing drift**: `learningEngineering` (73) vs `learningengineering` (22). Same for `c++`/`C++`, `project`/`projects`. Any Bases filter on the canonical spelling silently drops the drifted files. Fix via Obsidian's `tag-wrangler` plugin (GUI-only).
- **Section-heading embeds** (~50 Tree files) carry literal source markdown including `**bold**` syntax — any heading typo-fix in a Seed breaks dependents. No link-audit runs. Convert to block-ref `^cite-*` embeds as you touch their Seeds.
- **Empty Tree stubs**: 40% of `Trees/` notes (~209 files) have empty bodies. Mix of stub-being-filled vs abandoned. One empty stub (`Trees/Unprocessed/MS Data Science/Classes/DATA622 ML/Neural Networks.md`) absorbs 15 inbound wikilinks because Obsidian resolves ambiguous basenames to first match.

### MEDIUM

- **Basename collisions** `Trees/Unprocessed/` vs `Trees/` proper — 7 pairs: `Dunder Methods`, `Iteration`, `Python Native Data Structures`, `Recursion`, `User-Defined Classes`, `User-Defined Functions`, `Variables`. `[[Variables]]` resolves to whichever Obsidian picks first. Tracked in `[[Trees Unprocessed Refactor Plan]]` Pass 2.
- `Trees/Unprocessed/` has 147 broken wikilinks pointing to notes that exist nowhere in the vault.
- `Seeds/Sources/Research/` has 235 `.md.bak` files from a prior rewrite. Gitignored ✓ (local clutter only).
- **No "All Documents" or "Project Documents" `Meridian.base` view** despite `Document` being a `kind`.
- **YOLO**: `chatModels[].toolType: "none"` — verify at runtime whether this clamps the per-agent tool configs (agents look tool-capable in config, but provider-level "none" may block them). Gates all other YOLO work.
- **YOLO skills written** (9 total: 4 original + 5 Nathaniel-mimicry); need UI wiring per agent (YOLO overwrites external edits to `data.json`).
- **YOLO RAG indexing unscoped** — PDFs + `_attachments` + `_src` all indexed; 1.28 GB vector DB. Needs UI exclude globs.

### LOW

- `workspace.json` has a `smtcmp-chat-view` pane leftover from an uninstalled Smart Composer plugin. (`workspace.json` is YOLO-auto-written; may resolve itself on next layout save.)
- `Trees/Machine Learning/Algorithms/dai_transformer-xl_2019.md` — a Research seed sitting in `Trees/`. Move to `Seeds/Sources/Research/`.
- `Bugs/Ideas` folders under `Mountains`: `Bugs` has 1 file, `Ideas` doesn't exist.

---

## Active initiatives

Full scope + open decisions live in the planning Documents (linked from each Slope). This section is just pointers. **Re-verify against `Meridian.md` for current state — this list may have drifted since last update.**

| Slope | Status (snapshot) | Planning Document |
|---|---|---|
| `[[Trees Unprocessed Refactor]]` | Unstarted — 8 decisions pending | `[[Trees Unprocessed Refactor Plan]]` |
| `[[YOLO Nathaniel Mimicry]]` | **Descoped 2026-05-11 (Q-23)** — superseded by Hypatia build; YOLO being replaced as vault LLM substrate | `[[YOLO Nathaniel Mimicry Report]]` |

See `[[Meridian]]` for the full PM dashboard.

---

## Writing rules

### Default to drafting

This role flips the typical "user-authors" default. Propose writes freely; the harness `ask` permissions give the user a per-write veto. If a request could resolve as either a full diff or a verbal summary, give the diff.

### Approval granularity (decided 2026-04-22)

**Batched approval** for deterministic scripted work — one prompt covers many files. Qualifies when:
- (a) the transformation is pure find-and-replace with a regex/pattern that can be shown
- (b) the affected file count can be stated beforehand
- (c) the pattern can be verified on 2-3 samples before running

Examples: `Topics:` lowercase pass; the 2026-04-22 `kind:` list-form migration (124 files, 1 approval).

**Per-file approval** for judgment-heavy work. Qualifies when the right answer depends on reading the note's context. Examples: merging duplicate YAML keys with different values, splitting composite notes into atomic zettels, choosing target paths for lifted notes, any content rewrite.

**Before batching, always pre-verify** with a grep sample. The 2026-04-21 `kind:` backfill incident (249 files broken) happened because agent-summarized counts were trusted without sample inspection. Never skip the pre-verify step.

### Content rules

- **One concept per Tree note.** If a draft would have two `## Sections` about distinct ideas, that's two Trees, not one.
- **Use the canonical April-2026 atomic Tree schema** (see `librarian-note-schemas.md` § Canonical atomic Tree note). Preserve `created` if present; always set/refresh `last_updated` to the current `YYYY-MM-DD HH:mm`.
- **Use block-ref embeds, not heading embeds**, for new work. `![[<citekey>#^cite-<anchor>]]` is the durable form. Heading embeds (`#Section Name`) are fragile to source rewrites; only use them when the source has no block anchors and adding them is out of scope.

### Rename rules

- **Never rename a file** without first grepping `[[<basename>]]` and `![[<basename>` across the vault. Link rot is silent in Obsidian.
- **Never rename a frontmatter field** without checking `Bases/` files — `kind, parent, project, due, complete, priority, status, cover_image, content_type, read, processed, annotated, is_read, title, author, year, topics` are load-bearing. Adding new fields is fine; renaming or removing existing ones requires updating Base filters too.

### Format rules

- **Honor `obsidian-linter`** — it runs on save inside Obsidian and will reformat. Write what it expects: multi-line `tags`/`aliases`/`topics` arrays, Title Case headings, `created`/`last_updated` as `YYYY-MM-DD HH:mm`. Don't fight the linter; align with it.

### Commit + branch rules

- **Atomic commits.** One concept per commit. Imperative-mood message explaining *why*, not *what*. `ingest: add Adaptive RAG Tree from du_2026` not `add files`.
- **Auto-commit every 15 min via `obsidian-git`.** Assume any write will be committed within the quarter-hour. Good: always recoverable via git. Bad: don't batch unrelated changes within a 14-min window without pausing — the auto-commit will lump them.
- **`work-safe` branch excludes `Seedlings/` and `Forests/`.** Don't try to read files in those folders when on this branch.
- **Append to `Trees/log.md`** after every ingest, lint, refactor, merge, split, delete, or significant query-filed-back.

---

## Lessons learned from prior errors

- **Don't sed multi-line YAML structures.** YAML keys whose values span lines (lists with `-` items, multiline strings, nested objects) cannot be safely transformed line-by-line. The 2026-04-21 attempt to backfill `kind:` on 249 Research seeds with `sed 's/^kind: *$/kind: Research/'` caught only the first line; the orphaned `  - Research` list items below produced invalid YAML on all 249 files. Use a YAML-aware tool (Python with PyYAML, `yq`) for any multi-line YAML edit, or hand-edit per file.
- **`^Pattern:` is a YAML key only inside the frontmatter block.** Markdown body content can also start lines with `Word:` — e.g., interview agenda labels (`Topics: SQL Paired Programming`), section headers, definition lists. Anchor any sed/grep YAML edit to the frontmatter `---` … `---` boundaries (e.g., `awk '/^---$/,/^---$/'` to extract). The 2026-04-21 Topics: lowercase pass over-replaced 5 inline occurrences in `Trees/Unprocessed/Job Search/Braze Interviewers.md`. Reverted.
- **Verify agent-summarized counts and structures before scripting destructive operations.** A 30-second `grep -A1 <pattern> <sample>` beats a 249-file revert. The earlier codebase-analysis subagent reported "blank `kind` on ~25/30 Research seeds" — actual state was list-form on 249 of 298. The summary was qualitatively misleading; only direct inspection revealed the structure.
- **Duplicate YAML keys masked by capitalization can become real conflicts when normalized.** Four files (`Hotkeys.md`, `Chain-of-Thought Prompting.md`, `Objects.md`, `fernandezDiVERTDistractorGeneration2024.md`) had pre-existing `Topics:` AND `topics:` as separate keys. Lowercasing one creates a YAML duplicate-key conflict with the other. Resolution requires merging the two values (a list union), not lowercasing alone.

---

## Update protocol for this directory

When vault conventions change meaningfully — a new canonical note schema, a new load-bearing Base, a resolved landmine, a new plugin, a refined operating pattern, a new lesson — update the relevant section in the relevant `librarian-*.md` file here. Don't let these files drift; stale librarian protocols are worse than none. The schema co-evolves with the wiki (per `llm-wiki.md`); both belong in the same git history.

When a landmine resolves, **remove it from `librarian-writing-rules.md § Known drift`** and note the resolution in the commit message. When a new convention emerges, **add it to `librarian-note-schemas.md`** alongside the existing schemas.

---

## Cross-references

- **Librarian role, operations, duties** — `librarian-role.md`
- **Vault identity, folder layout, entry points** — `librarian-vault-structure.md`
- **Note schemas, naming, tags, Mountains hierarchy** — `librarian-note-schemas.md`
- **Bases, plugins, YOLO config** — `librarian-tooling.md`
