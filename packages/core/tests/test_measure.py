"""Shadow estimator: computed per-call delta, offline, labelled (ADR-003)."""
from leanscene_core import Measurement, TokenMeter, canonical_json, estimate, with_envelope


class CharCounter:
    """Deterministic offline counter: 1 token per character."""

    def count(self, text: str) -> int:
        return len(text)


def test_estimate_delta_is_computed_from_inputs():
    meter = TokenMeter(counter=CharCounter())
    lean = {"a": 1}
    firehose = {"a": 1, "verbose": "x" * 100}
    m = estimate(lean, firehose, meter)
    assert isinstance(m, Measurement)
    assert m.firehose_tokens > m.lean_tokens
    expected = round((m.firehose_tokens - m.lean_tokens) / m.firehose_tokens * 100, 1)
    assert m.delta_pct_this_call == expected  # not hardcoded


def test_envelope_shape_and_per_call_label():
    meter = TokenMeter(counter=CharCounter())
    env = with_envelope({"x": 1}, {"x": 1, "y": 2}, meter)
    assert set(env) == {"result", "measure"}
    assert set(env["measure"]) == {"lean_tokens", "firehose_tokens", "delta_pct_this_call"}


def test_zero_firehose_gives_zero_delta():
    class Zero:
        def count(self, text: str) -> int:
            return 0

    m = estimate({"a": 1}, {}, TokenMeter(counter=Zero()))
    assert m.firehose_tokens == 0
    assert m.delta_pct_this_call == 0.0


def test_estimate_with_offline_tiktoken_is_stable():
    meter = TokenMeter()  # vendored tiktoken, offline
    m1 = estimate({"id": "a"}, {"id": "a", "verbose": [1, 2, 3, 4, 5]}, meter)
    m2 = estimate({"id": "a"}, {"id": "a", "verbose": [1, 2, 3, 4, 5]}, meter)
    assert m1 == m2  # deterministic
    assert m1.lean_tokens > 0 and m1.firehose_tokens >= m1.lean_tokens
    assert 0 <= m1.delta_pct_this_call <= 100


def test_canonical_json_is_stable_regardless_of_key_order():
    assert canonical_json({"b": 1, "a": 2}) == canonical_json({"a": 2, "b": 1})
