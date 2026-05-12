// Hypatia frontend bootstrap.
// Loads identity + config on startup; wires chat send/receive to Tauri commands.

const { invoke } = window.__TAURI__.core;

const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("input-form");
const inputEl = document.getElementById("input-box");
const sendBtn = document.getElementById("send-btn");

let sessionId = null;

// ── Init ──────────────────────────────────────

async function loadIdentity() {
  try {
    const id = await invoke("get_identity");
    document.getElementById("hypatia-name").textContent = id.name;
    document.getElementById("hypatia-pronouns").textContent = id.pronouns;
    document.getElementById("super-objective").textContent = id.super_objective;
  } catch (e) {
    console.error("get_identity failed:", e);
  }
}

async function loadConfig() {
  try {
    const cfg = await invoke("get_config");
    document.getElementById("vault-path").textContent = cfg.vault_path || "(not configured)";
    document.getElementById("model").textContent = cfg.design_target_model || "(not configured)";
  } catch (e) {
    console.error("get_config failed:", e);
    document.getElementById("vault-path").textContent = "(error reading config)";
    document.getElementById("model").textContent = "—";
  }
}

// ── Chat ──────────────────────────────────────

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const p = document.createElement("p");
  p.textContent = text;
  div.appendChild(p);
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage(message) {
  appendMessage("user", message);
  sendBtn.disabled = true;
  inputEl.disabled = true;

  // Show a thinking indicator
  const thinkingEl = document.createElement("div");
  thinkingEl.className = "message system";
  thinkingEl.innerHTML = "<p>Hypatia is thinking…</p>";
  messagesEl.appendChild(thinkingEl);

  try {
    const response = await invoke("send_message", {
      message,
      sessionId,
    });
    thinkingEl.remove();
    sessionId = response.session_id || sessionId;
    appendMessage("hypatia", response.message);
  } catch (e) {
    thinkingEl.remove();
    console.error("send_message failed:", e);
    appendMessage("system", `Error: ${e}`);
  } finally {
    sendBtn.disabled = false;
    inputEl.disabled = false;
    inputEl.focus();
  }
}

// ── Wire-up ───────────────────────────────────

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = "";
  sendMessage(text);
});

// Enter-to-send; Shift+Enter for newline.
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    formEl.requestSubmit();
  }
});

// ── Boot ──────────────────────────────────────

(async function init() {
  await Promise.all([loadIdentity(), loadConfig()]);
  inputEl.focus();
})();
