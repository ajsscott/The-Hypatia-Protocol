# Planning Protocol

**Purpose**: Systematic methodology for project planning, scoping, estimation, and roadmap creation.
**Last Updated**: 2026-05-11 (Hypatia adaptation)
**Trigger Keywords**: plan, roadmap, estimate, scope, breakdown, project, timeline, milestone, dependency, prioritize, phases

---

## Integration

**Decision Engine integration** (`.clinerules/11-decision-routes.md`):
- Triggered during Phase 2 (KB Consultation) when planning keywords surface.
- Default route: D (Present Options) for scope decisions with viable alternatives.
- Route B (Execute with Context) for straightforward breakdowns.
- Route F (Pre-Action Analysis) when the plan involves a new system, framework choice, or architectural decision.

### Route F triggers during planning

| Situation | Action |
|---|---|
| Multiple valid approaches to scope | Route F: compare options |
| Significant trade-offs (time vs quality vs scope) | Route F: analyze trade-offs |
| Uncertainty about priorities | Route F: evaluate priority options |
| Resource allocation decisions | Route F: compare allocation strategies |
| Architecture / approach decisions embedded in plan | Route F: technical analysis |

### Route F skip triggers

- Simple task breakdowns with clear sequence.
- Single obvious approach.
- Scholar explicitly wants speed over analysis.

**Related protocols**:
- `research-protocol.md`: research that informs planning (unknowns surface as research questions).
- `writing-protocol.md`: documenting plans formally.
- `problem-solving-protocol.md`: when planning surfaces an unresolved problem that needs decomposition.

**Voice integration**: outputs filtered through `.clinerules/02-voice.md`. State estimates with confidence. Distinguish "estimated" from "validated". Cite when a plan derives from a Tree or Seed.

---

## Quick reference

### Trigger tiers

| Tier | Keywords |
|---|---|
| 1 (Absolute) | plan, roadmap, project-plan |
| 2 (Strong) | estimate, scope, breakdown, timeline, milestone |
| 3 (Contextual) | prioritize, dependency, schedule (+ planning context) |

### Output formats

| Format | Use when | Detail level |
|---|---|---|
| Quick Breakdown | Simple task decomposition | Tasks + sequence |
| Standard Plan | Typical project planning | Tasks + estimates + dependencies |
| Comprehensive Roadmap | Strategic initiatives | Phases + milestones + risks + resources |

---

## Planning methodology

### Phase 1: Scope definition

Before planning:

1. **Define objective**: what does "done" look like?
2. **Identify stakeholders**: who cares about this? (For Hypatia work, often just the Scholar; for vault work, the answer is the Scholar; for cross-system work, may include external collaborators.)
3. **Establish constraints**: time, resources, dependencies.
4. **Clarify boundaries**: what's in scope vs. explicitly out.

**Scope template**:

```markdown
## Project Scope: [Name]

Objective:          [Clear statement of what will be achieved]
Success criteria:   [How we know it's done right]
Stakeholders:       [Who is involved/affected]
Constraints:
- Time:             [Deadline or timeframe]
- Resources:        [Available people, budget, tools]
- Dependencies:     [External factors]
In scope:           [What's included]
Out of scope:       [What's explicitly excluded]
```

### Phase 2: Work breakdown

**Decomposition rules**:
- Break work into tasks that can be completed in 1-5 days.
- Each task has a clear deliverable.
- Tasks are independently verifiable.
- No task should be "and then magic happens."

**Work breakdown structure**:

```
Project
├── Phase 1: [Name]
│   ├── Task 1.1: [Specific deliverable]
│   ├── Task 1.2: [Specific deliverable]
│   └── Task 1.3: [Specific deliverable]
├── Phase 2: [Name]
│   ├── Task 2.1: [Specific deliverable]
│   └── Task 2.2: [Specific deliverable]
└── Phase 3: [Name]
    └── Task 3.1: [Specific deliverable]
```

**Task definition template**:

```markdown
### Task: [Name]

Deliverable:         [What is produced]
Effort:              [Estimate]
Dependencies:        [What must complete first]
Owner:               [Who is responsible]
Acceptance criteria: [How we verify completion]
```

### Phase 3: Estimation

**Estimation approaches**:

