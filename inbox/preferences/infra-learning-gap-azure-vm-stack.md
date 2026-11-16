---
observed: 2026-11-16
source-session: sandboxed_claude — ers-contract-explorer, Azure VM deploy walkthrough
candidate-type: knowledge
confidence: high
status: new
---

# Infra learning gap: single-VM web stack (NSG, ACME/TLS, reverse proxy, OIDC proxy, managed identity, secrets)

During a nine-piece architecture walkthrough of the TRACE Azure deployment
(VM + NSG + Caddy + oauth2-proxy/Entra + container + Key Vault secrets +
deploy.sh + Entra SSH + backup/alerts), AJ answered piece 1 correctly
(SQLite WAL + in-process queue force a VM over App Service), then at piece 2
(why port 80 is open to the world for ACME HTTP-01 while 443 is CIDR-locked)
said "I have no idea", and asked for resources "where I can learn a lot more
about all these different pieces of infrastructure and how they work together".

Observation: AJ's strong model is at the application/data layer (why the
code constrains hosting). The gap is the network-and-identity layer of a
classic single-host deployment: how TLS issuance, L7 proxying, OIDC
auth-proxying, cloud instance identity, and host-level secret delivery
compose. This is consistent with her global CLAUDE.md assuming K8s/Terraform
fluency being aspirational for this specific stack rather than current.

Signal for Hypatia: when AJ asks "walk me through", expect to teach the
network/identity composition from first principles; don't assume the
ACME / reverse-proxy / instance-metadata mental models are in place.
