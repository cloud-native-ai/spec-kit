"""Contract test: self-explanatory constitution landing (Feature 082, C-1 group).

Implements ``.specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md``
**C-1** — the template carries the new principle titled `[[STR-001]]` verbatim.

This module is deliberately SEPARATE from ``test_constitution_double_landing.py``: that carrier
holds load-time count constants (C-5/C-7/C-8/C-9) that Feature 082 must bump in a later phase
(T016). Writing the new assertions into a new module keeps the whole US1 red-first capture out of
an existing file's import-time constants, so the red is attributable to the missing artifact and
not to a half-updated carrier.

Red-first provenance (`tasks.md` T006): this module was created and run BEFORE the principle
existed, and the run is recorded in
``.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md``. The red comes from
the assertion below — NOT from the two pre-existing suites, which pass and never reference
`[[STR-001]]`.

Term isolation: the headings' identity is `[[STR-001]]`; the owner location is `[[STR-002]]`
(framework source) / `[[STR-004]]` (runtime). The literal values live in
``requirements.md`` § Shared Strings and are NOT restated here beyond the one string this module
asserts.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "constitution-template.md"

# C-3 / C-4: numeral-agnostic matcher, `re.M` load-bearing for the same reason as the carrier.
TEMPLATE_TITLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)

# [[STR-001]] — the one literal this module asserts.
PRINCIPLE_TITLE = "Self-Explanatory Structure (不言自明)"


def _template_titles(text: str) -> set[str]:
    return {m.group(2).strip() for m in TEMPLATE_TITLE_RE.finditer(text)}


def test_c1_template_carries_the_principle() -> None:
    """C-1: the title is a MEMBER of the template's title set (set membership, never substring)."""
    titles = _template_titles(TEMPLATE.read_text(encoding="utf-8"))
    assert PRINCIPLE_TITLE in titles, (
        f"templates/constitution-template.md is missing the principle titled {PRINCIPLE_TITLE!r}; "
        f"present titles: {sorted(titles)}"
    )
