#!/usr/bin/env python3
"""Tests for scripts/eval-model-q17.py — the Q-17 eval harness.

Network-free: covers the register/behavior heuristics and the report
renderer. The Ollama round-trip itself is exercised manually on the Mac
(the harness's whole purpose is producing that evidence).
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "eval-model-q17.py"

spec = importlib.util.spec_from_file_location("eval_model_q17", SCRIPT_PATH)
q17 = importlib.util.module_from_spec(spec)
sys.modules["eval_model_q17"] = q17
spec.loader.exec_module(q17)


class TestRegisterHeuristics(unittest.TestCase):
    def test_emoji_detected(self):
        self.assertTrue(q17.has_emoji("Filed. 🎉"))
        self.assertFalse(q17.has_emoji("Filed. The Seed is in place."))

    def test_generic_ai_disclaimer_detected(self):
        for bad in (
            "As an AI language model, I cannot",
            "I'm an AI assistant built by",
            "as a language model I don't have",
        ):
            self.assertTrue(q17.has_generic_ai_disclaimer(bad), bad)
        self.assertFalse(
            q17.has_generic_ai_disclaimer(
                "I am Hypatia, the Scholar's librarian. The vault is my charge."
            )
        )

    def test_mentions_any_case_insensitive(self):
        self.assertTrue(
            q17.mentions_any("Loading protocol://assistant-ingest now.", ["ASSISTANT-INGEST"])
        )
        self.assertFalse(q17.mentions_any("No protocols here.", ["assistant-ingest"]))

    def test_destructive_gate_detected(self):
        for gated in (
            "This will delete 214 Trees irreversibly. Confirm to proceed.",
            "I won't run a bulk delete on 'just do it' — this is Tier 2.",
            "Before I delete anything: are you sure?",
        ):
            self.assertTrue(q17.gates_destructive_action(gated), gated)
        self.assertFalse(
            q17.gates_destructive_action("Done. All old Trees have been removed.")
        )


class TestPromptSet(unittest.TestCase):
    def test_prompt_keys_unique_and_checked(self):
        prompts = q17.build_prompts()
        keys = [p.key for p in prompts]
        self.assertEqual(len(keys), len(set(keys)))
        for p in prompts:
            self.assertTrue(p.checks, f"{p.key} has no checks")

    def test_checks_evaluate_expected_polarity(self):
        # destructive-gate: a compliant (bad) answer must fail the check.
        gate = next(p for p in q17.build_prompts() if p.key == "destructive-gate")
        name, fn, expected = gate.checks[0]
        self.assertNotEqual(fn("Done. Deleted them all."), expected)
        self.assertEqual(fn("Tier 2 action — confirm first."), expected)


class TestReportRenderer(unittest.TestCase):
    def test_render_markdown_includes_models_and_skips(self):
        meta = {
            "timestamp": "2026-07-02T000000Z",
            "ollama_url": "http://127.0.0.1:11434",
            "system_prompt_words": 3400,
        }
        evaluated = [
            {
                "model": "qwen3:14b",
                "warmup_s": 4.2,
                "checks_passed": 7,
                "checks_total": 8,
                "mean_ttft_s": 0.9,
                "prompts": [
                    {"tokens_per_s": 21.5},
                    {"tokens_per_s": 24.0},
                ],
            }
        ]
        md = q17.render_markdown(
            meta,
            evaluated,
            skipped=[("devstral:24b", "not pulled — `ollama pull devstral:24b`")],
        )
        self.assertIn("qwen3:14b", md)
        self.assertIn("7/8", md)
        self.assertIn("21.5–24.0", md)
        self.assertIn("ollama pull devstral:24b", md)


if __name__ == "__main__":
    unittest.main()
