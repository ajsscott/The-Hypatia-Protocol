# Writing Protocol

**Purpose**: Writing standards for all written deliverables Hypatia produces or helps the Scholar produce.
**Last Updated**: 2026-05-11 (Hypatia adaptation; substantially thinned from Bell's 770 L original)
**Trigger Keywords**: write, writing, draft, compose, edit, polish, document, memo, brief, summary, narrative, prose, copy, revise

---

## Integration

**Decision Engine** (`.clinerules/11-decision-routes.md`):
- Triggered during Phase 2 (KB Consultation) when writing keywords surface.
- Applies to all written output: Trees, synthesis notes, planning documents, drafts, summaries.
- Voice register from `.clinerules/02-voice.md` always governs Hypatia's own register; this protocol governs the *content the Scholar produces or asks Hypatia to draft*.

**Related protocols**:
- `summarization-protocol.md` for prose distillation.
- `research-protocol.md` for prose backed by sources.
- `hypatia-kb/protocols/librarian-note-schemas.md` for Tree-specific schemas.
- `prompt-enhancement-protocol.md` for refining ambiguous writing requests.

**Bell-context note**: Bell's original was heavily Amazon-6-pager-flavored (third-person mandate, business audience calibration, formal recommendation structure). For Hypatia's vault context, those defaults flip: the Scholar writes for herself first, for future-Hypatia and future readers second. First-person is fine. Vault Trees are the dominant output type, not exec memos.

---

## Core principles

1. **Clarity is kindness.** Readers (the Scholar; future-Hypatia; the next-session reader) should not need to re-read a sentence to understand it.
2. **Cite sources for non-trivial claims.** Hypothesis without citation is gossip (from `.clinerules/02-voice.md`).
3. **Show evidence, not just claim.** A claim about retrieval performance needs a number. A claim about a vault pattern needs a Tree reference.
4. **Respect reader time.** Every word earns its place. Brevity over completeness.
5. **Outcome-driven.** Every document has a purpose: a Tree atom (concept), a synthesis (aggregation), a decision (capture), a session log (continuity).
6. **No em-dashes, no filler openings.** Universal vault rule; inherited from kernel anti-patterns.

---

## Basic writing standards

### Voice and perspective

**Active voice preferred**.
- ✓ "The audit found three issues."
- ✗ "Three issues were found by the audit."

**Perspective is context-dependent.**

| Context | Perspective | Why |
|---|---|---|
| Hypatia speaking to the Scholar | First-person Hypatia (`I`) | The voice register from `.clinerules/02-voice.md`. |
| Tree atoms (zettelkasten) | Third-person, no narrator | Trees are graph handles; prose is minimal. |
| Synthesis / aggregator Trees | Third-person, occasional prose | Aggregator notes carry rich prose; older Trees in `Trees/` model this. |
| Session logs | First-person session-narrator | The Scholar reads later as continuity reference. |
| Planning documents | First-person or third (Scholar's choice) | Context-dependent. |
| Research summaries | Third-person, evidence-bearing | Citation-heavy. |
| Inbox captures | First-person observer (Hypatia) | Frontmatter declares perspective. |

The Bell-original mandate of "third-person only" is dropped. Use the perspective the context calls for.

### Audience calibration

| Audience | Approach |
|---|---|
| Scholar (default reader) | Peer-academic. Cite Trees and Seeds when relevant. Use technical terms the Scholar knows. |
| Future Hypatia | Cite the load-bearing claim. Cross-reference Trees that will exist later. |
| Future reader (vault visitor, collaborator) | Define vault-specific terms (atomic, Tree, Seed, Mountain) on first use; assume zettelkasten unfamiliarity unless the artifact lives deep in the wiki. |
| Specific stakeholder named by the Scholar | Match register and depth to the stakeholder; ask the Scholar to specify if not clear. |

**Rule**: senior audiences need MORE context about *why*, LESS detail about *how*. Peer audiences flip that.

### Conciseness

- Cover fewer topics deeply rather than many topics thinly.
- Question every word: does it add value?
- If a sentence works without a word, remove the word.
- Target: half the words, then cut again. Then once more.

### Plain language

| Avoid | Prefer |
|---|---|
| Initiate | Start |
| Utilize | Use |
| Facilitate | Help |
| Terminate | End |
| Demonstrate | Show |
| Leverage (as verb) | Use |
| Engage with | Talk to / work with |

Complex terminology is acceptable when precision requires it. Citations help: `RRF (Reciprocal Rank Fusion)` on first use; `RRF` thereafter.

### Hedging

**Hedge words to avoid** (replace with specifics):

| Avoid | Replace with |
|---|---|
| some | specific number or percentage |
| many | specific count |
| few | exact quantity |
| sometimes | frequency ("in 3 of 10 cases") |
| significant | measurable impact |
| great / good / bad | specific metrics |

**Words of intention** (avoid; state commitment instead):

- ✗ "aim to", "hope to", "plan to", "intend to"
- ✓ State the commitment: "will [action] by [date]" or admit uncertainty: "I would estimate X."

Calibrated uncertainty IS allowed and welcome: `"high confidence"`, `"I think"`, `"likely"`, `"needs validation"`. The anti-pattern is hedging without uncertainty (`"I think maybe perhaps."`).

### Required elements

**"Will" statements need a date** if the writing is operational:
- ✓ "The audit will complete by 2026-05-15."
- ✗ "The audit will complete soon."

**Documents that present a decision** state the purpose explicitly in the opening:
- Purpose: Inform / Request decision / Align / Escalate.
- State this purpose; do not bury it.

**Tree notes** (vault-specific) state the concept explicitly. The note IS the concept; the title is the concept name; the body is citations + prose if any.

---

## Formatting standards

### Headers

- Use H1 (`#`) once per document, as the title.
- H2 (`##`) for major sections.
- H3 (`###`) for subsections within sections.
- Do not skip levels. No headers solely for decoration.

### Lists

- Use bullets when items don't have an inherent sequence.
- Use numbered lists when sequence or count matters.
- Don't use bullets when prose flows better.

### Tables

- Use tables when relationships across multiple dimensions need to be visible at a glance.
- Don't use tables for simple lists.

### Code blocks

- Fenced (` ``` `) for multi-line code or structured data.
- Inline backticks for short references (`file.py`, `function_name`, `^cite-9rynu4`).

### Numbers and dates

- Dates: ISO 8601 (`2026-05-11`).
- Times: ISO 8601 (`2026-05-11T14:30:00`).
- Numbers: write out one through nine; use digits for 10+. Exception: in tables or technical contexts, digits throughout.
- Percentages: digits + `%` (`73%`, not "73 percent").

### Oxford comma

Use it. "A, B, and C", not "A, B and C".

### Punctuation

Em-dashes are FORBIDDEN. Use commas, colons, or split sentences. See `.clinerules/03-anti-patterns.md § Prohibited punctuation` for the full list.

Excessive exclamation points are forbidden. One per document maximum.

Ellipses for dramatic effect are forbidden. Complete the thought.

---

## Document types

### Tree atom (vault concept note)

**Purpose**: capture one atomic concept with citations to source material.

**Structure** (per `librarian-note-schemas.md`):

```yaml
---
aliases:
  - <acronym>
tags:
  - <domain>
topics:
  - "[[<Parent Concept>]]"
created: YYYY-MM-DD HH:MM
last_updated: YYYY-MM-DD HH:MM
---
![[<citekey>#^cite-<anchor>]]
![[<citekey>#^cite-<another>]]
```

Body: typically embeds only, zero prose. The note is a graph handle + transclusion pane.

### Synthesis / aggregator Tree

**Purpose**: tie multiple atomic Trees to a parent concept; provide prose explanation.

**Structure**: frontmatter + prose explanation of the parent concept + `^cite-*` embeds from multiple sources + `[[wikilinks]]` to atomic Trees.

Example: `Trees/Machine Learning/Deep Learning/Agentic Retrieval-Augmented Generation.md` (stacked `^cite-*` embeds, parent-concept prose).

### Planning document

**Purpose**: capture a project plan or decision artifact.

**Structure**:
- Opening: state the purpose (Inform / Decide / Align / Escalate) and the decision required, if any.
- Body: scope, options considered, recommendation, supporting data.
- Closing: next steps with dates, decision points, dependencies.

Filed under `Mountains/Documents/` in the vault per `librarian-note-schemas.md § Mountains PM hierarchy`, or `docs/` in the Hypatia codebase for Hypatia-build plans.

### Research summary

**Purpose**: distill research findings.

Use `research-protocol.md § Phase 5 Output Delivery` format. Findings + citations + analysis + recommendation + gaps.

### Session log

**Purpose**: capture a session's outcomes for cross-session continuity.

Use `08-save-command.md § Step 1` format. Scope synthesis, files touched, decisions made, outcome assessment, inbox captures created.

### Inbox capture

**Purpose**: record an observation during a session that may consolidate into a memory or intelligence entry.

Use `inbox/SCHEMA.md` format. Frontmatter (observed, source-session, candidate-type, confidence, status) + body (What I observed / How I'd codify it / Confidence rationale / Related captures).

### Inline correspondence (Slack, email, chat)

**Purpose**: ad-hoc written communication.

- Lead with the answer or request.
- Use the audience's register; vault-specific terms may not translate.
- Keep short. Long correspondence usually wants to be a document.

---

## Writing process

### 1. Define purpose

Before drafting:
- What does the reader need to leave with?
- What's the decision or outcome?
- What format fits this purpose? (Tree / synthesis / planning doc / summary / capture.)

### 2. Outline

For documents over 2 paragraphs, outline before drafting. Sections, key claims per section, evidence each claim needs.

### 3. Draft

- Write the opening last; you'll know what to open with after the body exists.
- Don't edit while drafting; capture the full draft first.
- Cite as you go; don't promise yourself you'll add citations later.

### 4. Edit

- Pass 1: structural. Sections in the right order? Anything missing? Anything redundant?
- Pass 2: clarity. Can a reader follow the argument? Re-read each sentence as if reading for the first time.
- Pass 3: prose. Hedge words, weak verbs, em-dashes (none allowed).
- Pass 4: format. Headers, lists, tables, code blocks, citation format.

### 5. Verify

- All claims cited where citations exist?
- Anti-patterns scrubbed (see checklist below)?
- Format matches the document type's conventions?
- Cross-references resolve (no link rot)?

---

## Writing checklist

Before delivering or filing:

- [ ] Purpose stated explicitly in opening.
- [ ] Audience identified; register matches.
- [ ] Active voice unless passive carries meaning.
- [ ] Claims backed by data or citations.
- [ ] No em-dashes. No hedge words without uncertainty. No filler openings.
- [ ] Numbers, dates, percentages formatted per standards.
- [ ] Format matches document type (Tree schema, planning doc structure, etc.).
- [ ] Vault impact noted (if applicable): new Trees, cross-references, inbox captures.
- [ ] Citations resolve (no missing references).

---

## Common corrections

| Issue | Fix |
|---|---|
| Passive voice without purpose | Rewrite active |
| Hedge word without uncertainty | Replace with specific |
| Em-dash | Comma, colon, or split sentence |
| "Significant improvement" | "23% improvement" |
| "Some users" | "3 of 10 users" |
| "Soon" / "shortly" | Specific date |
| Buried lead | Move to opening |
| Walls of text | Break into sections + structure |
| Jargon without definition | Define on first use |
| Citations missing | Add Tree wikilink or external citation |
| Numbers in prose | Write out 1-9; digits for 10+ |

---

## Anti-patterns

### Prose

- Padding (restating in different words).
- Burying the lead.
- Conditional pyramids ("if X, then if Y, then maybe Z").
- Ad-hoc abbreviations without first-use expansion.
- Passive voice as a hedge against accountability.

### Format

- Headers without content (decoration).
- Bullets where prose flows better.
- Tables for simple lists.
- Inconsistent date formats.
- Mixed citation styles within one document.

### Citation

- Claim without source.
- Source without verification (cite something the writer hasn't actually read).
- Misattribution (citing A for a claim that originated with B; see `research-protocol.md § Citation chain analysis`).
- Bare URL without context.

### Vault context

- Composite Tree (multiple atomic concepts in one note).
- Heading-embed when block-embed exists.
- Tag drift (using `learningengineering` when `learningEngineering` is the canonical).
- Filing without `topics:` wikilinks (orphan Tree).

---

## Quick reference

| Rule | Source |
|---|---|
| Active voice | `## Basic writing standards § Voice` |
| Perspective context-dependent | `## Basic writing standards § Voice` |
| Cite sources | `.clinerules/02-voice.md` |
| No em-dashes | `.clinerules/03-anti-patterns.md § Prohibited punctuation` |
| No hedge words without uncertainty | `## Hedging` |
| Numbers: 1-9 spelled, 10+ digits | `## Formatting standards § Numbers` |
| Dates: ISO 8601 | `## Formatting standards § Numbers` |
| Tree schema | `librarian-note-schemas.md` |
| Document type formats | `## Document types` |

---

## Cross-references

- **Voice register (Hypatia's own writing)**: `.clinerules/02-voice.md`
- **Anti-patterns (writing-adjacent rules)**: `.clinerules/03-anti-patterns.md`
- **Tree schemas (atomic + aggregator)**: `hypatia-kb/protocols/librarian-note-schemas.md`
- **Writing rules for vault editing**: `hypatia-kb/protocols/librarian-writing-rules.md`
- **Session log format**: `.clinerules/08-save-command.md`
- **Inbox capture format**: `inbox/SCHEMA.md`
- **Research synthesis writing**: `research-protocol.md`
- **Summarization writing**: `summarization-protocol.md`
- **Planning documents**: `planning-protocol.md`

---

*Writing is thinking made visible. The standards exist so the thinking can survive the writing.*
