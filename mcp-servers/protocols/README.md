# hypatia-protocols-mcp

MCP server that serves Hypatia's protocol library + kernel-archive detail files as MCP resources.

## What it serves

**Cluster + cross-cutting protocols** (from `hypatia-kb/protocols/`):

- `protocol://librarian-role`, `librarian-vault-structure`, `librarian-note-schemas`, `librarian-tooling`, `librarian-writing-rules`, `librarian-memory`, `librarian-lint`, `librarian-customize`
- `protocol://researcher-investigate`, `researcher-prompt-enhance`
- `protocol://writer-draft`, `writer-summarize`, `writer-executive`
- `protocol://assistant-development`, `assistant-plan`, `assistant-problem-solve`, `assistant-proactive`, `assistant-ingest`
- `protocol://security`, `protocol://critical-file-protection`

**Kernel-archive detail** (from `docs/reference/phase-1-kernel-archive/`):

- `protocol://detail/anti-patterns` — full anti-pattern enumeration
- `protocol://detail/session-gates` — full session gate behaviors
- `protocol://detail/tools` — tool inventory reference
- `protocol://detail/cognitive` — OBSERVE>QUESTION>DEDUCE + CSP detail
- `protocol://detail/intelligence` — tiered surfacing, confidence thresholds, claim-match
- `protocol://detail/save` — full 6-step save flow
- `protocol://detail/security-gates` — full Git Hardening + External Content Security
- `protocol://detail/skills-map` — canonical keyword map
- `protocol://detail/decision-routes` — full Decision Routes A-F spec
- `protocol://detail/voice` — full voice register, examples, pattern of shifting

## Building

```bash
# From repo root
cargo build --release --bin hypatia-protocols-mcp
# Or build the whole workspace:
cargo build --release
```

The binary lands at `target/release/hypatia-protocols-mcp`.

## Running

```bash
HYPATIA_REPO_ROOT=/Users/ajsscott/GitHub/The-Hypatia-Protocol \
  ./target/release/hypatia-protocols-mcp
```

Transport: stdio. Goose's MCP host launches this and communicates via JSON-RPC over stdin/stdout. Logs go to stderr (stdout is reserved for the MCP protocol).

## Goose registration

Add to your Goose custom-distro config (see `goose-config/`):

```yaml
extensions:
  hypatia-protocols:
    type: stdio
    command: /path/to/target/release/hypatia-protocols-mcp
    env:
      HYPATIA_REPO_ROOT: /Users/ajsscott/GitHub/The-Hypatia-Protocol
```

## Architecture decisions

- **No caching v1.** Resources are read from disk on every `resources/read`. Hot-reload behavior; trivial cost given small markdown files.
- **stdio transport.** Goose's MCP host spawns the binary; no network surface.
- **Logging to stderr.** stdout is reserved for MCP JSON-RPC.
- **`HYPATIA_REPO_ROOT` env var.** Lets the server locate files regardless of cwd. Goose's extension config sets this.
- **rmcp version pinned at workspace level.** See repo-root `Cargo.toml`. Update Goose and Hypatia MCP servers in lockstep.

## Phase 1.5 caveats

- `rmcp` API specifics may shift between versions. The current code targets rmcp 0.3+. If compilation fails on API mismatches, check [the rmcp changelog](https://github.com/modelcontextprotocol/rust-sdk) and adjust.
- Per-route decision-route URIs (`protocol://detail/decision-route-a` … `f`) are aspirational — current implementation serves the whole 11-decision-routes.md as one resource. Split into per-route resources in Phase 2 if helpful.

## Tests

Pytest tests exercise the server end-to-end. See `tests/test_protocols_mcp.py`. They spawn the binary and run JSON-RPC fixtures against it.

```bash
uv run pytest tests/test_protocols_mcp.py -v
```
