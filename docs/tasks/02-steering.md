# Task 02 — Steering (Component B)

Three levers, in preference order (ADR-001). Free = levers 1–2 (`steering-core`); premium = lever 3 (`premium/`).

## Lever 1 — Tuned tool descriptions (free)
Each efficient tool's MCP description biases selection: compact/token-efficient, "prefer over full-level reads", with the task it is for. Owned jointly with Task 01.
**Acceptance:** descriptions reviewed; in a manual agent eval, the agent prefers efficient tools for the target tasks more often than with neutral descriptions.

## Lever 2 — Static rules starter (free)
A `CLAUDE.md` / `.cursorrules` starter that: forbids native broad sweeps (outliner dumps, full actor lists), points at the efficient tools by task, and encodes the verify-before-vision pattern. Ship as a template users drop into their project.
**Acceptance:** template is self-contained and correct; a fresh agent given it avoids the firehose on the demo task.

## Lever 3 — Dynamic steering engine (PREMIUM; ADR-007)
A **deterministic generator**, not runtime ML.
- **Input:** live toolset registry snapshot + a small project manifest (task types, conventions).
- **Output:** a tailored ruleset / `CLAUDE.md` mapping the project's tasks to the efficient tools.
- **Trigger:** regenerated when the toolset changes.
**Acceptance:** given a fixed (registry, manifest) input, emits a deterministic, correct ruleset; fully tested headless. If its behavior cannot be expressed as input→output, **stop and redefine** (ADR-007).

## Out of scope
Registry deregistration/override as a default mechanism (ADR-001). Only behind an opt-in flag where the engine cleanly supports it.

## Build note
Levers 1–2 are built and headless-tested in `packages/steering-core/` (descriptions shared with mcp-tools; static `CLAUDE.md`/`.cursorrules` starter via `static_rules()`). The "does the agent obey" parts of L1/L2 acceptance are **manual** — protocol in `docs/steering-eval.md`. Lever 3 is **premium**: per ADR-004 no premium code lives in the public repo, so only its extension-point contract (`steering-core/extension.py` `SteeringGenerator`) is free; the generator itself is implemented out-of-tree (the v1-premium build step). A repo test (`tests/test_open_core_boundary.py`) guards that `premium/` ships no `.py`.
