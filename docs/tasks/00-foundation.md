# Task 00 — Foundation

**Goal.** Stand up the skeleton that makes everything else buildable and testable headless. No feature code until this is done.

## Deliverables
- Repo layout per `CLAUDE.md` → Repo topology. Free `packages/*` (MIT), `premium/*` placeholder (commercial license note), `docs/`, `tests/fixtures/`.
- `UnrealGateway` interface in `packages/core` — coarse methods returning plain dicts/dataclasses (see `docs/ARCHITECTURE.md` → core). No `unreal` import.
- `FakeGateway` in `packages/unreal-gateway` serving fixtures from `tests/fixtures/`. Seed with 2–3 hand-written fixtures (small / medium / large-ish scene payloads) so tools can be built before any live capture exists.
- `RealGateway` stub in `packages/unreal-gateway` — method signatures + TODOs; real Web Remote Control calls marked `@pytest.mark.editor`.
- Token meter in `packages/core` — tiktoken + Anthropic counting, pure, offline.
- CI: default run is headless + offline; `@pytest.mark.editor` excluded by default; an **import check that fails if `unreal` is imported outside `unreal-gateway`**.
- MIT `LICENSE` in each free package; a separate commercial license note under `premium/`.
- A short "capturing fixtures" doc: how to run against a live editor and save raw Web Remote Control payloads into `tests/fixtures/`.

## Acceptance
- [ ] `pytest` passes with no editor and no network.
- [ ] Importing `unreal` in `packages/core` fails CI.
- [ ] Token meter returns stable counts for fixed strings, offline.
- [ ] FakeGateway returns the seeded fixtures through the `UnrealGateway` interface.

## Out of scope
Any actual tool, any steering, any cache. Foundation only.
