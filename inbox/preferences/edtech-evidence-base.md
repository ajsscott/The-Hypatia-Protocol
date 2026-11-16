---
observed: 2026-10-26
source-session: scratch workspace — global Claude config update
candidate-type: knowledge
confidence: high
status: new
---

## What I observed

AJ asked to update her global Claude settings "to know about and use" the
Renaissance AI and Education Resource Hub
(https://jchoi92k.github.io/Learning-Engineering-Resource-Hub/) "when
designing and other tasks." When offered the choice, she picked the full
integration: a CLAUDE.md research rule plus registering the hub's MCP server
(`renaissance-hub`, semantic search over ~3,900 curated K-12/higher-ed
resources from WWC, Evidence for ESSA, Mathematica, LPI, WestEd) at user
scope, with llms.txt/data.json fetch as fallback.

## How I'd codify it

AJ's evidence base for education-domain work is the Renaissance AI and
Education Resource Hub. Assistants should ground edtech design and
recommendations in this corpus rather than general knowledge, treat it as a
citation index (follow through to the underlying paper/report and cite
that), and prefer its semantic-search MCP endpoint over raw fetches.

## Confidence rationale

High. Explicit request plus an explicit "both" choice when offered lighter
integrations. Could drift if the hub (beta, built for tools-competition.org)
goes stale or its worker endpoint dies — the fallback note covers that.

## Related captures

(First on this topic.)
