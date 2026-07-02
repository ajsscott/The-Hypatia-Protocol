#!/usr/bin/env python3
"""Tests for hypatia-kb/vectorstore/vault_index.py — pure logic only.

Embedding (fastembed) and artifact I/O are exercised on the Mac via
vault_rebuild; these tests cover chunking, frontmatter parsing, change
classification, and keyword ranking, which decide index correctness.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "hypatia-kb" / "vectorstore"))

import vault_index as vi  # noqa: E402

NOTE_WITH_FM = """---
aliases:
  - RAG
tags:
  - deeplearning
kind: Tree
---
Retrieval-augmented generation grounds model output in retrieved context.
"""

LONG_NOTE = "---\nkind: Seed\n---\n" + "\n\n".join(
    f"## Section {i}\n" + ("lorem ipsum " * 40) for i in range(8)
)


class TestFrontmatter(unittest.TestCase):
    def test_parses_fields_and_body(self):
        fm, body = vi.parse_frontmatter(NOTE_WITH_FM)
        self.assertEqual(fm["kind"], "Tree")
        self.assertIn("RAG", fm["aliases"])
        self.assertTrue(body.startswith("Retrieval-augmented"))

    def test_no_frontmatter_passthrough(self):
        fm, body = vi.parse_frontmatter("just text")
        self.assertEqual(fm, {})
        self.assertEqual(body, "just text")

    def test_malformed_frontmatter_tolerated(self):
        fm, body = vi.parse_frontmatter("---\n: : bad [yaml\n---\ncontent")
        self.assertEqual(fm, {})
        self.assertEqual(body.strip(), "content")


class TestChunking(unittest.TestCase):
    def test_short_note_single_chunk_with_identity(self):
        chunks = vi.chunk_note("Trees/ai/RAG Basics.md", NOTE_WITH_FM)
        self.assertEqual(len(chunks), 1)
        c = chunks[0]
        self.assertEqual(c["uid"], "Trees/ai/RAG Basics.md::0")
        self.assertEqual(c["kind"], "Tree")
        # identity line carries title + alias + tag for short-query recall
        self.assertIn("RAG Basics", c["text"])
        self.assertIn("deeplearning", c["text"])

    def test_long_note_splits_on_headings_under_target(self):
        chunks = vi.chunk_note("Seeds/long.md", LONG_NOTE, chunk_target=1500)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c["text"]), 1500 * 2 + 100)
        # chunk uids are stable and ordered
        self.assertEqual([c["chunk"] for c in chunks], list(range(len(chunks))))

    def test_frontmatter_only_note_still_indexed(self):
        chunks = vi.chunk_note("Seeds/stub.md", "---\nkind: Seed\n---\n")
        self.assertEqual(len(chunks), 1)
        self.assertIn("stub", chunks[0]["text"])

    def test_chunking_deterministic(self):
        a = vi.chunk_note("x.md", LONG_NOTE)
        b = vi.chunk_note("x.md", LONG_NOTE)
        self.assertEqual([c["hash"] for c in a], [c["hash"] for c in b])


class TestClassifyChanges(unittest.TestCase):
    def test_full_matrix(self):
        previous = {"a::0": "h1", "b::0": "h2", "c::0": "h3"}
        current = {"a::0": "h1", "b::0": "CHANGED", "d::0": "h4"}
        added, updated, removed, unchanged = vi.classify_changes(current, previous)
        self.assertEqual(added, {"d::0"})
        self.assertEqual(updated, {"b::0"})
        self.assertEqual(removed, {"c::0"})
        self.assertEqual(unchanged, {"a::0"})


class TestKeywordResults(unittest.TestCase):
    def test_ranks_by_token_coverage(self):
        entries = [
            {"uid": "a::0", "path": "Trees/a.md", "text": "prompt injection and role confusion"},
            {"uid": "b::0", "path": "Trees/b.md", "text": "prompt engineering only"},
            {"uid": "c::0", "path": "Trees/c.md", "text": "nothing relevant"},
        ]
        results = vi._keyword_results("prompt injection", entries, top_n=5)
        self.assertEqual(results[0]["id"], "a::0")
        self.assertEqual(len(results), 2)  # c has zero hits and is excluded

    def test_path_match_counts(self):
        entries = [{"uid": "a::0", "path": "Trees/injection.md", "text": "unrelated body"}]
        results = vi._keyword_results("injection", entries, top_n=5)
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
