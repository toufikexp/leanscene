"""UnrealGateway is an abstract contract returning plain dataclasses (ADR-002)."""
import inspect

import pytest

from leanscene_core import ActorRecord, AssetRecord, LevelSummary, UnrealGateway


def test_gateway_is_abstract():
    with pytest.raises(TypeError):
        UnrealGateway()  # the interface itself must not be instantiable


def test_gateway_surface_is_coarse_and_few():
    # Guard that the surface stays small: every method is an engine-bump risk.
    abstract = {
        name
        for name, member in inspect.getmembers(UnrealGateway, predicate=inspect.isfunction)
        if getattr(member, "__isabstractmethod__", False)
    }
    assert abstract == {
        "list_actors",
        "get_actor",
        "get_level_summary",
        "get_assets",
        "get_world_state_hash",
    }


def test_records_are_plain_and_minimal():
    actor = ActorRecord(
        id="a1",
        actor_class="StaticMeshActor",
        location=(0.0, 0.0, 0.0),
        bounds=(1.0, 1.0, 1.0),
        flags=("no_lod",),
    )
    assert actor.id == "a1"
    assert actor.flags == ("no_lod",)

    asset = AssetRecord(path="/Game/Meshes/SM_Rock", asset_class="StaticMesh")
    assert asset.flags == ()  # defaults are empty, not None

    summary = LevelSummary(name="L_Test", actor_count=1, class_histogram={"StaticMeshActor": 1})
    assert summary.actor_count == 1
    assert summary.class_histogram["StaticMeshActor"] == 1
