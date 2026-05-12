//! hypatia-frontend (Tauri 2.0)
//!
//! Phase 1.5 v1: a single-window chat UI that talks to a local Goose daemon.
//!
//! Not yet (Phase 2+):
//! - Menubar/tray persistence
//! - USB-mount auto-launch
//! - Screen capture surface
//! - Flash-drive packaging

#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod commands;
mod goose_client;

use tracing::info;

fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "hypatia_frontend=info".into()),
        )
        .init();

    info!("starting hypatia-frontend");

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            commands::send_message,
            commands::get_config,
            commands::get_identity,
        ])
        .setup(|_app| {
            info!("Tauri app initialized");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running Hypatia frontend");
}
