"""Per-call report keeps the label and never writes a fixed % literal (ADR-003)."""
import pathlib
import re

from leanscene_core import PER_CALL_LABEL, Measurement, ReportRow, format_per_call_report


def _rows():
    return [
        ReportRow("get_actor_brief", "scene_small", Measurement(56, 424, 86.8)),
        ReportRow("summarize_level", "scene_large", Measurement(202, 19560, 99.0)),
    ]


def test_report_carries_the_per_call_label():
    out = format_per_call_report(_rows())
    assert "this call" in out.lower()
    assert PER_CALL_LABEL in out
    assert "end-to-end" in out.lower()  # the caveat names what it is NOT


def test_report_includes_each_row_value():
    out = format_per_call_report(_rows())
    assert "get_actor_brief" in out and "summarize_level" in out
    assert "86.8" in out and "99.0" in out


def test_report_note_is_appended():
    out = format_per_call_report(_rows(), note="seed caveat here")
    assert "seed caveat here" in out


def test_report_source_has_no_fixed_percentage_literal():
    import leanscene_core.report as report_mod

    src = pathlib.Path(report_mod.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\d+(\.\d+)?\s*%", src)
