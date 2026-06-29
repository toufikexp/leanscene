"""RealGateway — the ONLY module in LeanScene permitted to import ``unreal`` (ADR-002).

Talks to UE 5.8's experimental Web Remote Control API and translates its verbose,
unstable payloads into the coarse ``UnrealGateway`` contract. When the engine
bumps, THIS is the file that changes; the blast radius stops here.

Status: STUB. Method signatures + TODOs only. The real Web Remote Control calls
and their payload shapes are an experimental surface we do NOT guess from memory
(project instructions). They must be verified against a live editor and are
exercised only by ``@pytest.mark.editor`` tests (run manually). See
``docs/capturing-fixtures.md``.
"""
from __future__ import annotations

from typing import Optional

from leanscene_core import (
    ActorRecord,
    AssetRecord,
    FirehoseSource,
    LevelSummary,
    UnrealGateway,
)

# ADR-002: ``unreal`` is allowed here and ONLY here. Guarded so this module still
# imports headless (where ``unreal`` is absent); the methods are stubs regardless.
try:  # pragma: no cover - depends on a live editor
    import unreal  # noqa: F401  # TODO(editor): used by the real implementations below
except ImportError:  # headless / CI
    unreal = None  # type: ignore[assignment]


_TODO = (
    "RealGateway.{method} is a stub. TODO(manual, @pytest.mark.editor): implement "
    "via UE 5.8 Web Remote Control; verify the exact request path and response "
    "payload shape against a live editor before trusting it "
    "(see docs/capturing-fixtures.md)."
)


class RealGateway(UnrealGateway, FirehoseSource):
    """Web Remote Control implementation. Not usable headless (needs a live editor)."""

    def __init__(self, base_url: str = "http://127.0.0.1:30010") -> None:
        # TODO(editor): confirm the default Web Remote Control host/port for UE 5.8.
        self.base_url = base_url

    def list_actors(self) -> list[ActorRecord]:
        raise NotImplementedError(_TODO.format(method="list_actors"))

    def get_actor(self, actor_id: str) -> Optional[ActorRecord]:
        raise NotImplementedError(_TODO.format(method="get_actor"))

    def get_level_summary(self) -> LevelSummary:
        raise NotImplementedError(_TODO.format(method="get_level_summary"))

    def get_assets(self) -> list[AssetRecord]:
        raise NotImplementedError(_TODO.format(method="get_assets"))

    def get_world_state_hash(self, sector: str) -> str:
        raise NotImplementedError(_TODO.format(method="get_world_state_hash"))

    # -- FirehoseSource: the raw native payloads for the per-call estimator ----
    # TODO(editor): capture the real verbose Web Remote Control responses and
    # record their shape (docs/capturing-fixtures.md) before trusting any delta.
    def raw_actors(self) -> list[dict]:
        raise NotImplementedError(_TODO.format(method="raw_actors"))

    def raw_actor(self, actor_id: str) -> Optional[dict]:
        raise NotImplementedError(_TODO.format(method="raw_actor"))

    def raw_assets(self) -> list[dict]:
        raise NotImplementedError(_TODO.format(method="raw_assets"))
