# leanscene-mcp-tools (free, MIT) — Component A

The pinned **v1 tool set**. Each tool calls the gateway for the minimum it needs,
shapes the result into a fixed minimal schema via `core`, and attaches a per-call
measurement envelope.

v1 tools (pinned — not expanded in v1):
`get_actors_in_radius`, `get_unlinked_materials`, `get_assets_missing_lods`,
`summarize_level`, `get_actor_brief`, and the `verify_*` group
(`verify_bounds`, `verify_overlap`, `verify_transform`).

Every tool returns:

```json
{ "result": { ... fixed minimal schema ... },
  "measure": { "lean_tokens": N, "firehose_tokens": M, "delta_pct_this_call": P } }
```

`delta_pct_this_call` is **per-call** and computed locally with the offline token
meter (ADR-003). It is **not** an end-to-end workflow saving, and there is no fixed
percentage anywhere. On the seed fixtures the firehose payloads are synthetic
seeds, so the numbers are illustrative until real captures exist.

Pure tool logic lives in `tools.py` and is tested headless against `FakeGateway`.
The FastMCP exposure (`server.py`) is a **stub** — see its TODO and `CLAUDE.md`.
