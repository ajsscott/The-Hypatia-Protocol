#!/usr/bin/env python3
"""ollama-think-shim.py — local proxy that forces `think: false` on Ollama chat.

Why this exists: Q-17 picked Gemma 4 12B QAT, whose hybrid-thinking must be
disabled (60-90s to first visible token otherwise; docs/q17-eval/). The
Ollama API's `think: false` parameter fully disables it for this model —
empirically verified — but Goose cannot send it (block/goose#7617) and
Ollama 0.31's Modelfile grammar doesn't accept it as a model default.

So: point Goose's OLLAMA_HOST at this shim. It forwards every request to
the real Ollama untouched, except POST /api/chat and /api/generate bodies,
where it sets `think: false` unless the client explicitly sent a value.
Delete this shim when goose#7617 ships a provider-level toggle.

Stdlib only. Streaming (NDJSON) responses are piped through chunk-by-chunk.

Environment:
    SHIM_PORT        listen port          (default 11435)
    OLLAMA_UPSTREAM  real Ollama URL      (default http://127.0.0.1:11434)

Invocation:
    python3 scripts/ollama-think-shim.py            # foreground; ctrl-c to stop
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SHIM_PORT = int(os.environ.get("SHIM_PORT", "11435"))
UPSTREAM = os.environ.get("OLLAMA_UPSTREAM", "http://127.0.0.1:11434").rstrip("/")

# Endpoints whose JSON bodies accept the top-level `think` option.
THINK_PATHS = ("/api/chat", "/api/generate")

# Only these models get think:false injected — non-thinking models may
# reject the parameter, and the shim must stay transparent for them.
THINK_MODEL_MARKERS = ("hypatia-gemma4", "gemma-4", "gemma4")

# Hop-by-hop headers that must not be forwarded verbatim.
SKIP_HEADERS = {
    "host",
    "content-length",
    "transfer-encoding",
    "connection",
    "keep-alive",
}


def inject_think(body: bytes, path: str) -> bytes:
    """Set think:false on Gemma-4-family chat/generate bodies; leave
    everything else alone.

    A client that explicitly set `think` keeps its value — the shim only
    supplies the default Goose can't.
    """
    if not any(path.startswith(p) for p in THINK_PATHS):
        return body
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return body
    if not isinstance(payload, dict) or "think" in payload:
        return body
    model = str(payload.get("model", "")).lower()
    if not any(marker in model for marker in THINK_MODEL_MARKERS):
        return body
    payload["think"] = False
    return json.dumps(payload).encode()


class ShimHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:  # stderr, one line per request
        sys.stderr.write(f"shim: {fmt % args}\n")

    def _forward(self, body: bytes | None) -> None:
        url = f"{UPSTREAM}{self.path}"
        headers = {
            k: v for k, v in self.headers.items() if k.lower() not in SKIP_HEADERS
        }
        req = urllib.request.Request(
            url, data=body, headers=headers, method=self.command
        )
        try:
            resp = urllib.request.urlopen(req, timeout=600)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            payload = e.read()
            self.send_header("Content-Type", e.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        except (urllib.error.URLError, OSError) as e:
            self.send_response(502)
            payload = json.dumps({"error": f"shim: upstream {UPSTREAM} unreachable: {e}"}).encode()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        with resp:
            self.send_response(resp.status)
            for k, v in resp.getheaders():
                if k.lower() in SKIP_HEADERS:
                    continue
                self.send_header(k, v)
            # Stream through with chunked encoding so NDJSON tokens reach the
            # client as they are generated, not after the reply completes.
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                self.wfile.write(f"{len(chunk):x}\r\n".encode() + chunk + b"\r\n")
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")

    def do_GET(self) -> None:
        self._forward(None)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""
        self._forward(inject_think(body, self.path))

    def do_DELETE(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else None
        self._forward(body)

    def do_HEAD(self) -> None:
        self._forward(None)


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", SHIM_PORT), ShimHandler)
    print(
        f"ollama-think-shim: listening on 127.0.0.1:{SHIM_PORT} → {UPSTREAM} "
        f"(injecting think:false on {', '.join(THINK_PATHS)})",
        file=sys.stderr,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("ollama-think-shim: stopped", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
