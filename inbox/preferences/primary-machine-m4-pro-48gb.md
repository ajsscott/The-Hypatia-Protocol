---
observed: 2026-10-27
source-session: host Claude Code — local coding model sizing query
candidate-type: knowledge
confidence: high
status: new
---

## What I observed

Read directly from the machine AJ ran the session on: Apple M4 Pro,
48 GB unified memory, 14 CPU cores, 20 GPU cores. AJ asked which local
model this box can carry as a primary coding model (autocomplete plus
agentic build/edit/debug) and which VS Code extension to drive it.

## How I'd codify it

AJ's primary dev machine (as of 2026-10-27): MacBook Pro, M4 Pro,
48 GB unified memory, 20-core GPU. Sizing envelope for local LLMs:
~22–33 GB of weights is comfortable (30B-class MoE at Q4–Q8, or 27B
dense at Q4); 80B-class MoE at Q4 (~45 GB) does not fit. AJ is
evaluating local models as a primary coding model in VS Code, not just
as a Hypatia substrate.

## Confidence rationale

High. Hardware read from sysctl/system_profiler, not self-report.
Supersedes the "32GB Mac" figure in [[hypatia-near-term-vision-macbook]]
unless that referred to a different machine.

## Related captures

[[hypatia-near-term-vision-macbook]]
