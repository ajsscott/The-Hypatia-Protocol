# Executive Communication Protocol

**Purpose**: Framework for communication with senior stakeholders (executives, board members, investors, sponsors).
**Last Updated**: 2026-05-11 (Hypatia adaptation; substantially thinned from Bell's 253 L original)
**Trigger Keywords**: executive, C-suite, CEO, CFO, CIO, CTO, board, investor, stakeholder presentation, pitch, exec comms

---

## Scope note

This protocol is **not load-bearing for Hypatia's primary work**. The Scholar's main domains (zettelkasten curation, scholarly research, vault maintenance, Hypatia development) rarely involve executive communication.

When executive comms ARE needed (Scholar requests a stakeholder document, board update, sponsor communication, conference pitch, or similar), apply the universal principles below. They derive from Bell's original framework, distilled to the parts that survive outside the SaaS/CTO context where Bell wrote them.

If the deliverable is substantial (multi-page memo, formal presentation, investor briefing), engage Route F (`.roo/rules-hypatia/11-decision-routes.md`) to scope it properly before drafting.

---

## Universal principles

1. **Listen first, validate the problem.** Do not lead with the solution.
2. **Speak in outcomes, not features.** Business or scholarly impact over implementation detail.
3. **Understand the audience's decision frame.** What's the question they need to answer? What evidence will satisfy them?
4. **Tailor to the specific audience.** Generic framings fail. What does THIS reader need?
5. **Facilitate the decision; don't push.** Help the audience make an informed decision, not coerce one.

---

## Working Backwards framework

For substantial deliverables, the Working Backwards sequence (originally Amazon's pattern) still applies:

### 1. Listen

Understand the audience: what they care about, what their decision frame is, what evidence has historically moved them. If you don't know these, find out before drafting.

### 2. Define

Write the press release / executive summary first: what does success look like from the audience's perspective? If you can't write this, you don't understand the goal yet.

### 3. Invent

Generate the options that achieve the defined success. Multiple options, with trade-offs.

### 4. Refine

Apply Route F-style analysis to the options. ROI, feasibility, risk, alignment with audience constraints.

### 5. Test and iterate

Show a draft early. Refine on feedback. Production-quality version comes last, not first.

---

## Output formats

### Quick stakeholder update

```markdown
## [Topic]: Update for [Audience]

What changed:    [1-2 sentences]
Why it matters:  [Outcome framing, not feature]
What's next:     [Decision or action needed, if any]
```

### Substantive memo

Use the Working Backwards sequence. Lead with the executive summary (the "press release"). Body fills in detail in the order: problem → options → recommended option → implementation outline → risks.

### Decision-support brief

When the audience needs to make a decision:

```markdown
## Decision: [Subject]

Recommendation:    [One sentence]
Rationale:         [3-5 bullets, evidence-anchored]

Options considered:
1. [Option A]. Pros: [X]. Cons: [Y]. Why not: [Z].
2. [Option B]. 
3. [Recommended option]. Pros: [X]. Cons: [Y]. Why this one: [Z].

Implementation outline: [If recommendation is accepted]
Risks and mitigations: [What could go wrong]
```

---

## Anti-Patterns

- Leading with the solution before the audience has agreed there's a problem.
- Technical detail without outcome framing.
- Generic pitches that don't reference the audience's specific context.
- Treating executive comms as a vehicle for personal-position-building.
- Over-padding to seem substantive.
- Sycophancy. The audience knows when they're being managed.

---

## When this protocol does NOT fire

Most Hypatia work. Scholar-to-Hypatia conversation uses `.roo/rules-hypatia/02-voice.md`. Vault-internal documentation uses `writing-protocol.md`. Research synthesis uses `research-protocol.md`. Project planning uses `planning-protocol.md`. Documents for the Scholar's own consumption don't need executive framing.

---

## Cross-references

- **Voice register (default Hypatia-to-Scholar communication)**: `.roo/rules-hypatia/02-voice.md`
- **Route F (substantial deliverable analysis)**: `.roo/rules-hypatia/11-decision-routes.md § Route F`
- **Writing standards (when the executive deliverable is a written document)**: `writing-protocol.md`
- **Research (when the deliverable derives from research)**: `research-protocol.md`
- **Planning (when the deliverable is a project plan or roadmap)**: `planning-protocol.md`

---

*This protocol is reference material for an edge case in Hypatia's primary domain. The universal principles transfer; the SaaS/B2B-specific tactics from Bell's original were dropped as out of scope.*
