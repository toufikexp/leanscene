"""LeanScene MCP tools (free, MIT) — Component A.

The pinned v1 tool set: each tool returns a fixed minimal schema with a per-call
measurement envelope, built on the gateway + core shapers/estimator. Pure logic is
in ``tools.py`` (headless-tested); the FastMCP adapter in ``server.py`` is a stub.
"""
from .descriptions import TOOL_DESCRIPTIONS
from .tools import (
    OFFENDERS_CAP,
    RADIUS_CAP,
    V1_TOOLS,
    get_actor_brief,
    get_actors_in_radius,
    get_assets_missing_lods,
    get_unlinked_materials,
    summarize_level,
    verify_bounds,
    verify_overlap,
    verify_transform,
)

__all__ = [
    "V1_TOOLS",
    "TOOL_DESCRIPTIONS",
    "RADIUS_CAP",
    "OFFENDERS_CAP",
    "get_actors_in_radius",
    "get_unlinked_materials",
    "get_assets_missing_lods",
    "summarize_level",
    "get_actor_brief",
    "verify_bounds",
    "verify_overlap",
    "verify_transform",
]
