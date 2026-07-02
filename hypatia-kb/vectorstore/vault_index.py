#!/usr/bin/env python3
"""vault_index.py - Semantic + keyword search over the TabulaJacqueliana vault.

Extends the store vectorstore (kb_vectorize/kb_sync/kb_query) to the vault's
markdown notes. Same machinery, same lessons (docs/plugin-architecture-lessons.md
Tier 3): content-hash incremental sync, model version stamping, RRF fusion
(imported from kb_query — identical math), results as pointers + snippets,
never whole notes.

Chunking: note-level by default; notes longer than CHUNK_TARGET chars split
on H2+ heading boundaries ("fewest chunks that fit" — no overlap, no
mid-thought cuts). Chunk 0 always carries the note's identity (title +
frontmatter aliases/tags/kind) so short queries land on the right note.

Artifacts (vault-vectors.npy, vault-metadata.json) are gitignored — they
embed AJ's private vault content and stay local.

CLI:
    python3 vault_index.py build            # full index
    python3 vault_index.py sync             # hash-incremental
    python3 vault_index.py search "query"   # top-5 hybrid
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import UTC, datetime
from hashlib import sha256

import numpy as np

VS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(VS_DIR))

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSIONS = 384
CHUNK_TARGET = 1500  # chars; ~ MiniLM's useful window with headroom
RRF_K = 60
SCORE_FLOOR = 0.005
SNIPPET_CHARS = 400

VEC_PATH = os.path.join(VS_DIR, "vault-vectors.npy")
META_PATH = os.path.join(VS_DIR, "vault-metadata.json")

EXCLUDED_DIRS = {".obsidian", ".smart-env", ".trash", ".git", "node_modules", ".hypatia"}

HEADING_RE = re.compile(r"^#{2,6}\s+\S", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)


def vault_root() -> str:
    """Vault path from env override or hypatia.config.yaml."""
    override = os.environ.get("HYPATIA_VAULT_PATH")
    if override:
        return override
    import yaml

    cfg_path = os.path.join(REPO_ROOT, "hypatia.config.yaml")
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    return cfg["vault"]["path"]


def content_hash(text: str) -> str:
    return sha256(text.encode()).hexdigest()[:16]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Malformed frontmatter -> ({}, text)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        import yaml

        fm = yaml.safe_load(m.group(1))
        if not isinstance(fm, dict):
            fm = {}
    except Exception:
        fm = {}
    return fm, text[m.end():]


def _identity_line(relpath: str, fm: dict) -> str:
    """Compact identity string embedded with chunk 0 so title/alias/tag
    queries rank the note even when the body doesn't repeat them."""
    title = os.path.splitext(os.path.basename(relpath))[0]
    parts = [title]
    for key in ("aliases", "tags"):
        vals = fm.get(key)
        if isinstance(vals, list):
            parts.extend(str(v) for v in vals if v)
    kind = fm.get("kind")
    if kind:
        parts.append(str(kind))
    return " | ".join(parts)


def chunk_note(relpath: str, text: str, chunk_target: int = CHUNK_TARGET) -> list[dict]:
    """Split one note into embeddable chunks.

    Short notes -> one chunk. Long notes split at H2+ heading boundaries;
    consecutive sections pack together while they fit under chunk_target
    (fewest chunks that capture everything — no overlap).
    """
    fm, body = parse_frontmatter(text)
    identity = _identity_line(relpath, fm)
    kind = str(fm.get("kind", "")) or None
    body = body.strip()

    if len(body) <= chunk_target:
        sections = [body] if body else []
    else:
        # Split at heading starts, keeping headings with their section.
        starts = [m.start() for m in HEADING_RE.finditer(body)]
        if not starts or starts[0] != 0:
            starts = [0, *starts]
        raw = [body[a:b].strip() for a, b in zip(starts, [*starts[1:], len(body)])]
        raw = [s for s in raw if s]
        # Pack consecutive sections up to chunk_target.
        sections = []
        current = ""
        for section in raw:
            if current and len(current) + len(section) + 2 > chunk_target:
                sections.append(current)
                current = section
            else:
                current = f"{current}\n\n{section}" if current else section
        if current:
            sections.append(current)
        # Oversized single sections split hard on paragraph boundaries.
        packed = []
        for s in sections:
            while len(s) > chunk_target * 2:
                cut = s.rfind("\n\n", 0, chunk_target)
                cut = cut if cut > 200 else chunk_target
                packed.append(s[:cut].strip())
                s = s[cut:].strip()
            packed.append(s)
        sections = packed

    chunks = []
    for i, section in enumerate(sections):
        text_for_embedding = f"{identity}\n\n{section}" if i == 0 else section
        chunks.append(
            {
                "uid": f"{relpath}::{i}",
                "path": relpath,
                "chunk": i,
                "kind": kind,
                "text": text_for_embedding,
                "hash": content_hash(text_for_embedding),
            }
        )
    if not chunks:  # frontmatter-only note: identity still searchable
        chunks.append(
            {
                "uid": f"{relpath}::0",
                "path": relpath,
                "chunk": 0,
                "kind": kind,
                "text": identity,
                "hash": content_hash(identity),
            }
        )
    return chunks


