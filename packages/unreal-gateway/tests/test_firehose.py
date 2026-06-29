"""FakeGateway implements FirehoseSource by serving the fixture firehose seeds."""
import json

import pytest

from leanscene_core import FirehoseSource
from leanscene_unreal_gateway import FakeGateway

SCENES = ["scene_small", "scene_medium", "scene_large"]


@pytest.fixture(params=SCENES)
def gw(request) -> FakeGateway:
    return FakeGateway.from_fixture_name(request.param)


def test_is_firehose_source(gw):
    assert isinstance(gw, FirehoseSource)


def test_raw_actors_match_coarse_count(gw):
    raw = gw.raw_actors()
    assert len(raw) == len(gw.list_actors())
    assert all(isinstance(r, dict) for r in raw)


def test_raw_actor_by_id_and_miss(gw):
    known = gw.list_actors()[0]
    payload = gw.raw_actor(known.id)
    assert payload is not None and payload["Name"] == known.id
    assert gw.raw_actor("does-not-exist") is None


def test_raw_assets_match_coarse_count(gw):
    assert len(gw.raw_assets()) == len(gw.get_assets())


def test_firehose_payload_is_more_verbose_than_coarse(gw):
    known = gw.list_actors()[0]
    raw_len = len(json.dumps(gw.raw_actor(known.id)))
    assert raw_len > 100  # verbose seed, much bigger than the lean brief


def test_missing_firehose_section_raises_clearly():
    gw = FakeGateway({"actors": [], "assets": []})  # no "firehose" key
    with pytest.raises(KeyError):
        gw.raw_actors()
