"""Contract tests for ``scripts/python/validate-falsification-quartet.py`` (Feature 076, US3).

The quartet turns "the falsification attempt ran" from a claim into a fact the artifact can
distinguish: four literal keys, each appearing once, judged by a deterministic program whose
exit code *is* the verdict. This suite drives the real CLI
(``validate-falsification-quartet.py <payload.md> [--json]``) and never re-implements the parser —
a second copy of the grammar would be a second source of truth.

The matrix is fixed by SC-004 / FR-021: eleven runs — one compliant payload, one sample per
rejection reason in the closed six-value set, and four additional ``missing-field`` samples (one
per omitted field). A twelfth, independent fixture pins the ``red:`` split point: the split is the
**first** occurrence, so a payload carrying a second ``red:`` still has one determinate verdict.
Every payload is built as a literal in ``tmp_path``; nothing is checked in.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "python" / "validate-falsification-quartet.py"

# The closed rejection-reason set (FR-021 / contracts/falsification-quartet.md C-3).
REASONS = (
    "missing-field",
    "empty-field",
    "exit-code-not-integer",
    "observation-not-raw",
    "tautology",
    "input-unreadable",
)

KEYS = ("attempt", "exit_code", "observation", "would_go_red_if")

# One compliant payload. The `would_go_red_if` value carries the literal `red:` marker exactly
# once; the input half is a backtick span before it, the signal half a backtick span after it.
COMPLIANT = """attempt: `pytest -q tests/contract/test_decision_tension_validator.py`
exit_code: 0
observation: raw: 16 passed in 2.15s
would_go_red_if: 把 `expected_sacrifice` 的值改成字面 `none`，则 red: `test_inverse_samples_turn_red[sacrifice-none]` 必须 FAILED（退出码 1）
"""


def payload(**overrides) -> str:
    """The compliant payload with whole lines replaced; ``None`` deletes the key line."""
    lines = {}
    for line in COMPLIANT.splitlines():
        key = line.split(":", 1)[0]
        lines[key] = line
    for key, value in overrides.items():
        assert key in KEYS, f"unknown quartet key: {key}"
        if value is None:
            lines.pop(key, None)
        else:
            lines[key] = f"{key}: {value}"
    return "\n".join(lines[key] for key in KEYS if key in lines) + "\n"


def write(tmp_path: Path, text: str, name: str = "payload.md") -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def run(target: Path, *extra: str) -> subprocess.CompletedProcess:
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target), *extra],
        capture_output=True,
        text=True,
    )


def verdict_of(proc: subprocess.CompletedProcess) -> dict:
    """The ``--json`` envelope; a non-JSON print is a readable failure, never a pass."""
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:  # pragma: no cover - surfaced as a readable failure
        raise AssertionError(
            f"--json did not print JSON; exit={proc.returncode} stdout={proc.stdout!r} "
            f"stderr={proc.stderr!r}"
        )


# --------------------------------------------------------------------------- #
# C-3 — the compliant payload is accepted
# --------------------------------------------------------------------------- #

def test_compliant_payload_is_accepted(tmp_path):
    proc = run(write(tmp_path, COMPLIANT), "--json")
    assert proc.returncode == 0, f"a compliant quartet must be accepted:\n{proc.stdout}"
    verdict = verdict_of(proc)
    assert verdict["status"] == "accepted", verdict
    assert verdict["reason"] is None, (
        f"an accepted payload carries no rejection reason; got {verdict['reason']!r}"
    )
    assert set(verdict) == {"payload", "status", "reason", "detail"}, (
        f"the --json envelope must carry exactly the four declared fields; got {sorted(verdict)}"
    )


# --------------------------------------------------------------------------- #
# C-3 — the closed six rejection reasons, one sample each (6/6)
# --------------------------------------------------------------------------- #

REJECTION_MATRIX = [
    pytest.param(
        lambda: payload(attempt=None, exit_code=None),
        "missing-field", 1, "attempt",
        id="missing-field",
    ),
    pytest.param(
        lambda: payload(observation=""),
        "empty-field", 1, "observation",
        id="empty-field",
    ),
    pytest.param(
        lambda: payload(exit_code="ok"),
        "exit-code-not-integer", 1, "exit_code",
        id="exit-code-not-integer",
    ),
    pytest.param(
        lambda: payload(observation="测试通过，16 passed"),
        "observation-not-raw", 1, "raw:",
        id="observation-not-raw",
    ),
    pytest.param(
        lambda: payload(would_go_red_if="若实现有误就会失败"),
        "tautology", 1, "red:",
        id="tautology",
    ),
    pytest.param(
        lambda: None,  # never written: the path does not exist
        "input-unreadable", 2, None,
        id="input-unreadable",
    ),
]


@pytest.mark.parametrize("build,reason,exit_code,detail_token", REJECTION_MATRIX)
def test_rejection_is_program_verdict_closed_reasons(tmp_path, build, reason, exit_code, detail_token):
    text = build()
    target = (tmp_path / "missing.md") if text is None else write(tmp_path, text)

    proc = run(target, "--json")
    assert proc.returncode == exit_code, (
        f"{reason}: expected exit {exit_code}, got {proc.returncode}:\n{proc.stdout}\n{proc.stderr}"
    )
    verdict = verdict_of(proc)
    assert verdict["status"] == "rejected", verdict
    assert verdict["reason"] == reason, (
        f"expected reason {reason!r}, got {verdict['reason']!r}"
    )
    assert verdict["reason"] in REASONS, (
        f"{verdict['reason']!r} is outside the closed reason set {REASONS!r}"
    )
    assert verdict["detail"], f"{reason}: the verdict must carry a non-empty detail"
    if detail_token is not None:
        assert detail_token in verdict["detail"], (
            f"{reason}: the verdict must name the missing field or the failing half; "
            f"detail={verdict['detail']!r}"
        )


def test_rejection_rate_is_six_of_six():
    """A guard on the matrix itself: six reasons, six samples, no silent gap."""
    covered = {param.values[1] for param in REJECTION_MATRIX}
    assert covered == set(REASONS), (
        f"the matrix must cover the closed six reasons exactly once; gaps={sorted(set(REASONS) - covered)}, "
        f"extras={sorted(covered - set(REASONS))}"
    )
    exits = {param.values[2] for param in REJECTION_MATRIX} | {0}
    assert exits == {0, 1, 2}, f"the matrix must exercise the exit-code triple; got {sorted(exits)}"


# --------------------------------------------------------------------------- #
# C-3 — the four single-field omissions are ADDITIONAL `missing-field` samples
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("field", KEYS)
def test_each_omitted_field_is_a_missing_field_rejection(tmp_path, field):
    proc = run(write(tmp_path, payload(**{field: None})), "--json")
    assert proc.returncode == 1, (
        f"omitting {field} must be rejected (exit 1), not accepted; stdout={proc.stdout!r}"
    )
    verdict = verdict_of(proc)
    assert verdict["reason"] == "missing-field", verdict
    assert field in verdict["detail"], (
        f"the verdict must name the omitted field {field!r}; detail={verdict['detail']!r}"
    )


# --------------------------------------------------------------------------- #
# C-3 — the `red:` split is the FIRST occurrence, so the verdict is determinate
# --------------------------------------------------------------------------- #

DOUBLE_RED = payload(
    would_go_red_if=(
        "把 `input_a` 改坏，则 red: `check_label_a` 必须变红；"
        "同一行再出现一次 red: 也不得移动切分点"
    ),
)


def test_double_red_splits_at_first_occurrence(tmp_path):
    value = DOUBLE_RED.split("would_go_red_if:", 1)[1]
    positions = [match.start() for match in re.finditer("red:", value)]
    assert len(positions) == 2, (
        f"this fixed fixture must carry exactly two `red:` markers; found {len(positions)}"
    )
    first, second = positions
    assert "`" in value[:first], "the input half (before the FIRST `red:`) must carry a span"
    assert "`" in value[first:second], (
        "the signal half is the segment after the first marker — it must carry a span, "
        "otherwise the fixture cannot distinguish the two split points"
    )
    assert "`" not in value[second:], (
        "the text after the SECOND `red:` must carry no span, so splitting there would yield "
        "an empty signal half and a `tautology` — that is what makes this fixture discriminating"
    )

    proc = run(write(tmp_path, DOUBLE_RED, "double-red.md"), "--json")
    assert proc.returncode == 0, (
        "splitting at the first `red:` leaves both halves non-empty, so the payload is accepted; "
        f"stdout={proc.stdout!r}"
    )
    verdict = verdict_of(proc)
    assert verdict["status"] == "accepted", verdict


# --------------------------------------------------------------------------- #
# C-3 — the key anchor: a list marker or heading prefix is not a second grammar
# --------------------------------------------------------------------------- #
#
# SI-4 payloads are markdown, so the ordinary shape an author produces is a bullet list under a
# heading. The key is the same four literal names in the same order — only the prefix differs — so
# the payload must be read identically and accepted (review: code important-a). What the anchor
# still forbids is an INDENTED key: that line belongs to the value above it.

BULLET_PAYLOAD = """## Falsification attempt

