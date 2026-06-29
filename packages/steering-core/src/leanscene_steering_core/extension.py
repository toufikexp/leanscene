"""Lever 3 (PREMIUM) extension point — the dynamic steering engine plugs in HERE.

Per ADR-007 the engine is a DETERMINISTIC generator:
``(toolset snapshot, project manifest) -> ruleset``, regenerated when the toolset
changes — NOT runtime ML, NOT per-prompt rewriting. Per ADR-004 the implementation
is PREMIUM and lives out-of-tree; only this contract is free, so premium can extend
the core through a defined extension point without ever forking it.

This module defines the data shapes + the ``SteeringGenerator`` protocol. It ships
NO generator implementation (the open-core boundary is enforced by
`tests/test_open_core_boundary.py`).

NOTE: ``ToolsetSnapshot`` mirrors a live UE ``ToolsetRegistry`` snapshot. The real
registry payload shape is experimental and is NOT modelled here — this is a coarse,
stable contract; the adapter that builds a snapshot from the live registry is part
of the premium impl (capture + verify against a live editor; do not guess).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class ToolEntry:
    """One tool visible to the agent."""

    name: str
    description: str
    efficient: bool = True  # a lean LeanScene tool, vs a native firehose tool


@dataclass(frozen=True)
class ToolsetSnapshot:
    """A snapshot of the tools the agent can see (lean + native)."""

    tools: List[ToolEntry] = field(default_factory=list)


@dataclass(frozen=True)
class ProjectManifest:
    """Small project description the generated ruleset maps tasks against."""

    task_types: List[str] = field(default_factory=list)
    conventions: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class GeneratedRuleset:
    """The generator's output — a tailored ruleset for one target."""

    target: str  # "claude" | "cursor"
    text: str
    source_tool_names: List[str] = field(default_factory=list)


@runtime_checkable
class SteeringGenerator(Protocol):
    """Deterministic generator (ADR-007): same inputs -> same ruleset."""

    def generate(
        self,
        snapshot: ToolsetSnapshot,
        manifest: ProjectManifest,
        *,
        target: str = "claude",
    ) -> GeneratedRuleset:
        ...
