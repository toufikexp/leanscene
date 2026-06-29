# leanscene-steering-core (free, MIT) — Component B (levers 1–2)

Agent-side steering only (ADR-001): tool descriptions + rules, never engine
mutation.

- **Lever 1 — tuned descriptions.** The MCP tool descriptions are the steering
  descriptions; this package re-exports the **same** `TOOL_DESCRIPTIONS` object
  from `mcp-tools` (single source of truth) and adds `review_descriptions()` for a
  headless bias check.
- **Lever 2 — static rules starter.** `static_rules("claude" | "cursor")` returns a
  fixed, self-contained starter that forbids native broad sweeps, maps each task to
  the lean tool, and encodes verify-before-vision. Users drop it into their project
  as `CLAUDE.md` / `.cursorrules`. The raw templates live under
  `src/leanscene_steering_core/templates/`.
- **Lever 3 (premium) — extension point only.** `extension.py` defines the
  deterministic-generator contract (`SteeringGenerator` + `ToolsetSnapshot` /
  `ProjectManifest` / `GeneratedRuleset`). The generator itself is **premium and
  out-of-tree** (ADR-004/ADR-007); nothing here implements it.

The "does the agent actually obey" question is a **manual** eval — see
`docs/steering-eval.md`.
