---
observed: 2026-09-17
source-session: host Claude Code — AI-Coach repo sweep + aj.local/docs read-through
candidate-type: pattern
confidence: high
status: new
---

## What I observed

Across every analysis plan in `aj.local/docs/plans/` (Experiment B v1/v2, the RQ1 classification plan, the RQ1–3 options doc) AJ states hypotheses, priors, thresholds, and the exact inference set *before* running anything, then records changes as dated amendments in the same file rather than rewriting. Examples in her words: "Written per-question, before looking at the data"; "Named priors turn each result into a comparison … rather than a Rorschach test"; "The pre-specified inference set is exactly: 3 criterion tiers × 2 layers + 2 Steiger contrasts. Everything else is labeled sensitivity/descriptive. No p-hacking surface." The same discipline extends to modeling: "Before anyone writes Stan/PyMC code, simulate the design at our ns and cadences and check the posterior on B is narrower than the prior" — a 100-fit power gate was run before the first real fit. Reliability gates for new measures are declared in the notebook intro before results appear.

## How I'd codify it

Pattern: AJ pre-registers. For any empirical question she writes the question, the prior, the falsification threshold, and the exact set of tests first; results are appended as dated amendments, never edited in place; anything outside the registered set is labeled exploratory. Before fitting a complex model she runs a simulation gate on the real design matrix and treats a fail as decisive, a pass as necessary-not-sufficient. Supersession is marked at the top of the old document, which is kept as the reasoning record.

## Confidence rationale

High. Recurs in at least six documents over July–September 2026, stated explicitly as method, and enforced in code (notebooks fail loudly on pre-fix data; gates stated before results). Consistent with the existing capture on reading raw sources herself.

## Related captures

[[reading-raw-sources-herself]] · [[ground-truth-verification-protocol]] · [[observational-claims-language-rules]]
