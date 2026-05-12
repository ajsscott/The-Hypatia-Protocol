# Assistant — Ingest

**Purpose**: How Hypatia triages a new incoming source (PDF, article, web clipping, Claude Code capture, manual paste) into the TabulaJacqueliana vault. The atomic operation is `source-in-Seeds/ → atomic Tree note(s) with citation embeds`. This protocol is the orchestration layer; the schemas, naming, and link contracts live in `librarian-note-schemas.md`.
**Last Updated**: 2026-05-12
**Trigger Keywords**: ingest, file source, process source, intake, onboard source, capture Seed, new source, file PDF, file article, drop in

---

## When this fires

The Scholar drops a new source into the vault (or, in Phase 2, a watcher detects one) and signals "process this." Typical openers:

- "Ingest this paper."
- "File this article."
- "Process this Seed."
- "Drop this in." (with attached PDF / link / pasted content)
- Phase 2: a Claude Code capture lands in `~/Desktop/claude-captures/`; the watcher invokes ingest with `source_type=claude_capture`.

If the trigger fires without an attached source, ask: *"Which source?"* Do not invent one.

---

## The ingest flow

Six steps. Each step is concrete; no implicit "etc."

### 1. Identify and classify the source

Determine `content_type` per `librarian-note-schemas.md § Frontmatter schemas`. Common cases:

| Source | content_type | Where it lands |
|---|---|---|
| Academic paper / preprint | `research` | `Seeds/Sources/Research/` |
| Web article / blog post | `article` | `Seeds/Sources/Articles/` |
| Book chapter | `book` | `Seeds/Sources/Literature/` |
| Podcast / video transcript | `transcript` | `Seeds/Sources/Transcripts/` |
| Claude Code session capture (Phase 2) | `claude_capture` | `Seeds/Sources/Captures/` |
| Personal note / memo | `memo` | `Seeds/Sources/Memos/` |

If the source doesn't match a known type, surface ambiguity to the Scholar before proceeding.

### 2. Create or update the Seed note

Place the source file (PDF, .md, transcript) under the appropriate `Seeds/Sources/<type>/` folder. Create a matching `.md` Seed note with the canonical frontmatter for that `content_type` (see `librarian-note-schemas.md`).

Required for every Seed:

- `aliases`, `tags` (flat lowercase camelCase), `topics` (wikilinks to relevant Trees), `created`, `kind: Seed`, `content_type: <type>`, `citekey` if a citable work.
- Type-specific fields per schema (`journal`, `doi`, `zotero_link`, `cover_image`, `published`, `genre-mood`, `isbn` as applicable).

If a Seed already exists (Scholar dropped a duplicate or update), update frontmatter and append source notes rather than creating a second file.

### 3. Read the source

Read the Seed body. If the Seed references a PDF / video / external resource, read or fetch that too (subject to `.roo/rules-hypatia/09-security.md` external-content rules).

Form a working understanding sufficient to draft atomic notes. If the source is long (book, paper > 30 pages), surface that to the Scholar — *"This is a 60-page paper; should I distill the whole thing or focus on a specific section?"* — before drafting.

### 4. Draft atomic Tree note(s)

Per `librarian-note-schemas.md § Canonical atomic Tree note`, draft one Tree note per atomic concept the source contributes. **Atomic = one idea per note.** A single source may produce 3-15 Tree notes; that's the pattern, not bloat.

Each Tree note:

- Lives under `Trees/<domain>/` (domain inferred from content + existing taxonomy).
- Frontmatter: `aliases`, `tags`, `topics` (wikilinks to related Trees), `created`, `kind: Tree`, `content_type` (often empty; sometimes `concept`, `definition`, `pattern`).
- Body: a paragraph or two of prose + one or more `^cite-*` block-ref embeds back to the Seed.
- Block-ref embeds are the citation contract — not section-heading embeds (those are fragile per `librarian-writing-rules.md § landmine`).

### 5. Update graph edges

For every newly-drafted Tree:

- Add its wikilink to the `topics:` field of related Trees the Scholar will recognize (peer concepts, parent concepts).
- Update `Trees/index.md` (content catalog) with the new entry.
- Append an `ingest` operation row to `Trees/log.md` with timestamp, source, list of new Tree paths.

If the new content **contradicts or supersedes** an existing Tree, flag the conflict to the Scholar at save time. Do not silently overwrite.

### 6. Surface output to the Scholar

End the ingest with a single concise message:

```
Ingested: <source>
Seed: <path>
Trees drafted: N
  - <path> [<one-line synthesis>]
  ...
Edges updated: M Trees in topics:
Conflicts: <none | N flagged>
Suggested next: <save | continue with another | ingest related source>
```

The Scholar reviews; ingests may require iteration. Treat each ingest as one editable artifact, not a fire-and-forget action.

---

## Multi-source triage (Phase 2)

When the Phase 2 watcher (`scripts/hypatia-watcher.py`, not yet written) queues multiple captures at once, do not bulk-ingest. Process one at a time. For each:

1. Surface the queued source(s) to the Scholar at session start.
2. Confirm intent — *"Three Claude captures queued. Process all, or pick?"*
3. Process per the six-step flow above.

Watcher captures often arrive without explicit `content_type`; infer from path + content and confirm with the Scholar before committing the Seed schema.

---

## What ingest does NOT do

- **Does not** promote anything to `hypatia-kb/Memory/memory.json` or `hypatia-kb/Intelligence/*.json`. Those stores grow only through deliberate consolidation; see `librarian-memory.md § What does NOT get saved`.
- **Does not** auto-commit. Save is a separate step (`.roo/rules-hypatia/08-save-command.md`).
- **Does not** delete or move the original source file from where the Scholar dropped it (only adds Seed metadata + new Tree files).
- **Does not** synthesize across multiple Seeds in one ingest. Cross-Seed synthesis is a separate `query` operation.

---

## Cross-references

- **Role definition (where ingest fits in the three operations)**: `librarian-role.md`
- **Frontmatter schemas + naming + tag taxonomy**: `librarian-note-schemas.md`
- **Block-ref embed contract + linkage rules**: `librarian-note-schemas.md § Seed → Tree linkage`
- **Atomic-note principle + split heuristics**: `librarian-writing-rules.md`
- **Save flow (what happens after ingest)**: `.roo/rules-hypatia/08-save-command.md`
- **External content security (fetching, vault Seeds, web clippings)**: `.roo/rules-hypatia/09-security.md`
