"""FakeGateway serves the seeded fixtures through the UnrealGateway interface.

Headless: no editor, no network (ADR-002).
"""
import pytest

from leanscene_core import ActorRecord, LevelSummary, UnrealGateway
from leanscene_unreal_gateway import FakeGateway, default_fixtures_dir

SCENES = ["scene_small", "scene_medium", "scene_large"]


@pytest.fixture(params=SCENES)
def gateway(request) -> FakeGateway:
    return FakeGateway.from_fixture_name(request.param)


def test_fake_gateway_implements_the_interface(gateway):
    assert isinstance(gateway, UnrealGateway)


def test_all_seed_fixtures_exist():
    directory = default_fixtures_dir()
    for name in SCENES:
        assert (directory / f"{name}.json").is_file(), name


def test_list_actors_returns_records(gateway):
    actors = gateway.list_actors()
    assert actors, "seed scene should have at least one actor"
    assert all(isinstance(a, ActorRecord) for a in actors)
    # each record is plain + minimal: tuples, not UE objects
    first = actors[0]
    assert isinstance(first.location, tuple) and len(first.location) == 3
    assert isinstance(first.bounds, tuple) and len(first.bounds) == 3


def test_get_actor_roundtrips_and_misses(gateway):
    known = gateway.list_actors()[0]
    assert gateway.get_actor(known.id) == known
    assert gateway.get_actor("does-not-exist") is None


def test_level_summary_is_bounded_and_consistent(gateway):
    summary = gateway.get_level_summary()
    assert isinstance(summary, LevelSummary)
    assert summary.actor_count == len(gateway.list_actors())
    assert sum(summary.class_histogram.values()) == summary.actor_count


def test_get_assets_returns_records(gateway):
    for asset in gateway.get_assets():
        assert asset.path.startswith("/")
        assert isinstance(asset.flags, tuple)


def test_world_state_hash_is_deterministic(gateway):
    h1 = gateway.get_world_state_hash("0,0")
    h2 = gateway.get_world_state_hash("0,0")
    assert h1 == h2 and isinstance(h1, str) and h1


def test_small_scene_exact_seed_values():
    # Pin a couple of exact seed values so the fixture<->gateway mapping is locked.
    gw = FakeGateway.from_fixture_name("scene_small")
    summary = gw.get_level_summary()
    assert summary.name == "L_Seed_Small"
    actor = gw.get_actor("sm_floor")
    assert actor is not None
    assert actor.actor_class == "StaticMeshActor"
    assert actor.location == (0.0, 0.0, 0.0)
