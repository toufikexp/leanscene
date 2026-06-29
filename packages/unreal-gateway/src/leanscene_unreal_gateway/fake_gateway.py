"""FakeGateway — fixture-backed UnrealGateway for headless tests (ADR-002).

Serves hand-written SEED fixtures from ``tests/fixtures/`` so every other package
can be built and tested with no editor and no network. Capturing real fixtures is
a documented manual step — see ``docs/capturing-fixtures.md``.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional, Union

from leanscene_core import (
    ActorRecord,
    AssetRecord,
    FirehoseSource,
    LevelSummary,
    UnrealGateway,
)


def default_fixtures_dir(start: Optional[Path] = None) -> Path:
    """Locate the repo's ``tests/fixtures`` dir by walking up from ``start``.

    Dev convenience for in-repo headless tests; this is not a packaged data path.
    """
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "tests" / "fixtures"
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("could not locate tests/fixtures (run inside the repo)")


class FakeGateway(UnrealGateway, FirehoseSource):
    """A gateway backed by an in-memory scene dict (loaded from a fixture file).

    Also implements ``FirehoseSource`` by serving the fixture's ``firehose``
    section (verbose seed payloads) so the shadow estimator has a native
    equivalent to measure against headless.
    """

    def __init__(self, scene: dict) -> None:
        self._scene = scene
        self._actors = [self._actor(a) for a in scene.get("actors", [])]
        self._actors_by_id = {a.id: a for a in self._actors}
        self._assets = [self._asset(a) for a in scene.get("assets", [])]
        firehose = scene.get("firehose", {})
        self._raw_actors_by_id = dict(firehose.get("actors", {}))
        self._raw_assets = list(firehose.get("assets", []))

    # -- construction helpers ------------------------------------------------
    @classmethod
    def from_file(cls, path: Union[Path, str]) -> "FakeGateway":
        with open(path, "r", encoding="utf-8") as handle:
            return cls(json.load(handle))

    @classmethod
    def from_fixture_name(
        cls, name: str, fixtures_dir: Optional[Path] = None
    ) -> "FakeGateway":
        directory = fixtures_dir or default_fixtures_dir()
        filename = name if name.endswith(".json") else f"{name}.json"
        return cls.from_file(directory / filename)

    @staticmethod
    def _actor(raw: dict) -> ActorRecord:
        return ActorRecord(
            id=raw["id"],
            actor_class=raw["class"],
            location=tuple(raw["loc"]),
            bounds=tuple(raw["bounds"]),
            flags=tuple(raw.get("flags", [])),
        )

    @staticmethod
    def _asset(raw: dict) -> AssetRecord:
        return AssetRecord(
            path=raw["path"],
            asset_class=raw["class"],
            flags=tuple(raw.get("flags", [])),
        )

    # -- UnrealGateway contract ----------------------------------------------
    def list_actors(self) -> list[ActorRecord]:
        return list(self._actors)

    def get_actor(self, actor_id: str) -> Optional[ActorRecord]:
        return self._actors_by_id.get(actor_id)

    def get_level_summary(self) -> LevelSummary:
        histogram: dict[str, int] = {}
        for actor in self._actors:
            histogram[actor.actor_class] = histogram.get(actor.actor_class, 0) + 1
        name = self._scene.get("level", {}).get("name", "UnknownLevel")
        return LevelSummary(
            name=name, actor_count=len(self._actors), class_histogram=histogram
        )

    def get_assets(self) -> list[AssetRecord]:
        return list(self._assets)

    def get_world_state_hash(self, sector: str) -> str:
        stored = self._scene.get("sector_hashes", {})
        if sector in stored:
            return str(stored[sector])
        # Deterministic, offline fallback so a fake still yields stable,
        # change-sensitive hashes even for sectors a fixture didn't pin.
        payload = json.dumps(
            {
                "sector": sector,
                "actors": [[a.id, list(a.location)] for a in self._actors],
            },
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    # -- FirehoseSource contract (verbose seed payloads) ----------------------
    def _require_firehose(self) -> None:
        if "firehose" not in self._scene:
            raise KeyError(
                "fixture has no 'firehose' section; the shadow estimator needs the "
                "verbose native payload to measure against (see tests/fixtures/README.md)"
            )

    def raw_actors(self) -> list[dict]:
        self._require_firehose()
        return list(self._raw_actors_by_id.values())

    def raw_actor(self, actor_id: str) -> Optional[dict]:
        self._require_firehose()
        return self._raw_actors_by_id.get(actor_id)

    def raw_assets(self) -> list[dict]:
        self._require_firehose()
        return list(self._raw_assets)
