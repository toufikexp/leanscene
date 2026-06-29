#!/usr/bin/env python3
"""Fail the build if ``unreal`` is imported outside ``packages/unreal-gateway`` (ADR-002).

This is the CI guard for the gateway seam: all business logic must be
UE-independent, so only the gateway package may import ``unreal``.

Detection is AST-based (so strings/comments mentioning "unreal" do not trip it).
It catches the common static forms:

    import unreal
    import unreal.something
    from unreal import X
    from unreal.sub import X
    importlib.import_module("unreal")
    __import__("unreal")

Limitation: a fully dynamic import where the module name is computed at runtime
(e.g. ``importlib.import_module(name)``) cannot be caught statically. That is an
accepted gap; the gateway boundary is also enforced by code review.

Usage:
    python tools/check_no_unreal_import.py [ROOT]   # ROOT defaults to repo root
Exit code is non-zero if any violation is found.
"""
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Path prefixes (repo-relative, posix) allowed to import ``unreal``.
ALLOWLISTED_DIRS: Sequence[str] = ("packages/unreal-gateway",)

#: Directory names never scanned.
SKIP_DIRS = frozenset(
    {".git", "__pycache__", "_vendor", ".venv", "venv", "env", "node_modules", "build", "dist"}
)


@dataclass(frozen=True)
class Violation:
    path: Path
    lineno: int
    statement: str


def _targets_unreal(module: Optional[str]) -> bool:
    return module is not None and (module == "unreal" or module.startswith("unreal."))


def _is_dynamic_unreal_import(node: ast.Call) -> bool:
    """Detect importlib.import_module("unreal") / __import__("unreal") with a literal."""
    func = node.func
    name = None
    if isinstance(func, ast.Name):
        name = func.id  # __import__(...)
    elif isinstance(func, ast.Attribute):
        name = func.attr  # importlib.import_module(...)
    if name not in {"import_module", "__import__"}:
        return False
    if not node.args:
        return False
    first = node.args[0]
    return isinstance(first, ast.Constant) and _targets_unreal(first.value if isinstance(first.value, str) else None)


def scan_file(path: Path) -> List[Violation]:
    try:
        source = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        # Not a parseable Python file (or a deliberately broken fixture); skip.
        return []

    violations: List[Violation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _targets_unreal(alias.name):
                    violations.append(Violation(path, node.lineno, f"import {alias.name}"))
        elif isinstance(node, ast.ImportFrom):
            # node.level > 0 is a relative import (never ``unreal``).
            if node.level == 0 and _targets_unreal(node.module):
                violations.append(Violation(path, node.lineno, f"from {node.module} import ..."))
        elif isinstance(node, ast.Call) and _is_dynamic_unreal_import(node):
            violations.append(Violation(path, node.lineno, "dynamic import of 'unreal'"))
    return violations


def _is_allowlisted(rel_posix: str, allowlist: Sequence[str]) -> bool:
    return any(rel_posix == d or rel_posix.startswith(d + "/") for d in allowlist)


def find_violations(
    root: Path, allowlist: Sequence[str] = ALLOWLISTED_DIRS
) -> List[Violation]:
    root = Path(root)
    violations: List[Violation] = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if _is_allowlisted(rel.as_posix(), allowlist):
            continue
        violations.extend(scan_file(path))
    return violations


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    root = Path(args[0]) if args else REPO_ROOT
    violations = find_violations(root)
    if violations:
        print("ADR-002 violation: `unreal` imported outside packages/unreal-gateway:")
        for v in violations:
            rel = v.path.relative_to(root) if v.path.is_relative_to(root) else v.path
            print(f"  {rel}:{v.lineno}: {v.statement}")
        print(f"\n{len(violations)} violation(s). Move this logic behind UnrealGateway.")
        return 1
    print("OK: no `unreal` import outside packages/unreal-gateway.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
