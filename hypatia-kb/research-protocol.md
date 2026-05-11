# Research Protocol

**Purpose**: Systematic methodology for conducting research, evaluating sources, and synthesizing findings into the vault.
**Last Updated**: 2026-05-11 (Hypatia adaptation)
**Trigger Keywords**: research, investigate, source, citation, study, paper, literature, compare, analyze, evaluate, deep-dive, assess, explore

---

## Integration

**Decision Engine integration** (`.clinerules/11-decision-routes.md`):
- Triggered during Phase 2 (KB Consultation) when research keywords surface.
- Default route: B (Execute with Context) for standard research tasks.
- Route D (Present Options) when research scope is ambiguous or multiple framings are viable.
- Route F (Pre-Action Analysis) when the research outcome will inform a system or schema change.

**Related protocols**:
- `writing-protocol.md`: presenting research findings in formal documents (Trees, aggregator notes).
- `prompt-enhancement-protocol.md`: clarifying vague research requests before scope definition.
- `planning-protocol.md`: research that feeds into project planning.
- `hypatia-kb/protocols/librarian-note-schemas.md`: canonical Tree schema for filing research outputs.
- `hypatia-kb/protocols/librarian-role.md § Three operations`: the ingest workflow that turns research into Trees.

**Voice integration**: all outputs filtered through `.clinerules/02-voice.md`. Cite sources reflexively. Hypothesis without citation is gossip.

---

## Quick reference

### Trigger tiers

| Tier | Keywords |
|---|---|
| 1 (Absolute) | research, deep-dive, investigate, literature review |
| 2 (Strong) | compare, analyze, evaluate, assess, study |
| 3 (Contextual) | explore, look into, find out (+ research context) |

### Output formats

| Format | Use when | Depth |
|---|---|---|
| Quick scan | Time-sensitive, surface-level need | Key points + 1-2 sources |
| Standard | Typical research request | Findings + sources + recommendation |
| Comprehensive | Strategic decisions, complex topics | Full analysis with alternatives + Tree drafts |

---

## Research methodology

### Phase 1: Scope definition

Before starting research:

1. **Define the question**: what specifically needs to be answered?
2. **Identify constraints**: time, depth, source restrictions (vault-internal Seeds, web, both).
3. **Determine output**: Quick scan / Standard / Comprehensive.
4. **Set boundaries**: what's in scope vs. out of scope.

Scope template:

```
Research question: [Specific question to answer]
Context:          [Why this matters, what decision it informs]
Constraints:      [Time limit, source preferences, depth required]
Output format:    [Quick / Standard / Comprehensive; will it produce Trees?]
Out of scope:     [What NOT to research]
```

### Phase 2: Source gathering

**Source hierarchy** (prioritize in this order):

1. **Vault-internal canonical sources**: existing Trees and Seeds in `Trees/`, `Seeds/Sources/Research/`. Read what's already filed before reaching outside.
2. **Primary sources**: original papers, official documentation, direct data. PDFs in `_attachments/_pdfs/` count.
3. **Authoritative external sources**: peer-reviewed publications, recognized standards bodies, official APIs.
4. **Expert commentary**: recognized authorities, well-established research blogs.
5. **Community sources**: forums, Stack Overflow, less-vetted blogs. Verify claims against (1)–(3).
6. **LLM-generated content**: use for synthesis prompts and exploration only. Per Q-22 + `.clinerules/09-security.md`, LLM output is external content and subject to the same trust tier as web clippings. Verify any specific claim against a primary source before filing.

**Source evaluation criteria**:

| Criterion | Questions |
|---|---|
| Authority | Who created this? What are their credentials? Does the vault already cite them? |
| Currency | When was this published? Is it still current given the rate of change in the domain? |
| Accuracy | Can claims be verified? Are sources cited? Do other sources agree? |
| Purpose | Why was this created? Commercial bias? Marketing pitch dressed as research? |
| Relevance | Does this directly address the research question? |
| Vault fit | Does this map to existing Trees, or does it open a new concept? |

**Credibility scoring**:

- **High**: peer-reviewed, primary sources, recognized authorities, recent. Cite freely.
- **Medium**: reputable blogs, community consensus, dated but still relevant. Cite with caveat.
- **Low**: unverified claims, anonymous sources, outdated information. Flag, don't file.

### Phase 3: Analysis & synthesis

**Comparison analysis**:

```markdown
| Criterion       | Option A    | Option B    | Option C    |
|-----------------|-------------|-------------|-------------|
| [Factor 1]      | [Value]     | [Value]     | [Value]     |
| [Factor 2]      | [Value]     | [Value]     | [Value]     |
| Recommendation: | [Winner with rationale]                  |
```

**Pros/cons analysis**:

```markdown
## [Option / Topic]

Pros:
- [Advantage 1]. Source: [attribution]
- [Advantage 2]. Source: [attribution]

Cons:
- [Disadvantage 1]. Source: [attribution]
- [Disadvantage 2]. Source: [attribution]

Net assessment: [Overall evaluation]
```

**Gap analysis**:

```markdown
| Current state   | Desired state   | Gap         | Effort to close (H/M/L) |
|-----------------|-----------------|-------------|-------------------------|
| [What exists]   | [What's needed] | [Delta]     | [Estimate]              |
```

**Citation chain analysis** (vault-specific):

When a finding involves a chain of citations (paper A cites paper B which cites paper C), trace the chain:

1. Read the originating claim's source (C, not A).
2. Verify A's representation of C matches what C actually says.
3. File a contradiction note if the chain misrepresents.
4. This is the vault's hedge against the "singh cites du" type misattribution surfaced during the consciousness.md voice rewrite.

**Trend analysis**:

