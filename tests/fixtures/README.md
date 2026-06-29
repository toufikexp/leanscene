# tests/fixtures — seed scene payloads

These are **hand-written seed fixtures**, not real captures. They exist so tools
and core logic can be built and tested headless *before* any live Unreal capture
exists (Task 00).

- `scene_small.json` — ~3 actors.
- `scene_medium.json` — ~12 actors.
- `scene_large.json` — ~47 actors (deterministically generated seed).

Each file is marked `"_seed": true` with a `"_note"` saying so. The top-level
sections (`level`, `actors`, `assets`, `sector_hashes`) are the **gateway-coarse**
`UnrealGateway` view (already minimal per ADR-005).

Each file also has a **`firehose`** section: verbose, redundant payloads that stand
in for the native Web Remote Control "dump everything" response, served by
`FakeGateway` via the `FirehoseSource` interface so the shadow estimator has a
native equivalent to measure against. These firehose payloads are **synthetic
seeds** (deterministically inflated from the coarse records), also marked
`"_seed": true` — their shape is provisional and any per-call token delta computed
against them is **illustrative until real captures exist**.

⚠️ The exact payload shape is **provisional**. It was not verified against a live
editor (project constraint #1: verify against a captured fixture, never memory).
Replace these with real captures as soon as a live editor is available — see
`docs/capturing-fixtures.md`.
