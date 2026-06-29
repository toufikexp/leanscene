"""Lever 3 boundary: the generator contract exists; no public implementation."""
import inspect

import leanscene_steering_core as pkg
from leanscene_steering_core.extension import (
    GeneratedRuleset,
    ProjectManifest,
    SteeringGenerator,
    ToolEntry,
    ToolsetSnapshot,
)


def test_contract_dataclasses_construct():
    snap = ToolsetSnapshot(
        tools=[ToolEntry(name="get_actor_brief", description="…", efficient=True)]
    )
    manifest = ProjectManifest(task_types=["lighting"], conventions={"naming": "SM_*"})
    ruleset = GeneratedRuleset(
        target="claude", text="…", source_tool_names=["get_actor_brief"]
    )
    assert snap.tools[0].name == "get_actor_brief"
    assert manifest.task_types == ["lighting"]
    assert ruleset.target == "claude"


def test_generator_is_a_runtime_checkable_protocol():
    class GoodGen:
        def generate(self, snapshot, manifest, *, target="claude"):
            return GeneratedRuleset(target=target, text="x")

    class NotAGen:
        pass

    assert isinstance(GoodGen(), SteeringGenerator)
    assert not isinstance(NotAGen(), SteeringGenerator)


def test_free_tree_ships_no_concrete_generator():
    # ADR-004/ADR-007: the deterministic generator is premium/out-of-tree. The free
    # package must not export a concrete SteeringGenerator implementation.
    for name in pkg.__all__:
        obj = getattr(pkg, name)
        if inspect.isclass(obj) and obj is not SteeringGenerator:
            assert not hasattr(obj, "generate"), f"free tree exports a generator: {name}"
