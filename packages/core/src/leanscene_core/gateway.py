"""UnrealGateway — the single, narrow interface to the Unreal Editor.

ADR-002: all business logic is UE-independent and runs headless behind this
interface. Implementations return plain dataclasses (below), never live ``unreal``
objects, so every consumer is testable with no editor and no network.

This module imports NOTHING from Unreal and never may — enforced by
``tools/check_no_unreal_import.py`` in CI.

The method set is intentionally coarse and small; the exact names mirror
``docs/ARCHITECTURE.md``. Records are gateway-coarse and already minimal
(ADR-005); they are NOT the raw Web Remote Control "firehose" (that is captured
separately for the shadow estimator — see ``docs/tasks/03-measurement.md``).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Mapping, Optional, Tuple

#: A 3-component vector (location / bounds extents). Plain tuple, not a UE type.
Vec3 = Tuple[float, float, float]


@dataclass(frozen=True)
class ActorRecord:
    """A single actor, coarse and minimal.

    Maps to the illustrative ``actor_brief`` in ``docs/ARCHITECTURE.md`` once a
    shaper renames fields for the wire (``actor_class`` -> ``class`` etc.).
    """

    id: str
    actor_class: str
    location: Vec3
    bounds: Vec3
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class AssetRecord:
    """An asset referenced by the level, coarse and minimal."""

    path: str
    asset_class: str
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class LevelSummary:
    """Bounded summary of a level — never a per-actor firehose (ADR-005)."""

    name: str
    actor_count: int
    class_histogram: Mapping[str, int] = field(default_factory=dict)


class UnrealGateway(ABC):
    """Coarse, few-method contract over the editor.

    Keep this surface small: every method is a place an engine bump can break, so
    the contract stays minimal and the blast radius stays inside the real
    implementation (ADR-002).
    """

    @abstractmethod
    def list_actors(self) -> list[ActorRecord]:
        """All actors in the current level, as minimal records."""

    @abstractmethod
    def get_actor(self, actor_id: str) -> Optional[ActorRecord]:
        """One actor by id, or ``None`` if absent."""

    @abstractmethod
    def get_level_summary(self) -> LevelSummary:
        """Level name + bounded summary stats (no per-actor firehose)."""

    @abstractmethod
    def get_assets(self) -> list[AssetRecord]:
        """Assets referenced by the level, as minimal records."""

    @abstractmethod
    def get_world_state_hash(self, sector: str) -> str:
        """A stable hash of one sector's state, for the premium diff/cache.

        Deterministic and offline for fakes.
        """
