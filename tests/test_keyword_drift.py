#!/usr/bin/env python3
"""Tests for scripts/check-keyword-drift.py — kernel keyword map vs protocol
declarations (addendum landmine #12).

Two layers:
  1. Unit-style: parser + diff functions handle expected inputs.
  2. Repo-state assertion: the live repo must have zero drift. This is the
     CI gate that prevents the Phase 1 reconciliation from re-rotting.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-keyword-drift.py"

# Load hyphenated script as module
spec = importlib.util.spec_from_file_location("check_keyword_drift", SCRIPT_PATH)
ckd = importlib.util.module_from_spec(spec)
sys.modules["check_keyword_drift"] = ckd
spec.loader.exec_module(ckd)


class TestKeywordParser(unittest.TestCase):
    def test_parse_keyword_set_basic(self):
        self.assertEqual(
            ckd.parse_keyword_set("foo, bar, baz"),
            {"foo", "bar", "baz"},
        )

    def test_parse_keyword_set_strips_whitespace(self):
        self.assertEqual(
            ckd.parse_keyword_set("  foo  ,bar,  baz  "),
            {"foo", "bar", "baz"},
        )

    def test_parse_keyword_set_drops_empty(self):
        self.assertEqual(
            ckd.parse_keyword_set("foo,,bar,"),
            {"foo", "bar"},
        )

    def test_parse_protocol_keywords_finds_trigger_line(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Heading\n\n**Trigger Keywords**: alpha, beta, gamma\n\n## Section\n")
            tmp = Path(f.name)
        try:
            self.assertEqual(
                ckd.parse_protocol_keywords(tmp),
                {"alpha", "beta", "gamma"},
            )
        finally:
            tmp.unlink()

    def test_parse_protocol_keywords_falls_back_to_plain_keywords(self):
        # The regex accepts `**Keywords**:` as well as `**Trigger Keywords**:`
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Heading\n\n**Keywords**: alpha, beta\n")
            tmp = Path(f.name)
        try:
            self.assertEqual(ckd.parse_protocol_keywords(tmp), {"alpha", "beta"})
        finally:
            tmp.unlink()

    def test_parse_protocol_keywords_returns_none_if_absent(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Heading\n\nNo trigger keywords line here.\n")
            tmp = Path(f.name)
        try:
            self.assertIsNone(ckd.parse_protocol_keywords(tmp))
        finally:
            tmp.unlink()


class TestKernelMapParser(unittest.TestCase):
    def test_parses_live_kernel_map(self):
        kernel = ckd.parse_kernel_map(ckd.KERNEL_MAP)
        self.assertGreater(len(kernel), 0)
        # Spot-check a few we know to be present after Phase 1 relocation
        kernel_str = str(kernel)
        self.assertIn("librarian-role.md", kernel_str)
        self.assertIn("assistant-ingest.md", kernel_str)
        self.assertIn("security.md", kernel_str)


class TestLiveDrift(unittest.TestCase):
    """CI gate: the live repo must have zero drift."""

    def test_no_drift_in_live_repo(self):
        kernel = ckd.parse_kernel_map(ckd.KERNEL_MAP)
        code, report = ckd.diff_report(kernel)
        self.assertEqual(
            code, 0,
            f"Keyword drift detected in live repo. Run "
            f"`uv run python scripts/check-keyword-drift.py` to see the diff.\n"
            f"Report:\n{report}",
        )


if __name__ == "__main__":
    unittest.main()
