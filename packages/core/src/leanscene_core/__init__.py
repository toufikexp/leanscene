"""LeanScene free core (MIT): pure logic, no Unreal import (ADR-002).

Holds the ``UnrealGateway`` interface + plain record types and the offline token
meter. Schema shapers, shadow estimator and diff engine land here in later tasks.
"""
from .gateway import (
    ActorRecord,
    AssetRecord,
    FirehoseSource,
    LevelSummary,
    UnrealGateway,
    Vec3,
)
from .benchmark import EndToEndBenchmark, EndToEndResult
from .measure import Measurement, canonical_json, estimate, with_envelope
from .report import PER_CALL_LABEL, ReportRow, format_per_call_report
from .shapers import actor_brief, asset_brief, level_summary_brief
from .tokens import (
    DEFAULT_ENCODING,
    VENDORED_TIKTOKEN_CACHE,
    AnthropicTokenCounter,
    TiktokenCounter,
    TokenCounter,
    TokenMeter,
)

__all__ = [
    # gateway
    "UnrealGateway",
    "FirehoseSource",
    "ActorRecord",
    "AssetRecord",
    "LevelSummary",
    "Vec3",
    # shapers
    "actor_brief",
    "asset_brief",
    "level_summary_brief",
    # measurement
    "Measurement",
    "estimate",
    "with_envelope",
    "canonical_json",
    # measurement report (per-call surface)
    "format_per_call_report",
    "ReportRow",
    "PER_CALL_LABEL",
    # end-to-end benchmark (free contract; premium impl out-of-tree)
    "EndToEndResult",
    "EndToEndBenchmark",
    # tokens
    "TokenMeter",
    "TokenCounter",
    "TiktokenCounter",
    "AnthropicTokenCounter",
    "DEFAULT_ENCODING",
    "VENDORED_TIKTOKEN_CACHE",
]
