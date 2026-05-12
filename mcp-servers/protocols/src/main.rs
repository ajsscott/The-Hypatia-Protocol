//! hypatia-protocols-mcp
//!
//! MCP server that serves Hypatia's protocol library + kernel-archive detail
//! files as MCP resources. The compact always-loaded kernel (`kernel/`) carries
//! identity / voice / critical gates / routing. Everything else loads on demand
//! via this server.
//!
//! URI scheme:
//! - `protocol://<cluster>-<role>`         (e.g. protocol://librarian-role)
//! - `protocol://<cross-cutting>`          (e.g. protocol://security)
//! - `protocol://detail/<topic>`           (kernel-archive detail expansion)
//!
//! Transport: stdio (standard MCP). Goose's MCP host spawns this binary and
//! communicates via JSON-RPC over stdin/stdout.

use anyhow::{Context, Result};
use rmcp::{
    Error as McpError, ServerHandler, ServiceExt,
    model::*,
    service::*,
};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use tracing::{info, warn};

const SERVER_NAME: &str = "hypatia-protocols-mcp";

/// Resources served by this MCP server. URI → (filesystem path, description).
type ResourceMap = HashMap<String, ResourceEntry>;

#[derive(Clone)]
struct ResourceEntry {
    path: PathBuf,
    name: String,
    description: String,
}

#[derive(Clone)]
struct ProtocolsServer {
    resources: Arc<ResourceMap>,
}

impl ProtocolsServer {
    fn new(repo_root: &Path) -> Result<Self> {
        let mut resources = HashMap::new();

        // Cluster + cross-cutting protocols at hypatia-kb/protocols/*.md
        let protocols_dir = repo_root.join("hypatia-kb/protocols");
        if protocols_dir.exists() {
            for entry in walkdir::WalkDir::new(&protocols_dir)
                .min_depth(1)
                .max_depth(1)
                .into_iter()
                .filter_map(Result::ok)
                .filter(|e| {
                    e.path().extension().and_then(|s| s.to_str()) == Some("md")
                        && e.file_name() != "README.md"
                })
            {
                let stem = entry
                    .path()
                    .file_stem()
                    .and_then(|s| s.to_str())
                    .unwrap_or_default()
                    .to_string();
                let uri = format!("protocol://{}", stem);
                resources.insert(
                    uri.clone(),
                    ResourceEntry {
                        path: entry.path().to_path_buf(),
                        name: stem.clone(),
                        description: format!(
                            "Hypatia protocol: {} (loaded on keyword match)",
                            stem
                        ),
                    },
                );
            }
        } else {
            warn!("protocols dir not found: {:?}", protocols_dir);
        }

        // Kernel-archive detail resources at docs/reference/phase-1-kernel-archive/
        let archive_dir = repo_root.join("docs/reference/phase-1-kernel-archive");
        if archive_dir.exists() {
            // Map filename → URI topic (compact kernel content is in kernel/;
            // detail expansion lives here).
            let archive_map: &[(&str, &str, &str)] = &[
                (
                    "03-anti-patterns.md",
                    "detail/anti-patterns",
                    "Full anti-pattern enumeration (language, behavioral, truth, response, process)",
                ),
                (
                    "04-session-gates.md",
                    "detail/session-gates",
                    "Full session gate behaviors: IMG, pre-task, session start, destructive action",
                ),
                (
                    "05-tools.md",
                    "detail/tools",
                    "Tool inventory reference (largely archival once Goose tool system is live)",
                ),
                (
                    "06-cognitive.md",
                    "detail/cognitive",
                    "OBSERVE>QUESTION>DEDUCE + Cognitive Synchronization Pattern detail",
                ),
                (
                    "07-intelligence-layer.md",
                    "detail/intelligence",
                    "Full tiered surfacing, confidence thresholds, claim-match verification",
                ),
                (
                    "08-save-command.md",
                    "detail/save",
                    "Full 6-step save flow specification",
                ),
                (
                    "09-security.md",
                    "detail/security-gates",
                    "Full Git Hardening + External Content Security gates (kernel-level)",
                ),
                (
                    "10-skills-loading.md",
                    "detail/skills-map",
                    "Full canonical protocol keyword map",
                ),
                (
                    "11-decision-routes.md",
                    "detail/decision-routes",
                    "Full Decision Routes A-F spec with frameworks, ROI, examples",
                ),
                (
                    "02-voice.md",
                    "detail/voice",
                    "Full voice register: cadence, signature phrasings, examples, pattern of shifting",
                ),
            ];

            for (filename, topic, desc) in archive_map.iter() {
                let path = archive_dir.join(filename);
                if !path.exists() {
                    warn!("archive file missing: {:?}", path);
                    continue;
                }
                let uri = format!("protocol://{}", topic);
                resources.insert(
                    uri.clone(),
                    ResourceEntry {
                        path,
                        name: topic.to_string(),
                        description: desc.to_string(),
                    },
                );
            }
        } else {
            warn!("kernel-archive dir not found: {:?}", archive_dir);
        }

        info!("loaded {} protocol resources", resources.len());

        Ok(Self {
            resources: Arc::new(resources),
        })
    }
}

impl ServerHandler for ProtocolsServer {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            protocol_version: ProtocolVersion::V_2024_11_05,
            capabilities: ServerCapabilities::builder().enable_resources().build(),
            server_info: Implementation {
                name: SERVER_NAME.into(),
                version: env!("CARGO_PKG_VERSION").into(),
            },
            instructions: Some(
                "Hypatia's protocol library, served as MCP resources. The compact \
                 always-loaded kernel (kernel/01-04.md) is in context from session \
                 start; deeper protocols load on demand via this server when \
                 keyword matches fire."
                    .into(),
            ),
        }
    }

    async fn list_resources(
        &self,
        _request: Option<PaginatedRequestParam>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListResourcesResult, McpError> {
        let resources = self
            .resources
            .iter()
            .map(|(uri, entry)| Resource {
                uri: uri.clone(),
                name: entry.name.clone(),
                description: Some(entry.description.clone()),
                mime_type: Some("text/markdown".into()),
                annotations: None,
            })
            .collect();
        Ok(ListResourcesResult {
            resources,
            next_cursor: None,
        })
    }

    async fn read_resource(
        &self,
        request: ReadResourceRequestParam,
        _context: RequestContext<RoleServer>,
    ) -> Result<ReadResourceResult, McpError> {
        let entry = self.resources.get(&request.uri).ok_or_else(|| {
            McpError::resource_not_found(
                format!("no resource at URI: {}", request.uri),
                None,
            )
        })?;
        let content = std::fs::read_to_string(&entry.path).map_err(|e| {
            McpError::internal_error(format!("failed to read {:?}: {}", entry.path, e), None)
        })?;
        Ok(ReadResourceResult {
            contents: vec![ResourceContents::TextResourceContents {
                uri: request.uri,
                mime_type: Some("text/markdown".into()),
                text: content,
            }],
        })
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "hypatia_protocols_mcp=info".into()),
        )
        .with_writer(std::io::stderr)  // stdout is reserved for MCP protocol
        .init();

    let repo_root = std::env::var("HYPATIA_REPO_ROOT")
        .map(PathBuf::from)
        .or_else(|_| std::env::current_dir())
        .context("could not determine HYPATIA_REPO_ROOT")?;

    info!(?repo_root, "starting hypatia-protocols-mcp");
    let server = ProtocolsServer::new(&repo_root)?;

    let service = server
        .serve(rmcp::transport::stdio())
        .await
        .context("failed to start MCP service")?;
    service.waiting().await.context("MCP service failed")?;
    Ok(())
}
