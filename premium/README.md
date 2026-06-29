# premium/ — placeholder only (NOT in the public repo)

This directory marks the open-core boundary (ADR-004). **No premium code, keys, or
licensed logic ever lives here in the public repo.**

The paid packs — dynamic steering engine, local context cache, end-to-end
measurement — are developed and distributed in a separate, private tree and sold
via Gumroad. They **extend** the free core through defined extension points; they
never fork it.

What is here:
- `LICENSE-COMMERCIAL.md` — the commercial license note (premium is **not** MIT).

Defined extension points the premium packs implement (in their private tree),
without forking the free core:
- **Dynamic steering engine (Task 02, lever 3 / ADR-007)** → implements the
  `SteeringGenerator` contract in `packages/steering-core/.../extension.py`
  (`(ToolsetSnapshot, ProjectManifest) -> GeneratedRuleset`, deterministic,
  regenerated on toolset change).

If you are an agent working in this repo: building any actual premium feature is
out of scope for the public trees. Stop and confirm the boundary before adding
code under `premium/` (see `CLAUDE.md` → "Stop and ask before").
