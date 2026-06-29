"""Descriptions present and reviewed for selection bias (ADR-001)."""
import pytest

from leanscene_mcp_tools import TOOL_DESCRIPTIONS, V1_TOOLS

# A description must steer toward the lean tool ...
BIAS_CUES = (
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
ANTI_FIREHOSE_CUES = (
    "firehose",
    "full",
    "whole",
    "verbose",
    "outliner",
    "entire",
    "native",
    "registry",
)


def test_every_tool_has_a_description():
    assert set(TOOL_DESCRIPTIONS) == set(V1_TOOLS)


@pytest.mark.parametrize("name", sorted(V1_TOOLS))
def test_description_biases_selection(name):
    text = TOOL_DESCRIPTIONS[name].lower()
    assert len(text) > 40, f"{name}: description too thin"
    assert any(cue in text for cue in BIAS_CUES), f"{name}: no selection-bias cue"
    assert any(cue in text for cue in ANTI_FIREHOSE_CUES), f"{name}: no anti-firehose cue"
