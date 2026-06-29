"""LeanScene unreal-gateway (MIT): the only tree that may import ``unreal`` (ADR-002).

Exposes ``FakeGateway`` (headless, fixture-backed) and ``RealGateway`` (live
editor; currently a stub).
"""
from .fake_gateway import FakeGateway, default_fixtures_dir
from .real_gateway import RealGateway

__all__ = ["FakeGateway", "RealGateway", "default_fixtures_dir"]
