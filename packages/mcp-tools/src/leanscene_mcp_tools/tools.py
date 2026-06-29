"""The pinned v1 tool set — pure logic, headless-testable (Component A, free).

Each tool is a pure function ``(gateway, meter, args) -> envelope dict``:
  1. calls the gateway for the minimum it needs,
  2. shapes the result via ``core`` into a fixed minimal schema (ADR-005),
  3. attaches the per-call measurement envelope from the shadow estimator (ADR-003).

The gateway argument must implement both ``UnrealGateway`` (data) and
``FirehoseSource`` (the native payload to measure against); ``FakeGateway`` does.

Bounded by construction: every list-returning tool caps its items and reports the
true ``total`` + a ``truncated`` flag, so output never grows unbounded with scene
size (ADR-005). The FastMCP/MCP exposure of these functions is a separate, stubbed
adapter (``server.py``) — kept out of headless tests.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Optional, Sequence

from leanscene_core import (
    FirehoseSource,
    TokenMeter,
    UnrealGateway,
    actor_brief,
    asset_brief,
    level_summary_brief,
    with_envelope,
)

#: Caps that bound output size regardless of scene scale (ADR-005). Configurable.
RADIUS_CAP = 32
OFFENDERS_CAP = 64

#: Sector edge length (cm) used to derive occupied sectors in summarize_level.
SECTOR_SIZE = 1000.0

#: Default numeric tolerance for the verify_* checks.
DEFAULT_TOL = 1.0

#: Asset flags that mean "missing LODs" (coarse seed flags differ by source).
_MISSING_LOD_FLAGS = frozenset({"missing_lods", "no_lod"})


def _distance(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))


def _half_extents(bounds: Sequence[float]) -> tuple:
    return tuple(float(b) / 2.0 for b in bounds)


def _capped(items: list, cap: int) -> Dict[str, Any]:
    """Fixed bounded container: capped items + true total + truncated flag."""
    return {"items": items[:cap], "total": len(items), "truncated": len(items) > cap}


# --------------------------------------------------------------------------- #
# 1. spatial filter
# --------------------------------------------------------------------------- #
def get_actors_in_radius(
    gateway: UnrealGateway,
    meter: TokenMeter,
    point: Sequence[float],
    radius: float,
    *,
    cap: int = RADIUS_CAP,
) -> Dict[str, Any]:
    # No narrower spatial gateway call exists yet, so filter after list_actors().
    # TODO(gateway): if Web Remote Control gains a spatial query, push the filter
    # down and prefer it over fetch-all-then-filter.
    matched = [a for a in gateway.list_actors() if _distance(a.location, point) <= radius]
    matched.sort(key=lambda a: _distance(a.location, point))  # deterministic order
    result = _capped([actor_brief(a) for a in matched], cap)
    firehose = gateway.raw_actors()  # native equivalent = dump every actor
    return with_envelope(result, firehose, meter)


# --------------------------------------------------------------------------- #
# 2 + 3. semantic asset filters
# --------------------------------------------------------------------------- #
def get_unlinked_materials(
    gateway: UnrealGateway, meter: TokenMeter, *, cap: int = OFFENDERS_CAP
) -> Dict[str, Any]:
    offenders = [a for a in gateway.get_assets() if "unlinked" in a.flags]
    result = _capped([asset_brief(a) for a in offenders], cap)
    firehose = gateway.raw_assets()
    return with_envelope(result, firehose, meter)


def get_assets_missing_lods(
    gateway: UnrealGateway, meter: TokenMeter, *, cap: int = OFFENDERS_CAP
) -> Dict[str, Any]:
    offenders = [
        a for a in gateway.get_assets() if _MISSING_LOD_FLAGS.intersection(a.flags)
    ]
    result = _capped([asset_brief(a) for a in offenders], cap)
    firehose = gateway.raw_assets()
    return with_envelope(result, firehose, meter)


# --------------------------------------------------------------------------- #
# 4. structural summary
# --------------------------------------------------------------------------- #
def _occupied_sectors(gateway: UnrealGateway, size: float = SECTOR_SIZE) -> set:
    sectors = set()
    for actor in gateway.list_actors():
        x, y = actor.location[0], actor.location[1]
        sectors.add(f"{int(math.floor(x / size))},{int(math.floor(y / size))}")
    return sectors


def summarize_level(gateway: UnrealGateway, meter: TokenMeter) -> Dict[str, Any]:
    summary = gateway.get_level_summary()
    result = level_summary_brief(summary, sectors=_occupied_sectors(gateway))
    firehose = gateway.raw_actors()  # native equivalent = the full outliner
    return with_envelope(result, firehose, meter)


# --------------------------------------------------------------------------- #
# 5. single actor brief
# --------------------------------------------------------------------------- #
def get_actor_brief(
    gateway: UnrealGateway, meter: TokenMeter, actor_id: str
) -> Dict[str, Any]:
    record = gateway.get_actor(actor_id)  # narrow call, not list_actors()
    result: Dict[str, Any] = (
        {"actor": actor_brief(record)} if record else {"actor": None, "id": actor_id}
    )
    firehose = gateway.raw_actor(actor_id) or {}
    return with_envelope(result, firehose, meter)


# --------------------------------------------------------------------------- #
# 6 + 7 + 8. verify_* group (cheap deterministic checks before any vision check)
# --------------------------------------------------------------------------- #
def verify_bounds(
    gateway: UnrealGateway,
    meter: TokenMeter,
    actor_id: str,
    expected_bounds: Sequence[float],
    *,
    tol: float = DEFAULT_TOL,
) -> Dict[str, Any]:
    record = gateway.get_actor(actor_id)
    if record is None:
        result: Dict[str, Any] = {"check": "bounds", "id": actor_id, "found": False, "ok": False}
    else:
        ok = all(abs(a - float(e)) <= tol for a, e in zip(record.bounds, expected_bounds))
        result = {
            "check": "bounds",
            "id": actor_id,
            "ok": ok,
            "actual": [round(float(b), 2) for b in record.bounds],
            "expected": [round(float(e), 2) for e in expected_bounds],
            "tol": tol,
        }
    firehose = gateway.raw_actor(actor_id) or {}
    return with_envelope(result, firehose, meter)


def verify_transform(
    gateway: UnrealGateway,
    meter: TokenMeter,
    actor_id: str,
    expected_loc: Sequence[float],
    *,
    tol: float = DEFAULT_TOL,
) -> Dict[str, Any]:
    record = gateway.get_actor(actor_id)
    if record is None:
        result: Dict[str, Any] = {"check": "transform", "id": actor_id, "found": False, "ok": False}
    else:
        ok = all(abs(a - float(e)) <= tol for a, e in zip(record.location, expected_loc))
        result = {
            "check": "transform",
            "id": actor_id,
            "ok": ok,
            "actual": [round(float(c), 2) for c in record.location],
            "expected": [round(float(e), 2) for e in expected_loc],
            "tol": tol,
        }
    firehose = gateway.raw_actor(actor_id) or {}
    return with_envelope(result, firehose, meter)


def verify_overlap(
    gateway: UnrealGateway, meter: TokenMeter, id_a: str, id_b: str
) -> Dict[str, Any]:
    a = gateway.get_actor(id_a)
    b = gateway.get_actor(id_b)
    if a is None or b is None:
        result: Dict[str, Any] = {
            "check": "overlap",
            "a": id_a,
            "b": id_b,
            "found": False,
            "ok": False,
        }
    else:
        # AABB overlap: per-axis center distance <= sum of half-extents.
        # Convention: bounds are full box extents; half-extent = bounds / 2.
        ha, hb = _half_extents(a.bounds), _half_extents(b.bounds)
        ok = all(
            abs(a.location[i] - b.location[i]) <= (ha[i] + hb[i]) for i in range(3)
        )
        result = {"check": "overlap", "a": id_a, "b": id_b, "ok": ok}
    firehose = {"a": gateway.raw_actor(id_a) or {}, "b": gateway.raw_actor(id_b) or {}}
    return with_envelope(result, firehose, meter)


#: Stable registry of the pinned v1 tools (name -> callable). Used by tests and by
#: the FastMCP adapter. Do not expand in v1.
V1_TOOLS = {
    "get_actors_in_radius": get_actors_in_radius,
    "get_unlinked_materials": get_unlinked_materials,
    "get_assets_missing_lods": get_assets_missing_lods,
    "summarize_level": summarize_level,
    "get_actor_brief": get_actor_brief,
    "verify_bounds": verify_bounds,
    "verify_overlap": verify_overlap,
    "verify_transform": verify_transform,
}
