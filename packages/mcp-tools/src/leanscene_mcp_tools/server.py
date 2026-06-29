"""FastMCP exposure of the v1 toolset — STUB (uncertain API, not invented).

The tool *logic* in ``tools.py`` is pure and fully headless-tested. THIS module is
the thin adapter that registers those functions as MCP tools (with their tuned
descriptions) on a FastMCP server. The exact FastMCP / ``ToolsetDefinition`` /
``ToolsetRegistry`` API for UE 5.8's native MCP plugin is an experimental surface
we do NOT guess from memory (project rule). It is left as a stub with TODOs and is
exercised only by an ``@pytest.mark.mcp`` test (run manually), never in headless CI.

TODO(manual, @pytest.mark.mcp): confirm the import path and registration API —
candidates are the standalone ``fastmcp`` package (``from fastmcp import FastMCP``)
and the MCP SDK's ``mcp.server.fastmcp.FastMCP``. Then register each entry of
``V1_TOOLS`` with ``TOOL_DESCRIPTIONS[name]`` and verify tools resolve over a real
MCP connection (Task 01 acceptance, manual).
"""
from __future__ import annotations

from typing import Any

from .descriptions import TOOL_DESCRIPTIONS
from .tools import V1_TOOLS

try:  # pragma: no cover - optional/uncertain dependency, absent in headless CI
    import fastmcp as _fastmcp  # type: ignore  # noqa: F401  # TODO(verify): correct package?
except ImportError:
    _fastmcp = None


def build_server(gateway: Any, meter: Any) -> Any:
    """Build and return a FastMCP server exposing the v1 tools. STUB."""
    raise NotImplementedError(
        "build_server is a stub: the FastMCP/ToolsetDefinition registration API is "
        "an experimental surface we do not invent. See this module's TODO and "
        "docs/capturing-fixtures.md. Tool LOGIC is in tools.py and is tested headless. "
        f"(tools to register: {sorted(V1_TOOLS)}; "
        f"descriptions available for: {sorted(TOOL_DESCRIPTIONS)})"
    )
