"""Measurement envelope present, per-call labelled, computed (ADR-003)."""
import pathlib
import re

import pytest

import leanscene_core
import leanscene_mcp_tools
from leanscene_core import TokenMeter, estimate
from leanscene_mcp_tools import (
    get_actor_brief,
    get_actors_in_radius,
    get_assets_missing_lods,
    get_unlinked_materials,
    summarize_level,
    verify_bounds,
    verify_overlap,
    verify_transform,
)
from leanscene_unreal_gateway import FakeGateway


@pytest.fixture
def meter() -> TokenMeter:
    return TokenMeter()


def _call_all(gw, meter):
    actors = gw.list_actors()
    first, second = actors[0], actors[1]
    return [
        get_actors_in_radius(gw, meter, (0, 0, 0), 10_000.0),
        get_unlinked_materials(gw, meter),
        get_assets_missing_lods(gw, meter),
        summarize_level(gw, meter),
        get_actor_brief(gw, meter, first.id),
        verify_bounds(gw, meter, first.id, list(first.bounds)),
        verify_transform(gw, meter, first.id, list(first.location)),
        verify_overlap(gw, meter, first.id, second.id),
    ]


def test_every_tool_carries_a_per_call_envelope(meter):
    gw = FakeGateway.from_fixture_name("scene_medium")
    for env in _call_all(gw, meter):
        assert set(env) == {"result", "measure"}
        m = env["measure"]
        assert set(m) == {"lean_tokens", "firehose_tokens", "delta_pct_this_call"}
        # the per-call label is structural and never dropped
        assert "delta_pct_this_call" in m
        assert isinstance(m["lean_tokens"], int) and m["lean_tokens"] > 0


def test_delta_equals_estimator_output(meter):
    gw = FakeGateway.from_fixture_name("scene_medium")
    env = get_actors_in_radius(gw, meter, (0, 0, 0), 10_000.0)
    expected = estimate(env["result"], gw.raw_actors(), meter)
    m = env["measure"]
    assert m["lean_tokens"] == expected.lean_tokens
    assert m["firehose_tokens"] == expected.firehose_tokens
    assert m["delta_pct_this_call"] == expected.delta_pct_this_call


def test_lean_payload_smaller_than_firehose_for_data_tools(meter):
    gw = FakeGateway.from_fixture_name("scene_large")
    for env in (
        get_actors_in_radius(gw, meter, (0, 0, 0), 10_000_000.0),
        summarize_level(gw, meter),
    ):
        m = env["measure"]
        assert m["firehose_tokens"] >= m["lean_tokens"]
        assert 0 <= m["delta_pct_this_call"] <= 100


def test_no_fixed_percentage_advertised_in_source():
    # ADR-003: no fixed percentage hard-coded/advertised anywhere in core/mcp-tools.
    roots = [
        pathlib.Path(leanscene_core.__file__).parent,
        pathlib.Path(leanscene_mcp_tools.__file__).parent,
    ]
    pattern = re.compile(r"\d+(\.\d+)?\s*%")
    offenders = []
    for root in roots:
        for py in root.rglob("*.py"):
            for lineno, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
                if pattern.search(line):
                    offenders.append(f"{py}:{lineno}: {line.strip()}")
    assert not offenders, offenders
