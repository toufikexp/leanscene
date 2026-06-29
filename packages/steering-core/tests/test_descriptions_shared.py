"""Lever 1: descriptions are shared with mcp-tools and pass bias review."""
from leanscene_mcp_tools import TOOL_DESCRIPTIONS as MCP_DESCRIPTIONS
from leanscene_mcp_tools import V1_TOOLS
from leanscene_steering_core import TOOL_DESCRIPTIONS as STEERING_DESCRIPTIONS
from leanscene_steering_core.descriptions import review_descriptions


def test_descriptions_are_the_same_shared_object():
    # Same object -> the two surfaces cannot drift.
    assert STEERING_DESCRIPTIONS is MCP_DESCRIPTIONS


def test_every_v1_tool_has_a_description():
    assert set(STEERING_DESCRIPTIONS) == set(V1_TOOLS)


def test_all_descriptions_pass_bias_review():
    assert review_descriptions() == []


def test_review_flags_a_neutral_description():
    # A neutral, non-biasing description must be flagged (proves the check works).
    neutral = {"x": "Returns some actors."}
    problems = review_descriptions(neutral)
    assert problems and problems[0][0] == "x"
