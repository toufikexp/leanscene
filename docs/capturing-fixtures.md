# Capturing fixtures (manual, needs a live editor)

The seed fixtures in `tests/fixtures/` are hand-written placeholders. To make them
real, capture actual Web Remote Control payloads from a running UE 5.8 editor and
save them here. This is an irreducibly manual step (ADR-002) — budget for it.

> ⚠️ The exact request paths and response shapes below are **TODO**. They were not
> verified against a live editor and must not be trusted until they are. Do not
> guess them from memory — capture, inspect, then write them down.

## 1. Enable the API in UE 5.8
- Enable the **Remote Control API** / **Web Remote Control** plugin (and the
  native MCP / `ModelContextProtocol` plugin, if testing the MCP round-trip).
- TODO(editor): confirm the HTTP host/port the editor serves (the stub assumes
  `http://127.0.0.1:30010` — verify).

## 2. Capture raw payloads
- Drive the editor to the state you want (open a level, select actors).
- Issue the Web Remote Control calls that back each `UnrealGateway` method and
  save the **raw** JSON responses verbatim.
- TODO(editor): record the exact endpoint + request body for each of:
  `list_actors`, `get_actor`, `get_level_summary`, `get_assets`,
  `get_world_state_hash`.

## 3. Save two shapes
1. **Gateway-coarse** (what `FakeGateway` serves) → `tests/fixtures/scene_*.json`,
   matching the current seed shape. Drop the `"_seed"` marker once it is a real
   capture and record provenance (engine version, date, level).
2. **Raw firehose** (the verbose native output, for the shadow estimator in
   Task 03) → `tests/fixtures/raw/` (added when Task 03 lands).

## 4. Wire and verify
- Implement the corresponding `RealGateway` method (`real_gateway.py` TODOs).
- Run the live test: `pytest -m editor packages/unreal-gateway`.
- Re-run the headless suite to confirm `FakeGateway` still serves the new shape.
