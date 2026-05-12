//! Tauri commands exposed to the frontend JS.

use crate::goose_client::{ChatRequest, ChatResponse, GooseClient};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::sync::OnceLock;
use tracing::error;

static CLIENT: OnceLock<GooseClient> = OnceLock::new();

fn client() -> &'static GooseClient {
    CLIENT.get_or_init(GooseClient::new)
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HypatiaConfig {
    pub vault_path: String,
    pub instance_name: String,
    pub design_target_model: String,
    pub register: String,
    pub address_term: String,
}

#[derive(Debug, Serialize)]
pub struct Identity {
    pub name: String,
    pub pronouns: String,
    pub address_term: String,
    pub super_objective: String,
}

/// Send a message to Hypatia (via Goose) and return her response.
#[tauri::command]
pub async fn send_message(message: String, session_id: Option<String>) -> Result<ChatResponse, String> {
    let req = ChatRequest { message, session_id };
    client().send_chat(req).await.map_err(|e| {
        error!(?e, "send_message failed");
        e.to_string()
    })
}

/// Read hypatia.config.yaml and return curated fields.
#[tauri::command]
pub fn get_config() -> Result<HypatiaConfig, String> {
    let repo_root = std::env::var("HYPATIA_REPO_ROOT")
        .map(PathBuf::from)
        .or_else(|_| std::env::current_dir().map_err(|e| e.to_string()))
        .map_err(|e| e.to_string())?;
    let config_path = repo_root.join("hypatia.config.yaml");
    let content = std::fs::read_to_string(&config_path)
        .map_err(|e| format!("could not read {:?}: {}", config_path, e))?;
    let yaml: serde_yaml::Value = serde_yaml::from_str(&content)
        .map_err(|e| format!("invalid yaml at {:?}: {}", config_path, e))?;

    Ok(HypatiaConfig {
        vault_path: yaml["vault"]["path"]
            .as_str()
            .unwrap_or("")
            .to_string(),
        instance_name: yaml["instance"]["name"]
            .as_str()
            .unwrap_or("Hypatia")
            .to_string(),
        design_target_model: yaml["instance"]["design_target_model"]
            .as_str()
            .unwrap_or("")
            .to_string(),
        register: yaml["preferences"]["register"]
            .as_str()
            .unwrap_or("alexandrian-scholar")
            .to_string(),
        address_term: yaml["preferences"]["address_term"]
            .as_str()
            .unwrap_or("Scholar")
            .to_string(),
    })
}

/// Return Hypatia's identity summary for the UI sidebar.
/// Static for now; could parse kernel/01-identity.md dynamically later.
#[tauri::command]
pub fn get_identity() -> Identity {
    Identity {
        name: "Hypatia".into(),
        pronouns: "she / her".into(),
        address_term: "Scholar".into(),
        super_objective:
            "Make the Scholar's knowledge compound, and never let stale claims or quiet \
             contradictions outlast a session that could have caught them."
                .into(),
    }
}
