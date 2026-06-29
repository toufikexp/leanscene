"""Each v1 tool, exercised headless against FakeGateway seed fixtures."""
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


@pytest.fixture
def meter() -> TokenMeter:
    return TokenMeter()


@pytest.fixture
def small() -> FakeGateway:
    return FakeGateway.from_fixture_name("scene_small")


def test_actors_in_radius_filters(small, meter):
    env = get_actors_in_radius(small, meter, point=(0, 0, 0), radius=200.0)
    ids = [b["id"] for b in env["result"]["items"]]
    assert "sm_floor" in ids  # dist 0
    assert "sm_crate_01" in ids  # dist 130
    assert "light_key" not in ids  # dist 400 > 200
    assert env["result"]["total"] == len(ids)
    assert env["result"]["truncated"] is False


def test_actor_brief_found_and_missing(small, meter):
    found = get_actor_brief(small, meter, "sm_floor")
    assert found["result"]["actor"]["id"] == "sm_floor"
    assert found["result"]["actor"]["class"] == "StaticMeshActor"
    missing = get_actor_brief(small, meter, "nope")
    assert missing["result"]["actor"] is None


def test_unlinked_materials_returns_only_offenders(meter):
    gw = FakeGateway.from_fixture_name("scene_medium")
    env = get_unlinked_materials(gw, meter)
    paths = [a["path"] for a in env["result"]["items"]]
    assert paths and all("unlinked" in a["flags"] for a in env["result"]["items"])
    assert any("M_Concrete" in p for p in paths)


def test_assets_missing_lods_returns_only_offenders(meter):
    gw = FakeGateway.from_fixture_name("scene_large")
    env = get_assets_missing_lods(gw, meter)
    paths = [a["path"] for a in env["result"]["items"]]
    assert any("HighPoly" in p for p in paths)


def test_summarize_level_is_compact(small, meter):
    env = summarize_level(small, meter)
    result = env["result"]
    assert result["actors"] == 3
    assert result["classes"]["StaticMeshActor"] == 2
    assert result["classes"]["DirectionalLight"] == 1
    assert result["sectors"]  # non-empty occupied-sector list


def test_verify_bounds_ok_and_fail(small, meter):
    ok = verify_bounds(small, meter, "sm_floor", [1000.0, 1000.0, 10.0])
    assert ok["result"]["ok"] is True
    bad = verify_bounds(small, meter, "sm_floor", [1.0, 1.0, 1.0])
    assert bad["result"]["ok"] is False


def test_verify_transform_ok(small, meter):
    ok = verify_transform(small, meter, "sm_floor", [0.0, 0.0, 0.0])
    assert ok["result"]["ok"] is True
    off = verify_transform(small, meter, "sm_floor", [500.0, 0.0, 0.0])
    assert off["result"]["ok"] is False


def test_verify_overlap_returns_bool(small, meter):
    env = verify_overlap(small, meter, "sm_floor", "sm_crate_01")
    assert env["result"]["check"] == "overlap"
    assert isinstance(env["result"]["ok"], bool)


def test_verify_handles_missing_actor(small, meter):
    env = verify_bounds(small, meter, "nope", [1.0, 1.0, 1.0])
    assert env["result"]["found"] is False
    assert env["result"]["ok"] is False