- attempt: `pytest -q tests/contract/test_decision_tension_validator.py`
- exit_code: 0
- observation: raw: 16 passed in 2.15s
- would_go_red_if: 把 `expected_sacrifice` 改成字面 `none`，则 red: `test_inverse_samples_turn_red[sacrifice-none]` 必须 FAILED（退出码 1）
"""

HEADING_PAYLOAD = """### attempt: `pytest -q tests/contract/test_falsification_quartet_validator.py`
### exit_code: 1
### observation: raw: 1 failed, 20 passed
### would_go_red_if: 把 `KEYS` 里删掉一个名字，则 red: `test_rejection_rate_is_six_of_six` 必须 FAILED
"""


def test_bullet_list_payload_is_the_same_grammar(tmp_path):
    """Four keys as markdown list items: accepted, and read as the same quartet."""
    proc = run(write(tmp_path, BULLET_PAYLOAD, "bullet.md"), "--json")
    assert proc.returncode == 0, (
        "a bullet-list quartet is the ordinary markdown shape and must be accepted; "
        f"stdout={proc.stdout!r}"
    )
    verdict = verdict_of(proc)
    assert verdict["status"] == "accepted", verdict
    assert verdict["reason"] is None, verdict


def test_heading_prefix_payload_is_the_same_grammar(tmp_path):
    """A heading prefix is read the same way — the prefix is markup, not part of the key."""
    proc = run(write(tmp_path, HEADING_PAYLOAD, "headings.md"), "--json")
    assert proc.returncode == 0, (
        f"a heading-prefixed quartet must be accepted; stdout={proc.stdout!r}"
    )
    assert verdict_of(proc)["status"] == "accepted"


def test_indented_key_stays_part_of_the_value_above(tmp_path):
    """The guard on the other side: an indented key is a continuation, never a second key.

    Without this half, widening the anchor would let an indented `- attempt:` inside a value start
    a second `attempt` — which is what makes the exactly-once rule unreadable.
    """
    indented = payload(
        observation="raw: 16 passed\n  - attempt: 这不是第二个 attempt，而是 observation 的续行",
    )
    proc = run(write(tmp_path, indented, "indented.md"), "--json")
    assert proc.returncode == 0, (
        "an indented key-shaped line is a continuation of the value above it, so the payload "
        f"still carries four keys exactly once; stdout={proc.stdout!r}"
    )


def test_duplicate_key_under_a_prefix_is_still_one_field_too_many(tmp_path):
    """A repeat is a repeat whatever prefix it wears: no second `attempt` may pass as first."""
    duplicated = BULLET_PAYLOAD.replace(
        "- exit_code: 0",
        "- attempt: `pytest -q another_test.py`\n- exit_code: 0",
    )
    assert duplicated.count("attempt:") == 2, "the fixture must carry two `attempt` keys"
    proc = run(write(tmp_path, duplicated, "duplicate.md"), "--json")
    assert proc.returncode == 1, (
        f"a duplicated key must be rejected, not silently collapsed; stdout={proc.stdout!r}"
    )
    verdict = verdict_of(proc)
    assert verdict["reason"] == "missing-field", (
        "the closed set has no duplicate-field member: a key that does not appear exactly once "
        f"cannot be read unambiguously. got {verdict!r}"
    )
    assert "attempt" in verdict["detail"], verdict