| Method | Use when | Accuracy |
|---|---|---|
| T-shirt sizing | Early planning, rough scoping | Low (±50%) |
| Story points | Relative complexity comparison | Medium (±30%) |
| Time-based | Detailed planning, known work | Higher (±20%) |
| Three-point | Uncertainty is high | Accounts for variance |

**T-shirt sizing**:

| Size | Relative effort | Typical duration |
|---|---|---|
| XS | Trivial | < 2 hours |
| S | Small | 2-4 hours |
| M | Medium | 1-2 days |
| L | Large | 3-5 days |
| XL | Very large | 1-2 weeks (should decompose) |

**Three-point estimation**:

```
Optimistic (O):  Best case, everything goes right
Pessimistic (P): Worst case, problems encountered
Most likely (M): Realistic expectation

Expected = (O + 4M + P) / 6
```

**Estimation anti-patterns**:
- Estimating without understanding scope.
- Ignoring unknowns and risks.
- Padding estimates instead of stating uncertainty.
- Treating estimates as commitments.
- Not revisiting estimates as information emerges.

### Phase 4: Dependency mapping

**Dependency types**:

| Type | Description | Example |
|---|---|---|
| Finish-to-start | B can't start until A finishes | Deploy after testing |
| Start-to-start | B can't start until A starts | Testing starts when dev starts |
| External | Depends on outside factor | Waiting for upstream library |
| Resource | Same resource needed | Scholar's attention; one person, two tasks |

**Dependency visualization**:

```
[Task A] → [Task B] → [Task C]
              │
              └─→ [Task D]

Critical path: A → B → C (longest sequence)
```

**Critical path**:
- Identify the longest chain of dependent tasks.
- This determines minimum project duration.
- Focus risk mitigation on critical-path items.
- Parallel work happens off critical path.

### Phase 5: Risk identification

**Risk categories**:

| Category | Examples |
|---|---|
| Technical | Unknown technology, integration complexity, schema migration |
| Resource | Scholar's attention contended, skill gap surfaces mid-task |
| External | Upstream library changes, plugin behavior changes, API drift |
| Scope | Requirements unclear, scope creep |
| Timeline | Aggressive deadlines, competing priorities |

**Risk assessment matrix**:

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Risk 1] | H/M/L | H/M/L | [Action to reduce] |

**Risk response strategies**:
- **Avoid**: change plan to eliminate the risk.
- **Mitigate**: reduce likelihood or impact.
- **Transfer**: shift the risk to another party.
- **Accept**: acknowledge and monitor.

### Phase 6: Timeline construction

1. Start with critical-path duration.
2. Add buffer for risks (10-20% typical).
3. Account for non-working time (holidays, focus periods).
4. Set milestones at phase boundaries.
5. Identify decision points and dependencies.

**Milestone definition**:

```markdown
### Milestone: [Name]

Date:           [Target date]
Criteria:       [What must be true]
Deliverables:   [What is produced]
Decision point: [Any decisions needed here]
```

**Timeline formats**:

**Simple list**:

```
Week 1: [Phase/Tasks]
Week 2: [Phase/Tasks]
Week 3: [Phase/Tasks]
Milestone: [Checkpoint]
```

**Gantt-style** (text):

```
Task          | W1 | W2 | W3 | W4 |
--------------|----|----|----|----|
Task A        | ██ |    |    |    |
Task B        |    | ██ | ██ |    |
Task C        |    |    |    | ██ |
Milestone     |    |    | ◆  |    |
```

---

## Planning outputs

### Quick breakdown format

```markdown
## [Project Name]: Task Breakdown

Objective:  [One sentence]
Timeline:   [Duration]

### Tasks
1. [ ] [Task 1]. [Estimate]
2. [ ] [Task 2]. [Estimate]
3. [ ] [Task 3]. [Estimate]

Total estimate: [Sum]
Dependencies:   [Key dependencies]
```

### Standard plan format

```markdown
## Project Plan: [Name]

Objective: [Clear goal]
Timeline:  [Start] to [End]
Owner:     [Responsible party]

---

### Scope
[In scope / Out of scope]

### Work breakdown
| Phase | Task   | Estimate | Owner | Dependencies |
|-------|--------|----------|-------|--------------|
| 1     | [Task] | [Est]    | [Who] | [Deps]       |

### Timeline
[Week-by-week or milestone view]

### Risks
| Risk     | Likelihood | Impact | Mitigation       |
|----------|------------|--------|------------------|
| [Risk 1] | H/M/L      | H/M/L  | [Action]         |

### Success criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### Comprehensive roadmap format

```markdown
## Roadmap: [Initiative Name]

