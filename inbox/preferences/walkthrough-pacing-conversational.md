---
observed: 2026-05-27
source-session: sandboxed_claude — OYM codebase walkthrough
candidate-type: preference
confidence: high
status: new
---

## What I observed

During a multi-file code walkthrough across three repos (AI-Coach, Progress-Monitoring, Progress-MonitoringFront), AJ chose "line-by-line walkthrough" depth. I responded with a single ~3000-word explanation of one file (`utils/settings.py`) covering all sections at once. AJ interrupted and corrected:

> "I'm going to open each file and read along with you. Give me the file name, confirm I've opened it, point me to the lines, and then give me an explanation. Confirm I understand, then move on to the next section of lines in the code with explanation. This should be a conversation, not a wall of text from you."

The correction is about **pacing**, not content. The information density was fine; the unit of delivery was wrong.

## How I'd codify it

User preference for **interactive, paced code walkthroughs**:

When walking through code with AJ, default to a turn-based loop, not a monologue:

1. State the file name.
2. **Wait for AJ to confirm she has it open.**
3. Point to a specific line range (e.g. "lines 16–24").
4. Explain that section.
5. **Wait for AJ to confirm understanding** (or ask questions).
6. Advance to the next section on her cue.

One section per assistant turn. Never deliver a whole file in one response when she's chosen line-by-line mode. The shape of the conversation is more important than getting all the explanation out — AJ wants to read along in real time, not chase a wall of text.

This applies to: codebase tours, "explain this script," didactic walkthroughs, line-by-line code review when she's reading along. It does NOT apply to: targeted Q&A, one-shot debugging answers, or summaries she's explicitly asked for.

## Confidence rationale

High. Explicit correction with exact prescription of the desired protocol, delivered as an interruption to a violating response. Also asked it be saved as a durable preference in both CLAUDE memory and Hypatia inbox — signals durability beyond this session.

## Related captures

(First on this topic.)
