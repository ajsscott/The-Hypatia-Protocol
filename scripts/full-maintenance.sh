#!/bin/bash
# Unified System Maintenance Script
# Chains Phases 1-2 in the correct order. Phase 3 (VHDX compact) is a manual
# follow-up that runs from Admin PowerShell on Windows.
#
# Usage:
#   ./scripts/full-maintenance.sh                  # Run all phases
#   ./scripts/full-maintenance.sh --dry-run        # Preview all phases
#   ./scripts/full-maintenance.sh --skip-phase 2   # Skip Linux/WSL cleanup
#   ./scripts/full-maintenance.sh --delete-stale-venvs  # Pass to Python phase

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Defaults ---
DRY_RUN=false
DELETE_STALE=false
SKIP_PHASE_1=false
SKIP_PHASE_2=false

# --- Parse flags ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --delete-stale-venvs) DELETE_STALE=true; shift ;;
        --skip-phase)
            case "${2:-}" in
                1) SKIP_PHASE_1=true ;;
                2) SKIP_PHASE_2=true ;;
                *) echo "[ERROR] --skip-phase requires 1 or 2"; exit 1 ;;
            esac
            shift 2 ;;
        --help)
            echo "Usage: $0 [--dry-run] [--skip-phase N] [--delete-stale-venvs]"
            echo ""
            echo "Runs maintenance phases in order:"
            echo "  Phase 1: Python cleanup (caches, __pycache__, venv audit)"
            echo "  Phase 2: Linux/WSL cleanup + fstrim"
            echo ""
            echo "Flags:"
            echo "  --dry-run              Preview all phases without changing anything"
            echo "  --skip-phase N         Skip phase N (1 or 2)"
            echo "  --delete-stale-venvs   Pass --delete-stale-venvs to Python phase"
            echo ""
            echo "Phase 3 (VHDX compact) must be run separately from Admin PowerShell on Windows:"
            echo "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\\wsl-compact.ps1"
            echo ""
            echo "Note: Bell's original Phase 2 was Kiro cache cleanup. The Roo Code"
            echo "substrate (per substrate decision) manages its own state via VS Code's"
            echo "extension storage; no external Roo maintenance script needed."
            exit 0 ;;
        *) echo "[ERROR] Unknown flag: $1. Use --help for usage."; exit 1 ;;
    esac
done

# --- Helpers ---
BOLD="\033[1m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

banner() { echo -e "\n${BOLD}════════════════════════════════════════════════════════════${RESET}"; echo -e "${BOLD}  $1${RESET}"; echo -e "${BOLD}════════════════════════════════════════════════════════════${RESET}\n"; }
log() { echo -e "${GREEN}[MAINT]${RESET} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${RESET} $1"; }
err() { echo -e "${RED}[ERROR]${RESET} $1"; }

# --- Header ---
banner "UNIFIED SYSTEM MAINTENANCE"
log "Mode: $( $DRY_RUN && echo 'DRY RUN' || echo 'LIVE' )"
log "Phases: $( $SKIP_PHASE_1 && echo '⊘1' || echo '✓1' ) $( $SKIP_PHASE_2 && echo '⊘2' || echo '✓2' )"
echo ""

# Track timing
TOTAL_START=$(date +%s)
PHASE_RESULTS=()

run_phase() {
    local phase_num="$1"
    local phase_name="$2"
    local script="$3"
    shift 3
    local args=("$@")

    banner "PHASE $phase_num: $phase_name"

    if [ ! -f "$script" ]; then
        err "Script not found: $script"
        PHASE_RESULTS+=("Phase $phase_num: SKIPPED (script missing)")
        return 1
    fi

    local phase_start
    phase_start=$(date +%s)

    if bash "$script" "${args[@]}"; then
        local elapsed=$(( $(date +%s) - phase_start ))
        PHASE_RESULTS+=("Phase $phase_num: DONE (${elapsed}s)")
        log "Phase $phase_num complete (${elapsed}s)"
    else
        local elapsed=$(( $(date +%s) - phase_start ))
        PHASE_RESULTS+=("Phase $phase_num: FAILED (${elapsed}s)")
        warn "Phase $phase_num had errors (${elapsed}s). Continuing."
    fi
}

# ═══════════════════════════════════════════
# PHASE 1: Python Cleanup
# ═══════════════════════════════════════════
if $SKIP_PHASE_1; then
    log "Phase 1 (Python): skipped"
    PHASE_RESULTS+=("Phase 1: SKIPPED")
else
    PY_ARGS=()
    $DRY_RUN && PY_ARGS+=(--dry-run)
    $DELETE_STALE && PY_ARGS+=(--delete-stale-venvs)

    run_phase 1 "PYTHON CLEANUP" "$SCRIPT_DIR/python-maintenance.sh" "${PY_ARGS[@]}"
fi

# ═══════════════════════════════════════════
# PHASE 2: Linux/WSL Cleanup + fstrim
# ═══════════════════════════════════════════
if $SKIP_PHASE_2; then
    log "Phase 2 (Linux/WSL): skipped"
    PHASE_RESULTS+=("Phase 2: SKIPPED")
else
    WSL_ARGS=()
    $DRY_RUN && WSL_ARGS+=(--dry-run)

    run_phase 2 "LINUX/WSL CLEANUP" "$SCRIPT_DIR/wsl-maintenance.sh" "${WSL_ARGS[@]}"
fi

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════
TOTAL_ELAPSED=$(( $(date +%s) - TOTAL_START ))

banner "MAINTENANCE COMPLETE"
for result in "${PHASE_RESULTS[@]}"; do
    log "  $result"
done
log ""
log "Total time: ${TOTAL_ELAPSED}s"

# Phase 3 reminder (WSL only)
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo ""
    log "━━━ Phase 3: VHDX Compact (manual) ━━━"
    log "To reclaim disk space on Windows:"
    log "  1. Open PowerShell as Administrator"
    log "  2. Run:"
    log "     powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\\wsl-compact.ps1"
    echo ""
fi
