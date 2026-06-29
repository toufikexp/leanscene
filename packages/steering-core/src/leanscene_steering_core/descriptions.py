"""Lever 1 — tuned tool descriptions (shared with Task 01's mcp-tools).

The MCP tool descriptions ARE the steering descriptions (lever 1 is owned jointly
with Task 01, ADR-001). We re-export the SAME object from mcp-tools as the single
source of truth, so the two can never drift. Descriptions are sourced in mcp-tools
(not here) to avoid a steering-core <-> mcp-tools import cycle.
"""
from __future__ import annotations

from typing import Dict, List, Mapping, Optional, Tuple

from leanscene_mcp_tools import TOOL_DESCRIPTIONS as _MCP_TOOL_DESCRIPTIONS

#: Shared, single source of truth (same object as leanscene_mcp_tools.TOOL_DESCRIPTIONS).
TOOL_DESCRIPTIONS: Dict[str, str] = _MCP_TOOL_DESCRIPTIONS

# A good description steers toward the lean tool ...
_BIAS_CUES = (
    "prefer",
    "instead",
    "avoid",
    "cheap",
    "compact",
    "token-efficient",
    "only",
    "before",
)
# ... and explicitly away from the native broad read / firehose.
_ANTI_FIREHOSE_CUES = (
    "firehose",
    "full",
    "whole",
    "verbose",
    "outliner",
    "entire",
    "native",
    "registry",
)


def review_descriptions(
    descriptions: Optional[Mapping[str, str]] = None,
) -> List[Tuple[str, List[str]]]:
    """Return ``(tool_name, [issues])`` for any description that fails bias review.

    Empty list == every description is reviewed-clean. Operationalizes lever 1's
    "descriptions reviewed" acceptance headlessly.
    """
    descriptions = descriptions if descriptions is not None else TOOL_DESCRIPTIONS
    problems: List[Tuple[str, List[str]]] = []
    for name, text in descriptions.items():
        lowered = text.lower()
        issues: List[str] = []
        if len(lowered) < 40:
            issues.append("too thin")
        if not any(cue in lowered for cue in _BIAS_CUES):
            issues.append("no selection-bias cue")
        if not any(cue in lowered for cue in _ANTI_FIREHOSE_CUES):
            issues.append("no anti-firehose cue")
        if issues:
            problems.append((name, issues))
    return problems
