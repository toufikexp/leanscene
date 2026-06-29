# Architecture

## Design thesis
The only way to build and test this reliably against an **experimental** Unreal API is to keep almost all logic **independent of Unreal** and put the editor behind a single, narrow interface. Everything valuable — shaping data, counting tokens, diffing state, generating steering — is pure logic that runs headless. The editor binding is thin, isolated, and the only part that needs a running editor to test.

## End-to-end flow

```
AI agent (Claude Code / Cursor)
  │  reads steering (free static rules OR premium dynamic engine)
  │  → biased to efficient tools, told to avoid the native firehose
  ▼
MCP (native UE 5.8 plugin / local HTTP)
  ▼
mcp-tools (FastMCP ToolsetDefinitions)              [FREE]
  │   each tool: filter/summarize → fixed minimal schema
  │   each tool: emit per-call token delta via shadow estimator
  ├─► core: schema shapers, token meter, shadow estimator, diff   [FREE, pure logic]
  │       └─ depends on UnrealGateway (interface), never on UE directly
  ├─► context cache: skip unchanged sectors across a session       [PREMIUM]
  ▼
UnrealGateway (interface)                            [FREE]
  ├─ RealGateway → Web Remote Control API → live editor            [FREE, editor-only tests]
  └─ FakeGateway → tests/fixtures/ (captured payloads)             [FREE, headless tests]
```

## Components

### core (free, pure logic, no UE import)
The heart. Contains:
- **`UnrealGateway`** — the one interface to the editor. Methods are coarse and few: `list_actors()`, `get_actor(id)`, `get_level_summary()`, `get_assets()`, `get_world_state_hash(sector)`, etc. Returns plain dicts/dataclasses, not UE objects.
- **Schema shapers** — turn raw gateway payloads into fixed, minimal output schemas (the `*_brief` shapes). Token-budget-by-construction lives here.
- **Token meter** — wraps tiktoken + Anthropic counting. Pure function: bytes/string → token count. Offline.
- **Shadow estimator** — given a lean result and the raw firehose payload, compute the **per-call** token delta. Pure, deterministic. The firehose payload is exposed via a separate `FirehoseSource` interface (`raw_actors` / `raw_actor` / `raw_assets`) that gateways implement, so measurement plumbing stays off the coarse `UnrealGateway` contract.
- **Diff engine** (used by the premium cache) — sector hashing + change-detection primitives. Kept in free core because they are generic; the *caching policy* that uses them is premium.

`core` imports nothing from Unreal. This is enforced by an import check in CI.

### unreal-gateway (free)
`RealGateway`: the only code that talks to Web Remote Control. Translates the experimental, verbose API into the coarse `UnrealGateway` contract. When UE changes, **this is the file that changes** — the blast radius of an engine bump is contained here. Tests here are `@pytest.mark.editor` and run manually against a live editor.

`FakeGateway`: serves captured fixtures from `tests/fixtures/`. Lets every other package be tested headless. Capturing new fixtures is a documented manual step (run against a real editor, save the raw payloads).

### mcp-tools (free, Component A)
FastMCP `ToolsetDefinition`s. Each tool:
1. Calls the gateway for the minimum it needs.
2. Shapes via `core` into a fixed schema.
3. Attaches a per-call token delta from the shadow estimator.
4. Carries a **tuned description** that biases selection ("compact, token-efficient … prefer over full-level reads").

v1 tool set (pin exactly — see `docs/tasks/01-mcp-tools.md`):
`get_actors_in_radius`, `get_unlinked_materials`, `get_assets_missing_lods`, `summarize_level`, `get_actor_brief`, and a `verify_*` group (bounding-box / overlap / transform checks) for cheap deterministic confirmation before any vision check.

### steering-core (free, Component B levers 1–2)
- Tuned tool descriptions (shared with mcp-tools).
- A static `CLAUDE.md` / `.cursorrules` starter that forbids native broad sweeps and points the agent at the efficient tools.

### premium (paid, separate tree)
- **Dynamic steering engine (Component B lever 3).** Concrete v1 definition: a generator that reads (a) the live toolset registry and (b) a small project manifest, and **emits a tailored ruleset** mapping the project's tasks to the efficient tools, regenerated when the toolset changes. "Dynamic" = regenerated on change, **not** runtime ML or per-prompt rewriting. If you cannot express its input→output as a deterministic generator, stop and redefine it (see `docs/DECISIONS.md` ADR-007).
- **Local context cache (Component D).** Uses `core`'s diff engine to detect unchanged sectors and short-circuit re-queries within a session. Invalidation against live editor state is the single most fragile part of the product — see `docs/tasks/04-context-cache.md`.
- **End-to-end measurement.** Runs a representative agent task with and without LeanScene and reports true workflow savings — clearly separated from the per-call metric.

## Data contracts

Principle: **fixed schema, minimal fields, bounded size.** Output must not grow unbounded with scene size; if a query could return thousands of items, it returns a capped, summarized, or filtered result by design.

Illustrative `actor_brief`:
```json
{ "id": "...", "class": "StaticMeshActor", "loc": [x,y,z], "bounds": [sx,sy,sz], "flags": ["no_lod"] }
```
No transforms-as-prose, no nested component trees, no redundant metadata. Every field earns its tokens.

Every tool result carries a measurement envelope:
```json
{ "result": { ... }, "measure": { "lean_tokens": N, "firehose_tokens": M, "delta_pct_this_call": P } }
```
`delta_pct_this_call` is explicitly per-call. The UI and docs must never drop the `this_call` framing.

## What is testable where
| Layer | Headless (default CI) | Needs live editor (manual, `@pytest.mark.editor`) |
|---|---|---|
| core (shapers, meter, shadow estimator, diff) | all | — |
| mcp-tools (shaping + measurement, via FakeGateway) | yes | tool round-trip over real MCP |
| steering-core (rule generation) | yes | whether the agent actually obeys (manual eval) |
| unreal-gateway (RealGateway) | — | all |
| premium cache (diff logic) | yes | invalidation against live edits |

The right-hand column is irreducibly manual. Budget for it; do not pretend it is CI-covered.
