"""Lever 2: the static rules starter is self-contained and correct."""
import pytest

from leanscene_mcp_tools import V1_TOOLS
from leanscene_steering_core import static_rules
from leanscene_steering_core.rules import TARGETS

TARGET_IDS = sorted(TARGETS)


@pytest.mark.parametrize("target", TARGET_IDS)
def test_template_is_self_contained(target):
    text = static_rules(target)
    assert len(text) > 400  # a real, droppable starter, not a stub


@pytest.mark.parametrize("target", TARGET_IDS)
def test_template_forbids_the_firehose(target):
    text = static_rules(target).lower()
    assert "outliner" in text
    assert "asset registry" in text
    assert "actor list" in text
    assert ("never" in text) or ("do not" in text)


@pytest.mark.parametrize("target", TARGET_IDS)
def test_template_maps_every_v1_tool(target):
    text = static_rules(target)
    for name in V1_TOOLS:
        assert name in text, f"{target} starter is missing tool {name}"


@pytest.mark.parametrize("target", TARGET_IDS)
def test_template_encodes_verify_before_vision(target):
    text = static_rules(target).lower()
    assert "verify" in text
    assert "before" in text
    assert ("vision" in text) or ("screenshot" in text)


@pytest.mark.parametrize("target", TARGET_IDS)
def test_template_does_not_instruct_registry_mutation(target):
    # ADR-001: steering never deregisters/monkey-patches native tools.
    text = static_rules(target).lower()
    assert "deregister" not in text
    assert "monkey-patch" not in text
    assert "monkeypatch" not in text


def test_unknown_target_raises():
    with pytest.raises(ValueError):
        static_rules("emacs")
