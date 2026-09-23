"""Contract test (US2): command feedback-step classification.

Driven by ``contracts/command-classification.md``: every **complex** command
template carries the feedback step; every **simple** template (``agents``,
``constitution``, ``feature``) does NOT.

Since the 2026-09-24 Known-Gap closure the two lists below are **derived from the
contract table**, not hand-maintained beside it — the table is the operative
enumeration, which is what the contract's own ``## Maintenance`` bullet asks for.
Deriving makes the table load-bearing, so the parse is guarded by an anti-vacuity
floor (``MIN_COMMANDS``) and an explicit coverage assertion: "zero gap because the
table is complete" must stay distinguishable from "zero gap because no row parsed".
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
CONTRACT = (
    REPO_ROOT / ".specify" / "specs" / "027-feedback-mechanism"
    / "contracts" / "command-classification.md"
)

# The stable marker embedded by the feedback step (the engine record invocation).
FEEDBACK_MARKER = "feedback-utils.py"

# Anti-vacuity sentinel (same pattern as test_feedback_step_reference_form.py's
# MIN_SURFACES): a derived set that silently came out empty or truncated would make
# every per-command assertion below pass vacuously. 25 = the measured
# templates/commands/*.md count on 2026-09-24.
MIN_COMMANDS = 25

_ROW_CMD = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|")
_ROW_CLASS = re.compile(r"\*\*(Complex|Simple)\*\*")
RESULT_LINE = re.compile(r"\*\*Result\*\*: (\d+) complex .*?(\d+) simple")


def _parse_table() -> dict[str, str]:
    """{command: 'Complex'|'Simple'} from the contract's classification table.

    Raises rather than returning a short dict: a collection error naming this file
    is loud, whereas an empty parametrization would be a silent green.
    """
    if not CONTRACT.is_file():
        raise RuntimeError(f"contract missing: {CONTRACT}")
    rows: dict[str, str] = {}
    for line in CONTRACT.read_text(encoding="utf-8").splitlines():
        m = _ROW_CMD.match(line)
        if not m:
            continue
        classes = _ROW_CLASS.findall(line)
        if len(classes) != 1:
            raise RuntimeError(
                f"row `{m.group(1)}` carries {len(classes)} Class markers; expected exactly 1"
            )
        rows[m.group(1)] = classes[0]
    if len(rows) < MIN_COMMANDS:
        raise RuntimeError(
            f"only {len(rows)} classification rows parsed (< {MIN_COMMANDS}) — the table "
            f"shape changed or the parse broke; every derived assertion below would be vacuous"
        )
    return rows


TABLE = _parse_table()
COMPLEX_COMMANDS = sorted(c for c, k in TABLE.items() if k == "Complex")
SIMPLE_COMMANDS = sorted(c for c, k in TABLE.items() if k == "Simple")

# `team` was reclassified simple → complex on 2026-09-23 (user-adjudicated,
# introspection-20260923T120035Z#F-02); the criteria are recorded in its table row.


def template_stems() -> set[str]:
    return {p.stem for p in COMMANDS_DIR.glob("*.md")}


def measured_feedback_carriers() -> set[str]:
    """Templates that actually carry a `## Feedback` heading — measured, not listed."""
    return {
        p.stem for p in COMMANDS_DIR.glob("*.md")
        if re.search(r"(?m)^## Feedback[ \t]*$", p.read_text(encoding="utf-8"))
    }


def test_classification_counts():
    # The one place these literals are pinned (test_docs_command_template.py::test_c8
    # deliberately does not restate them, to keep a reclassification a one-file edit).
    assert len(COMPLEX_COMMANDS) == 22
    assert len(SIMPLE_COMMANDS) == 3


def test_table_covers_every_command_template():
    """Zero-gap coverage, both directions, with a non-zero floor."""
    stems = template_stems()
    assert len(stems) >= MIN_COMMANDS, (
        f"only {len(stems)} command templates found — the glob looks broken, which would "
        f"let 'no unlisted command' pass without any command being counted"
    )
    assert set(TABLE) == stems, (
        f"table/template drift — unlisted templates: {sorted(stems - set(TABLE))}; "
        f"rows with no template: {sorted(set(TABLE) - stems)}"
    )
    assert len(COMPLEX_COMMANDS) + len(SIMPLE_COMMANDS) == len(stems)


def test_complex_set_equals_measured_feedback_carriers():
    """Tie the classification to the templates: complex == carries `## Feedback`."""
    assert set(COMPLEX_COMMANDS) == measured_feedback_carriers()
    for cmd in SIMPLE_COMMANDS:
        assert cmd not in measured_feedback_carriers(), f"{cmd}.md is simple but carries ## Feedback"


def test_result_line_matches_the_counted_rows():
    m = RESULT_LINE.search(CONTRACT.read_text(encoding="utf-8"))
    assert m, "contract lost its **Result** count line"
    assert int(m.group(1)) == len(COMPLEX_COMMANDS), "**Result** complex count != counted rows"
    assert int(m.group(2)) == len(SIMPLE_COMMANDS), "**Result** simple count != counted rows"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", COMPLEX_COMMANDS)
def test_complex_command_carries_feedback_step(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert "## Feedback" in text, f"{cmd}.md missing '## Feedback' heading"
    assert FEEDBACK_MARKER in text, f"{cmd}.md missing feedback record invocation"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", SIMPLE_COMMANDS)
def test_simple_command_omits_feedback_step(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert FEEDBACK_MARKER not in text, f"{cmd}.md must NOT carry the feedback step"
