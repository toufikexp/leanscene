# CLAUDE.md — mcp-tools (nested)

Conventions for this package. Read after the root `CLAUDE.md`.

- **Pure logic vs MCP binding.** Tool behaviour is a pure function
  `(gateway, meter, args) -> envelope dict` in `tools.py` — headless-tested. The
  FastMCP registration in `server.py` is a thin, **stubbed** adapter (uncertain
  API; do not invent it). Never put gateway/shaping logic in `server.py`.
- **Bounded by construction (ADR-005).** Every list-returning tool goes through
  `_capped()` → `{items: […≤cap], total, truncated}`. If you add a tool whose
  output could scale with scene size, cap it. No raw passthrough.
- **Envelope on every tool (ADR-003).** Return `with_envelope(result, firehose,
  meter)`. Keep the `delta_pct_this_call` key intact; never advertise a fixed %.
- **Firehose = the native payload avoided.** Get it from the gateway's
  `FirehoseSource` (`raw_actors` / `raw_actor` / `raw_assets`). Pick the one that
  matches the tool's native equivalent (single-actor tools → `raw_actor`).
- **Descriptions are steering (ADR-001).** Tuned strings in `descriptions.py` are
  the source of truth shared with `steering-core`. Each must bias toward the lean
  tool and away from the firehose. Agent-side only — never mutate native tools.
