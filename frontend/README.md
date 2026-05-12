# Hypatia Frontend (Rust + Tauri)

Custom Tauri-based frontend for Hypatia. Talks to Goose backend daemon over HTTP. Built for macOS (Phase 1.5 target); cross-platform deferred.

## Phase 1.5 scope (this v1 scaffold)

- Single window with chat history + input
- HTTP client → Goose daemon API
- Reads `hypatia.config.yaml` for vault path + provider settings
- Loads `kernel/01-04.md` for Hypatia's identity display (sidebar showing "Hypatia, Scholar's partner")
- macOS app bundle build via `cargo tauri build`

**Not in this v1:**
- Menubar / tray persistence (Phase 2)
- USB-mount detection / auto-launch (Phase 2)
- Screen-capture surface (Phase 2)
- Flash-drive packaging (Phase 4)
- Notarization / signing (Phase 4)

## Stack

| Layer | Tech |
|---|---|
| Window + system integration | Tauri 2.0 (Rust) |
| Frontend HTML/CSS/JS | Plain HTML + vanilla JS for v1 (Yew/Leptos optional later) |
| HTTP client to Goose | reqwest |
| Config parser | serde_yaml |
| State management | Tauri commands + frontend localStorage |

## Building

```bash
# Install Tauri CLI if not present
cargo install tauri-cli --version "^2.0"

# From repo root
cd frontend
cargo tauri dev    # dev mode with hot reload
# OR
cargo tauri build  # production .app bundle (lands at frontend/src-tauri/target/release/bundle/macos/)
```

## Running against Goose

Prerequisite: Goose daemon must be running with Hypatia config loaded.

```bash
# Terminal 1: launch Goose daemon
HYPATIA_REPO_ROOT="$PWD" \
GOOSE_CONFIG_PATH="$PWD/goose-config/config.yaml" \
  goose serve --port 8765

# Terminal 2: launch Hypatia frontend (dev mode)
cd frontend && cargo tauri dev
```

The frontend defaults to `http://127.0.0.1:8765` for the Goose daemon. Override via `HYPATIA_GOOSE_URL` env var if needed.

## Layout

```
frontend/
├── src-tauri/              Tauri Rust backend (window mgmt, IPC commands)
│   ├── Cargo.toml
│   ├── tauri.conf.json     App bundle config (name, icon, permissions, build)
│   ├── build.rs
│   └── src/
│       ├── main.rs         Entry point + Tauri setup
│       ├── goose_client.rs Goose daemon HTTP client
│       └── commands.rs     Tauri commands exposed to frontend
├── src/                    Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── styles.css
│   └── main.js
└── README.md               This file
```

## Phase 1.5 Week 2 acceptance criteria

- [ ] `cargo tauri dev` launches a window successfully
- [ ] Window shows Hypatia's identity (from kernel/01-identity.md)
- [ ] Input box + send button work
- [ ] Pressing send issues HTTP request to Goose daemon
- [ ] Response from Goose renders in the chat history
- [ ] Conversation persists during the session (lost on quit; full persistence is Phase 2)

## Caveats

- Tauri 2.0 stable as of late 2025. Verify version in `Cargo.toml` against current crates.io.
- The Goose daemon API specifics are not yet stabilized as of 2026-04. The HTTP client below may need adjustments once Goose's `goose serve` endpoint behavior is confirmed.
- macOS code signing: this v1 produces an unsigned `.app`. First-run requires right-click → Open. Notarization is Phase 4.
