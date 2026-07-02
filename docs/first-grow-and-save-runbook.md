# First conformant grow + first save — step-by-step runbook

2026-07-02. The last two Phase 1.5 boxes. Everything here happens on AJ's
Mac; Hypatia does the work, AJ reviews and executes the one script she
can't. Written in extreme detail on purpose — this is the first time the
full contract runs end to end.

---

## Part A — Preconditions (2 minutes)

1. **Keep-alive is active** (kills the 2-minute mid-session stalls):

   ```bash
   ollama ps
   ```

   After any recent Hypatia reply, the `UNTIL` column should read ~1 hour
   out. If it says ~4 minutes, run `launchctl setenv OLLAMA_KEEP_ALIVE 1h`,
   quit the Ollama menu-bar app, reopen it.

2. **Fresh terminal session on the full model** (NOT the Obsidian sidebar —
   the terminal session launches from the repo/vault parent so she can
   reach both, and pins the 12B + freshest kernel):

   ```bash
   hypatia
   ```

   The launcher pre-flights the shim, the model, and regenerates the
   recipe from the kernel. Wait for the greeting (~20–40s, one-time load).

3. **The Seed is planted**: you have read and annotated
   `Seeds/Sources/Articles/Prompt Injection as Role Confusion.md`. Growing
   follows planting; that's the division of labor.

## Part B — The grow (15–30+ minutes, mostly hands-off)

Paste this to her **verbatim**:

> Grow the Seed at /Users/ajsscott/GitHub/other/TabulaJacqueliana/Seeds/Sources/Articles/Prompt Injection as Role Confusion.md. Load protocol://assistant-ingest first and follow all six steps: atomic Trees, one per concept; create the ^cite anchors in the Seed for every passage you embed; update the graph edges in Trees/index.md, Trees/log.md, and related Trees' topics; and finish with the Seed-side closure — grown: true and the Seed's topics updated with every new Tree. An aggregate Tree from an earlier attempt exists at Trees/Machine Learning/Prompt Injection Interaction Reasoning.md; propose whether to split or replace it before changing anything.

**What you should see, in roughly this order** (tool cards in the terminal):

1. `read_protocol: protocol://assistant-ingest` (possibly also
   `librarian-note-schemas`, `librarian-role` — multiple loads are correct)
2. `read_text_file` on the Seed
3. A **proposal about the aggregate Tree** — she should ASK before
   changing it (Failure discipline + Route D). Answer her.
4. `edit_file`/`write_file` on the **Seed** — adding `> [!quote]` callouts
   ending in `^cite-<6chars>` anchors for the passages she'll embed
5. `write_file` × N — the atomic Trees (expect roughly 3–8 for this
   article; her own summary named 4+ concepts)
6. Edits to `Trees/index.md`, `Trees/log.md`, and `topics:` of related
   Trees (e.g. the existing RAG/agentic-AI Trees if she links them)
7. Seed frontmatter closure: `grown: true`, `topics:` gains every new Tree
8. Her step-6 report: `Ingested / Seed / Trees drafted: N / Edges updated /
   Conflicts / Suggested next`

**Timing:** each tool round-trip is a full model turn at ~14 tok/s; the
whole grow may run 15–30+ minutes. Start it and walk away. If a single
turn exceeds ~15 minutes with no tool activity, tell Claude (with the
terminal contents) rather than force-killing.

**Interruptions are safe**: nothing here is destructive; the worst case
is a half-finished grow you review and have her continue.

## Part C — The review (yours; this IS the milestone)

Open Obsidian. Four tells, in order of importance:

1. **Embeds render.** Open each new Tree. Every `![[...#^cite-...]]`
   must show the quoted Seed passage — a grey "unable to find" box means
   she embedded an anchor she never created Seed-side. That fails the
   citation contract; have her fix Seed-side first.
2. **Trees are atomic.** One idea per note. A Tree whose body covers
   "role confusion AND spoofed thoughts AND benchmark gaps" is an
   aggregate — have her split it. But also: no filler notes padding the
   count (fewest atomic notes that capture all concepts).
