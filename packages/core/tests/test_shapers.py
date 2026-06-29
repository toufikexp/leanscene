"""Schema shapers produce fixed, minimal dicts (ADR-005)."""
from leanscene_core import (
    ActorRecord,
    AssetRecord,
    LevelSummary,
    actor_brief,
    asset_brief,
    level_summary_brief,
)


def test_actor_brief_is_fixed_and_minimal():
    rec = ActorRecord(
        id="a1",
        actor_class="StaticMeshActor",
        location=(1.234, 2.0, 3.0),
        bounds=(10.0, 20.0, 30.0),
        flags=("no_lod",),
    )
    brief = actor_brief(rec)
    assert set(brief) == {"id", "class", "loc", "bounds", "flags"}
    assert brief["class"] == "StaticMeshActor"
    assert brief["loc"] == [1.23, 2.0, 3.0]  # rounded, list (json-friendly)
    assert brief["flags"] == ["no_lod"]


def test_asset_brief_fixed_keys():
    brief = asset_brief(AssetRecord(path="/Game/X", asset_class="Material", flags=("unlinked",)))
    assert set(brief) == {"path", "class", "flags"}


def test_level_summary_brief_sectors_optional_and_sorted():
    summary = LevelSummary(name="L", actor_count=2, class_histogram={"A": 1, "B": 1})
    assert set(level_summary_brief(summary)) == {"name", "actors", "classes"}
    with_sectors = level_summary_brief(summary, sectors={"1,0", "0,0"})
    assert with_sectors["sectors"] == ["0,0", "1,0"]
