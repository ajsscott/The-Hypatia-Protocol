#!/usr/bin/env python3
"""Tests for scripts/ollama-think-shim.py — the think:false injection proxy.

Network-free: covers inject_think (the only logic that rewrites traffic).
The proxy loop itself is exercised live on the Mac (its purpose is the
Goose → Ollama session path).
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "ollama-think-shim.py"

spec = importlib.util.spec_from_file_location("ollama_think_shim", SCRIPT_PATH)
shim = importlib.util.module_from_spec(spec)
sys.modules["ollama_think_shim"] = shim
spec.loader.exec_module(shim)


class TestInjectThink(unittest.TestCase):
    def test_injects_on_chat(self):
        body = json.dumps({"model": "hypatia-gemma4", "messages": []}).encode()
        out = json.loads(shim.inject_think(body, "/api/chat"))
        self.assertIs(out["think"], False)

    def test_injects_on_generate(self):
        body = json.dumps(
            {"model": "hf.co/unsloth/gemma-4-12B-it-qat-GGUF:UD-Q4_K_XL", "prompt": "hi"}
        ).encode()
        out = json.loads(shim.inject_think(body, "/api/generate"))
        self.assertIs(out["think"], False)

    def test_leaves_non_gemma_models_alone(self):
        body = json.dumps({"model": "qwen2.5-coder:14b", "messages": []}).encode()
        self.assertEqual(shim.inject_think(body, "/api/chat"), body)

    def test_openai_endpoint_gets_reasoning_effort_none(self):
        # Goose calls /v1/chat/completions, where `think` is ignored and
        # reasoning_effort:"none" is the working control (ollama#15288).
        body = json.dumps({"model": "hypatia-gemma4", "messages": []}).encode()
        out = json.loads(shim.inject_think(body, "/v1/chat/completions"))
        self.assertEqual(out["reasoning_effort"], "none")
        self.assertNotIn("think", out)

    def test_openai_endpoint_respects_client_reasoning(self):
        body = json.dumps(
            {"model": "hypatia-gemma4", "messages": [], "reasoning_effort": "low"}
        ).encode()
        out = json.loads(shim.inject_think(body, "/v1/chat/completions"))
        self.assertEqual(out["reasoning_effort"], "low")

    def test_respects_explicit_client_value(self):
        body = json.dumps({"model": "m", "messages": [], "think": True}).encode()
        out = json.loads(shim.inject_think(body, "/api/chat"))
        self.assertIs(out["think"], True)

    def test_leaves_other_paths_alone(self):
        body = json.dumps({"name": "m"}).encode()
        self.assertEqual(shim.inject_think(body, "/api/tags"), body)
        self.assertEqual(shim.inject_think(body, "/api/pull"), body)

    def test_leaves_malformed_bodies_alone(self):
        self.assertEqual(shim.inject_think(b"not json", "/api/chat"), b"not json")
        self.assertEqual(shim.inject_think(b"", "/api/chat"), b"")

    def test_preserves_payload_fields(self):
        body = json.dumps(
            {"model": "m", "messages": [{"role": "user", "content": "x"}],
             "options": {"num_ctx": 32768}, "stream": True}
        ).encode()
        out = json.loads(shim.inject_think(body, "/api/chat"))
        self.assertEqual(out["options"]["num_ctx"], 32768)
        self.assertTrue(out["stream"])
        self.assertEqual(out["messages"][0]["content"], "x")


if __name__ == "__main__":
    unittest.main()
