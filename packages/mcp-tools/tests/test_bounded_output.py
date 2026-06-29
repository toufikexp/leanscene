"""Property: output size stays bounded as fixture scene size grows (ADR-005)."""
import pytest

from leanscene_core import TokenMeter, canonical_json
from leanscene_mcp_tools import (
    RADIUS_CAP,
    get_actors_in_radius,
    get_assets_missing_lods,
    get_unlinked_materials,
    summarize_level,
)
from leanscene_unreal_gateway import FakeGateway

SCENES = ["scene_small", "scene_medium", "scene_large"]
WHOLE_SCENE_RADIUS = 10_000_000.0
#: A fixed ceiling: every lean RESULT must stay well under this for every scene.
RESULT_TOKEN_CEILING = 4000


@pytest.fixture
def meter() -> TokenMeter:
    return TokenMeter()


@pytest.mark.parametrize("scene", SCENES)
def test_list_results_are_capped_and_bounded(scene, meter):
    gw = FakeGateway.from_fixture_name(scene)
    # Radius covers the whole scene -> would return everything if unbounded.
    radius = get_actors_in_radius(gw, meter, (0, 0, 0), WHOLE_SCENE_RADIUS, cap=RADIUS_CAP)
    assert len(radius["result"]["items"]) <= RADIUS_CAP

    for tool in (get_unlinked_materials, get_assets_missing_lods):
        env = tool(gw, meter)
        items, total = env["result"]["items"], env["result"]["total"]
        assert len(items) <= 64
        assert len(items) <= total

    # Serialized result token size stays under a FIXED ceiling for every scene.
    for env in (radius, summarize_level(gw, meter)):
        tokens = meter.count_tokens(canonical_json(env["result"]))
        assert tokens <= RESULT_TOKEN_CEILING


def test_result_size_does_not_track_scene_size(meter):
    # The largest scene (47 actors) must not blow the radius result past the cap.
    small = get_actors_in_radius(
        FakeGateway.from_fixture_name("scene_small"), meter, (0, 0, 0), WHOLE_SCENE_RADIUS
    )
    large = get_actors_in_radius(
        FakeGateway.from_fixture_name("scene_large"), meter, (0, 0, 0), WHOLE_SCENE_RADIUS
    )
    assert len(large["result"]["items"]) <= RADIUS_CAP
    # large scene has more actors than small, but capped output never exceeds cap
    assert large["result"]["total"] > small["result"]["total"]
    assert len(large["result"]["items"]) <= RADIUS_CAP


def test_radius_cap_truncates_and_reports_total(meter):
    gw = FakeGateway.from_fixture_name("scene_large")  # 47 actors
    env = get_actors_in_radius(gw, meter, (0, 0, 0), WHOLE_SCENE_RADIUS, cap=5)
    assert env["result"]["truncated"] is True
    assert len(env["result"]["items"]) == 5
    assert env["result"]["total"] == 47
