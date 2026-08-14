---
name: tooling-venv-isolation
description: Never run `uv run` inside AJ's project directories — uv replaces the project's .venv and breaks poetry.
metadata:
  type: feedback
---

Never run `uv run` inside one of AJ's project directories that has its own
`.venv` (poetry-managed or otherwise). Even `--no-project` isn't safe: if uv
sees a broken interpreter link in `.venv/`, it silently removes and
recreates the venv with a different Python, then poetry has to reinstall
everything from scratch — several minutes on projects with ML deps
(torch/faster-whisper/pyannote).

**Why:** on 2026-07-29 I did `uv run --no-project --with pandas` from
`/Users/ajsscott/GitHub/renphil/OYM-playground/AI-Coach/` in the sandbox to
inspect cached parquets. It removed AJ's `.venv/` and recreated it with
Linux-aarch64 CPython 3.13.11. When AJ then ran `poetry run ...` on her
Mac, poetry saw a broken venv and started a full reinstall. Real
disruption to her workflow, not just to the sandbox.

**How to apply:**

- For sandbox pandas / json / csv exploration of files that live inside an
  AJ project: either `cd /tmp` first and run uv there against absolute
  paths to the data files, or ask AJ to run the inspection herself and
  paste output back.
- For any command that would install or invoke tools in a project's
  managed env, stick to that project's tool (poetry for AI-Coach,
  bundler/rails for Progress-Monitoring). Don't reach for a different
  package manager just because it's on PATH in the sandbox.
- If AJ's env already has the tool I need available on her Mac, prefer
  dictating the command for her to run over doing it in the sandbox.
- Sandbox-only exception: when the task is purely local (writing a
  scratch script under the scratchpad dir) and doesn't touch any project
  paths, uv is fine.
