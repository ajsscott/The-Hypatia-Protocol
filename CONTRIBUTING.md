# Contributing to The Hypatia Protocol

Hypatia is AJ Strauman-Scott's personal-use AI partner-scholar. The codebase is MIT-licensed and public in case the architecture is useful to others, but the persona itself is tuned for a single Scholar's working register. Contributions are welcome with that scope in mind.

---

## What's open for contribution

**Substrate-agnostic improvements**: vectorstore (RRF tuning, fastembed model swaps, performance), save pipeline (`save-session.py`), schema validation (`validate-schemas.py`, `normalize-schemas.py`), security filters (`git-filter-clean.py`, `git-filter-smudge.py`), cross-platform polyfills if anyone wants to port off Mac, test scaffolding under `tests/`.

**Bug reports**: anything in `scripts/` or `hypatia-kb/vectorstore/` that doesn't work as documented.

**Documentation improvements**: typos, broken cross-references, stale paths.

---

## What's NOT open for contribution

**Hypatia's persona**: name, voice register, address term ("Scholar"), Greco-Roman Alexandrian framing. These are tuned for one user. Forks are encouraged for other personas.

**Decision routes (A-F) and gates**: the kernel architecture in `.roo/rules-hypatia/` is purpose-built for vault-librarian work. Changes here are unlikely to be accepted unless they fix a load-bearing bug.

**Bell-derived content** in `docs/reference/`: frozen historical artifacts. Do not edit.

---

## How to contribute

### Report a bug

[Open an issue](../../issues/new) with:
- What you expected to happen.
- What actually happened.
- Steps to reproduce.
- Platform (must be Mac for runtime issues; substrate is Roo Code in VS Code).
- Output of `uv run python --version` and `uv run pip list | grep -i hypatia`.

### Suggest an improvement

[Open an issue](../../issues/new) describing the substrate-agnostic problem you're trying to solve and your proposed fix. Persona-tuning suggestions will be politely declined.

### Submit a pull request

1. Fork the repo.
2. Create a branch (`git checkout -b fix/<short-name>`).
3. Make your changes. Add tests if the change affects `scripts/` or `hypatia-kb/vectorstore/`.
4. Verify locally:
   - `uv run pytest` passes.
   - `uv run ruff check` passes.
   - `bash -n scripts/<changed-script>.sh` passes for shell changes.
5. Atomic commit per concern; imperative-mood subject explaining *why*.
6. Submit PR with a clear description and links to relevant issues.

---

## Style guide

- **No em-dashes.** Use commas, colons, or split sentences. (Kernel-level rule per `.roo/rules-hypatia/03-anti-patterns.md`.)
- **No filler openings** ("Great question!", "So,", "Well,"). Lead with the answer.
- **Active voice preferred.** "The audit found three issues." not "Three issues were found."
- **Cite sources** for non-trivial claims. Tree wikilinks for vault content; external URLs for documentation references.
- **Markdown files should read without rendering.** Tables, code blocks, headers should work in raw form.
- **JSON files validate.** Run `uv run python -m json.tool < file.json` before committing.
- **Imperative-mood commits.** `fix: vectorstore returns wrong rank on tied scores` not `fixed bug`.

---

## Code of conduct

Be respectful. Be specific. Focus on the work, not the person. Disagree in writing if you have evidence; defer otherwise.
