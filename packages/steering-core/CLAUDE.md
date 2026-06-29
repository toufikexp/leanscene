# CLAUDE.md — steering-core (nested)

Conventions for this package. Read after the root `CLAUDE.md`.

- **Steering is agent-side only (ADR-001).** Descriptions + rules. Never add code
  or rule text that deregisters, overrides, or monkey-patches native tools. The
  templates must not instruct registry mutation either.
- **Descriptions are shared, not copied.** `TOOL_DESCRIPTIONS` is re-exported from
  `mcp-tools` (the source of truth) so the two can't drift. Don't fork the strings
  here. (Sourcing them here would create a `mcp-tools` <-> `steering-core` cycle.)
- **Lever 2 is static.** `static_rules()` returns fixed template files. Anything
  that tailors rules to a *project* (manifest-driven) is lever 3 — premium, behind
  the `extension.py` contract, out-of-tree (ADR-004/ADR-007). Do not implement a
  `SteeringGenerator` in this free tree.
- **Keep the template in sync with the tools.** `test_rules_template.py` asserts
  every v1 tool name appears in each starter; if the tool set changes, update the
  templates in the same change.
