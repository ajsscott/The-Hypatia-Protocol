# Benchmarks

Performance, scale, and behavioral metrics for the Hypatia ecosystem.

## Contents

| File | What It Tracks |
|---|---|
| `run-benchmark.py` | 24-test harness — CSR routing, integrity, retrieval, schemas, gate coverage. Run from `hypatia-kb/`. |
| `benchmark-candidates.md` | Catalog of measurable metrics, tiered by collection readiness. |
| `save-protocol-benchmark.md` | Per-save timing, token estimates, capture counts. |
| `img-gate-stress-test.md` | Image-source gate adversarial stress test. |

## Running

```bash
cd hypatia-kb
uv run python Benchmarks/run-benchmark.py
```

The harness loads `Intelligence/*.json` + `Memory/*.json` + the `.roo/rules-hypatia/` kernel (concatenated) and emits PASS / FAIL / INFO per test.

## Expected behavior with empty stores

Hypatia ships with empty Intelligence/Memory stores per Q-06. On a fresh-clone run, the harness will return zero-hit results for entry-counting / retrieval / coverage tests. That's correct, not broken — the stores grow only through deliberate Scholar consolidation.

Tests against the kernel (gate coverage, anti-pattern coverage, kernel coherence) run independent of store population and produce real signal even on a fresh clone.

## Re-baseline cadence

Once Hypatia has accumulated ≥3 months of consolidated entries (rough threshold for representative usage), regenerate baseline snapshots. Suggested cadence after that: quarterly, or after major protocol edits / refactors.

The 2026-03-21/22 Bell-era snapshot reports were deleted during the Phase 1 rewrite — they measured a different system. The first Hypatia baseline will be its own ground truth.

## Test catalog (24 tests)

| # | Test | Type | What It Proves |
|---|---|---|---|
| 1 | CSR Retrieval Accuracy | Component | Index lookup mechanics work |
| 2 | End-to-End Retrieval | E2E | Full CSR pipeline surfaces relevant entries |
| 3 | Adversarial CSR Routing | Adversarial | Off-domain signals return zero hits |
| 4 | Index-Store Consistency | Integrity | No orphans, ghosts, or duplicates |
| 5 | Tag Reachability | Coverage | Every entry findable via ≥1 tag |
| 6 | Cross-Reference Integrity | Integrity | All reasoning-chain references valid |
| 7 | Protocol Trigger Accuracy | Routing | Every keyword maps to an existing protocol |
| 8 | Gate Coverage | Docs | All gates documented with triggers |
| 9 | Vectorstore Quality | Integrity | Vectors normalized, self-consistent |
| 10 | Memory Retrieval | E2E | Active projects reach relevant memories |
| 11 | Session Index Integrity | Integrity | 1:1 index-to-file correspondence |
| 12 | Confidence Distribution | Quality | Scores distributed enough for prioritization |
| 13 | Kernel & Anti-Pattern Coverage | Docs | All kernel sections non-empty |
| 14 | Reasoning Retrieval via Reuse Signals | E2E | Reasoning entries findable via native routing |
| 15 | Synonym Map Effectiveness | Behavioral | Synonym expansion catches what direct lookup misses |
| 16 | RRF Hybrid Retrieval | E2E | Semantic + keyword fusion bridges vocabulary gaps |
| 17 | Tag Quality Audit | Quality | Tags match likely query terms |
| 18 | Negative Protocol Routing | Adversarial | Non-matching keywords don't trigger protocols |
| 19 | Schema Integrity | Integrity | Every entry has required fields per schema |
| 20 | ID Sequence Integrity | Integrity | IDs sequential with documented gaps only |
| 21 | Index Meta Accuracy | Integrity | `_meta.total` matches actual entry counts |
| 22 | Proxy URL Filtering | Security | Blocked URLs rejected; legitimate pass |
| 23 | Behavioral Trigger Detection | Security | Injection patterns caught; low false positive rate |
| 24 | Kernel Coherence | Integrity | Keyword-map protocols all exist on disk |

## Phase status

This harness is structurally ready but contains tests (8, 23, 24) referencing Bell-era gate names that may not match Hypatia's evolved vocabulary 1:1. Phase 1.5 follow-up: audit gate references, pin to actual Hypatia gate enumeration.

Phase 3 follow-up: re-baseline against populated stores; capture as `baseline-YYYY-MM-DD.md`.
