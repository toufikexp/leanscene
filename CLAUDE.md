# CLAUDE.md — LeanScene

> Operating manual for the coding agent. Read this fully before any task. Keep it accurate: if reality diverges from this file, fix the file in the same change.

## What this is
LeanScene is a plugin + agent-rules pack that cuts an AI agent's token cost when it works in large Unreal Engine 5.8 scenes, and **proves the saving with a local, no-API measurement**. It ships open-core: a free MIT tool library + steering starter, and paid premium packs (dynamic steering engine, local context cache, end-to-end measurement).

## Prime directive
Every change must make the agent's scene interaction cheaper (fewer tokens) **or** prove that it did, without ever overstating the saving. Token discipline *is* the product, not a side effect.

## The five constraints that govern everything
1. **Experimental ground.** UE 5.8's MCP plugin and the Web Remote Control API are unstable and will break across versions. Assume nothing about payload shapes — verify against a captured fixture, never against memory.
2. **The headless/editor seam is sacred.** All business logic (tokenizing, schema-shaping, diffing, shadow estimation, steering generation) MUST run and be tested with **no Unreal Editor running**, behind the `UnrealGateway` interface. Only the thin gateway implementation touches the live editor. If you need the editor to test core logic, the boundary is wrong — fix the boundary.
3. **Measurement honesty is non-negotiable.** The headline metric is a **per-call payload delta** (lean tool output vs. the native firehose output for the same query), computed locally with a real tokenizer. Never report a fixed percentage. Never present per-call deltas as end-to-end workflow savings. End-to-end is a separate, opt-in, clearly-labelled benchmark.
4. **Steer the agent; do not mutate the engine.** Bias tool selection via tool descriptions + generated rules (`CLAUDE.md` / `.cursorrules`). Do **not** deregister or monkey-patch native MCP tools as a core mechanism — it is fragile against an experimental subsystem. If a clean, supported override exists, it is an opt-in last resort behind a flag, never the default.
5. **Open-core boundary is physical.** Free MIT core and premium code live in separate trees and never mix in the public repo. Premium extends the core through defined extension points; it never forks it. Before adding code, know which side of the line it is on.

## Tech stack
- Engine: Unreal Engine 5.8 (target), MCP via the native `ModelContextProtocol` plugin + `ToolsetRegistry`.
- Tools: Python 3.11+, FastMCP, `ToolsetDefinition` classes.
- Editor access: UE Python Editor Scripting + Web Remote Control API — **only inside the gateway**.
- Tokenizer: tiktoken + Anthropic token counting, local only, no network.
- Cache (premium): Python state-diff + change detection.
- Targets: Claude Code / Claude API, Cursor.

## Repo topology
- `packages/core/` — free, MIT. Pure-logic core + `UnrealGateway` interface + `FakeGateway`.
- `packages/unreal-gateway/` — free, MIT. The real Web Remote Control implementation of `UnrealGateway`. **The only place `unreal` is imported.**
- `packages/mcp-tools/` — free, MIT. FastMCP tool definitions (Component A) + tuned descriptions.
- `packages/steering-core/` — free, MIT. Static rules template + description-tuning helpers.
- `premium/` — **paid, not MIT, never in the public repo.** Dynamic steering engine, context cache, end-to-end measurement.
- `docs/` — design + task specs (this is your build backlog).

## How to work
- **Test-first for all core logic.** A change to `packages/core` or `packages/mcp-tools` lands with tests that run headless — no editor, no network.
- **Fixtures over live calls.** Capture real Web Remote Control payloads once into `tests/fixtures/`, then test shaping/measurement against them. Mark anything needing a live editor with `@pytest.mark.editor` and exclude it from the default run.
- **Token-budget by construction.** Every tool returns a fixed, minimal schema. If output size scales with scene size unboundedly, the design is wrong — add a filter, a summary, or a cap.
- **Small, verifiable changes.** One tool or one capability per change, with its acceptance criteria from the task spec met and demonstrated.

## Definition of done (every change)
- [ ] Headless tests pass with no editor and no network.
- [ ] Output schema is fixed and minimal; size does not grow unbounded with scene size.
- [ ] If it touches measurement: per-call delta only, labelled as such; no fixed %.
- [ ] If it touches steering: agent-side only; no engine mutation by default.
- [ ] Correct side of the open-core line; no premium code in free trees.
- [ ] Docs touched by the change are updated in the same change.

## Stop and ask before
- Deregistering / overriding any native MCP tool.
- Making any numeric savings claim that is not a measured per-call delta.
- Adding a dependency that reaches the network at runtime.
- Moving code across the free/premium boundary.

## Where to go deeper
- `docs/ARCHITECTURE.md` — system design + the gateway seam + data contracts.
- `docs/DECISIONS.md` — why the load-bearing choices are what they are (read before challenging them).
- `docs/ROADMAP.md` — v1 scope, build order, catalog.
- `docs/tasks/` — the build backlog, in order.

## Note on these docs
Docs are context budget — the same budget this product exists to protect. Keep them lean and high-signal. When a package grows its own conventions, add a short nested `CLAUDE.md` in that package rather than bloating this one.
