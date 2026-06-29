# Task 03 — Measurement (Component C)

**Goal.** Make the saving visible and honest. The per-call shadow estimator is the demo's hero; end-to-end is a separate premium benchmark.

## Basic shadow estimator (free)
When a lean tool runs, also obtain the raw firehose payload the gateway exposes for the equivalent native query, count both with the local token meter, and emit `{ lean_tokens, firehose_tokens, delta_pct_this_call }`. Deterministic, offline, instant.
**Honesty (ADR-003):** this is a **per-call payload** proxy — not end-to-end workflow savings (which depend on call count + caching). The label `this_call` must never be dropped.

## Acceptance (basic)
- [ ] For each tool + fixture, estimator emits a stable per-call delta, offline.
- [ ] Envelope is labelled per-call everywhere it surfaces (tool output, docs, demo).
- [ ] No fixed percentage is hard-coded or advertised anywhere.

## End-to-end benchmark (PREMIUM)
Runs a representative agent task with and without LeanScene and reports true workflow token use. Clearly separated from the per-call metric in name, output, and docs.
**Acceptance:** produces a reproducible end-to-end figure for a defined task; output cannot be confused with the per-call delta.

## Demo asset
The 2–3 min video shows a real before/after on a real scene using these numbers — never a slogan, never a fixed %.
