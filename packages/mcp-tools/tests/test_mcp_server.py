"""FastMCP adapter: stubbed headless; live resolution is manual (@pytest.mark.mcp)."""
import pytest

from leanscene_mcp_tools import TOOL_DESCRIPTIONS, V1_TOOLS
from leanscene_mcp_tools.server import build_server


def test_build_server_is_stubbed_headless():
    # The FastMCP/ToolsetDefinition API is uncertain and not invented; the adapter
    # is a stub. Calling it headless makes that explicit.
    with pytest.raises(NotImplementedError):
        build_server(gateway=None, meter=None)


def test_all_tools_have_a_description_ready_for_registration():
    assert set(V1_TOOLS) == set(TOOL_DESCRIPTIONS)


@pytest.mark.mcp
def test_tools_resolve_over_real_mcp_connection():
    # MANUAL (not headless): requires a live MCP / FastMCP runtime.
    #   1. Confirm the FastMCP package + ToolsetDefinition API (server.py TODO).
    #   2. Implement build_server: register V1_TOOLS with TOOL_DESCRIPTIONS.
    #   3. Run: pytest -m mcp packages/mcp-tools
    # Fails until build_server is implemented, by design.
    from leanscene_core import TokenMeter
    from leanscene_unreal_gateway import FakeGateway

    server = build_server(FakeGateway.from_fixture_name("scene_small"), TokenMeter())
    assert server is not None
