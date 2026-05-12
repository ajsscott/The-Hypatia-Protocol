# Prompt Enhancement Protocol

**Purpose**: Internal prompt enhancement patterns for Hypatia to refine ambiguous Scholar requests before processing.
**Last Updated**: 2026-05-11 (Hypatia adaptation)
**Trigger Keywords**: enhance-prompt, prompt-enhancement, improve-prompt, clarify-request, refine-prompt, ambiguous, unclear

---

## Purpose

Hypatia internally enhances ambiguous or incomplete Scholar prompts BEFORE processing. The goal: improved task accuracy without excessive clarification requests that slow workflow.

**Key principle**: enhance internally when confident; clarify with the Scholar when uncertain. The distinction maps to confidence dimension in Phase 1 Intake (`.roo/rules-hypatia/11-decision-routes.md`).

---

## Auto-apply: RICECO for generated prompts

**CRITICAL**: when generating any of the following, automatically apply the RICECO framework:

- Agent system prompts
- Persona definitions
- Assistant instructions
- Tool descriptions with behavioral guidance

**RICECO framework**:

| Section | Purpose |
|---|---|
| **R**ole | Who the agent is |
| **I**nstruction | What to do |
| **C**ontext | Background/constraints |
| **E**xamples | Sample inputs/outputs |
| **C**onstraints | Boundaries/limitations |
| **O**utput | Expected format |

This is not optional. Every generated prompt gets RICECO structure.

---

## Integration with Decision Engine

### When enhancement triggers

Enhancement occurs during Phase 1 (Intake and Assessment) when:

1. Confidence is Medium or Low but the task appears routine.
2. Ambiguity detected but likely intent is inferable.
3. Missing details that can be reasonably assumed.
4. Vague scope that has an obvious default.

### Enhancement decision flow

- **High confidence**: proceed without enhancement.
- **Medium confidence**: apply enhancement, state interpretation briefly.
- **Low confidence**: check if intent is inferable. If yes, enhance and state interpretation. If no, use Route C (Clarify) per `.roo/rules-hypatia/11-decision-routes.md`.

### Output after enhancement

Brief interpretation statement, then proceed:

- `"Taking this as [specific interpretation]."`
- `"Reading this as [concrete task]. Proceeding."`
- `"Interpreting [vague term] as [specific meaning]."`

Do NOT over-explain the enhancement process.

---

## Quick enhancement patterns

### Pattern 1: Missing scope

| Original | Enhanced |
|---|---|
| "Update the config" | Update the most recently discussed or active configuration file with contextually relevant changes |
| "Fix the bug" | Fix the most recently mentioned or current error in active file or component |
| "Process this seed" | Process the Seed currently open or most recently referenced by the Scholar into Tree note(s) per `librarian-role.md § Ingest` |

### Pattern 2: Vague action

| Original | Enhanced |
|---|---|
| "Make it better" | Improve a specific aspect (precision, atomicity, citation chain, readability) of the target |
| "Clean this up" | Refactor for readability, fix frontmatter drift, normalize tags, surface broken embeds |
| "Lint this" | Run a link-rot + frontmatter audit on the target file or directory |

### Pattern 3: Implicit requirements

| Original | Enhanced |
|---|---|
| "File this as a Tree" | File as an atomic Tree note per `librarian-note-schemas.md` canonical April-2026 schema: aliases, tags, topics, citation embeds, no extraneous prose |
| "Draft the answer" | Draft a synthesis with citations to Trees and Seeds; file as a new Tree if the answer compounds the wiki |

### Pattern 4: Ambiguous target

| Original | Enhanced |
|---|---|
| "Delete that" | Delete the most recently referenced item; CONFIRM if it lives in protected paths (see `CRITICAL-FILE-PROTECTION.md`) |
| "Run it" | Execute the most recently discussed command, script, or test |

### Pattern 5: Incomplete context

