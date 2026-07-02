# Hypatia in Obsidian — setup

2026-07-02. Hypatia reaches Obsidian through ACP: the community **Agent
Client** plugin is an ACP client; `goose acp` is an ACP agent. No custom
plugin required. Obsidian sessions read the GLOBAL Goose config (not the
recipes) and get the kernel via the global goosehints file the regen script
maintains.

All steps are idempotent — re-running any of them is safe.

## 1. Think-shim as a login service

Obsidian sessions bypass the terminal launcher, so the shim must be
always-on (without it, Gemma-4 thinking returns: 60s+ per reply):

```bash
mkdir -p ~/.hypatia ~/Library/LaunchAgents
cp "$HYPATIA_REPO_ROOT/goose-config/com.hypatia.think-shim.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.hypatia.think-shim.plist
curl -s http://127.0.0.1:11435/api/version && echo " ← shim alive"
```

## 2. Global Goose config carries Hypatia's extensions

```bash
cd "$HYPATIA_REPO_ROOT" && uv run python - <<'EOF'
from pathlib import Path
import yaml

repo = "/Users/ajsscott/GitHub/other/The-Hypatia-Protocol"
vault = "/Users/ajsscott/GitHub/other/TabulaJacqueliana"
p = Path.home() / ".config/goose/config.yaml"
cfg = yaml.safe_load(p.read_text())
ext = cfg.setdefault("extensions", {})

ext["hypatia-protocols"] = {
    "enabled": True, "type": "stdio", "name": "hypatia-protocols",
    "description": "Hypatia's protocol library (36 resources, read_protocol tool)",
    "cmd": f"{repo}/target/release/hypatia-protocols-mcp", "args": [],
    "envs": {"HYPATIA_REPO_ROOT": repo}, "timeout": 300,
}
ext["filesystem"] = {
    "enabled": True, "type": "stdio", "name": "filesystem",
    "description": "Bounded filesystem access (repo + vault)",
    "cmd": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", repo, vault],
    "envs": {}, "timeout": 300,
}
ext["time"] = {
    "enabled": True, "type": "stdio", "name": "time",
    "description": "Current time", "cmd": "uvx",
    "args": ["mcp-server-time"], "envs": {}, "timeout": 60,
}
ext["kb-vectorstore"] = {
    "enabled": True, "type": "stdio", "name": "kb-vectorstore",
    "description": "Vault semantic search (vault_search) + KB stores",
    "cmd": "uv",
    "args": ["run", "--project", repo, "python", f"{repo}/hypatia-kb/vectorstore/kb_server.py"],
    "envs": {}, "timeout": 300,
}
# Obsidian sessions default to the lite tier: sidebar work is chat/Q&A;
# grows belong in the terminal on the full model.
cfg.setdefault("providers", {}).setdefault("ollama", {})["model"] = "hypatia-gemma4-lite"
p.write_text(yaml.safe_dump(cfg, sort_keys=False))
print("global config: extensions registered, model = hypatia-gemma4-lite")
EOF
```

## 3. Persona file current

```bash
"$HYPATIA_REPO_ROOT/goose-config/regen-system-prompt.sh"
```

This writes `~/.config/goose/.goosehints` (the kernel + substrate note),
which Goose loads into every session — ACP included. The terminal launcher
runs this on every start, so it is normally already current.

## 4. Install the plugin

Obsidian → Settings → Community Plugins → Browse → **Agent Client**
(RAIT-09) → Install → Enable.

In the plugin's settings, add a custom agent:

- **Command**: `goose`
- **Args**: `acp`

(If the plugin has an env field, add `HYPATIA_REPO_ROOT` →
`/Users/ajsscott/GitHub/other/The-Hypatia-Protocol`.)

## 5. First session checks

Open the Agent Client sidebar, select the goose agent, say hello.

- Greeting is Hypatia (Alexandrian register, "Scholar") — proves the
  goosehints persona path. Generic-Goose greeting = goosehints not loading;
  re-run step 3 and check `~/.config/goose/.goosehints` exists.
- Reply lands in ~seconds, not 60+ — proves the shim. Slow = check step 1.
- Ask "What do we have about <topic>?" — expect a `vault_search` call.
- `@`-mention a note to hand her context; her file edits go through the
  plugin's permission prompts (a hard gate layered on her Tier rules).

## Known limitations

- The plugin likely spawns sessions with the vault as cwd, so filesystem
  access may be vault-only (repo unreachable). Fine for curation; use the
  terminal `hypatia` for anything repo-side (saves, protocol work).
- Sidebar sessions run the lite (E4B) model. For a heavy grow, use the
  terminal: `hypatia` (full 12B).
- New session per task applies in Obsidian too — start a fresh sidebar
  session rather than growing one all day.