Vision:       [What success looks like]
Timeline:     [Quarters / Months]
Stakeholders: [Key parties]

---

### Executive summary
[2-3 paragraph overview]

### Phases

#### Phase 1: [Name]. [Dates]

Objective: [Goal]
Key deliverables:
- [Deliverable 1]
- [Deliverable 2]
Milestone: [Phase completion criteria]
Resources: [Required]
Risks:     [Phase-specific risks]

[Repeat for each phase]

### Dependencies & critical path
[Visualization and explanation]

### Risk register
[Full risk assessment]

### Resource requirements
[People, time, tools]

### Success metrics
[How we measure success]

### Decision points
[Key decisions and timing]
```

---

## Prioritization frameworks

### MoSCoW

| Priority | Meaning | Guidance |
|---|---|---|
| Must have | Critical, non-negotiable | Project fails without these |
| Should have | Important, high value | Include if possible |
| Could have | Nice to have | Include if time permits |
| Won't have | Out of scope for now | Explicitly deferred |

### Impact/Effort matrix

```
          │ Low Effort │ High Effort │
──────────┼────────────┼─────────────┤
High      │ Quick Wins │ Major       │
Impact    │ (Do First) │ Projects    │
──────────┼────────────┼─────────────┤
Low       │ Fill-ins   │ Avoid       │
Impact    │            │ (or defer)  │
```

### Value vs complexity

- Plot items on a 2x2 grid.
- Prioritize high-value, low-complexity.
- Question high-complexity, low-value items.

---

## Vault-side planning (Hypatia-specific)

Plans that involve the TabulaJacqueliana vault should be filed as Slopes / Trails / Steps under a relevant Mountain, per `hypatia-kb/protocols/librarian-note-schemas.md § Mountains PM hierarchy`. The plan goes in a Document attached to the Slope; not in a chat message.

For Hypatia development plans (this codebase), use `docs/` for the planning artifacts (e.g., this repo's `Hypatia Build Plan.md` and `hypatia-build-plan-addendum.md`). Decision-log entries go in `docs/open-questions.md` as Q-N entries.

For planning that surfaces inbox-worthy content (capture-able patterns, decisions, anti-preferences), file an inbox capture per Q-22 alongside the plan.

---

## Anti-Patterns

### Planning

- Planning without clear objective.
- Skipping scope definition.
- Tasks too large to track ("build the system").
- Ignoring dependencies.
- No risk consideration.
- Over-planning (analysis paralysis).
- Under-planning (winging it).

### Estimation

- Single-point estimates for uncertain work.
- Estimating under pressure to please.
- Not accounting for meetings, reviews, rework.
- Treating estimates as promises.

---

## Quality checklist

Before delivering a plan:

- [ ] Objective clearly stated.
- [ ] Scope defined (in and out).
- [ ] Tasks decomposed to actionable size (1-5 days).
- [ ] Estimates provided with basis.
- [ ] Dependencies identified.
- [ ] Critical path understood.
- [ ] Risks identified with mitigations.
- [ ] Timeline realistic with buffer.
- [ ] Success criteria defined.
- [ ] Stakeholders identified.
- [ ] Vault impact noted if applicable (Mountain/Slope filing).
- [ ] Inbox captures drafted for any noteworthy decisions or patterns (Q-22).

---

## Cross-references

- **Decision Engine + Route F (analysis-heavy planning)**: `.clinerules/11-decision-routes.md`
- **Cognitive stance (planning engages CSP + OBSERVE→QUESTION→DEDUCE for unknowns)**: `.clinerules/06-cognitive.md`
- **Research feeding into planning**: `research-protocol.md`
- **Writing the plan into a formal document**: `writing-protocol.md`
- **Mountain/Slope/Trail/Step hierarchy (vault PM filing)**: `hypatia-kb/protocols/librarian-note-schemas.md § Mountains PM hierarchy`
- **Inbox capture for plan-surfaced decisions**: `inbox/SCHEMA.md`
- **Save command (plan checkpoints)**: `.clinerules/08-save-command.md`

---

*Plans are hypotheses about the future. Build them thoughtfully, revisit them regularly, and adapt as reality unfolds.*
