#!/usr/bin/env python3
"""export-intelligence-to-markdown.py — render JSON stores as Dataview-queryable
markdown.

Reads `hypatia-kb/Intelligence/{patterns,knowledge,reasoning}.json` and the
curated stanzas of `hypatia-kb/Memory/memory.json`. Writes four markdown
files under `hypatia-kb/exports/` with top-level YAML frontmatter for the
export itself + per-entry inline Dataview fields (`field:: value`).

The export directory is gitignored — regenerated per-machine after every
save-session (kernel `.roo/rules-hypatia/08-save-command.md` § Step 5
should invoke this script as part of the post-write sequence; wiring lives
in save-session.py or downstream).

Format choice: one file per store, inline DV-fields. Dataview reads inline
fields throughout the body; this preserves the JSON store as canonical
while letting the Scholar query the same content from inside Obsidian.

Idempotency: identical JSON in → identical markdown out. Entries iterated
in sorted-by-id order; lists rendered with stable ordering.

Exit codes:
    0 — exports written cleanly
    1 — at least one store failed to render (other stores still written)
    2 — fatal (missing source JSON, malformed structure)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
KB = REPO_ROOT / "hypatia-kb"
EXPORTS = KB / "exports"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def fmt_inline_field(key: str, val: Any) -> str:
    """Render a single inline Dataview field. Lists become bracketed."""
    if isinstance(val, list):
        return f"- **{key}**:: [{', '.join(str(v) for v in val)}]"
    if isinstance(val, bool):
        return f"- **{key}**:: {'true' if val else 'false'}"
    return f"- **{key}**:: {val}"


def render_entry(entry: dict[str, Any], heading_field: str) -> str:
    """Render one store entry as a ## section + inline DV fields + content quote."""
    eid = entry.get("id", "unknown")
    label = entry.get(heading_field, "")
    title = f"## {eid}" + (f" [{label}]" if label else "")
    fields = []
    skip = {"id", "content", "_history"}
    for key in sorted(entry.keys()):
        if key in skip:
            continue
        fields.append(fmt_inline_field(key, entry[key]))
    content = entry.get("content", "").strip()
    body = "\n".join(fields)
    if content:
        body += "\n\n> " + content.replace("\n", "\n> ")
    return f"{title}\n\n{body}\n"


def render_store(
    store_name: str, json_path: Path, heading_field: str, dataview_type: str
) -> str:
    data = load_json(json_path)
    entries = sorted(data.get("entries", []), key=lambda e: e.get("id", ""))
    frontmatter = [
        "---",
        f"type: {dataview_type}",
        f"source: {json_path.relative_to(REPO_ROOT)}",
        f"generated: {now_utc()}",
        f"count: {len(entries)}",
        f"store_last_updated: {data.get('lastUpdated', 'unknown')}",
        "---",
        "",
        f"# {store_name.title()} Export",
        "",
        f"*Generated from `{json_path.relative_to(REPO_ROOT)}`. Do not edit "
        "directly — the JSON store is canonical; this file is regenerated "
        "on every save-session.*",
        "",
        f"Entries: **{len(entries)}**",
        "",
        "---",
        "",
    ]
    if not entries:
        frontmatter.append("*(no entries yet — stores ship empty; grow through Scholar consolidation)*")
        return "\n".join(frontmatter) + "\n"
    rendered = [render_entry(e, heading_field) for e in entries]
    return "\n".join(frontmatter) + "\n".join(rendered) + "\n"


def render_memory(memory_path: Path) -> str:
    """Curated memory.json export: instance_identity, last_session_snapshot,
    memories, anti_preferences. Skips ephemeral operational stanzas."""
    data = load_json(memory_path)
    identity = data.get("instance_identity", {})
    snapshot = data.get("last_session_snapshot", {})
    memories = data.get("memories", {})
    anti = data.get("anti_preferences", {}).get("entries", [])
    out = [
        "---",
        "type: hypatia-memory-export",
        f"source: {memory_path.relative_to(REPO_ROOT)}",
        f"generated: {now_utc()}",
        f"memory_count: {len(memories)}",
        f"anti_preference_count: {len(anti)}",
        f"memory_version: {data.get('version', 'unknown')}",
        "---",
        "",
        "# Memory Export",
        "",
        "*Generated from `hypatia-kb/Memory/memory.json`. Curated stanzas only "
        "(instance_identity, last_session_snapshot, memories, anti_preferences). "
        "Ephemeral operational stanzas are intentionally omitted.*",
        "",
        "---",
        "",
        "## Instance Identity",
        "",
    ]
    for key in sorted(identity.keys()):
        out.append(fmt_inline_field(key, identity[key]))
    out.append("")
    out.append("## Last Session Snapshot")
    out.append("")
    if snapshot:
        for key in sorted(snapshot.keys()):
            out.append(fmt_inline_field(key, snapshot[key]))
    else:
        out.append("*(no session saved yet)*")
    out.append("")
    out.append(f"## Memories ({len(memories)})")
    out.append("")
    if memories:
        for mid in sorted(memories.keys()):
            mem = memories[mid]
            out.append(f"### {mid}")
            out.append("")
            for key in sorted(mem.keys()):
                if key == "content":
                    continue
                out.append(fmt_inline_field(key, mem[key]))
            content = mem.get("content", "").strip()
            if content:
                out.append("")
                out.append("> " + content.replace("\n", "\n> "))
            out.append("")
    else:
        out.append("*(no memories yet)*")
        out.append("")
    out.append(f"## Anti-Preferences ({len(anti)})")
    out.append("")
    if anti:
        for item in anti:
            out.append(f"### {item.get('id', 'unknown')}")
            out.append("")
            for key in sorted(item.keys()):
                if key == "content":
                    continue
                out.append(fmt_inline_field(key, item[key]))
            content = item.get("content", "").strip()
            if content:
                out.append("")
                out.append("> " + content.replace("\n", "\n> "))
            out.append("")
    else:
        out.append("*(no anti-preferences yet)*")
        out.append("")
    return "\n".join(out)


def main() -> int:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    targets = [
        ("patterns", KB / "Intelligence" / "patterns.json", "category", "hypatia-patterns-export"),
        ("knowledge", KB / "Intelligence" / "knowledge.json", "category", "hypatia-knowledge-export"),
        ("reasoning", KB / "Intelligence" / "reasoning.json", "type", "hypatia-reasoning-export"),
    ]
    failures: list[str] = []
    for name, src, heading, dv_type in targets:
        out_path = EXPORTS / f"{name}.md"
        try:
            content = render_store(name, src, heading, dv_type)
            out_path.write_text(content)
            print(f"  ✓ {out_path.relative_to(REPO_ROOT)}")
        except Exception as exc:
            print(f"  ✗ {name}: {exc}", file=sys.stderr)
            failures.append(name)
    memory_src = KB / "Memory" / "memory.json"
    memory_out = EXPORTS / "memory.md"
    try:
        memory_out.write_text(render_memory(memory_src))
        print(f"  ✓ {memory_out.relative_to(REPO_ROOT)}")
    except Exception as exc:
        print(f"  ✗ memory: {exc}", file=sys.stderr)
        failures.append("memory")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
