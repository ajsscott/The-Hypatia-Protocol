# Plugin architecture lessons — Claudian, YOLO, Smart Connections, Note Companion

2026-07-02. Source-level analysis of four Obsidian AI plugins (shallow clones
in repo root, gitignored), mined for patterns that make Hypatia more
efficient on a local 12B model. Each section: the pattern, who proved it,
and what Hypatia does about it.

The headline: **three of the four independently converge on the same
doctrine — never inline what can be pointed to.** Claudian sends the current
note as a *path* once per session, not its body. YOLO injects skill *names*
and file *outlines*, loading bodies via tool call. Smart Connections hands
chat only user-curated result keys. Hypatia's Q-33 kernel redistribution is
the same doctrine — validated. The upgrades below extend it to the places we
haven't applied it yet.

---

## Tier 1 — direct efficiency wins (days)

### 1.1 Trim the tool-schema payload (YOLO's biggest local-model lesson)

YOLO sends *stubs* for rarely-used tools (name + one-liner, permissive
schema) and a `load_tool_schemas` tool to fetch full schemas on demand
(`tool-selection.ts:223-328`, `tool-stub.ts`), keeping the prompt-cache
prefix small and frozen. Goose gives us a cruder but effective equivalent:
**every enabled platform extension injects its tool schemas into every
turn.** Our sessions carry `todo`, `apps`, `summon`, `extensionmanager`,
`tom`, `skills`, `developer` schemas — most unused by Hypatia. That's a
chunk of the ~5K non-kernel overhead in the 10k first-turn prefill.

**Action:** disable unused platform extensions in `~/.config/goose/config.yaml`
for now (`apps`, `summon`, `extensionmanager`, `tom`; keep `todo` — it maps
onto AJ's PM use case — and `skills` pending §1.2; `developer` stays off in
recipe sessions already). Revisit per-session control when Goose supports it.

### 1.2 Protocols as Goose-native skills (investigate)

