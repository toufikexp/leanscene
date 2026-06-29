# Steering eval (manual)

Whether the agent *actually obeys* steering can't be checked headless (ADR /
ARCHITECTURE: it's the irreducibly-manual column). This is the reproducible
protocol for the two manual acceptance items in Task 02. Run it against a target
agent (Claude Code / Cursor) connected to the LeanScene tools.

> ⚠️ Manual + subjective. Record outcomes; don't claim a fixed number. The
> headline product metric is still the per-call payload delta (ADR-003), not these
> eval rates.

## Demo task (use the same one for both levers)
On a large scene:

> "List the actors within 500 units of the player start, and tell me which of the
> level's assets are missing LODs."

This naturally tempts a firehose read (dump the outliner / the whole asset
registry). The lean path is `get_actors_in_radius` + `get_assets_missing_lods`
(and `summarize_level` for context).

## Lever 1 — descriptions bias selection (A/B)
1. **A (tuned):** expose the tools with their real `TOOL_DESCRIPTIONS`.
2. **B (neutral):** expose the same tools with neutralized one-liners (e.g.
   "Returns actors.", "Returns assets.") — no efficiency/anti-firehose cues.
3. Run the demo task N times per arm (e.g. N=5), fresh context each run.
4. Record how often the agent picks the lean tool over a broad/native read.
**Pass:** arm A prefers the efficient tools for the target tasks **more often**
than arm B.

## Lever 2 — static rules avoid the firehose
1. Drop `static_rules("claude")` into the project as `CLAUDE.md` (or
   `static_rules("cursor")` as `.cursorrules`).
2. Give a **fresh** agent the demo task.
3. Observe whether it goes straight to the lean tools or dumps the outliner /
   asset registry.
**Pass:** with the starter present, a fresh agent avoids the firehose on the demo
task.

## Notes
- Keep the captured transcripts; they are the evidence for these acceptance items.
- These evals gate "does steering work", not "is the saving real" — keep the two
  separate (ADR-003).
