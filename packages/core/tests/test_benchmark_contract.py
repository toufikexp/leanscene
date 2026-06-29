"""End-to-end contract is free, distinct from per-call, with no public impl (ADR-004)."""
import inspect
from dataclasses import fields

import leanscene_core as pkg
from leanscene_core import EndToEndBenchmark, EndToEndResult, Measurement


def test_end_to_end_result_is_not_confusable_with_per_call():
    per_call_fields = {f.name for f in fields(Measurement)}
    e2e_fields = {f.name for f in fields(EndToEndResult)}
    # No shared field names -> the two cannot be mixed up.
    assert per_call_fields.isdisjoint(e2e_fields)
    # The per-call tell-tale never appears on the e2e result.
    assert "delta_pct_this_call" not in e2e_fields
    result = EndToEndResult(
        task_id="t1",
        runs=3,
        baseline_tokens=1000,
        leanscene_tokens=200,
        workflow_delta_pct_end_to_end=80.0,
    )
    assert result.kind == "end_to_end"


def test_benchmark_is_runtime_checkable_protocol():
    class GoodBench:
        def run(self, task_id, *, runs=1):
            return EndToEndResult(task_id, runs, 1000, 200, 80.0)

    class NotABench:
        pass

    assert isinstance(GoodBench(), EndToEndBenchmark)
    assert not isinstance(NotABench(), EndToEndBenchmark)


def test_free_tree_ships_no_concrete_benchmark():
    # ADR-004/ADR-007: the benchmark is premium/out-of-tree. The free package must
    # not export a concrete EndToEndBenchmark implementation.
    for name in pkg.__all__:
        obj = getattr(pkg, name)
        if inspect.isclass(obj) and obj is not EndToEndBenchmark:
            assert not hasattr(obj, "run"), f"free tree exports a benchmark impl: {name}"
