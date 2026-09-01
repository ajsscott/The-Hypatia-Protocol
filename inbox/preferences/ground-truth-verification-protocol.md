---
observed: 2026-08-26
source-session: host Claude Code — ers-contract-explorer, benchmark ground-truth labeling
candidate-type: pattern
confidence: high
status: new
---

## What I observed

AJ redesigned a manual labeling task mid-flight: "If all I'm doing is verifying page numbers in the document, you're going to tell me where you think each number is one by one, and I'm going to verify, and then you put the number in the csv." She then sustained that propose→human-verify→scribe loop across 22 documents in one sitting, moving fast on confirmations and pushing back only where her eyes disagreed with the evidence (Boston p124, Malden p41). She kept the human-judgment step for herself but delegated all candidate-generation and record-keeping.

## How I'd codify it

For ground-truth or verification work, AJ's preferred division of labor: assistant proposes each item with the evidence for it, AJ verifies with her own eyes, assistant writes the record. She will not page through documents cold, but she also won't rubber-stamp — discrepancies between the assistant's evidence and her observation get resolved explicitly, in her favor only after re-checking. Batch friction (per-item permission asks) kills the flow; a single up-front protocol agreement plus a running tally works.

## Confidence rationale

High. Explicit protocol statement in her own words, then sustained across ~22 iterations with corrections in both directions (she caught label errors; the evidence caught her viewer/page-number slips). Consistent with her existing supervise-mode rule (she authors, Claude reviews) — this is its inverse for data work: Claude drafts, she authorizes.

## Related captures

(First on this topic.)
