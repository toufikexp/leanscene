# tests/fixtures — seed scene payloads

These are **hand-written seed fixtures**, not real captures. They exist so tools
and core logic can be built and tested headless *before* any live Unreal capture
exists (Task 00).

- `scene_small.json` — ~3 actors.
- `scene_medium.json` — ~12 actors.
- `scene_large.json` — ~47 actors (deterministically generated seed).

Each file is marked `"_seed": true` with a `"_note"` saying so. The shape is the
**gateway-coarse** `UnrealGateway` view (already minimal per ADR-005) — it is NOT
the raw Web Remote Control "firehose". The firehose payloads needed by the shadow
estimator are a separate capture (Task 03).

⚠️ The exact payload shape is **provisional**. It was not verified against a live
editor (project constraint #1: verify against a captured fixture, never memory).
Replace these with real captures as soon as a live editor is available — see
`docs/capturing-fixtures.md`.