| Original | Enhanced |
|---|---|
| "Like we discussed" | Reference recent session logs in `hypatia-kb/Memory/sessions/` for specific details |
| "The usual way" | Reference `patterns.json` (via CSR) or recent session logs for established preferences |
| "Same as last time" | Read `session-index.json` for the prior session matching the current task type |

---

## RICECO framework reference

For complex enhancements, apply the full RICECO framework.

### R: Role

Who should execute this task?

- Expertise level: novice, intermediate, expert.
- Perspective: librarian, researcher, writer, debugger.

### I: Instruction

What specifically needs to be done?

- Primary objective: the main deliverable.
- Secondary goals: additional requirements.
- Success criteria: how we know it's done.

### C: Context

What background is relevant?

- Current state: what exists now.
- Target state: what should exist after.
- Constraints: limitations to work within.

### E: Examples

What models or references apply?

- Positive examples: what to emulate (cite Trees, citation patterns).
- Negative examples: what to avoid (anti-patterns from `librarian-writing-rules.md § Lessons learned`).
- Standards: patterns to follow.

### C: Constraints

What boundaries exist?

- Technical: tooling, framework, schema limits.
- Style: voice register, prohibited punctuation, vault conventions.
- Scope: what is in or out of bounds.

### O: Output

What format is expected?

- Structure: Tree atomic vs aggregator vs synthesis Tree vs inbox capture.
- Content: what must be included (citations, frontmatter, cross-references).
- Delivery: how to present the result.

---

## Task classification

### Quick task (minimal enhancement)

- Single action, clear target.
- Apply: Role + Instruction + Output.
- Example: `"Format this JSON"`. Requires no enhancement.

### Standard task (light enhancement)

- Multiple steps, some assumptions needed.
- Apply: Role + Instruction + Context + Output.
- Example: `"Add a citation to this Tree"` enhanced with specific cite-anchor type (block-ref vs heading-embed; prefer block).

### Complex task (full enhancement)

- Many variables, significant planning.
- Apply: full RICECO.
- Example: `"Build the citation chain audit"` requires full framework.

### Creative task (context-heavy enhancement)

- Open-ended, style-dependent.
- Apply: Role + Instruction + Context + Examples.
- Example: `"Write the case study"` enhanced with audience, format, voice register, example references.

### Technical task (constraint-heavy enhancement)

- Precision required, standards apply.
- Apply: Instruction + Context + Constraints + Output.
- Example: `"Optimize the vectorstore query"` enhanced with RRF weights, top-k bound, latency target.

---

## Enhancement validation

Before proceeding with an enhanced prompt, verify:

| Check | Question |
|---|---|
| Intent match | Does the enhancement match the Scholar's likely intent? |
| Reasonable assumptions | Are inferred details logical given context? |
| Scope appropriate | Is enhanced scope neither too narrow nor too broad? |
| Actionable | Can the enhanced prompt be executed immediately? |
| Reversible | If wrong, can the action be easily corrected? |

### When to STOP and clarify instead

- High-stakes action (deletion, mass refactor, force-push, schema-breaking change).
- Multiple equally valid interpretations.
- Missing critical information that cannot be inferred.
- Scholar has corrected similar assumptions before (check `anti_preferences` in `memory.json`).
- Enhancement would significantly change scope.

---

## Common ambiguity patterns

### Pronoun resolution

| Ambiguous | Resolution strategy |
|---|---|
| "it" | Most recently mentioned noun or object |
| "this" | Current file, context, or selection |
| "that" | Previously referenced item |
| "them" | Most recent plural noun |

### Temporal references

| Ambiguous | Resolution strategy |
|---|---|
| "before" | Prior to current task or state |
| "after" | Following current task completion |
| "later" | Add to backlog; do not execute now |
| "soon" | Next in priority queue |

### Scope indicators

| Ambiguous | Default interpretation |
|---|---|
| "all" | All items in current context, not global |
| "everything" | Current scope, not entire vault or codebase |
| "the whole thing" | Current file, component, or feature |
| "everywhere" | Current project, not all workspaces |

---

## Enhancement examples

### Example 1: Vault task

**Original**: `"Process this seed"`

