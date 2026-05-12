//! HTTP client for the Goose daemon API.
//!
//! Goose runs as `goose serve --port 8765` (configurable). This client wraps
//! the chat endpoint for now. As Goose's API surface stabilizes, expand to
//! session management, resource queries, etc.

use anyhow::{Context, Result};
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;
use tracing::{debug, warn};

const DEFAULT_GOOSE_URL: &str = "http://127.0.0.1:8765";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatRequest {
    pub message: String,
    pub session_id: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatResponse {
    pub message: String,
    pub session_id: String,
    /// Goose may also return tool invocations, resource loads, etc.
    /// For v1 we just surface the assistant message.
    #[serde(default)]
    pub raw: serde_json::Value,
}

pub struct GooseClient {
    base_url: String,
    http: Client,
}

impl GooseClient {
    pub fn new() -> Self {
        let base_url = env::var("HYPATIA_GOOSE_URL").unwrap_or_else(|_| DEFAULT_GOOSE_URL.into());
        Self {
            base_url,
            http: Client::new(),
        }
    }

    /// Send a chat message; await Goose's response.
    ///
    /// Endpoint and payload shape are placeholders pending Goose API
    /// stabilization. Adjust against actual `goose serve` schema.
    pub async fn send_chat(&self, req: ChatRequest) -> Result<ChatResponse> {
        let url = format!("{}/chat", self.base_url);
        debug!(?url, "sending chat to Goose");
        let response = self
            .http
            .post(&url)
            .json(&req)
            .send()
            .await
            .with_context(|| format!("failed to POST {}", url))?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            warn!(?status, ?body, "Goose returned non-success");
            anyhow::bail!("Goose error: {} — {}", status, body);
        }

        let body: serde_json::Value = response
            .json()
            .await
            .context("failed to parse Goose response as JSON")?;

        // Goose's response shape may vary; extract the assistant message
        // defensively. Tighten once schema is stable.
        let message = body
            .get("message")
            .and_then(|v| v.as_str())
            .or_else(|| body.get("content").and_then(|v| v.as_str()))
            .unwrap_or("(no message in Goose response)")
            .to_string();
        let session_id = body
            .get("session_id")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();

        Ok(ChatResponse {
            message,
            session_id,
            raw: body,
        })
    }

    pub async fn health_check(&self) -> bool {
        let url = format!("{}/health", self.base_url);
        match self.http.get(&url).send().await {
            Ok(r) => r.status().is_success(),
            Err(_) => false,
        }
    }
}

impl Default for GooseClient {
    fn default() -> Self {
        Self::new()
    }
}
