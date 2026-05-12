# Problem-Solving Protocol

**Purpose**: Deep structured problem-solving methodology for Complex and Novel problems.
**Last Updated**: 2026-05-11 (Hypatia adaptation)
**Trigger Keywords**: problem, debug, troubleshoot, root cause, fix, investigate, analyze problem, decompose, diagnose, systematic, trace
**Dependency**: kernel Cognitive Problem-Solving stance (`.roo/rules-hypatia/06-cognitive.md`, always active)

---

## When this protocol fires

Extends `.roo/rules-hypatia/06-cognitive.md`'s OBSERVE → QUESTION → DEDUCE cycle with:

- Structured decomposition frameworks (5 Whys, Fault Tree, Condition Mapping, Option Matrix).
- Evidence classification rigor.
- Hypothesis generation and testing.
- Domain-specific heuristics.
- Solution evaluation criteria.

The kernel stance handles Simple problems. This protocol handles Complex and Novel (per Complexity Gate classification).

---

## Phase 1: Problem definition (extends kernel OBSERVE)

### Symptom mapping

- List every observable symptom (not causes, symptoms).
- Classify each: intermittent vs. consistent, new vs. recurring, isolated vs. widespread.
- Identify the PRIMARY symptom: the one the Scholar cares about most.

### Context reconstruction

- What changed recently? (Edits, schema migrations, external linter passes, plugin updates.)
- What was the last known good state?
- What's the blast radius? (Which Trees, Bases, plugins are affected.)

### Problem statement

Synthesize into a single sentence: `"[Primary symptom] occurs when [conditions], affecting [scope]."`

If the sentence cannot be written, the problem is not yet understood. Return to OBSERVE.

---

## Phase 2: Structured decomposition (extends kernel QUESTION)

### Framework selection

| Problem type | Framework | When to use |
|---|---|---|
| "Why did X happen?" | 5 Whys | Linear causation, single failure chain |
| "What could cause X?" | Fault Tree | Multiple possible causes, need to enumerate |
| "X works sometimes but not always" | Condition Mapping | Intermittent issues, environment-dependent |
| "How should we approach X?" | Option Matrix | Design / strategy problems, not debugging |

### 5 Whys

1. State the problem.
2. Ask "Why?" with evidence, not speculation.
3. Repeat up to 5 times, stopping when reaching an actionable root cause.
4. Validate: does fixing the root cause address ALL symptoms?

### Fault Tree

1. Top event = primary symptom.
2. Branch into possible causes (OR gates: any one could cause it).
3. For each cause, identify sub-causes or evidence that confirms / eliminates.
4. Prune branches eliminated by evidence.
5. Remaining branches = investigation targets.

### Condition Mapping

1. List conditions where the problem occurs.
2. List conditions where it does NOT occur.
3. Identify the differentiating variable(s).
4. Hypothesize: the differentiator is the cause.

### Option Matrix

For design/strategy problems (not debugging), use Route D framework from `.roo/rules-hypatia/11-decision-routes.md § Route D`.

**Phase 2 output**: a root cause candidate (5 Whys), a ranked list of investigation targets (Fault Tree), a differentiating variable (Condition Mapping), or a set of evaluated options (Option Matrix).

---

## Phase 3: Hypothesis testing (extends kernel DEDUCE)

### Evidence classification

| Type | Weight | Example |
|---|---|---|
| **Hard evidence** | High | Error logs, stack traces, file diffs, reproducible steps |
| **Soft evidence** | Medium | Scholar reports, timing correlations, "it started after." |
| **Inference** | Low | "This usually means.", pattern matching from prior cases |
| **Assumption** | Flag | Anything not verified this session. Must be labeled. |

### Hypothesis protocol

