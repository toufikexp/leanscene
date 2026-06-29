"""Lever 2 — the static rules starter (free).

Ships a fixed, self-contained `CLAUDE.md` / `.cursorrules` starter that users drop
into their project: it forbids native broad sweeps, maps each task to the lean
tool, and encodes the verify-before-vision pattern.

This is STATIC by design (ADR-001/ADR-007): lever 2 is a fixed template. The
*dynamic, project-tailored* generator is lever 3 (premium) — see `extension.py`.
"""
from __future__ import annotations

from importlib import resources
from typing import Dict

#: target -> packaged template filename.
TARGETS: Dict[str, str] = {
    "claude": "steering.CLAUDE.md",
    "cursor": "steering.cursorrules",
}


def static_rules(target: str = "claude") -> str:
    """Return the static steering starter for ``target`` ("claude" or "cursor")."""
    if target not in TARGETS:
        raise ValueError(
            f"unknown steering target {target!r}; choose one of {sorted(TARGETS)}"
        )
    template = resources.files("leanscene_steering_core").joinpath(
        "templates", TARGETS[target]
    )
    return template.read_text(encoding="utf-8")
