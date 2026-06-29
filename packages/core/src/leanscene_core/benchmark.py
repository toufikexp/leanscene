"""End-to-end benchmark — FREE CONTRACT ONLY (premium impl is out-of-tree).

ADR-003: end-to-end workflow savings are a SEPARATE, premium metric — they depend
on call count + caching and need a live agent run, so they must never be confused
with the per-call payload delta. This module defines the contract only; per ADR-004
the implementation is premium and lives out-of-tree (guarded by
``tests/test_open_core_boundary.py``).

``EndToEndResult`` is intentionally NOT field-compatible with
``measure.Measurement``: different field names plus an explicit ``kind``, so the two
cannot be mixed up in code, output, or docs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class EndToEndResult:
    """Workflow-level token use for a defined task, with and without LeanScene.

    Deliberately distinct from the per-call ``Measurement`` (no shared field names).
    """

    task_id: str
    runs: int
    baseline_tokens: int  # total workflow tokens WITHOUT LeanScene
    leanscene_tokens: int  # total workflow tokens WITH LeanScene
    workflow_delta_pct_end_to_end: float
    kind: str = "end_to_end"  # explicit marker; never "this_call"


@runtime_checkable
class EndToEndBenchmark(Protocol):
    """Runs a defined agent task with and without LeanScene -> ``EndToEndResult``.

    PREMIUM; implemented out-of-tree. Reproducible for a fixed task definition.
    """

    def run(self, task_id: str, *, runs: int = 1) -> EndToEndResult:
        ...
