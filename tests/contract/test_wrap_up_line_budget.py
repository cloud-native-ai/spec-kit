"""Contract test: SC-007 compiled wrap-up line budget (056 US3, T025).

SC-007 pins the wrap-up faces at ≤ 853 non-empty lines (the T002 pre-change
baseline, pre-change-measurements.md § PM-1). Counting rule: per FILE, a
section starts at an H2 ``## Feedback`` / ``## Documentation`` / ``## Wrap-up``
line and ends at the next H2/H1 or EOF; non-blank lines inside count. (The
original PM-1 awk one-liner bled a file's trailing section state into the next
file's frontmatter when run over a glob — the per-file rule here is the same
intent, measured strictly: no phantom lines.)

Post-migration reality (measured 2026-10-13): 137 + 210 + 66 = 413 — the
five-in-one compiled form is strongly token-positive against the 853 ceiling.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

FACE = re.compile(r"^## (Feedback|Documentation|Wrap-up)( |$)")
BUDGET = 853

GROUPS = (
    ("templates/commands", "*.md"),
    ("skills/internal", "*/SKILL.md"),
    ("skills/external", "*/SKILL.md"),
)


def non_empty_section_lines(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    total = 0
    in_face = False
    for line in lines:
        if line.startswith("## "):
            in_face = bool(FACE.match(line))
        elif in_face and line.strip():
            total += 1
    return total


@pytest.mark.contract
def test_wrap_up_faces_within_line_budget():
    per_group = {}
    for base, pattern in GROUPS:
        per_group[base] = sum(
            non_empty_section_lines(p) for p in sorted((REPO_ROOT / base).glob(pattern))
        )
    total = sum(per_group.values())
    assert total >= 200, (
        f"wrap-up faces measure only {total} non-empty lines — the counting rule or the "
        f"unit universe looks broken (a compiled face is ~6-9 lines across ~69 units)"
    )
    assert total <= BUDGET, (
        f"SC-007 breached: wrap-up faces carry {total} non-empty lines > {BUDGET} — "
        f"the compiled form grew; shrink the section renderer or re-adjudicate the budget"
    )
