#!/usr/bin/env python3
"""Tests for mcp-servers/protocols/ — the Hypatia protocols MCP server.

These tests spawn the compiled binary and exercise its MCP behavior via
JSON-RPC over stdio. They are skipped when the binary hasn't been built
(use `cargo build --release --bin hypatia-protocols-mcp` first).

Coverage:
- Server starts cleanly + reports correct server_info
- list_resources returns all 30 expected resources (20 protocols + 10 kernel-archive)
- read_resource returns content for known URIs
- read_resource errors cleanly on unknown URIs
- All served files exist on disk + parse as UTF-8 markdown
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BINARY = REPO_ROOT / "target" / "release" / "hypatia-protocols-mcp"
PROTOCOLS_DIR = REPO_ROOT / "hypatia-kb" / "protocols"
ARCHIVE_DIR = REPO_ROOT / "docs" / "reference" / "phase-1-kernel-archive"

# Expected protocol-cluster URIs (from hypatia-kb/protocols/, excluding README.md)
EXPECTED_PROTOCOL_URIS = {
    "protocol://librarian-role",
    "protocol://librarian-vault-structure",
    "protocol://librarian-note-schemas",
    "protocol://librarian-tooling",
    "protocol://librarian-writing-rules",
    "protocol://librarian-memory",
    "protocol://librarian-lint",
    "protocol://librarian-customize",
    "protocol://researcher-investigate",
    "protocol://researcher-prompt-enhance",
    "protocol://writer-draft",
    "protocol://writer-summarize",
    "protocol://writer-executive",
    "protocol://assistant-development",
    "protocol://assistant-plan",
    "protocol://assistant-problem-solve",
    "protocol://assistant-proactive",
    "protocol://assistant-ingest",
    "protocol://security",
    "protocol://CRITICAL-FILE-PROTECTION",
}

EXPECTED_ARCHIVE_URIS = {
    "protocol://detail/anti-patterns",
    "protocol://detail/session-gates",
    "protocol://detail/tools",
    "protocol://detail/cognitive",
    "protocol://detail/intelligence",
    "protocol://detail/save",
    "protocol://detail/security-gates",
    "protocol://detail/skills-map",
    "protocol://detail/decision-routes",
    "protocol://detail/voice",
}


def _mcp_request(proc: subprocess.Popen, method: str, params: dict, req_id: int) -> dict:
    """Send a JSON-RPC request to the MCP server over stdio; return parsed response."""
    msg = json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
    proc.stdin.write(msg + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError(f"empty response from server for {method}; server may have exited")
    return json.loads(line)


def _mcp_notify(proc: subprocess.Popen, method: str, params: dict) -> None:
    """Send a JSON-RPC notification (no response expected)."""
    msg = json.dumps({"jsonrpc": "2.0", "method": method, "params": params})
    proc.stdin.write(msg + "\n")
    proc.stdin.flush()


@unittest.skipUnless(
    BINARY.exists(),
    f"binary not built; run `cargo build --release --bin hypatia-protocols-mcp` first ({BINARY} missing)",
)
class TestProtocolsMCPServer(unittest.TestCase):
    """End-to-end tests against the spawned MCP server binary."""

    @classmethod
    def setUpClass(cls):
        env = {**os.environ, "HYPATIA_REPO_ROOT": str(REPO_ROOT)}
        cls.proc = subprocess.Popen(
            [str(BINARY)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        # MCP initialize handshake: request -> response -> initialized notification.
        # Without the notification, rmcp 0.3.2 errors with "connection closed: initialized request".
        init_resp = _mcp_request(
            cls.proc,
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "0.1.0"},
            },
            1,
        )
        assert init_resp.get("result") is not None, f"initialize failed: {init_resp}"
        cls.init_resp = init_resp
        # Required completion of MCP handshake.
        _mcp_notify(cls.proc, "notifications/initialized", {})

    @classmethod
    def tearDownClass(cls):
        try:
            cls.proc.stdin.close()
            cls.proc.terminate()
            cls.proc.wait(timeout=2)
        except Exception:
            cls.proc.kill()

    def test_server_info(self):
        info = self.init_resp["result"]["serverInfo"]
        self.assertEqual(info["name"], "hypatia-protocols-mcp")
        self.assertTrue(info["version"])

    def test_list_resources_returns_expected_uris(self):
        resp = _mcp_request(self.proc, "resources/list", {}, 2)
        self.assertIn("result", resp, f"resources/list failed: {resp}")
        served_uris = {r["uri"] for r in resp["result"]["resources"]}
        expected = EXPECTED_PROTOCOL_URIS | EXPECTED_ARCHIVE_URIS
        self.assertEqual(
            served_uris,
            expected,
            f"\n  only served: {served_uris - expected}\n  only expected: {expected - served_uris}",
        )

    def test_read_known_resource(self):
        resp = _mcp_request(
            self.proc,
            "resources/read",
            {"uri": "protocol://librarian-role"},
            3,
        )
        self.assertIn("result", resp, f"resources/read failed: {resp}")
        contents = resp["result"]["contents"]
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0]["mimeType"], "text/markdown")
        text = contents[0]["text"]
        self.assertIn("Librarian Role", text)
        self.assertIn("Trigger Keywords", text)

    def test_read_kernel_archive_resource(self):
        resp = _mcp_request(
            self.proc,
            "resources/read",
            {"uri": "protocol://detail/decision-routes"},
            4,
        )
        self.assertIn("result", resp)
        text = resp["result"]["contents"][0]["text"]
        # 11-decision-routes.md content marker
        self.assertIn("Decision", text)
        self.assertIn("Route", text)

    def test_read_unknown_resource_errors(self):
        resp = _mcp_request(
            self.proc,
            "resources/read",
            {"uri": "protocol://does-not-exist"},
            5,
        )
        self.assertIn("error", resp, f"expected error, got: {resp}")


class TestServedFilesExist(unittest.TestCase):
    """File-system invariants — verifiable without spawning the binary."""

    def test_all_protocol_files_present(self):
        expected_filenames = {
            uri.removeprefix("protocol://") + ".md" for uri in EXPECTED_PROTOCOL_URIS
        }
        actual = {p.name for p in PROTOCOLS_DIR.glob("*.md")} - {"README.md"}
        self.assertEqual(actual, expected_filenames)

    def test_all_archive_files_present(self):
        archive_filenames = {
            "03-anti-patterns.md",
            "04-session-gates.md",
            "05-tools.md",
            "06-cognitive.md",
            "07-intelligence-layer.md",
            "08-save-command.md",
            "09-security.md",
            "10-skills-loading.md",
            "11-decision-routes.md",
            "02-voice.md",
        }
        actual = {p.name for p in ARCHIVE_DIR.glob("*.md")}
        # Archive may also contain 01-identity.md and others; check superset.
        for filename in archive_filenames:
            self.assertIn(filename, actual, f"{filename} missing from {ARCHIVE_DIR}")

    def test_all_files_are_utf8_markdown(self):
        for d in (PROTOCOLS_DIR, ARCHIVE_DIR):
            for f in d.glob("*.md"):
                with self.assertRaises(Exception) if False else open(f, encoding="utf-8") as fh:
                    fh.read()  # raises if not UTF-8


if __name__ == "__main__":
    unittest.main()
