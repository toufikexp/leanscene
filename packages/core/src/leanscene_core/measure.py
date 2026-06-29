"""Shadow estimator — the per-call payload token delta (ADR-003).

Given a lean tool result and the raw firehose payload the gateway exposes for the
equivalent native query, count both with the local token meter and emit
``{lean_tokens, firehose_tokens, delta_pct_this_call}``. Pure, deterministic,
offline, instant.

HONESTY (ADR-003): this is a PER-CALL PAYLOAD proxy — not end-to-end workflow
savings (those depend on call count + caching). The ``this_call`` suffix in the
field name is load-bearing; never drop it. No fixed percentage is ever hardcoded —
the number is always computed from the two payloads in front of it.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict

from .tokens import TokenMeter


def canonical_json(obj: Any) -> str:
    """Stable, compact JSON so token counts are deterministic across runs."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class Measurement:
    lean_tokens: int
    firehose_tokens: int
    delta_pct_this_call: float

    def as_dict(self) -> Dict[str, Any]:
        return {
            "lean_tokens": self.lean_tokens,
            "firehose_tokens": self.firehose_tokens,
            "delta_pct_this_call": self.delta_pct_this_call,
        }


def estimate(lean_obj: Any, firehose_obj: Any, meter: TokenMeter) -> Measurement:
    """Per-call delta between a lean payload and its native firehose equivalent."""
    lean_tokens = meter.count_tokens(canonical_json(lean_obj))
    firehose_tokens = meter.count_tokens(canonical_json(firehose_obj))
    if firehose_tokens > 0:
        delta = (firehose_tokens - lean_tokens) / firehose_tokens * 100.0
    else:
        delta = 0.0
    return Measurement(lean_tokens, firehose_tokens, round(delta, 1))


def with_envelope(result_obj: Any, firehose_obj: Any, meter: TokenMeter) -> Dict[str, Any]:
    """Wrap a shaped result with its per-call measurement envelope.

    Shape (see docs/ARCHITECTURE.md):
        {"result": <shaped>, "measure": {lean_tokens, firehose_tokens, delta_pct_this_call}}

    ``lean_tokens`` counts the ``result`` payload the agent actually receives;
    ``firehose_tokens`` counts the native payload it avoided.
    """
    measurement = estimate(result_obj, firehose_obj, meter)
    return {"result": result_obj, "measure": measurement.as_dict()}
