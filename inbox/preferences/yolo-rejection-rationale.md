---
observed: 2026-05-11
source-session: sandboxed_claude — Hypatia Phase 0 librarian migration
candidate-type: preference
confidence: high
status: new
---

## What I observed

AJ rejected using the Obsidian YOLO plugin alongside Hypatia: "I don't think
I'm going to use the YOLO extension with Hypatia. She should replace YOLO
(which also doesn't do what I want because it basically works as a SQL
query generator)." Came up unprompted during the Phase 0 librarian-protocol
migration, when she noticed I had drafted YOLO as a "future tuning target"
in `librarian-tooling.md`.

## How I'd codify it

**Preference**: AJ rejects vault-side LLM tooling that operates as a
query-generator over a vector DB. She wants an actual librarian — semantic
curation, ingest workflows, lint, schema enforcement, graph maintenance —
not retrieval ranking.

**Pattern**: when evaluating vault tools, the question to ask is "does this
do librarian work?" not "does this query the vault?" Anything that's
primarily a retrieval/query layer fails her bar. Tools that *file*,
*cross-reference*, *flag drift*, and *maintain the graph* pass.

**Design implication (codifies as)**: Hypatia is THE vault's LLM
substrate. Not an alongside-YOLO assistant. Not a vault-CLI tool that the
YOLO plugin can call. The runtime — Roo Code + local Ollama models —
replaces the YOLO Obsidian plugin entirely.

## Confidence rationale

High. Explicit rejection with stated rationale ("basically works as a SQL
query generator"). Came unprompted — surfaced naturally when AJ saw the
YOLO section in my draft, not in response to a leading question. Consistent
with her general framing of Hypatia as a "zettelkasten PKB partner," not a
"vault search tool."

## Related captures

(First on this topic. May later relate to captures about
retrieval-vs-curation distinctions in other tool evaluations.)