3. **Graph edges exist.** `Trees/index.md` has the new entries;
   `Trees/log.md` has an ingest row with timestamp + source + paths;
   at least the obviously-related existing Trees gained `topics:` links.
4. **Seed-side closure.** The Seed's frontmatter shows `grown: true`,
   and its `topics:` lists every new Tree (with your original entries
   intact). `planted:` untouched — that flag is yours.

**Reject without hesitation**: heading embeds (`![[seed#Some Heading]]` —
Pattern B, fragile), invented frontmatter fields, CamelCase filenames
(Trees are Title Case with spaces), confident claims without receipts.

**Iterating**: corrections go to her in the same session, one at a time —
"Split [[X]] into one Tree per concept" / "The embed in [[Y]] doesn't
render; create the anchor in the Seed first." Her memory of the grow is
the session, so finish the review before quitting.

When all four tells pass: the first-real-grow milestone is DONE.

## Part D — The first save

**How save actually works** (important): Hypatia has no shell — by design
(`developer` extension stays out of her sessions). The save flow is
therefore split: **she drafts the ops file; you execute the script.** This
is the designed contract (`save-session.py` docstring: "The save command
writes an ops file; this script executes the mechanical operations").

1. In the same session, after the review passes, say:

   > Save this session. Follow protocol://detail/save. You cannot run
   > scripts — write the ops file to
   > /Users/ajsscott/GitHub/other/The-Hypatia-Protocol/_save_ops_session-2026-07-02-001.json
   > and tell me when it's ready; I will execute the save script myself.

2. **What she should write** (SAVE MODE — the inbox boundary forbids new
   store entries at save time):

   ```json
   {
     "session_id": "session-2026-07-02-001",
     "session_index_entry": {
       "id": "session-2026-07-02-001",
       "date": "2026-07-02",
       "tags": ["ingest", "grow", "promptInjection"],
       "summary": "First conformant grow: Prompt Injection as Role Confusion → N atomic Trees",
       "outcome": "completed",
       "outcome_note": "..."
     },
     "memory_updates": { "snapshot": {} }
   }
   ```

   If she includes `new_patterns` / `new_knowledge` / `new_reasoning`,
   that violates the inbox boundary — have her remove them (captures
   belong in `inbox/preferences/`, promoted only by you at maintenance).

3. **Dry-run first, then execute** (your terminal, repo root):

   ```bash
   cd /Users/ajsscott/GitHub/other/The-Hypatia-Protocol
   uv run python scripts/save-session.py --dry-run _save_ops_session-2026-07-02-001.json
   uv run python scripts/save-session.py _save_ops_session-2026-07-02-001.json
   ```

   Exit codes: 0 = full success, 1 = partial (read the output — it names
   which store failed), 2 = total failure.

4. **Verify** (all three should pass):

   ```bash
   uv run python scripts/validate-schemas.py
   python3 -c "import json; d=json.load(open('hypatia-kb/Memory/session-index.json')); print('sessions:', d['stats']['totalSessions'], '| first:', d['sessions'][0]['id'])"
   git log -1 --format='%an <%ae> — %s'
   ```

   Expected: schemas green; `sessions: 1 | first: session-2026-07-02-001`;
   the commit authored by `Hypatia <hypatia@local>` (Q-08 — the script
   sets the git identity itself).

**If she can't produce a valid ops file** after one or two corrections:
don't fight the model. Save her attempt(s) verbatim, write the ops file
yourself from the template above, run the script, and hand the transcript
to Claude — it becomes the requirements spec for the Phase 2 save-session
MCP server (the eval already showed the model *wants* a `save_session`
tool; this is the evidence for building it).

## Part E — Closing the phase

Both milestones done = **Phase 1.5 complete**. Aftermath:

```bash
cd /Users/ajsscott/GitHub/other/The-Hypatia-Protocol
git log --oneline -5        # the save commit + your session's history
```

Tell Claude the outcome (including anything Hypatia fumbled — fumbles are
Phase 2 requirements, not failures). Phase 2 opens with the vault-rw MCP
server (schema-aware vault ops, tight boundary restore) and the
save-session MCP server if the transcript argues for it.
