"""Contract tests for the three measurement instruments (069b, T017).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/measurement-instruments.md``
C-1…C-10 that ``tasks.md`` T017 names:

* C-1  one freeze point for all three quantities — ``requirements.md``'s first
  commit, measured here with the same ``git log --diff-filter=A`` instrument the
  record must name (never ``git log -1``).
* C-2  four existing channels only (exec-quant, feedback frontmatter, clarify
  rounds, the run-determination endpoint + git start). Each channel command is
  executed here so "the instrument still exists" is measured, not asserted.
* C-3  the ``gate_calls`` filter set is frozen as the closed six-unit list. A
  record that only says "six check units" and never names them cannot be
  re-measured at wrap-up — it is the one red this file owns before T022.
* C-4/C-5 the two ``confirmations`` sub-items stay separate and ``wall_clock``
  is ``null`` + reason when the endpoint record is absent.
* C-6/C-8 every row carries the fixed seven fields, ``verdict`` stays inside
  ``{not-evaluated, measured}``, and the "unmeasurable part" (script-level checks
  are not exec-quant units) is written down instead of being counted as 0.
* C-7  ``not-evaluated`` is a verdict, never an SC state: the
  ``verification-log-template.md`` vocabulary stays the five declared values.
* C-10 no second baseline store and no new collector.

Red-first (Constitution IV): the record already exists (frozen at planning time),
so this file's red is a *missing record content* — the closed filter-set list —
not an import or collection error. Every channel probe is read-only.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "069b-isomorphism-migration-metrics"
NOTES = SPEC_DIR / "notes"
BASELINE = NOTES / "expression-baseline.md"
REQUIREMENTS = SPEC_DIR / "requirements.md"
VERIFICATION_TEMPLATE = REPO_ROOT / ".specify" / "templates" / "verification-log-template.md"

SEVEN_FIELDS = (
    "quantity",
    "frozen_value",
    "frozen_at",
    "frozen_commit",
    "instrument",
    "source_command",
    "verdict",
)
VERDICT_VALUES = ("not-evaluated", "measured")
QUANTITIES = ("gate_calls", "confirmations", "wall_clock")
SC_STATES = ("pass", "fail", "partial", "deferred", "unknown")

# Contract C-3: the closed filter set, frozen before any measurement.
GATE_UNITS = (
    "/speckit.checklist",
    "/speckit.analyze",
    "/speckit.review",
    "skill:create-checklist",
    "skill:analyze-artifacts",
    "skill:review-sdd-process",
)
CHANNEL_SCRIPTS = (
    "scripts/python/exec-quant.py",
    "scripts/python/feedback-utils.py",
    "scripts/python/run-determination.py",
)
BASELINE_HEADER = ("quantity", "frozen_value", "frozen_at", "frozen_commit", "instrument", "source_command", "verdict")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _text() -> str:
    assert BASELINE.is_file(), (
        "baseline record missing: %s — expected at planning time (contract C-8)"
        % BASELINE.relative_to(REPO_ROOT)
    )
    return BASELINE.read_text(encoding="utf-8")


def _rows() -> list[dict]:
    header = None
    rows: list[dict] = []
    for line in _text().splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    assert header is not None, "baseline record carries no Markdown table"
    assert tuple(header) == BASELINE_HEADER, (
        "baseline header MUST be the seven declared fields in order (C-8); got %r"
        % (header,)
    )
    return rows


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(args), cwd=str(REPO_ROOT), capture_output=True, text=True
    )


def _git_first_commit() -> tuple[str, str]:
    proc = _run(
        "git",
        "log",
        "--diff-filter=A",
        "--format=%h %as",
        "--",
        str(REQUIREMENTS.relative_to(REPO_ROOT)),
    )
    assert proc.returncode == 0, "git log failed: %r" % proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines, "requirements.md has no first commit — the freeze point is undefined"
    sha, date = lines[-1].split()[:2]  # oldest last
    return sha, date


def _strip(cell: str) -> str:
    return cell.replace("`", "").strip()


def _quantity(row: dict) -> str:
    """Normalise a quantity cell: `` `confirmations`（门控观察） `` → ``confirmations``."""
    value = _strip(row["quantity"])
    return re.split(r"[（(]", value, maxsplit=1)[0].strip()


# --------------------------------------------------------------------------- #
# C-8: shape
# --------------------------------------------------------------------------- #
def test_every_row_carries_the_seven_fields():
    rows = _rows()
    assert rows, "the baseline record must carry at least one data row"
    for row in rows:
        for field in SEVEN_FIELDS:
            assert field in row, "row lacks field %r: %r" % (field, row)
        assert _strip(row["quantity"]), "empty quantity: %r" % row
        assert _strip(row["frozen_at"]), "empty frozen_at: %r" % row
        assert _strip(row["frozen_commit"]), "empty frozen_commit: %r" % row
        assert _strip(row["instrument"]), "empty instrument: %r" % row
        assert _strip(row["source_command"]), "empty source_command: %r" % row
        # frozen_value may be `null` but never blank (C-6).
        assert _strip(row["frozen_value"]), "empty frozen_value: %r" % row


def test_three_quantities_are_frozen_and_confirmations_is_split():
    rows = _rows()
    quantities = [_quantity(row) for row in rows]
    assert set(QUANTITIES) <= set(quantities), (
        "the three quantities MUST each be present (C-1); got %r" % quantities
    )
    confirmations = [row for row in rows if _quantity(row) == "confirmations"]
    assert len(confirmations) == 2, (
        "the two `confirmations` sub-items MUST be recorded separately (C-4); got %r"
        % [row["instrument"] for row in confirmations]
    )
    assert len({row["instrument"] for row in confirmations}) == 2, (
        "the two sub-items must name two distinct instruments (C-4)"
    )


def test_all_quantities_share_one_freeze_point():
    rows = _rows()
    commits = {_strip(row["frozen_commit"]) for row in rows}
    assert len(commits) == 1, (
        "all rows MUST share the same frozen_commit (C-1); got %r" % commits
    )
    sha, _date = _git_first_commit()
    recorded = commits.pop()
    assert recorded.startswith(sha) or sha.startswith(recorded), (
        "frozen_commit %r does not match requirements.md's first commit %r (C-1)"
        % (recorded, sha)
    )


def test_verdicts_stay_inside_the_two_value_set():
    rows = _rows()
    for row in rows:
        verdict = _strip(row["verdict"])
        assert verdict in VERDICT_VALUES, (
            "verdict MUST be one of %r (C-6 / C-8); got %r" % (VERDICT_VALUES, verdict)
        )
        for forbidden in ("达成", "未达成"):
            assert forbidden not in verdict, (
                "the baseline record has no 达成/未达成 layer (C-8); got %r" % verdict
            )


# --------------------------------------------------------------------------- #
# C-3: the closed filter set + the unmeasurable part
# --------------------------------------------------------------------------- #
def test_gate_call_filter_set_is_the_closed_six_unit_ids():
    text = _text()
    missing = [unit for unit in GATE_UNITS if unit not in text]
    assert not missing, (
        "C-3 freezes the gate_calls filter set as the closed six-unit list; "
        "the record never names %r — a re-measurement at wrap-up would have to "
        "re-pick the set" % (missing,)
    )
    assert "MUST NOT" in text or "不得" in text or "不回选" in text, (
        "the record must state that the set is not re-picked at wrap-up (C-3)"
    )


def test_unmeasurable_part_is_declared_instead_of_counted_as_zero():
    text = _text()
    assert "不可计" in text, (
        "the instrument boundary (script-level checks are not exec-quant units) "
        "MUST be written into the record (C-3); it may not be counted as 0"
    )
    for script in (
        "pre-analyze-check.py",
        "validate-requirements.py",
        "doc-consistency-check.py",
    ):
        assert script in text, "the unmeasurable part should name %r (C-3)" % script


# --------------------------------------------------------------------------- #
# C-2: the four channels still exist and still run
# --------------------------------------------------------------------------- #
def test_exec_quant_channel_runs():
    proc = _run(
        sys.executable,
        "scripts/python/exec-quant.py",
        "--action",
        "list-records",
        "--since",
        "2026-10-24",
        "--format",
        "json",
    )
    assert proc.returncode == 0, "exec-quant channel broke: %r" % proc.stderr
    payload = json.loads(proc.stdout)
    assert isinstance(payload, list), "exec-quant --action list-records must emit a JSON list"


def test_feedback_channel_runs():
    proc = _run(
        sys.executable,
        "scripts/python/feedback-utils.py",
        "--action",
        "list",
        "--since",
        "2026-10-24",
        "--format",
        "json",
    )
    assert proc.returncode == 0, "feedback channel broke: %r" % proc.stderr
    payload = json.loads(proc.stdout)
    assert "matches" in payload, "feedback --action list must carry a `matches` field"


def test_run_determination_channel_runs():
    proc = _run(
        sys.executable,
        "scripts/python/run-determination.py",
        "--action",
        "history",
        "--target",
        "/speckit.analyze",
        "--json",
    )
    assert proc.returncode == 0, "run-determination channel broke: %r" % proc.stderr
    payload = json.loads(proc.stdout)
    assert "target" in payload, "run-determination --action history must name its target"


def test_git_start_channel_is_the_first_commit_not_the_last_touch():
    sha, date = _git_first_commit()
    assert sha and date, "git start channel returned an empty tuple"
    text = _text()
    assert "--diff-filter=A" in text, (
        "the record MUST name the first-commit instrument (`git log --diff-filter=A`), "
        "not the last touch (C-1)"
    )
    assert sha in text and date in text, (
        "the recorded start point (%s @ %s) does not appear in the record (C-1)"
        % (sha, date)
    )


# --------------------------------------------------------------------------- #
# C-7 / C-10: vocabulary boundary, no second store, no new collector
# --------------------------------------------------------------------------- #
def test_sc_state_vocabulary_stays_five_values():
    template = VERIFICATION_TEMPLATE.read_text(encoding="utf-8")
    match = re.search(r"`?status`?\s+is one of:\s*([a-z]+(?:\s*\|\s*[a-z]+)+)", template)
    assert match, "verification-log-template.md must declare its SC status vocabulary"
    states = tuple(token.strip() for token in match.group(1).split("|"))
    assert states == SC_STATES, (
        "the SC vocabulary MUST stay the five declared values (C-7); got %r" % (states,)
    )
    assert "not-evaluated" not in states, (
        "`not-evaluated` is a verdict, never an SC state (C-7)"
    )


def test_no_second_baseline_store_under_the_slice_notes():
    records = []
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if all(field in text for field in ("quantity", "frozen_value", "frozen_commit", "verdict")):
            records.append(path.name)
    assert records == ["expression-baseline.md"], (
        "exactly one baseline record may exist (C-10); found %r" % records
    )


def test_record_cites_only_existing_scripts():
    text = _text()
    named = {Path(match).name for match in re.findall(r"scripts/python/([a-z0-9-]+\.py)", text)}
    assert named, "the record must cite the channel scripts that can re-run it"
    absent = [name for name in sorted(named) if not (REPO_ROOT / "scripts" / "python" / name).is_file()]
    assert not absent, (
        "the record cites scripts that do not exist — a collector may have been "
        "invented instead of reused (C-2 / C-10): %r" % absent
    )
    for script in CHANNEL_SCRIPTS:
        assert Path(script).name in named, (
            "the record must cite its channel %s (C-2)" % script
        )
        assert (REPO_ROOT / script).is_file(), "channel script missing: %s" % script
