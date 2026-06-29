"""Basic acceptance: every tool x every fixture -> stable per-call delta, offline."""
import pytest

from leanscene_core import TokenMeter
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

SCENES = ["scene_small", "scene_medium", "scene_large"]


def _calls(gw, meter):
    actors = gw.list_actors()
    first, second = actors[0], actors[1]
    return {
        "get_actors_in_radius": lambda: get_actors_in_radius(gw, meter, (0, 0, 0), 1e7),
        "get_unlinked_materials": lambda: get_unlinked_materials(gw, meter),
        "get_assets_missing_lods": lambda: get_assets_missing_lods(gw, meter),
        "summarize_level": lambda: summarize_level(gw, meter),
        "get_actor_brief": lambda: get_actor_brief(gw, meter, first.id),
        "verify_bounds": lambda: verify_bounds(gw, meter, first.id, list(first.bounds)),
        "verify_overlap": lambda: verify_overlap(gw, meter, first.id, second.id),
        "verify_transform": lambda: verify_transform(gw, meter, first.id, list(first.location)),
    }


@pytest.mark.parametrize("scene", SCENES)
def test_every_tool_emits_a_stable_per_call_delta(scene):
    meter = TokenMeter()
    gw = FakeGateway.from_fixture_name(scene)
    calls = _calls(gw, meter)
    assert len(calls) == 8  # the full pinned v1 set

    for name, call in calls.items():
        first_run = call()["measure"]
        second_run = call()["measure"]
        assert first_run == second_run, f"{name} not deterministic on {scene}"
        assert set(first_run) == {"lean_tokens", "firehose_tokens", "delta_pct_this_call"}
        assert isinstance(first_run["delta_pct_this_call"], float)
        assert isinstance(first_run["lean_tokens"], int)