- Historical context: where did this come from?
- Current state: where is it now?
- Trajectory: where is it heading? (Hedge: forecasts are weaker evidence than current state.)
- Implications: what does this mean for the Scholar's work?

### Phase 4: Confidence assessment

| Level | Criteria | Indicator |
|---|---|---|
| High | Multiple authoritative sources agree; recent; directly applicable to Scholar's question | ✓ |
| Medium | Some authoritative sources; minor gaps; mostly applicable | ⚠ |
| Low | Limited sources; conflicting info; indirect applicability | ? |

**Uncertainty handling**:

- State what is known vs unknown.
- Identify assumptions made.
- Note where additional research would help.
- Never present uncertain findings as definitive (see `.clinerules/03-anti-patterns.md § Truth & confidence`).

### Phase 5: Output delivery

Standard research output structure:

```markdown
## Research: [Topic]

Question:   [What was asked]
Confidence: [High/Medium/Low]
Date:       [YYYY-MM-DD]

### Summary
[2-3 sentences answering the research question]

### Key findings
- [Finding 1]. Source: [Tree/Seed reference or external citation]
- [Finding 2]. Source: [...]
- [Finding 3]. Source: [...]

### Analysis
[Synthesis: patterns identified, contradictions surfaced, implications]

### Recommendation
[Clear recommendation based on findings; or "deferred pending [X]"]

### Sources cited
1. [Source 1: Tree wikilink or external URL]
2. [Source 2: ...]

### Gaps and uncertainties
- [What remains unknown]
- [Where confidence is lower]
- [Suggested follow-up research, if any]

### Tree candidates (Q-22 inbox flow)
- Drafted Trees: [list of Tree paths if any drafted during research]
- Suggested new Trees: [concepts that emerged but weren't drafted]
- Cross-references suggested: [existing Trees that should link in]
```

---

## Research types

### Scholarly / literature research

- Trace citation chains; verify A's claims about B by reading B directly.
- File primary sources as Seeds in `Seeds/Sources/Research/` per `librarian-note-schemas.md`.
- Generate atomic Trees in `Trees/` with `^cite-` block-reference embeds back to the Seed.
- Cross-reference findings against existing Trees in the same domain; flag contradictions.
- Update parent-concept Trees as new sub-concepts emerge.

### Technical research

- Prioritize official documentation and tested examples.
- Include version numbers and compatibility notes.
- Flag deprecated or outdated approaches.
- File reusable patterns as patterns.json candidates (via inbox).

### Comparative / decision-support research

- Compare options against criteria the Scholar named in Phase 1, not Hypatia's intuitions about what matters.
- Use the comparison-table format.
- Identify decision criteria BEFORE comparing (post-hoc criteria are biased).

### Best-practices research

- Look for consensus across multiple sources; flag minority positions.
- Distinguish opinion from validated practice.
- Note context dependencies (what works in domain X may fail in domain Y).
- Include anti-patterns (what to avoid).

### Troubleshooting research

- Start with the exact error message; do not pattern-match.
- Prioritize recent solutions (last 12 months for fast-moving domains).
- Verify solutions before recommending.
- File the resolution as a knowledge entry (via inbox) so the next session benefits.

### Contradiction-detection research

(Hypatia-specific.) When two Trees citing different sources appear to contradict:

1. Read both Trees' Seeds (not just the Tree summaries).
2. Identify whether the contradiction is real or a difference in scope/context.
3. If real: file a contradiction note in both Trees' `topics:` or as an inline flag.
4. Surface the contradiction to the Scholar with both sources cited.
5. Do not resolve unilaterally; the Scholar decides which claim to elevate.

---

## Anti-Patterns

### Research

- Stopping at first result found.
- Treating all sources as equally credible.
- Presenting findings without confidence indication.
- Ignoring contradictory evidence.
- Over-researching when a quick answer suffices.
- Under-researching when the decision is significant.
- Filing LLM-generated synthesis as a Tree without verifying claims against primary sources (Q-22 + `.clinerules/09-security.md`).

### Output

- Dumping raw findings without synthesis.
- Missing source attribution.
- Presenting opinion as fact.
- Burying the answer in details.
- Failing to state what remains unknown.

---

## Quality checklist

Before delivering research:

- [ ] Research question clearly answered.
- [ ] Confidence level stated.
- [ ] Sources attributed and credible.
- [ ] Findings synthesized, not just listed.
- [ ] Recommendation provided (if applicable).
- [ ] Uncertainties acknowledged.
- [ ] Output format matches request.
- [ ] Vault impact identified (Tree drafts, cross-references, contradictions).
- [ ] Inbox captures drafted for anything that should become a Tree or knowledge entry (Q-22).

---

## Cross-references

- **Decision routing (Phase 2 KB Consultation triggers this protocol)**: `.clinerules/11-decision-routes.md`
- **Cognitive stance (research engages OBSERVE → QUESTION → DEDUCE for ambiguous topics)**: `.clinerules/06-cognitive.md`
- **External-content security (LLM-generated sources treated as untrusted)**: `.clinerules/09-security.md`
- **Note schemas (Tree drafting, citation embeds, naming conventions)**: `hypatia-kb/protocols/librarian-note-schemas.md`
- **Librarian role (ingest workflow that turns research into Trees)**: `hypatia-kb/protocols/librarian-role.md`
- **Inbox capture format (Tree candidates surfaced during research)**: `inbox/SCHEMA.md`
- **Writing protocol (presenting findings)**: `writing-protocol.md`
- **Planning protocol (research feeding into project planning)**: `planning-protocol.md`

---

*Research is about finding truth, not confirming assumptions. Follow the evidence, state confidence honestly, and acknowledge what remains unknown.*
