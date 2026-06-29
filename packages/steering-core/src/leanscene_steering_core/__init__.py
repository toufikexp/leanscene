"""LeanScene steering-core (free, MIT) — Component B, levers 1-2.

- Lever 1: tuned tool descriptions, shared with mcp-tools (`descriptions`).
- Lever 2: the static `CLAUDE.md` / `.cursorrules` starter (`rules`).
- Lever 3 (premium) extension point only — the generator lives out-of-tree
  (`extension`).

Steering is agent-side only (ADR-001): descriptions + rules, never engine mutation.
"""
from .descriptions import TOOL_DESCRIPTIONS, review_descriptions
from .extension import (
    GeneratedRuleset,
    ProjectManifest,
    SteeringGenerator,
    ToolEntry,
    ToolsetSnapshot,
)
from .rules import TARGETS, static_rules

__all__ = [
    # lever 1
    "TOOL_DESCRIPTIONS",
    "review_descriptions",
    # lever 2
    "static_rules",
    "TARGETS",
    # lever 3 boundary (contract only)
    "ToolEntry",
    "ToolsetSnapshot",
    "ProjectManifest",
    "GeneratedRuleset",
    "SteeringGenerator",
]
