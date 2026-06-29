"""LeanScene free core (MIT): pure logic, no Unreal import (ADR-002).

Holds the ``UnrealGateway`` interface + plain record types and the offline token
meter. Schema shapers, shadow estimator and diff engine land here in later tasks.
"""
from .gateway import (
    ActorRecord,
    AssetRecord,
    LevelSummary,
    UnrealGateway,
    Vec3,
)
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
    "ActorRecord",
    "AssetRecord",
    "LevelSummary",
    "Vec3",
    # tokens
    "TokenMeter",
    "TokenCounter",
    "TiktokenCounter",
    "AnthropicTokenCounter",
    "DEFAULT_ENCODING",
    "VENDORED_TIKTOKEN_CACHE",
]
