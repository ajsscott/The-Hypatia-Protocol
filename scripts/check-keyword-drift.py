#!/usr/bin/env python3
"""check-keyword-drift.py — enforce alignment between Hypatia's keyword map
and each protocol's declared `**Trigger Keywords**:` line.

The kernel file `.roo/rules-hypatia/10-skills-loading.md` is the single
source of truth for which user-input keywords route to which protocol.
Each protocol file ALSO declares its trigger keywords at the top. The two
must match. Drift between them is the bug class that motivated the Phase 1
lint gate (addendum landmine #12, 2026-04-22).

Exit codes:
    0  — keyword map and all protocol declarations aligned
    1  — drift detected (kernel diff vs protocol diff per file)
    2  — parse error / missing files

Invocation:
    python3 scripts/check-keyword-drift.py
    uv run python scripts/check-keyword-drift.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_MAP = REPO_ROOT / ".roo/rules-hypatia/10-skills-loading.md"

KEYWORD_LINE_RE = re.compile(
    r"^\*\*(?:Trigger )?Keywords\*\*\s*:\s*(.+?)\s*$"
)
SECTION_HEADER_RE = re.compile(r"^###\s+.+?`(?P<path>[^`]+)`\)")
TABLE_ROW_RE = re.compile(
    r"^\|\s*`(?P<file>[^`]+)`\s*\|\s*(?P<keywords>[^|]+?)\s*\|"
)


def parse_keyword_set(raw: str) -> set[str]:
    return {k.strip() for k in raw.split(",") if k.strip()}


def parse_kernel_map(kernel_path: Path) -> dict[Path, set[str]]:
    """Return {absolute protocol path: keyword set} parsed from the kernel map.

    Section headers like `### Librarian protocols (`hypatia-kb/protocols/`)`
    establish the base directory for the table that follows. Table rows like
    `| `librarian-role.md` | kw1, kw2 |` map filenames to keyword lists.
    Globs in the base path (e.g., `hypatia-kb/*-protocol.md`) are treated as
    "base dir + literal filename from the table row".
    """
    out: dict[Path, set[str]] = {}
    current_base: str | None = None
    for line in kernel_path.read_text().splitlines():
        header = SECTION_HEADER_RE.match(line)
        if header:
            current_base = header.group("path")
            continue
        if current_base is None:
            continue
        row = TABLE_ROW_RE.match(line)
        if not row:
            continue
        filename = row.group("file")
        if "*" in current_base:
            base_dir = REPO_ROOT / current_base.rsplit("/", 1)[0]
        else:
            base_dir = REPO_ROOT / current_base.rstrip("/")
        full = (base_dir / filename).resolve()
        out[full] = parse_keyword_set(row.group("keywords"))
    return out


def parse_protocol_keywords(protocol_path: Path) -> set[str] | None:
    """Return the protocol file's declared keyword set, or None if no
    `**Trigger Keywords**:` (or `**Keywords**:`) line in the first 30 lines.
    """
    if not protocol_path.exists():
        return None
    for line in protocol_path.read_text().splitlines()[:30]:
        m = KEYWORD_LINE_RE.match(line)
        if m:
            return parse_keyword_set(m.group(1))
    return None


def diff_report(kernel: dict[Path, set[str]]) -> tuple[int, str]:
    """Compare kernel map to each protocol's declaration. Return (exit_code, report)."""
    missing: list[Path] = []
    no_declaration: list[Path] = []
    drift: list[tuple[Path, set[str], set[str]]] = []
    for proto_path, kernel_kws in kernel.items():
        if not proto_path.exists():
            missing.append(proto_path)
            continue
        proto_kws = parse_protocol_keywords(proto_path)
        if proto_kws is None:
            no_declaration.append(proto_path)
            continue
        if proto_kws != kernel_kws:
            drift.append((proto_path, kernel_kws - proto_kws, proto_kws - kernel_kws))
    lines = []
    if not (missing or no_declaration or drift):
        lines.append(f"OK: {len(kernel)} protocols aligned with kernel keyword map.")
        return 0, "\n".join(lines)
    lines.append("DRIFT DETECTED in keyword map vs protocol declarations.")
    if missing:
        lines.append(f"\nMISSING files ({len(missing)}):")
        for p in missing:
            lines.append(f"  {p.relative_to(REPO_ROOT)}")
    if no_declaration:
        lines.append(f"\nMISSING **Trigger Keywords**: line ({len(no_declaration)}):")
        for p in no_declaration:
            lines.append(f"  {p.relative_to(REPO_ROOT)}")
    if drift:
        lines.append(f"\nKEYWORD DRIFT ({len(drift)} protocols):")
        for p, only_kernel, only_proto in drift:
            lines.append(f"  {p.relative_to(REPO_ROOT)}")
            if only_kernel:
                lines.append(f"    only in kernel map: {sorted(only_kernel)}")
            if only_proto:
                lines.append(f"    only in protocol:   {sorted(only_proto)}")
    return 1, "\n".join(lines)


def main() -> int:
    if not KERNEL_MAP.exists():
        print(f"ERROR: kernel map not found at {KERNEL_MAP}", file=sys.stderr)
        return 2
    kernel = parse_kernel_map(KERNEL_MAP)
    if not kernel:
        print(
            f"ERROR: parsed zero protocols from {KERNEL_MAP}; check section "
            "headers (### Foo (`path/`)) and table row format.",
            file=sys.stderr,
        )
        return 2
    code, report = diff_report(kernel)
    print(report)
    return code


if __name__ == "__main__":
    sys.exit(main())
