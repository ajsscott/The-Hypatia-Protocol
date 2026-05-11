# Development Protocol

**Purpose**: Universal development practices for code Hypatia writes or helps the Scholar write.
**Last Updated**: 2026-05-11 (Hypatia adaptation; aggressively thinned from Bell's 2,464 L original)
**Trigger Keywords**: code, develop, programming, refactor, technical, implement, build, deploy, library, dependency, debug, test

---

## Scope and context

Bell's original was heavily AWS/cloud/CTO-flavored: 2,464 L covering Cloud Engineering, React 19, Node.js 22 LTS, state management, ES2026 Temporal API, and UI/UX design. For Hypatia's actual context, almost none of that applies. The Scholar's code work is:

- **Hypatia codebase** (Python, shell): scripts, vectorstore, validation, ingestion.
- **Vault tooling** (Python, shell, occasional JS for Obsidian plugins): one-off scripts, frontmatter audits, Tree generation helpers.
- **Research code** (Python, Jupyter, occasional R): data science, ML experiments.

This protocol covers universal dev practices that apply to that work. Cross-references to other protocols handle adjacent concerns.

**Cross-references for adjacent concerns**:
- `problem-solving-protocol.md` for debugging methodology.
- `planning-protocol.md` for project planning and decomposition.
- `writing-protocol.md` for documentation prose standards.
- `security-protocol.md` for credential and PII handling.
- `CRITICAL-FILE-PROTECTION.md` for protected paths during code that touches the kernel or stores.

---

## Core principles

1. **Boring code ages well.** No clever metaclass tricks, no implicit magic, no global side effects on import.
2. **Explicit over implicit.** Type hints on Python public functions. Named kwargs past two arguments. No magic globals.
3. **One source of truth.** If a constant lives in two places, one is wrong eventually.
4. **Trust internal code.** Validate at system boundaries (user input, external APIs); don't validate within trusted internal calls.
5. **Test alongside code.** Not after. If logic is hard to test, the design is wrong.
6. **Observability first.** Logs, metrics, traces before the feature ships. Structured logs over `print`.
7. **Security by default.** No secrets in code, config, logs, or error messages. Least privilege at every layer.

---

## Tool selection

### Languages

| Use case | Language | Why |
|---|---|---|
| Hypatia scripts, vault tooling | Python 3.11+ | Aligns with pyproject.toml + uv.lock |
| Shell helpers (setup, filters, hooks) | Bash with `set -euo pipefail` | Portable; no Python deps needed |
| Vault plugins (rare) | TypeScript or JS | Obsidian's plugin runtime |
| Data analysis | Python (pandas, polars) or R | Scholar's research preference |

### Python tooling (per `pyproject.toml`)

- **Package manager**: `uv`.
- **Linter / formatter**: `ruff` (line-length 100, py311 target).
- **Type checker**: `mypy` (strict=false, ignore_missing_imports for libraries without stubs).
- **Test runner**: `pytest` (testpaths include `tests/` + `hypatia-kb/vectorstore/tests/`).

### Dependency rules

- Pin major versions in `pyproject.toml`; let minors / patches float.
- Lockfile (`uv.lock`) committed.
- No unpinned dependencies in production paths.
- Audit `uv tree` periodically for transitive surprises.

---

## Code quality standards

### Python

**Required**:
- Type hints on all public functions: `def f(x: int, y: str = "default") -> bool:`.
- Docstrings only where they add information not in the signature.
- `f"."` for string formatting (Python 3.6+).
- `pathlib.Path` over `os.path` string manipulation.
- Context managers for file / resource handling: `with open(path) as f:`.

**Forbidden** (per `.clinerules/03-anti-patterns.md § Code & technical work`):
- Bare `except:` or `except Exception:` without re-raise or structured log.
- Mutable default arguments (`def f(items=[])` is a bug).
- `print` where a logger belongs.
- `os.environ[.]` scattered through modules; centralize at a config boundary.
- Missing type hints on public functions; `Any` as a shrug.
- Silent `.get` with no default and no handling of `None`.
- HTTP clients with no timeout, no retry policy.
- `subprocess` calls with `shell=True` and interpolated input.

### Bash

**Required**:
- `set -euo pipefail` at the top of every script.
- Quote all variables: `"$var"`, not `$var`.
- `cd` chained with `|| exit`: `cd path || exit 1`.

**Forbidden**:
- Parsing `ls`. Use `find -print0 | xargs -0` for whitespace-safe iteration.
- Globbing unsafe paths.

### SQL

**Required**:
- Explicit column lists; no `SELECT *` in production paths.
- `LIMIT` on exploratory queries.

**Forbidden**:
- Implicit joins (use explicit `JOIN. ON.`).
- `UPDATE` / `DELETE` without `WHERE` in scripts.
- Schema changes without a migration tool.

---

## Code analysis & verification

### Before any change

1. **Read the file fully** (`read_file`); don't pattern-match from memory.
2. **Understand the function's role** in the broader system (`search_files` for callers if unclear).
3. **Check existing tests**: do they cover the path being changed? If yes, the test will validate. If no, write one alongside the change.
4. **Check for cross-file impact**: schema changes, public interface changes, behavior-shape changes.

### After any change

1. **Run the relevant test**: `uv run pytest <path>`.
2. **Run the type checker** if touching typed code: `uv run mypy <path>`.
3. **Run the linter**: `uv run ruff check <path>`.
4. **Verify behavior** with a smoke test (manual or scripted).

---

## Testing

### Test alongside code

- New function → new test in the same commit.
- Bug fix → regression test for the bug in the same commit.
- Refactor → no behavior change; existing tests must still pass.

### Test types

- **Unit**: pure function in isolation. Fast (<1s). Most tests are this.
- **Integration**: multiple components together. Slower. Use sparingly.
- **End-to-end**: full system pipeline. Slowest. Use for critical paths only.

### Test discipline

- One assertion per test where possible. Multiple assertions OK if they validate one logical claim.
- Tests should fail clearly: failure message should tell the Scholar what's wrong.
- No mocks of internal code without strong reason. Mock at the external-boundary only (HTTP, filesystem when needed, time).
- For Hypatia's vault-side tests: hit a real test vault, not mocks. Real-vault tests catch the failures mocks miss.

### Test discovery

- pytest discovers `tests/test_*.py` and `*_test.py` by default per `pyproject.toml`.
- `hypatia-kb/vectorstore/tests/` contains the vectorstore property-based tests (hypothesis library).

---

## Debugging

When debugging surfaces, route through `problem-solving-protocol.md` for the methodology. Specific dev-context tools:

### Python

- `breakpoint` (Python 3.7+) drops into pdb.
- `python -m ipdb script.py` for ipdb if available.
- `pdb.post_mortem` after an unhandled exception in interactive sessions.
- Logging at DEBUG level beats print statements (`logging.debug(.)` with formatter showing module + line).

### Shell

- `set -x` to trace execution.
- `bash -n script.sh` to syntax-check without running.
- `bash -x script.sh` to run with trace.

### Cross-platform

- macOS `stat -f %m` vs GNU `stat -c %Y`. Cross-platform pattern: `stat -c %Y. || stat -f %m. || echo 0`.
- `sed -i` differs (`sed -i ''` on macOS vs `sed -i` on GNU). Prefer Python for in-place YAML / JSON edits.

---

## Code maintenance

### Comments

Default: don't write them. Add a comment only when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug, behavior that would surprise a reader.

Don't explain WHAT the code does. Well-named identifiers do that. Don't reference the current task ("added for X feature"); those rot.

### Naming

- Functions: verb_phrase (`load_config`, `parse_seed_frontmatter`).
- Classes: NounPhrase (`Capture`, `VectorIndex`).
- Constants: UPPER_SNAKE_CASE (`DEFAULT_MODEL_NAME`).
- Private: leading underscore (`_internal_helper`).

### Refactor discipline

- Small commits. One concept per commit.
- "Move + modify" splits into two commits (move first, then modify).
- Before refactoring, ensure tests pass. After refactoring, ensure tests still pass.

---

## Security in development

See `.clinerules/09-security.md` for the authoritative governance + `security-protocol.md` for specific patterns.

In-line dev-specific rules:

- **Never** hardcode credentials, API keys, tokens.
- **Never** log credentials, even at DEBUG.
- **Never** include credentials in error messages.
- **Never** commit `.env` files (gitignore them).
- **Validate inputs at system boundaries**: user input, external APIs. Don't validate trusted internal calls.
- **Use `subprocess.run(., shell=False)` and pass args as a list**. Never `shell=True` with interpolated input.
- **HTTP clients**: always set a timeout. Always handle network failure paths.

---

## Version control

### Commit hygiene

- Small, atomic commits.
- Imperative-mood messages explaining *why*, not *what*.
- One concern per commit; no mixing refactor + feature + bug-fix.
- No `WIP` or `temp` commits on shared branches.

### Branch hygiene

- `main` (or `master`) is the integration branch.
- Feature branches off `main`.
- Vault: `work-safe` branch excludes personal content (`Seedlings/`, `Forests/`).
- No force-push to shared branches (kernel rule per `.clinerules/09-security.md`).

### Pre-commit gates

- `scripts/pre-commit-kb-validate.sh` validates JSON stores before commit.
- `.gitattributes` filter chain sanitizes Memory + Intelligence content on commit.
- Tests run on save command's git commit step (per `.clinerules/08-save-command.md`).

---

## Documentation

For prose standards, see `writing-protocol.md`. For code-specific documentation:

- **Module docstrings**: one paragraph stating what the module does and why it exists.
- **Function docstrings**: only when signature alone is insufficient. Include "raises" if exceptions are part of the contract.
- **README per script directory**: high-level overview, run instructions, dependency notes.
- **Inline comments**: rare, WHY-focused.
- **Don't** create planning / decision documents unprompted. Use commit messages for durable rationale.

---

## Output expectations

When delivering code:

- Code that runs (no placeholder fragments left in).
- Tests included or named as a separate follow-up.
- Documentation updated where the change affects the user-facing interface.
- Commit message that explains why.
- If the change has rollback implications, name the rollback story.

---

## Anti-Patterns

See `.clinerules/03-anti-patterns.md § Code & technical work` for the canonical list. In summary:

- Placeholder code that doesn't actually work.
- TODO comments without context.
- Hardcoded credentials.
- Bare `except`.
- Mutable default arguments.
- `subprocess` with `shell=True` + interpolated input.
- HTTP clients without timeouts.
- `print` where logger belongs.
- Refactoring without tests passing first.
- Mixing refactor + feature + fix in one commit.

---

## Cross-references

- **Anti-patterns (canonical)**: `.clinerules/03-anti-patterns.md § Code & technical work`
- **Tool inventory (Roo tools, when to use which)**: `.clinerules/05-tools.md`
- **Save command (commits during dev work)**: `.clinerules/08-save-command.md`
- **Security gates (credentials, sensitive paths)**: `.clinerules/09-security.md` + `security-protocol.md`
- **Critical file protection**: `CRITICAL-FILE-PROTECTION.md`
- **Problem-solving (debug methodology)**: `problem-solving-protocol.md`
- **Planning (project decomposition)**: `planning-protocol.md`
- **Writing (documentation prose)**: `writing-protocol.md`

---

*Boring code ages well. Test alongside. Trust the lockfile. Security by default. Atomic commits. Explain why.*
