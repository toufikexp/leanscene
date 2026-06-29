"""RealGateway tests.

The interface-shape check runs headless. The actual round-trip over Web Remote
Control needs a LIVE UE 5.8 editor and is marked ``@pytest.mark.editor`` so it is
excluded from the default run (see pytest.ini). Run it manually.
"""
import pytest

from leanscene_core import UnrealGateway
from leanscene_unreal_gateway import RealGateway


def test_real_gateway_is_a_gateway_but_stubbed():
    # Constructible headless; calling a method makes the stub status explicit.
    gateway = RealGateway()
    assert isinstance(gateway, UnrealGateway)
    with pytest.raises(NotImplementedError):
        gateway.list_actors()


@pytest.mark.editor
def test_real_gateway_roundtrip_against_live_editor():
    # MANUAL STEP (not in headless CI):
    #   1. Launch UE 5.8 with the Web Remote Control / MCP plugin enabled.
    #   2. Open a level with a few actors.
    #   3. Run: pytest -m editor packages/unreal-gateway
    # This will fail until RealGateway is implemented (real_gateway.py TODOs) and
    # its payload shapes are verified against the live editor.
    gateway = RealGateway()
    actors = gateway.list_actors()
    assert actors  # placeholder assertion; refine once payloads are captured