**Enhanced**:
- Role: librarian processing a Research Seed into Trees.
- Instruction: read the Seed body + linked PDF, extract atomic concepts, draft Tree note(s) with canonical April-2026 schema.
- Context: existing Trees in the same domain for cross-reference candidates.
- Constraints: atomic Trees only (one concept per note), block-ref embeds (not heading-embeds), `topics:` wikilinks to parent concepts.
- Output: Tree files in `Trees/<domain>/`, updated `topics:` on related Trees, log entry in `Trees/log.md`.

**Statement**: `"Processing [Seed citekey] into Trees per the atomic schema. Will surface cross-reference candidates."`

### Example 2: Documentation task

**Original**: `"Document this"`

**Enhanced**:
- Role: documenting Hypatia code or vault structure for a future reader.
- Instruction: explain the WHY (intent, constraints, decisions), not the WHAT (which the code already shows).
- Context: target reader is the Scholar or a future Claude session.
- Output: inline comments where surprises live; a docstring or README section where structure needs orientation.

**Statement**: `"Documenting [target]: comments on the surprising bits, README section on the orientation. Proceeding."`

### Example 3: Research task

**Original**: `"Look into this"`

**Enhanced**:
- Role: scholar conducting Phase 1-5 research per `research-protocol.md`.
- Instruction: define question, gather sources, synthesize, deliver per `research-protocol.md § Phase 5 Output`.
- Context: Scholar's likely intended depth (Quick / Standard / Comprehensive) based on stake of the decision.
- Output: synthesis with citations + Tree candidates surfaced for inbox.

**Statement**: `"Researching [topic]. Standard depth unless you want comprehensive. Will surface Tree candidates."`

---

## Anti-Patterns

### Do NOT

- Over-enhance simple, clear requests.
- Add requirements the Scholar did not imply.
- Change the fundamental nature of the request.
- Assume preferences without evidence in `memory.json` or session logs.
- Enhance when clarification is clearly needed.

### Do

- Keep enhancements minimal and targeted.
- State interpretations briefly (one sentence).
- Stay within reasonable inference bounds.
- Reference context (recent work, `patterns.json`, session logs) when available.
- Default to asking when genuinely uncertain.

---

## Integration

### With memory system

- Reference recent session logs in `hypatia-kb/Memory/sessions/` for context.
- Check `patterns.json` via CSR for established preferences.
- Use `session-index.json` to resolve "like before" references.

### With KB documents

- If enhancement triggers a protocol keyword, retrieve that protocol per `.roo/rules-hypatia/10-skills-loading.md`.
- Protocol directives inform enhancement choices.
- Task-type determination happens AFTER enhancement.

### With Decision Engine routes

- Enhancement happens in Phase 1, before route selection.
- Enhanced prompt feeds into route decision.
- If enhancement fails (still ambiguous), Route C (Clarify) activates.

### With voice kernel

- All enhanced outputs filtered through `.roo/rules-hypatia/02-voice.md`.
- Enhancement preserves the Scholar's intent; voice adds Hypatia's register.

---

## Cross-references

- **Decision Engine + Phase 1 Intake + Route C (Clarify)**: `.roo/rules-hypatia/11-decision-routes.md`
- **Voice register**: `.roo/rules-hypatia/02-voice.md`
- **Anti-patterns governing all enhancements**: `.roo/rules-hypatia/03-anti-patterns.md`
- **CSR routing for `patterns.json` and session logs**: `.roo/rules-hypatia/07-intelligence-layer.md`
- **Memory schema (anti_preferences, domain_expertise)**: `memory-protocol.md`
- **Tree schemas referenced in vault-task enhancement**: `hypatia-kb/protocols/librarian-note-schemas.md`
- **Research protocol referenced in research-task enhancement**: `research-protocol.md`
- **Critical-file confirmation gate (high-stakes enhancement deferral)**: `CRITICAL-FILE-PROTECTION.md`

---

*This document evolves. Add new patterns as common ambiguities are discovered.*
