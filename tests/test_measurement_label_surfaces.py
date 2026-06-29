"""ADR-003: the per-call label surfaces on tool output, the demo, and the docs."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "demo"))


def test_tool_output_keys_the_per_call_label():
    from leanscene_core import TokenMeter
    from leanscene_mcp_tools import summarize_level
    from leanscene_unreal_gateway import FakeGateway

    env = summarize_level(FakeGateway.from_fixture_name("scene_small"), TokenMeter())
    # the label is carried in the field name itself
    assert "delta_pct_this_call" in env["measure"]


def test_demo_output_labels_per_call_and_names_the_caveat():
    import measure_demo  # from demo/ (on sys.path)

    out = measure_demo.render(["scene_small"]).lower()
    assert "this call" in out
    assert "end-to-end" in out  # explicitly says what it is NOT


def test_docs_carry_the_per_call_label():
    measurement_doc = (REPO_ROOT / "docs" / "measurement.md").read_text(encoding="utf-8").lower()
    assert ("this call" in measurement_doc) or ("this_call" in measurement_doc) or (
        "per-call" in measurement_doc
    )
    architecture = (REPO_ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8").lower()
    assert ("this_call" in architecture) or ("per-call" in architecture)
