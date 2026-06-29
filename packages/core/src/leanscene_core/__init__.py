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
from .measure import Measurement, canonical_json, estimate, with_envelope
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
    # tokens
    "TokenMeter",
    "TokenCounter",
    "TiktokenCounter",
    "AnthropicTokenCounter",
    "DEFAULT_ENCODING",
    "VENDORED_TIKTOKEN_CACHE",
]