Goose 1.40 ships a `skills` platform extension ("Discover and provide skill
instructions from filesystem and builtins") — the same progressive-disclosure
shape YOLO implements (frontmatter `name`/`description` discovered cheap,
body loaded on demand; YOLO `liteSkills.ts:14-152`, also reads Claude-style
`SKILL.md`). If Goose's skills scan a configurable directory, a generator can
emit SKILL.md wrappers from `hypatia-kb/protocols/` and Hypatia gets *native*
protocol discovery alongside (or instead of) `read_protocol`.

**Action:** run `goose skills --help` + locate its scan dir; if viable, add
`scripts/gen-goose-skills.py` deriving skills from protocols (same pattern
as split-decision-routes.py). Decide read_protocol's fate on the evidence.

### 1.3 Context-discipline lines for the kernel substrate note (Claudian)

Claudian's system prompt earns its keep with a few cheap, specific rules we
lack (`mainAgent.ts:28-126`):
- **Time context**: "your training data is the past; ask the time tool for
  the present" — directly relevant to a local model with a stale cutoff.
- **Reference notes back to the Scholar as wikilinks** (`[[folder/note]]`)
  so they're clickable in Obsidian.
- **Read-linked-notes instinct**: "when reading a note with wikilinks,
  consider reading linked notes; they often contain related context."
- **Never dump whole notes into replies**; quote the relevant lines.

**Action:** add these to the substrate note the regen script emits (not the
kernel — they're substrate-flavored).

## Tier 2 — the ingest pipeline (AJ's #1 use case; steal Note Companion's shape)

Note Companion runs a fixed step pipeline per inbound file —
VALIDATE → EXTRACT → CLASSIFY → FORMAT → MOVE → RENAME → TAG — with
per-step gating, quarantine-by-error-class folders, and backup-before-modify
(`inbox/index.ts:331-443`, `1086-1150`). Its prompt patterns are directly
reusable:

- **Classification against a closed template list** with an empty-string
  no-match sentinel that aborts downstream steps cleanly
  (`classify1/route.ts`): "If the content does not clearly match any of the
  template types, respond with an empty string."
- **Candidate scoring schema** for folders/tags/titles:
  `{score: 0-100, isNew: boolean, value, reason}` — REQUIRED reason field,
  existing candidates preferred, sorted desc (`folders/v2/route.ts:14-49`,
  `tags/v2/route.ts:45-66`). Feed the model the *actual* vault structure,
  capped and prioritized (parent chain + shallow folders first, max 100 —
  `organizer-limits.ts:16-63`).
- **The atomize prompt** (`concepts-and-chunks/route.ts:20-38`): "Aim to
  split the document into the FEWEST atomic chunks possible while capturing
  all key concepts" — anti-over-splitting, exactly the Seed→Trees instinct.
- **Their mistakes, avoided:** fake confidence scores (hardcoded 100),
  non-durable in-memory queue, 1000ms write-settle debounce race, auto-move
  with no approval. Hypatia stays human-in-the-loop (matches the
  reading-raw-sources preference) and stages instead of auto-moving.

**Action:** enrich `assistant-ingest` (and `librarian-note-schemas` cross
refs) with the staged pipeline, scoring schema, no-match sentinel, and
atomize phrasing. The Phase 2 file-watcher crate later adopts the
event+durable-queue+quarantine design.

## Tier 3 — Phase 3 vectorstore, pre-validated

- **RRF fusion is convergent**: YOLO fuses vector + keyword + path lists via
  RRF k=60 (`hybridSearch.ts:84-144`) — the same fusion `kb_query.py`
  already implements. Ship ours as-is.
- **Retrieval as a TOOL, not auto-injection**: YOLO removed automatic
  per-turn RAG; the model calls `fs_search` with its own limit/threshold
  args. Wire `kb_query` as an MCP `search_vault` tool on our server; let
  Hypatia budget her own retrieval.
- **Dual granularity, block-level opt-in** (Smart Connections): note-level
  embeddings by default, block/heading-level behind a toggle
  (`connections_lists.js:241-247`).
- **Incremental via content hash + model versioning**: hash chunks
  (YOLO sha256/16, `VectorManager.ts:504`), stamp the embedding model, full
  re-embed on model change (SC's "Sources reimported after model changes").
- **Avoid SC's brute-force scan** (O(N) cosine per query, no ANN) — fine for
  its UX, wrong for tool-latency budgets.
- **Embedding model**: Ollama `/v1/embeddings` works (YOLO `ollama.ts:157-186`);
  `mxbai-embed-large` is already pulled on the Mini.
- **Carry scores + cite tags into results** (YOLO's `cite: N` links;
  SC's `{key, score}` payloads) so answers cite vault sources.

## Tier 4 — session mechanics (later, mostly Goose's job)

- **Summarize-and-restart compaction** (YOLO `compaction.ts`): fixed
  8-section summary (incl. ALL verbatim user messages), triggered at a
  token threshold, cache-prefix re-sent byte-identical. If Goose's own
  compaction underwhelms in long curation sessions, this is the reference.
- **History reconstruction with lossy truncation** (Claudian
  `utils/session.ts:50-240`): drop successful tool results (re-executable),
  keep failures at 500 chars, replace thinking with a placeholder.
- **Cheap-model side tasks** (Claudian title-gen; YOLO strips heavy features
  for lightweight calls): route titling/summaries to a small model (E4B
  candidate) instead of the main 12B.
- **Detached subagents with deny-list tool inheritance** (YOLO
  `subagent/`): no recursion, no UI tools, per-task model override.

## Boundary + safety patterns worth noting

- Claudian's approval rules: Bash requires explicit wildcards to allowlist;
  file rules use segment-aware path-prefix matching
  (`ApprovalManager.ts:60-130`) — reference for vault-rw's permission model.
- Claudian's excluded-tags list keeps private notes out of auto-attached
  context (`FileContext.ts:361-384`) — adopt for Hypatia's vault reads
  (e.g. a `#private` frontmatter/tag convention).
- Note Companion's frontmatter writes go through Obsidian's
  `processFrontMatter` API, never string surgery — vault-rw should use a
  proper YAML layer for the same reason.
