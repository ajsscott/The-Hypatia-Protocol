# 05 — Tools

The tool inventory available to Hypatia when running in Roo Code (same tool-use protocol as Cline; Q-21). This file replaces Bell's `tool-inventory.md`, which enumerated Kiro tool names that do not apply.

Tool names are spelled in `snake_case` per the Cline/Roo protocol. When a workflow needs a different tool than the obvious one, this file lists when to prefer which.

---

## File operations

### `read_file`

Read the full contents of a file at a given path. Use when:

- The file is small enough to read whole (under ~550 lines).
- The full structure matters (frontmatter + body together).

Do NOT use when:

- The file is large and only a section is needed. Use `execute_command` with `sed -n 'A,Bp'` or with a Python `pathlib` read on a slice.

### `write_to_file`

Write entire file content, creating the file if it doesn't exist or overwriting it if it does. Use when:

- Creating a new file from scratch.
- Replacing a file's contents wholesale (full rewrite).

Do NOT use when:

- Editing a portion of an existing file. Use `replace_in_file` instead.
- Moving or copying files. Use `execute_command` + `mv` / `cp`.

### `replace_in_file`

Surgical edit using one or more `SEARCH` / `REPLACE` blocks. Use when:

- Editing a section of an existing file.
- The exact text to replace is small and unambiguous.

Do NOT use when:

- The file is large JSON (>400 lines). `replace_in_file` fails silently on large JSON. Use `execute_command` + `python` or `jq` instead.
- The change is wholesale rewrite. Use `write_to_file`.

### `list_files`

List the contents of a directory. Use when:

- Discovering what's in a directory at runtime.
- Pre-flight check before a `write_to_file` or `replace_in_file` operation.

### `search_files`

Regex search across files in a directory. Use when:

- Finding all occurrences of a pattern across multiple files.
- The pattern is well-bounded and unlikely to false-match.

Do NOT use when:

- A direct read of a known file would answer the question. Read the file.
- The KB intelligence store has the answer. Read the index first; fall back to grep only if the index misses.

---

## Shell execution

### `execute_command`

Run a shell command. Use when:

- File-system operations beyond simple read / write (mv, cp, mkdir, find).
- Running scripts, tests, linters, formatters.
- Querying git state.
- Operations that span multiple files via shell pipes (grep + xargs, find -exec).
- Working with large JSON via `jq` or `python`.

Refuse long-running commands: dev servers, watch processes, interactive editors. Suggest manual execution instead. Keywords: `dev`, `start`, `watch`, `serve`, `nodemon`, `runserver`.

---

## Interaction

### `ask_followup_question`

Ask the Scholar a question when:

- A decision requires their judgment.
- An ambiguity must be resolved before proceeding.
- A destructive operation needs confirmation.

Do NOT use when:

- The answer is in the Scholar's stated preferences or prior sessions.
- The question is rhetorical or could be answered by reading the wiki.

### `attempt_completion`

Signal task completion when:

- The requested work is done.
- A natural pause point has been reached and the Scholar should review.

Include in the completion: what was changed, what was deferred, what the Scholar should verify.

---

## MCP integration

### `use_mcp_tool`

Call a tool provided by an MCP server (configured in `~/.roo/mcp.json` or equivalent).

### `access_mcp_resource`

Read a resource provided by an MCP server.

The MCP server registry for Hypatia is configured per-machine. Common servers: vault-side query, embedding lookup, vector DB.

---

## Tool selection patterns

| Task | Right tool | Wrong tool | Reason |
|---|---|---|---|
| Read a small markdown file | `read_file` | `execute_command cat` | Native tool is faster; preserves line numbering. |
| Read a section of a large file | `execute_command` + `sed -n` | `read_file` whole | Avoids truncation; explicit line bounds. |
| Edit a paragraph | `replace_in_file` | `write_to_file` | Surgical; preserves the rest of the file. |
| Edit a 500-line JSON entry | `execute_command` + `python` | `replace_in_file` | `replace_in_file` fails silently on large JSON. |
| Move / copy / rename files | `execute_command` + `mv` / `cp` / `git mv` | `write_to_file` + delete | Shell preserves metadata, atomic, faster. |
| Find all uses of `[[BaseName]]` | `search_files` regex | `read_file` on every Tree | Designed for this; scales. |
| Verify git state | `execute_command` + `git status` / `log` | n/a | No native git tool. |
| Run pytest | `execute_command` + `uv run pytest` | n/a | Tests run in the project env via uv. |

---

## Capability boundaries

Things Hypatia cannot do via tools, must surface to the Scholar:

- Modify Obsidian plugin state (`.obsidian/plugins/*/data.json` is plugin-owned; some plugins overwrite external edits).
- Trigger Obsidian-side commands (linter run, dataview refresh, plugin install) — those require Obsidian itself.
- Network operations beyond what MCP servers provide and what `execute_command` + `curl` can reach.
- Long-running processes (see `execute_command` refusal list above).

When a request requires one of these, surface the limit and propose the manual step the Scholar can take.

---

## Cross-references

- **When to load which protocol** — `.clinerules/10-skills-loading.md`
- **Session boot gates that govern tool use** — `.clinerules/04-session-gates.md` (pending)
- **The vault-side tools the Scholar uses (Obsidian plugins, YOLO transition)** — `hypatia-kb/protocols/librarian-tooling.md`
