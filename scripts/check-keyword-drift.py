#!/usr/bin/env python3
"""check-keyword-drift.py — enforce alignment across the three places a
protocol's trigger keywords live, and that every MCP URI the kernel cites
is actually served.

The canonical keyword map lives at
`docs/reference/phase-1-kernel-archive/10-skills-loading.md` (post Phase
1.5 Q-33 kernel redistribution; was previously `.roo/rules-hypatia/`).
Three checks:

  1. Canonical map ↔ each protocol's `**Trigger Keywords**:` line
     (the original Phase 1 gate; addendum landmine #12, 2026-04-22).
  2. Canonical map ↔ the always-loaded routing table in
     `kernel/04-routing.md` (the check the Q-33 design doc mandated;
     its absence let the kernel table silently drop keywords).
  3. Every `protocol://` URI mentioned anywhere in `kernel/*.md` must be
     served by the MCP server (protocol stems on disk + `detail/*` topics
     declared in mcp-servers/protocols/src/main.rs).

At runtime, Hypatia's protocols MCP server serves the canonical map as
`protocol://detail/skills-map`. Goose's MCP host consults it when
deciding which protocol resource to load on keyword match.

Exit codes:
    0  — all three checks aligned
    1  — drift detected
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
# Canonical keyword map (post Q-33 redistribution).
KERNEL_MAP = REPO_ROOT / "docs/reference/phase-1-kernel-archive/10-skills-loading.md"
# Always-loaded compact kernel (Q-33). 04 carries the routing table.
KERNEL_DIR = REPO_ROOT / "kernel"
ROUTING_TABLE = KERNEL_DIR / "04-routing.md"
PROTOCOLS_DIR = REPO_ROOT / "hypatia-kb/protocols"
MCP_MAIN_RS = REPO_ROOT / "mcp-servers/protocols/src/main.rs"

KEYWORD_LINE_RE = re.compile(
    r"^\*\*(?:Trigger )?Keywords\*\*\s*:\s*(.+?)\s*$"
)
SECTION_HEADER_RE = re.compile(r"^###\s+.+?`(?P<path>[^`]+)`\)")
TABLE_ROW_RE = re.compile(
    r"^\|\s*`(?P<file>[^`]+)`\s*\|\s*(?P<keywords>[^|]+?)\s*\|"
)
# kernel/04-routing.md table rows: | kw1, kw2 | `protocol://uri` |
ROUTING_ROW_RE = re.compile(
    r"^\|\s*(?P<keywords>[^|`]+?)\s*\|\s*`protocol://(?P<uri>[^`]+)`\s*\|"
)
URI_MENTION_RE = re.compile(r"protocol://[A-Za-z0-9_/-]+")
DETAIL_TOPIC_RE = re.compile(r'"(detail/[A-Za-z0-9-]+)"')


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


def parse_routing_table(routing_path: Path) -> dict[str, set[str]]:
    """Return {MCP URI suffix: keyword set} from kernel/04-routing.md's
    `| keywords | \\`protocol://uri\\` |` table rows."""
    out: dict[str, set[str]] = {}
    for line in routing_path.read_text().splitlines():
        row = ROUTING_ROW_RE.match(line)
        if not row:
            continue
        keywords = row.group("keywords")
        if keywords.strip().lower().startswith("keywords"):  # header row
            continue
        out[row.group("uri")] = parse_keyword_set(keywords)
    return out


def served_uris() -> set[str]:
    """Return every URI suffix the MCP server serves: protocol filename stems
    scanned from disk (mirrors main.rs's walkdir) + `detail/*` topics declared
    in main.rs."""
    uris = {
        p.stem
        for p in PROTOCOLS_DIR.glob("*.md")
        if p.name != "README.md"
    }
    uris.update(DETAIL_TOPIC_RE.findall(MCP_MAIN_RS.read_text()))
    return uris


def routing_table_report(
    kernel: dict[Path, set[str]], routing: dict[str, set[str]]
) -> tuple[int, str]:
    """Check 2: kernel/04-routing.md table must carry the canonical keyword
    set for every protocol, exactly. Extra rows are allowed only for
    `detail/*` resources (Phase 1.5 kernel additions with no archive row)."""
    problems: list[str] = []
    canonical = {path.stem: kws for path, kws in kernel.items()}
    for stem, kws in sorted(canonical.items()):
        if stem not in routing:
            problems.append(f"  missing routing-table row: protocol://{stem}")
            continue
        if routing[stem] != kws:
            only_canonical = kws - routing[stem]
            only_routing = routing[stem] - kws
            problems.append(f"  protocol://{stem}")
            if only_canonical:
                problems.append(f"    only in canonical map: {sorted(only_canonical)}")
            if only_routing:
                problems.append(f"    only in routing table: {sorted(only_routing)}")
    for uri in sorted(routing):
        if uri not in canonical and not uri.startswith("detail/"):
            problems.append(
                f"  routing-table row with no canonical-map entry: protocol://{uri}"
            )
    if problems:
        header = "ROUTING TABLE DRIFT (kernel/04-routing.md vs canonical map):"
        return 1, "\n".join([header, *problems])
    return 0, f"OK: routing table aligned with canonical map ({len(canonical)} protocols)."


def uri_liveness_report(served: set[str]) -> tuple[int, str]:
    """Check 3: every protocol:// URI mentioned in kernel/*.md must be served."""
    dangling: list[str] = []
    for kernel_file in sorted(KERNEL_DIR.glob("*.md")):
        for uri in URI_MENTION_RE.findall(kernel_file.read_text()):
            suffix = uri.removeprefix("protocol://")
            if suffix not in served:
                dangling.append(f"  {kernel_file.name}: {uri}")
    if dangling:
        header = "DANGLING URIs (mentioned in kernel/, not served by MCP server):"
        return 1, "\n".join([header, *dangling])
    return 0, f"OK: all kernel-cited URIs are served ({len(served)} resources available)."


def main() -> int:
    for required in (KERNEL_MAP, ROUTING_TABLE, PROTOCOLS_DIR, MCP_MAIN_RS):
        if not required.exists():
            print(f"ERROR: required path not found: {required}", file=sys.stderr)
            return 2
    kernel = parse_kernel_map(KERNEL_MAP)
    if not kernel:
        print(
            f"ERROR: parsed zero protocols from {KERNEL_MAP}; check section "
            "headers (### Foo (`path/`)) and table row format.",
            file=sys.stderr,
        )
        return 2
    routing = parse_routing_table(ROUTING_TABLE)
    if not routing:
        print(
            f"ERROR: parsed zero rows from {ROUTING_TABLE}; check "
            "`| keywords | `protocol://uri` |` row format.",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for code, report in (
        diff_report(kernel),
        routing_table_report(kernel, routing),
        uri_liveness_report(served_uris()),
    ):
        print(report)
        exit_code = max(exit_code, code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
