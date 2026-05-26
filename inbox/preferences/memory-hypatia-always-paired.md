---
observed: 2026-05-19
source-session: renphil-tact-scripts — error handling refactor
candidate-type: preference
confidence: high
status: new
---

## What I observed

After I wrote a feedback memory without a corresponding Hypatia capture, AJ said:
"what you wrote to memory. anytime you write to memory, automatically write to hypatia too."

## How I'd codify it

Any time a memory is written to the project-scoped memory store, automatically write a
paired Hypatia capture in the same response. Do not wait to be asked. The two stores
serve different purposes (project-scoped vs. cross-project personal assistant), but
observations worth keeping in one are almost always worth keeping in both.

## Confidence rationale

High. AJ stated this explicitly as a standing rule, not a one-time request.
