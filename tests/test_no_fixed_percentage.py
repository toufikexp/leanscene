"""ADR-003: no fixed (advertised) percentage anywhere in the repo.

Computed, per-call values rendered at runtime are fine; this guard catches a
*literal* percentage written into source/docs (a marketing constant). Genuinely
non-savings mentions are allowlisted by substring with a reason.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PERCENT = re.compile(r"\d+(\.\d+)?\s*%")

SKIP_DIRS = frozenset(
    {".git", "__pycache__", "_vendor", ".venv", "venv", "env", ".pytest_cache",
     "node_modules", "build", "dist", ".egg-info"}
)
SCAN_SUFFIXES = frozenset({".py", ".md", ".txt", ".toml", ".cfg", ".ini", ".cursorrules"})

#: (substring -> why it is legitimately not a token-savings claim).
ALLOWLIST = {
    "80% of the product": "docs/DECISIONS.md ADR-002: codebase composition, not a savings claim",
}


def _scannable_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(REPO_ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if any(part.endswith(".egg-info") for part in rel_parts):
            continue
        if path.suffix in SCAN_SUFFIXES:
            yield path


def test_no_advertised_fixed_percentage_anywhere():
    offenders = []
    for path in _scannable_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if not PERCENT.search(line):
                continue
            if any(allowed in line for allowed in ALLOWLIST):
                continue
            offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")
    assert not offenders, "literal fixed percentage(s) found (ADR-003):\n" + "\n".join(offenders)