1. Generate 2-3 candidate hypotheses from decomposition.
2. For each: what evidence supports it? What evidence contradicts it?
3. Rank by: evidence strength, simplicity (Occam's razor), reversibility of the fix.
4. Test the strongest hypothesis first.
5. **Before testing**: state `"I expect [action] to [result] because [reasoning]."` (kernel hypothesis-first rule, see `.roo/rules-hypatia/06-cognitive.md`).
6. If the test fails, don't force-fit. State what specifically failed and why. Move to the next hypothesis.

### Deductive elimination

- One piece of contradicting hard evidence eliminates a hypothesis.
- Soft evidence weakens but doesn't eliminate.
- If all hypotheses are eliminated, the problem is misframed. Return to Phase 1.
- `"I don't know"` is a valid intermediate conclusion. State what's been eliminated and what remains.

**Phase 3 output**: the surviving hypothesis (or hypotheses) with supporting evidence, plus an explicit list of what was eliminated and why.

---

## Phase 4: Solution evaluation

Before implementing any solution, evaluate:

| Criterion | Question |
|---|---|
| **Effectiveness** | Does this address root cause, not just symptoms? |
| **Reversibility** | Can we undo this if it's wrong? |
| **Side effects** | What else does this change? |
| **Completeness** | Does this fix ALL symptoms, or just the primary one? |
| **Sustainability** | Is this permanent or a band-aid? |

### Solution confidence

| Level | Meaning | Action |
|---|---|---|
| High | Root cause confirmed, fix validated | Implement directly |
| Medium | Strong hypothesis, fix likely correct | Implement with monitoring |
| Low | Best guess, limited evidence | Implement as experiment, set success criteria |

**Phase 4 output**: `"[Solution] at [High/Medium/Low] confidence because [evidence summary]. [Action: implement directly / with monitoring / as experiment]."`

---

## Phase 5: Capture (feeds intelligence system via inbox)

After solving, evaluate:

1. Was this a novel solution? → candidate for `knowledge.json` (via inbox).
2. Did a framework work particularly well? → candidate for `patterns.json` pattern refinement (via inbox).
3. Did initial assumptions prove wrong? → candidate for failure pattern (via inbox).
4. Is this problem likely to recur? → candidate for Troubleshooting Gate entry (via inbox).
5. Did DEDUCE produce a reusable conclusion from combining facts + context? → candidate for `reasoning.json` (via inbox).

** flow**: every capture goes to `inbox/preferences/*.md` as a free-form markdown observation. The Scholar promotes during maintenance consolidation. Save command stages the inbox files; it does NOT auto-promote (per `.roo/rules-hypatia/08-save-command.md`).

---

## Domain Heuristics

### Vault / zettelkasten

- Reproduce before diagnosing: open Obsidian, observe the symptom in-app, not in `cat`.
- Check the diff (what changed since the wiki worked): `git log -p` on the affected files.
- Read the actual error: linter logs, plugin console, dataview parse errors.
- Check the linter chain: which plugin's pre-save hook fires when? Order matters.
- Check basename collisions: `[[Variables]]` resolves to whichever Obsidian picks first.

### Code / application

- Reproduce before diagnosing.
- Check the diff.
- Read the actual error message; do not pattern-match from memory.
- Check dependencies / versions; `uv.lock` may show a recently-resolved version drift.
- For Python: check `import` order, circular dependencies, virtual env activation.

### Schema / frontmatter

- Verify the entry parses as valid YAML before suspecting downstream issues.
- Check linter pass order: `obsidian-linter` overwrites multi-line YAML structures on save.
- Check Base filter syntax: `.contains("X")` vs `== ["X"]` behave differently with list-form vs scalar `kind:`.
- Bell's prior incident: 249 Research seeds broken by `sed` on multi-line YAML (2026-04-21). Never `sed` multi-line YAML. Use Python + PyYAML, `yq`, or hand-edit.

### Scholar / collaborative

- Separate the technical problem from the conceptual problem.
- Identify what the Scholar actually wants (often different from what they said).
- Check: is this a structure failure (wiki schema), a behavior failure (Hypatia's protocols), or a context failure (Hypatia missed prior decisions)?

**Maintenance**: review domain heuristics quarterly during `maintenance-protocol.md § Intelligence System Health` check. Add new domains as work evolves. Remove stale heuristics that no longer apply.

---

## Worked example: full protocol applied

**Scenario**: the `obsidian-linter` plugin destroyed YAML frontmatter on 47 Research Seeds after the Scholar saved a single edited Seed.

**Phase 1: Problem definition**

- Symptoms: 47 Research Seeds now have YAML parse errors (`Topics:` and `topics:` keys both present, conflict). Originally worked. Linter ran on save of one edited Seed; bulk damage followed.
- Context: linter was recently enabled. Single Seed was edited; mass damage occurred via plugin's "lint all on save" behavior. Last known good state: before the linter pass.
- Problem statement: *"YAML frontmatter parsing fails on 47 Research Seeds because the linter promoted `Topics:` to `topics:` while leaving the original `topics:` intact, affecting the Scholar's Bases queries that filter on `topics:`."*

**Phase 2: Structured decomposition (Fault Tree)**

- Top event: 47 Seeds have YAML parse errors.
 - Branch 1: Linter "lint all on save" promoted `Topics:` to `topics:` (hard evidence: visible in git diff).
 - Branch 2: Some Seeds already had `topics:` (hard evidence: same git diff, conflicting keys).
 - Branch 3: Linter's YAML duplicate-key handler is missing (inference: would resolve cleanly otherwise).

**Phase 3: Hypothesis testing**

- Hypothesis A: linter's lint-on-save scoped to all Seeds, not just the edited one. Evidence: hard (47 files modified in same commit timestamp). Eliminates the "user must trigger per-file" assumption.
- Hypothesis B: pre-existing `Topics:` + `topics:` duplicate keys masked by Obsidian's parser (which picked one). Linter normalized but didn't merge. Evidence: hard (4 files had both keys per `git log -p` on prior commits).
- Surviving: A and B together explain the symptom.

**Phase 4: Solution evaluation**

- Fix: `git reset --hard` to restore pre-linter state. Then disable `obsidian-linter` on `Seeds/Sources/Research/**`. Then design a YAML duplicate-key merge pass to handle the underlying conflict before re-enabling the linter.
- Confidence: High. Root cause confirmed (Hypothesis A + B). Reversible (`git reset` is clean since last commit was pre-linter). Side effects: linter disabled on Research Seeds requires future manual handling for that subtree.
- Recommendation: `"git reset --hard <pre-linter-commit>; disable linter on Seeds/Sources/Research/**; defer the duplicate-key merge to a planned maintenance session. High confidence, implement directly."`

**Phase 5: Capture**

- `knowledge.json` candidate (via inbox): "`obsidian-linter` runs lint-on-save across all open files in scope, not just the active file. Restrict scope with `excludedFolders` config."
- `patterns.json` candidate (via inbox; failure pattern): "Mass-YAML-destruction risk: any linter or pre-save hook that normalizes keys can produce duplicate-key conflicts on files with pre-existing capitalized-key drift. Pre-flight: audit for `Topic:` vs `topics:` (or analogous) before enabling auto-format."
- Both captures go to `inbox/preferences/*.md`. Scholar consolidates at next maintenance.

---

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skipping problem statement | Premature decomposition, wasted effort | Write the single-sentence statement first |
| Pattern-matching to familiar problem | Conflates similar with same | Run OBSERVE without prior context first |
| Confirming first hypothesis without elimination | Confirmation bias | DEDUCE eliminates, doesn't confirm |
| Soft evidence treated as hard | False confidence | Label evidence type explicitly |
| Skipping capture | Lessons don't compound | Capture phase is part of solving |

---

## Cross-references

- **Kernel cognitive stance (always-on)**: `.roo/rules-hypatia/06-cognitive.md`
- **Complexity Gate classification**: `.roo/rules-hypatia/06-cognitive.md § Complexity Gate`
- **Hypothesis-first stance**: `.roo/rules-hypatia/06-cognitive.md § Hypothesis-first`
- **Failure-to-Fix Cycle (systemic failures)**: `.roo/rules-hypatia/06-cognitive.md § Failure-to-Fix Cycle`
- **Save command (capture flush)**: `.roo/rules-hypatia/08-save-command.md`
- **Inbox capture format**: `inbox/SCHEMA.md`
- **Decision routes (Option Matrix → Route D)**: `.roo/rules-hypatia/11-decision-routes.md`
- **Domain anti-patterns (sed on multi-line YAML, etc.)**: `hypatia-kb/protocols/librarian-writing-rules.md § Lessons learned`
