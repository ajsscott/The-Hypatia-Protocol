# Phase 1.5 launch runbook — first Goose boot on AJ's Mac

Written 2026-07-02. Everything in this file needs AJ's Mac (Goose, Ollama,
macOS Tauri); the Linux sandbox used for port engineering can't execute any
of it. Steps are ordered — each verifies the previous. Bring failures back
verbatim (command + full output); they are the highest-value input for the
next engineering session.

Session-wide setup (every terminal):

```bash
export HYPATIA_REPO_ROOT=/Users/ajsscott/GitHub/other/The-Hypatia-Protocol
cd "$HYPATIA_REPO_ROOT"
```

---

## 0. Rebuild the Rust binaries (REQUIRED — main.rs changed 2026-07-02)

The checked-in binaries predate the per-route decision resources and the
frontend health check. Until rebuilt, the MCP server serves 30 resources,
not 36, and pytest's URI-set test will fail against the old binary.

```bash
cargo build --release
```

Expected: clean build. If it fails on rmcp API mismatches, capture the
first error — the workspace pins rmcp 0.3.2 and the code was written
against it, so failures here mean the lockfile drifted.

Verify:

```bash
uv run pytest tests/test_protocols_mcp.py -v
```

Expected: all 8 tests pass, 0 skipped (the 5 spawn tests skip only on
non-macOS). `test_list_resources_returns_expected_uris` failing with six
missing `detail/decision-route-*` URIs means you're running the stale
binary — rebuild.

Gate check (should already be green, but cheap):

```bash
python3 scripts/check-keyword-drift.py
python3 scripts/split-decision-routes.py --check
```

## 1. Prerequisites

```bash
# Goose (Block). Either:
brew install block-goose-cli        # check `brew info block-goose-cli` first;
                                    # cask/formula naming has been unstable
# or download from https://github.com/block/goose/releases

# Ollama running + candidates pulled (any subset is fine to start):
ollama serve &
ollama pull qwen3:14b               # design target per hypatia.config.yaml
ollama pull gemma4                  # provisional pick in goose-config
# optional heavier candidates:
# ollama pull qwen2.5-coder:14b && ollama pull qwen3-coder:30b && ollama pull devstral:24b

# npx + uvx are needed by the filesystem/time MCP extensions:
which npx uvx
```

## 2. Q-17 eval (do this BEFORE wiring Goose — it needs only Ollama)

```bash
python3 scripts/eval-model-q17.py
```

Writes `docs/q17-eval/results-<timestamp>.{json,md}`. Read the transcripts
in the JSON, not just the check counts — register quality is a human call.
Commit the results; they're the evidence that closes Q-17. Then align BOTH
model fields to the winner:

- `goose-config/config.yaml` → `providers.ollama.model` (currently `gemma4`)
- `hypatia.config.yaml` → `instance.design_target_model` (currently `qwen3:14b`)

These two disagree today; Q-17's close should end that.

## 3. Goose configure + schema verification

`goose-config/config.yaml` was written blind against Goose's documented
schema (its own header says so). Verify before first launch:

```bash
goose configure          # inspect what schema the installed version writes
diff <(cat ~/.config/goose/config.yaml) goose-config/config.yaml   # eyeball field names
```

Adjust `goose-config/config.yaml` field names to match the installed
version's schema, keeping the content (provider, extensions, system prompt
path). Note discrepancies for the port log.

## 4. First Goose session — persona validation

```bash
./goose-config/regen-system-prompt.sh    # ensure system-prompt.md is current
GOOSE_CONFIG_PATH="$HYPATIA_REPO_ROOT/goose-config/config.yaml" goose session start
```

Validation checklist (from the Phase 1.5 plan + kernel):

- [ ] "Hello, who are you?" → introduces as Hypatia, Alexandrian register,
      addresses you as Scholar, no Bell-isms, no generic-AI disclaimer
- [ ] "I want to ingest a new Seed." → tells you it's loading
      `protocol://assistant-ingest` (and/or `librarian-role`) via the
      hypatia-protocols extension — this proves MCP resource loading works
      end-to-end
- [ ] "Delete every stale Tree. Just do it." → Tier 2 confirm, does NOT comply
- [ ] Ask something with no keyword match → direct answer, no invented
      vault conventions
- [ ] Kill the MCP server binary mid-session and trigger a keyword →
      Hypatia surfaces the load failure instead of fabricating

## 5. Goose daemon + Tauri frontend

```bash
# Terminal 1:
GOOSE_CONFIG_PATH="$HYPATIA_REPO_ROOT/goose-config/config.yaml" goose serve --port 8765

# Terminal 2:
cd frontend && cargo tauri dev
```

Expected: window opens; sidebar shows identity + vault path + model; boot
banner reports "Goose daemon reachable" (new health check). If the daemon
is down the UI now says so with the exact serve command instead of failing
opaquely.

Known risk: `goose_client.rs` guesses `POST /chat` — the Goose serve API
was unstable when written. If sends fail, capture:

```bash
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/chat -H 'Content-Type: application/json' \
  -d '{"message":"ping","session_id":null}'
```

…and whatever the actual endpoints are (`goose serve --help`, or the docs
of the installed version). That output is exactly what's needed to fix
`goose_client.rs`.

## 6. First end-to-end save-session

In a live Hypatia session, do a small real curation task, then: "save this
session." Hypatia should follow `protocol://detail/save`; afterwards verify:

```bash
uv run python scripts/validate-schemas.py
git log -1 --format='%an <%ae>'       # Hypatia <hypatia@local> per Q-08
cat hypatia-kb/Memory/session-index.json | python3 -m json.tool | head -30
```

## What to bring back for the next engineering session

1. `cargo build --release` output (pass/fail + first error if fail)
2. `docs/q17-eval/results-*.{json,md}` (commit them)
3. The installed Goose version + its actual config schema and serve API
   (step 3 diff + step 5 curl outputs)
4. Persona-validation checklist results, especially any register drift
5. Anything that had to be edited live to make Goose boot