def collect_vault_chunks(root: str) -> dict[str, dict]:
    """Walk the vault; return {uid: chunk} for every markdown note."""
    out: dict[str, dict] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            relpath = os.path.relpath(full, root)
            try:
                with open(full, encoding="utf-8") as f:
                    text = f.read()
            except (OSError, UnicodeDecodeError) as e:
                print(f"Warning: skipping {relpath}: {e}", file=sys.stderr)
                continue
            for chunk in chunk_note(relpath, text):
                out[chunk["uid"]] = chunk
    return out


def classify_changes(
    current: dict[str, str], previous: dict[str, str]
) -> tuple[set[str], set[str], set[str], set[str]]:
    """(added, updated, removed, unchanged) between {uid: hash} maps."""
    added = {u for u in current if u not in previous}
    removed = {u for u in previous if u not in current}
    updated = {u for u in current if u in previous and current[u] != previous[u]}
    unchanged = {u for u in current if u in previous and current[u] == previous[u]}
    return added, updated, removed, unchanged


def _embed(texts: list[str]) -> np.ndarray:
    from fastembed import TextEmbedding

    model = TextEmbedding(model_name=MODEL_NAME)
    return np.array(list(model.embed(texts)), dtype=np.float32)


def _model_version() -> str:
    try:
        import fastembed

        return f"fastembed-{fastembed.__version__}"
    except Exception:
        return "unknown"


def _write_artifacts(vectors: np.ndarray, entries: list[dict], built: str | None = None) -> None:
    now = datetime.now(UTC).astimezone().isoformat()
    meta = {
        "model": MODEL_NAME,
        "model_version": _model_version(),
        "dimensions": DIMENSIONS,
        "built": built or now,
        "last_sync": now,
        "entry_count": len(entries),
        "entries": entries,
    }
    tmp_vec = VEC_PATH + ".tmp.npy"
    tmp_meta = META_PATH + ".tmp"
    np.save(tmp_vec, vectors)
    with open(tmp_meta, "w") as f:
        json.dump(meta, f)
    os.replace(tmp_vec, VEC_PATH)
    os.replace(tmp_meta, META_PATH)


def build() -> dict:
    """Full vault index build."""
    start = time.time()
    root = vault_root()
    chunks = collect_vault_chunks(root)
    if not chunks:
        return {"error": f"no markdown notes found under {root}"}
    uids = sorted(chunks)
    vectors = _embed([chunks[u]["text"] for u in uids])
    entries = [
        {**{k: chunks[u][k] for k in ("uid", "path", "chunk", "kind", "text", "hash")}, "row": i}
        for i, u in enumerate(uids)
    ]
    _write_artifacts(vectors, entries)
    elapsed = round(time.time() - start, 1)
    notes = len({c["path"] for c in chunks.values()})
    print(f"Indexed {notes} notes / {len(uids)} chunks in {elapsed}s")
    return {"notes": notes, "chunks": len(uids), "elapsed": elapsed}


def _load_artifacts():
    if not (os.path.exists(VEC_PATH) and os.path.exists(META_PATH)):
        return None
    try:
        vectors = np.load(VEC_PATH)
        with open(META_PATH) as f:
            meta = json.load(f)
        if vectors.shape[0] != meta.get("entry_count", -1):
            return None
        return vectors, meta
    except Exception:
        return None


