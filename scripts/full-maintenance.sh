#!/bin/bash
# Unified System Maintenance Script (Mac-only)
#
# Wraps python-maintenance.sh as the single maintenance phase Hypatia ships
# with on Mac. Bell's original had additional phases for Kiro cleanup, WSL
# cleanup, and VHDX compaction (Windows-specific); those were removed when
# the substrate changed to Roo Code and the platform scope narrowed to Mac.
#
# Usage:
#   ./scripts/full-maintenance.sh                       # Run Python cleanup
#   ./scripts/full-maintenance.sh --dry-run             # Preview without changing anything
#   ./scripts/full-maintenance.sh --delete-stale-venvs  # Pass through to python-maintenance.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Defaults ---
DRY_RUN=false
DELETE_STALE=false

# --- Parse flags ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --delete-stale-venvs) DELETE_STALE=true; shift ;;
        --help)
            echo "Usage: $0 [--dry-run] [--delete-stale-venvs]"
            echo ""
            echo "Mac-only system maintenance. Runs Python cleanup phase only."
            echo ""
            echo "Flags:"
            echo "  --dry-run              Preview without changing anything"
            echo "  --delete-stale-venvs   Pass --delete-stale-venvs to python-maintenance.sh"
            echo ""
            echo "Roo Code (the substrate) manages its own state via VS Code's"
            echo "extension storage; no external maintenance script is needed."
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

banner "HYPATIA SYSTEM MAINTENANCE (Mac)"
log "Mode: $( $DRY_RUN && echo 'DRY RUN' || echo 'LIVE' )"
echo ""

TOTAL_START=$(date +%s)

# Python cleanup
banner "PYTHON CLEANUP"
PY_ARGS=()
$DRY_RUN && PY_ARGS+=(--dry-run)
$DELETE_STALE && PY_ARGS+=(--delete-stale-venvs)

PY_SCRIPT="$SCRIPT_DIR/python-maintenance.sh"
if [ ! -f "$PY_SCRIPT" ]; then
    err "Script not found: $PY_SCRIPT"
    exit 1
fi

PHASE_START=$(date +%s)
if bash "$PY_SCRIPT" "${PY_ARGS[@]}"; then
    PHASE_ELAPSED=$(( $(date +%s) - PHASE_START ))
    log "Python cleanup complete (${PHASE_ELAPSED}s)"
else
    PHASE_ELAPSED=$(( $(date +%s) - PHASE_START ))
    warn "Python cleanup had errors (${PHASE_ELAPSED}s)"
fi

TOTAL_ELAPSED=$(( $(date +%s) - TOTAL_START ))
banner "MAINTENANCE COMPLETE"
log "Total time: ${TOTAL_ELAPSED}s"
