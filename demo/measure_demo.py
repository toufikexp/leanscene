"""Reproducible per-call measurement demo — the hero output (ADR-003).

Runs the lean query tools over the seed scenes and prints a per-call-labelled
report. Numbers are computed offline with the local tokenizer.

This is a dev/demo script, not a shipped package. Run it:  python demo/measure_demo.py

⚠️ On the SEED fixtures the firehose payloads are synthetic, so these absolute
deltas are illustrative until real captures exist (docs/capturing-fixtures.md). The
mechanism is real and offline; the inputs are placeholders.
"""
from __future__ import annotations

from typing import List

from leanscene_core import Measurement, ReportRow, TokenMeter, format_per_call_report
from leanscene_mcp_tools import (
    get_actor_brief,
    get_actors_in_radius,
    get_assets_missing_lods,
    get_unlinked_materials,
    summarize_level,
)
from leanscene_unreal_gateway import FakeGateway

SCENES = ["scene_small", "scene_medium", "scene_large"]
SEED_NOTE = (
    "NOTE: seed fixtures use SYNTHETIC firehose payloads, so these absolute deltas "
    "are illustrative until real captures exist (docs/capturing-fixtures.md)."
)


def build_rows(scenes: List[str] = SCENES) -> List[ReportRow]:
    meter = TokenMeter()  # offline, vendored tokenizer
    rows: List[ReportRow] = []
    for scene in scenes:
        gw = FakeGateway.from_fixture_name(scene)
        first_actor = gw.list_actors()[0].id
        envelopes = [
            ("get_actors_in_radius", get_actors_in_radius(gw, meter, (0, 0, 0), 1e7)),
            ("summarize_level", summarize_level(gw, meter)),
            ("get_unlinked_materials", get_unlinked_materials(gw, meter)),
            ("get_assets_missing_lods", get_assets_missing_lods(gw, meter)),
            ("get_actor_brief", get_actor_brief(gw, meter, first_actor)),
        ]
        for tool_name, env in envelopes:
            rows.append(ReportRow(tool_name, scene, Measurement(**env["measure"])))
    return rows


def render(scenes: List[str] = SCENES) -> str:
    return format_per_call_report(build_rows(scenes), note=SEED_NOTE)


if __name__ == "__main__":
    print(render())
