"""ADR-004: the public repo contains only free trees — no premium code here."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_premium_ships_no_python_code():
    premium = REPO_ROOT / "premium"
    py_files = sorted(str(p.relative_to(REPO_ROOT)) for p in premium.rglob("*.py"))
    assert py_files == [], f"premium/ must contain no .py in the public repo: {py_files}"


def test_premium_is_a_documented_placeholder():
    premium = REPO_ROOT / "premium"
    assert (premium / "README.md").is_file()
    assert (premium / "LICENSE-COMMERCIAL.md").is_file()
