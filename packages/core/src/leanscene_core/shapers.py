"""Schema shapers — turn coarse gateway records into fixed, minimal wire schemas.

Token-budget-by-construction lives here (ADR-005): each ``*_brief`` is a fixed set
of short-keyed fields — no nested component trees, no transforms-as-prose, no
redundant metadata. Every field earns its tokens. Field names match the
illustrative ``actor_brief`` in ``docs/ARCHITECTURE.md`` (``class``/``loc``).
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from .gateway import ActorRecord, AssetRecord, LevelSummary


def _round_vec(vec) -> list:
    return [round(float(component), 2) for component in vec]


def actor_brief(record: ActorRecord) -> Dict[str, Any]:
    """Fixed minimal actor schema."""
    return {
        "id": record.id,
        "class": record.actor_class,
        "loc": _round_vec(record.location),
        "bounds": _round_vec(record.bounds),
        "flags": list(record.flags),
    }


def asset_brief(record: AssetRecord) -> Dict[str, Any]:
    """Fixed minimal asset schema."""
    return {
        "path": record.path,
        "class": record.asset_class,
        "flags": list(record.flags),
    }


def level_summary_brief(
    summary: LevelSummary, *, sectors: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """Compact structural summary — counts + class histogram (+ sectors), never
    the full outliner. Size scales with the number of distinct classes/sectors,
    not with actor count (ADR-005)."""
    out: Dict[str, Any] = {
        "name": summary.name,
        "actors": summary.actor_count,
        "classes": dict(summary.class_histogram),
    }
    if sectors is not None:
        out["sectors"] = sorted(sectors)
    return out
