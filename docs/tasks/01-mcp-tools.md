# Task 01 — MCP tools (Component A, free)

**Goal.** The pinned v1 tool set, each returning a fixed minimal schema with a per-call measurement envelope, built on FastMCP and tested headless via FakeGateway.

## v1 tools (pinned — do not expand in v1)
1. `get_actors_in_radius(point, r)` — spatial filter; returns a capped list of `actor_brief`.
2. `get_unlinked_materials()` — semantic; returns only offending assets.
3. `get_assets_missing_lods()` — semantic; returns only assets missing LODs.
4. `summarize_level()` — compact structural summary (counts, classes, sectors), never the full outliner.
5. `get_actor_brief(id)` — fixed `actor_brief` schema.
6. `verify_*` group — `verify_bounds`, `verify_overlap`, `verify_transform`: deterministic boolean/struct checks so the agent confirms placement cheaply **before** any vision check.

## Each tool must
- Call the gateway for the minimum needed (no "fetch all then filter in Python" if a narrower gateway call exists).
- Shape output via `core` into a fixed schema; **bounded size** — `get_actors_in_radius` and any potentially-large result is capped/summarized by design (ADR-005).
- Attach the measurement envelope (`lean_tokens`, `firehose_tokens`, `delta_pct_this_call`) from the shadow estimator.
- Carry a tuned description biasing selection over native reads (shared with `steering-core`).

## Acceptance
- [ ] Each tool tested headless against FakeGateway fixtures.
- [ ] Output schema fixed; property test: output size does not grow unbounded as fixture scene size grows.
- [ ] Measurement envelope present and labelled per-call.
- [ ] Descriptions present and reviewed for selection bias.
- [ ] (Editor, manual) tools resolve and run over a real MCP connection.

## Notes
The `verify_*` group is a token-saving pattern (cheap deterministic check before expensive vision) — treat it as first-class, not an afterthought.

**Build note.** The per-call measurement envelope requires the **basic shadow estimator** (Task 03, free tier), which `docs/ROADMAP.md` flags as overlapping this task and living in `core`. It landed here (`core/measure.py` + a `FirehoseSource` interface + seed firehose fixtures) to satisfy the envelope. Task 03's **end-to-end (premium)** benchmark is untouched. On the seed fixtures the firehose payloads are synthetic seeds, so the deltas are illustrative until real captures exist.
