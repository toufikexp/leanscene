"""Per-call measurement report — the demo's hero surface (ADR-003).

Formats per-call deltas with the "this call" label travelling WITH every number,
so the per-call framing can never be dropped (ADR-003). No fixed percentage is ever
written as a literal here; every number is computed upstream by the estimator and
passed in.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .measure import Measurement

#: The caveat that MUST accompany the metric wherever it surfaces (ADR-003).
PER_CALL_LABEL = (
    "per-call payload delta (this call only) — NOT end-to-end workflow savings"
)


@dataclass(frozen=True)
class ReportRow:
    tool: str
    scene: str
    measure: Measurement


def _fmt_delta(measure: Measurement) -> str:
    # The per-call label travels with the number — it cannot be quoted bare.
    return f"{measure.delta_pct_this_call} pct (this call)"


def format_per_call_report(rows: List[ReportRow], *, note: str = "") -> str:
    """Render a labelled per-call report. The header, every row, and the footer
    all keep the "this call" framing (ADR-003)."""
    header = (
        f"{'tool':28} {'scene':14} {'lean':>6} {'firehose':>9} "
        f"{'delta (this call)':>22}"
    )
    lines: List[str] = [
        "LeanScene — per-call payload token delta (THIS CALL only)",
        "=" * len(header),
        header,
        "-" * len(header),
    ]
    for row in rows:
        lines.append(
            f"{row.tool:28} {row.scene:14} "
            f"{row.measure.lean_tokens:>6} {row.measure.firehose_tokens:>9} "
            f"{_fmt_delta(row.measure):>22}"
        )
    lines.append("-" * len(header))
    lines.append(PER_CALL_LABEL + ".")
    if note:
        lines.append(note)
    return "\n".join(lines)
