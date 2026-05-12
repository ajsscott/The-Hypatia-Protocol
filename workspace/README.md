# workspace/

Hypatia's per-machine scratch space. Not tracked except for this README.

Use this directory for:

- Logs Hypatia writes during sessions (not shipped, not curated)
- Draft markdown awaiting Scholar review before promotion to the vault or to `inbox/`
- Queued ingest payloads (Phase 2 watcher staging area)
- Throwaway artifacts from experiments

**This is not a Memory store.** Anything that should outlast a session and
inform future Hypatia behavior goes to:

- `inbox/preferences/` — free-form markdown for Scholar consolidation
- `hypatia-kb/Memory/memory.json` — canonical (Scholar-curated only)
- `hypatia-kb/Intelligence/*.json` — canonical (Scholar-curated only)

The `workspace/` contents are gitignored. Don't put anything here you
expect to recover after a clean checkout.
