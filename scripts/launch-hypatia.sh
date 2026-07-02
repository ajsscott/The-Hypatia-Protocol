#!/usr/bin/env bash
# launch-hypatia.sh — one-command Hypatia session.
#
# Does the full pre-flight, then drops into the interactive Goose session:
#   1. Ollama reachable (errors with the fix if not — we don't manage it)
#   2. think-shim on :11435 (starts it if absent; stops it on exit if we
#      started it; leaves it alone if it was already running)
#   3. hypatia-gemma4 model present
#   4. regenerate system-prompt.md + hypatia-recipe.yaml from the kernel
#   5. goose run --recipe ... --interactive
#
# Suggested alias (add to ~/.zshrc):
#   alias hypatia='"$HOME"/GitHub/other/The-Hypatia-Protocol/scripts/launch-hypatia.sh'
#
# `hypatia`      — full model (grows, heavy curation)
# `hypatia lite` — E4B light-burst tier (chat, PM, vault Q&A)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HYPATIA_REPO_ROOT="$REPO_ROOT"

OLLAMA_URL="${OLLAMA_UPSTREAM:-http://127.0.0.1:11434}"
SHIM_PORT="${SHIM_PORT:-11435}"
SHIM_URL="http://127.0.0.1:${SHIM_PORT}"
STATE_DIR="${HOME}/.hypatia"
SHIM_LOG="$STATE_DIR/think-shim.log"

MODE="${1:-full}"
if [[ "$MODE" == "lite" ]]; then
  MODEL="$(sed -n 's/^  lite_model: //p' "$REPO_ROOT/hypatia.config.yaml" | head -1)"
  RECIPE_FILE="$REPO_ROOT/goose-config/hypatia-lite-recipe.yaml"
else
  MODEL="$(sed -n 's/^  design_target_model: //p' "$REPO_ROOT/hypatia.config.yaml" | head -1)"
  RECIPE_FILE="$REPO_ROOT/goose-config/hypatia-recipe.yaml"
fi

# 1. Ollama up?
if ! curl -sf --max-time 3 "$OLLAMA_URL/api/version" >/dev/null; then
  echo "ERROR: Ollama not reachable at $OLLAMA_URL — start it first (ollama serve," >&2
  echo "or the menu-bar app). Tip: OLLAMA_KEEP_ALIVE=1h keeps the model resident." >&2
  exit 1
fi

# 2. Shim up? Start it if not; only stop it on exit if we started it.
started_shim=""
if ! curl -sf --max-time 3 "$SHIM_URL/api/version" >/dev/null; then
  mkdir -p "$STATE_DIR"
  python3 "$REPO_ROOT/scripts/ollama-think-shim.py" >>"$SHIM_LOG" 2>&1 &
  started_shim="$!"
  for _ in $(seq 1 20); do
    curl -sf --max-time 1 "$SHIM_URL/api/version" >/dev/null && break
    sleep 0.25
  done
  if ! curl -sf --max-time 1 "$SHIM_URL/api/version" >/dev/null; then
    echo "ERROR: think-shim failed to start; see $SHIM_LOG" >&2
    exit 1
  fi
  echo "think-shim started on :$SHIM_PORT (log: $SHIM_LOG)"
fi
cleanup() {
  if [[ -n "$started_shim" ]]; then
    kill "$started_shim" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# 3. Model present?
if ! curl -sf --max-time 3 "$OLLAMA_URL/api/tags" | grep -q "$MODEL"; then
  echo "ERROR: model '$MODEL' not found in Ollama. Build it with:" >&2
  echo "  ollama create $MODEL -f $REPO_ROOT/goose-config/$MODEL.Modelfile" >&2
  exit 1
fi

# 4. Kernel → prompt + recipe (fast, deterministic; guarantees no drift
#    between an edited kernel and the session that follows).
"$REPO_ROOT/goose-config/regen-system-prompt.sh" >/dev/null
echo "recipe current (model: $MODEL)"

# 5. Session. cwd is the PARENT of repo + vault: Goose hands the session
#    cwd to MCP servers as the filesystem root, overriding the recipe's
#    two-directory args (live finding 2026-07-02 — vault was unreachable).
#    Boundary is wider than repo+vault until the Phase 2 vault-rw server
#    restores the tight bound.
cd "$(dirname "$REPO_ROOT")"
goose run --recipe "$RECIPE_FILE" --interactive