def sync() -> dict:
    """Hash-incremental sync; full build on missing/mismatched artifacts or
    embedding-model change (the Smart Connections lesson)."""
    start = time.time()
    loaded = _load_artifacts()
    if loaded is None:
        result = build()
        result["action"] = "full_build"
        return result
    vectors, meta = loaded
    if meta.get("model_version") != _model_version() or meta.get("model") != MODEL_NAME:
        result = build()
        result["action"] = "full_build_model_change"
        return result

    current = collect_vault_chunks(vault_root())
    previous = {e["uid"]: e for e in meta["entries"]}
    added, updated, removed, unchanged = classify_changes(
        {u: c["hash"] for u, c in current.items()},
        {u: e["hash"] for u, e in previous.items()},
    )
    if not (added or updated or removed):
        return {"added": 0, "updated": 0, "removed": 0, "unchanged": len(unchanged),
                "elapsed": round(time.time() - start, 1)}

    to_embed = sorted(added | updated)
    new_vecs = _embed([current[u]["text"] for u in to_embed]) if to_embed else np.zeros((0, DIMENSIONS), dtype=np.float32)
    new_by_uid = {u: new_vecs[i] for i, u in enumerate(to_embed)}

    entries, rows = [], []
    for u in sorted(unchanged):
        entries.append({**current[u], "row": len(rows)})
        rows.append(vectors[previous[u]["row"]])
    for u in to_embed:
        entries.append({**current[u], "row": len(rows)})
        rows.append(new_by_uid[u])
    _write_artifacts(np.stack(rows), entries, built=meta.get("built"))
    return {"added": len(added), "updated": len(updated), "removed": len(removed),
            "unchanged": len(unchanged), "elapsed": round(time.time() - start, 1)}


def _keyword_results(query: str, entries: list[dict], top_n: int) -> list[dict]:
    """Token-in-text match over chunk text + path, coverage-ranked."""
    tokens = [t for t in query.lower().split() if t]
    if not tokens:
        return []
    scored = []
    for e in entries:
        text = e["text"].lower()
        path = e["path"].lower()
        hits = sum(1 for t in tokens if t in text) + sum(0.5 for t in tokens if t in path)
        if hits:
            scored.append((hits / len(tokens), e["uid"]))
    scored.sort(reverse=True)
    return [
        {"id": uid, "store": "vault", "score": s, "rank": i + 1}
        for i, (s, uid) in enumerate(scored[:top_n])
    ]


def search(query: str, top_k: int = 5, folder: str | None = None, kind: str | None = None) -> list[dict]:
    """Hybrid vault search. Returns pointers + snippets, never whole notes."""
    loaded = _load_artifacts()
    if loaded is None:
        return [{"error": "vault index missing — run vault_rebuild first"}]
    vectors, meta = loaded
    entries = meta["entries"]
    by_uid = {e["uid"]: e for e in entries}

    def keep(e: dict) -> bool:
        if folder and not e["path"].startswith(folder):
            return False
        if kind and (e.get("kind") or "").lower() != kind.lower():
            return False
        return True

    top_n = top_k * 3
    query_vec = _embed([query])[0]
    scores = vectors @ query_vec
    order = np.argsort(scores)[::-1]
    semantic = []
    for idx in order:
        e = entries[idx]
        if not keep(e):
            continue
        semantic.append({"id": e["uid"], "store": "vault", "score": float(scores[idx]),
                         "rank": len(semantic) + 1})
        if len(semantic) >= top_n:
            break

    keyword = _keyword_results(query, [e for e in entries if keep(e)], top_n)

    from kb_query import _rrf_fuse

    fused = _rrf_fuse(semantic, keyword, RRF_K, {"semantic": 1.0, "keyword": 1.0},
                      SCORE_FLOOR, store_filter=None)

    results = []
    for r in fused[:top_k]:
        e = by_uid[r["id"]]
        snippet = e["text"][:SNIPPET_CHARS]
        results.append({
            "path": e["path"],
            "chunk": e["chunk"],
            "kind": e.get("kind"),
            "score": r["score"],
            "semantic_rank": r["semantic_rank"],
            "keyword_rank": r["keyword_rank"],
            "snippet": snippet,
        })
    return results


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "search"
    if cmd == "build":
        print(json.dumps(build(), indent=2))
    elif cmd == "sync":
        print(json.dumps(sync(), indent=2))
    elif cmd == "search":
        q = " ".join(sys.argv[2:])
        print(json.dumps(search(q), indent=2))
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
