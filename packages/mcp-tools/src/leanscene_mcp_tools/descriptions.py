"""Tuned tool descriptions — the steering lever that biases selection (ADR-001).

These strings ship on the MCP tools and are the source of truth that
``steering-core`` reuses in Task 02. Each one is written to pull the agent toward
the lean tool and AWAY from the native broad read / firehose. Steering is
agent-side only — we never deregister or mutate native tools (ADR-001).

Keep every description: (1) compact/efficient framing, (2) an explicit "prefer …
instead of / avoid the full … firehose" cue.
"""

TOOL_DESCRIPTIONS = {
    "get_actors_in_radius": (
        "Compact, token-efficient spatial query. Returns a CAPPED list of minimal "
        "actor briefs within a radius of a point. Prefer this over reading the full "
        "actor list / outliner, which returns the entire scene firehose."
    ),
    "get_unlinked_materials": (
        "Token-efficient semantic query. Returns ONLY assets with unlinked "
        "materials, as minimal briefs. Prefer this over dumping the whole asset "
        "registry and scanning it yourself."
    ),
    "get_assets_missing_lods": (
        "Token-efficient semantic query. Returns ONLY assets missing LODs, as "
        "minimal briefs. Prefer this over the full asset-registry firehose."
    ),
    "summarize_level": (
        "Compact structural summary of the level — counts, class histogram, and "
        "occupied sectors. Use this instead of reading the full outliner; it never "
        "returns the per-actor firehose."
    ),
    "get_actor_brief": (
        "Returns one actor in the fixed minimal brief schema. Prefer this over the "
        "verbose native 'describe actor' call, which returns its full component "
        "tree and transforms."
    ),
    "verify_bounds": (
        "Cheap deterministic bounds check (boolean + struct). Use this to confirm "
        "placement BEFORE any expensive vision check or full-actor read."
    ),
    "verify_overlap": (
        "Cheap deterministic AABB overlap check between two actors (boolean + "
        "struct). Use this instead of fetching both full actors to eyeball overlap, "
        "and before any vision check."
    ),
    "verify_transform": (
        "Cheap deterministic transform/location check (boolean + struct). Use this "
        "to confirm an actor's position BEFORE any vision check or verbose read."
    ),
}
