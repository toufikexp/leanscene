"""The no-`unreal`-import guard (ADR-002) actually fails the build on a violation.

This demonstrates Task 00 acceptance: importing `unreal` under packages/core must
fail CI, while packages/unreal-gateway is allowed.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_no_unreal_import as chk  # noqa: E402


def test_real_repo_tree_is_clean():
    # The actual repo must have no violations (RealGateway's import is allowlisted).
    assert chk.find_violations(REPO_ROOT) == []


def test_planted_unreal_import_under_core_is_detected(tmp_path):
    core = tmp_path / "packages" / "core" / "src" / "leanscene_core"
    core.mkdir(parents=True)
    (core / "bad.py").write_text("import unreal\n")
    violations = chk.find_violations(tmp_path)
    assert violations, "checker must flag `import unreal` under packages/core"
    assert any(v.path.name == "bad.py" for v in violations)


def test_from_import_and_dynamic_forms_are_detected(tmp_path):
    pkg = tmp_path / "packages" / "core"
    pkg.mkdir(parents=True)
    (pkg / "a.py").write_text("from unreal import EditorAssetLibrary\n")
    (pkg / "b.py").write_text("import importlib\nimportlib.import_module('unreal')\n")
    (pkg / "c.py").write_text("__import__('unreal')\n")
    flagged = {v.path.name for v in chk.find_violations(tmp_path)}
    assert flagged == {"a.py", "b.py", "c.py"}


def test_unreal_gateway_is_allowlisted(tmp_path):
    gateway = tmp_path / "packages" / "unreal-gateway" / "src" / "pkg"
    gateway.mkdir(parents=True)
    (gateway / "ok.py").write_text("import unreal\n")
    assert chk.find_violations(tmp_path) == []


def test_strings_and_comments_do_not_trip_the_checker(tmp_path):
    pkg = tmp_path / "packages" / "core"
    pkg.mkdir(parents=True)
    (pkg / "fine.py").write_text(
        '"""mentions unreal in a docstring"""\n'
        "x = 'import unreal'  # not a real import\n"
    )
    assert chk.find_violations(tmp_path) == []


def test_cli_exit_codes(tmp_path, capsys):
    # clean tree -> 0
    clean = tmp_path / "clean"
    (clean / "packages" / "core").mkdir(parents=True)
    (clean / "packages" / "core" / "ok.py").write_text("x = 1\n")
    assert chk.main([str(clean)]) == 0

    # violation -> 1
    dirty = tmp_path / "dirty"
    (dirty / "packages" / "core").mkdir(parents=True)
    (dirty / "packages" / "core" / "bad.py").write_text("import unreal\n")
    assert chk.main([str(dirty)]) == 1
