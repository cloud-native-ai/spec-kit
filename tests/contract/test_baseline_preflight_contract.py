"""Contract test: implement's baseline pre-flight and drift attribution.

063-review-p1-governance, US5 (C-29/C-30, FR-022/FR-023/FR-030, SC-011).

C-29 — skills/internal/implement-feature/SKILL.md gains a pre-flight step BEFORE
       Step 1: re-capture every frozen baseline of the feature — the set derived
       from the spec directory by glob (`<spec-dir>/baseline-*`,
       `<spec-dir>/notes/baseline-*`) plus the coverage baseline file
       ([[STR-002]]); directory-derived, never a hand-written count. Where a
       re-capture differs from the frozen value, the new value is written into
       the row that cites it, and every difference is classified — BEFORE any
       drift verdict — as `upstream repair` / `inherited` / `attributable to
       this feature` / `undecidable` using `git log` provenance. `undecidable`
       is explicitly reported; no guessing between the attributed classes. A
       missing baseline file is a first capture with provenance recorded,
       never zero drift.
C-30 — templates/commands/implement.md states the same pre-flight duty in the
       command face (Skill Delegation inputs, BEFORE "follow its steps 1–9"),
       so the obligation reaches a reader of the command alone.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "internal" / "implement-feature" / "SKILL.md"
COMMAND = REPO_ROOT / "templates" / "commands" / "implement.md"

GLOB_ROOTS = ("<spec-dir>/baseline-*", "<spec-dir>/notes/baseline-*")
CLASSES = ("upstream repair", "inherited", "attributable to this feature", "undecidable")


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _preflight_step(text: str) -> str:
    """The pre-flight section: between the Workflow heading and Step 1."""
    m = re.search(r"(?ms)^(### Step 0 .*?)(?=^### Step 1 |\Z)", text)
    if not m:
        # Also accept a named pre-flight section before Step 1.
        m = re.search(r"(?ms)^(### .*[Pp]re-flight.*?)(?=^### Step 1 |\Z)", text)
    assert m, (
        "implement-feature SKILL.md lacks a pre-flight step before Step 1 "
        "(C-29: the baseline re-capture MUST run before any other workflow step)"
    )
    return m.group(1)


# --------------------------------------------------------------------------- #
# C-29 — the skill-side pre-flight step
# --------------------------------------------------------------------------- #

def test_c29_preflight_step_sits_before_step1():
    text = _skill_text()
    step = _preflight_step(text)
    step1_at = text.index("### Step 1")
    workflow_at = text.index("## Workflow")
    assert workflow_at < text.index(step.splitlines()[0]) < step1_at, (
        "the pre-flight step MUST sit after the Workflow heading and before Step 1"
    )


def test_c29_baseline_set_is_directory_derived():
    step = _preflight_step(_skill_text())
    for root in GLOB_ROOTS:
        assert root in step, (
            f"the re-capture set MUST include the glob root `{root}` "
            "(directory-derived, per FR-030)"
        )
    assert re.search(r"coverage-baseline|\[\[STR-002\]\]", step), (
        "the coverage baseline file ([[STR-002]]) MUST be part of the set"
    )
    assert re.search(r"never a hand-written count|not a hand-written count|"
                     r"不手写条数|directory-derived", step), (
        "the step MUST declare the set is derived from the directory, never a "
        "hand-written count"
    )


def test_c29_recapture_differences_write_back_the_citing_rows():
    step = _preflight_step(_skill_text())
    assert re.search(r"written\s+into\s+the\s+(row|line)\s+that\s+cites\s+it|"
                     r"写(入|回)(引用|它的行)|citing row", step, re.I), (
        "a differing re-capture MUST be written back into the row that cites it"
    )


def test_c29_classification_happens_before_any_drift_verdict():
    step = _preflight_step(_skill_text())
    for cls in CLASSES:
        assert cls in step, f"the classification set MUST name `{cls}`"
    before_at = step.lower().find("before any drift verdict")
    assert before_at != -1 or re.search(r"verdict.*之前|先.*分类", step), (
        "classification MUST happen BEFORE any drift verdict is issued"
    )


def test_c29_provenance_source_is_git_log():
    step = _preflight_step(_skill_text())
    assert "`git log`" in step or "git log" in step, (
        "the four-way classification MUST use `git log` provenance"
    )


def test_c29_undecidable_is_explicit_never_guessed():
    step = _preflight_step(_skill_text())
    assert re.search(r"undecidable.*(explicit|report)|explicit.*undecidable|"
                     r"显式报告", step, re.I | re.S), (
        "`undecidable` MUST be explicitly reported"
    )
    assert re.search(r"MUST NOT (guess|invent)|不猜测|不得猜测", step), (
        "guessing between the three attributed classes MUST NOT happen"
    )


def test_c29_missing_baseline_is_first_capture_not_zero_drift():
    step = _preflight_step(_skill_text())
    assert re.search(r"first capture", step, re.I), (
        "a missing baseline file MUST be handled as a first capture"
    )
    assert re.search(r"provenance", step, re.I), (
        "the first capture MUST record provenance"
    )
    assert re.search(r"never.*zero drift|not.*zero drift|不得当作零漂移|"
                     r"非零漂移", step, re.I), (
        "a missing baseline MUST NOT be treated as zero drift"
    )


# --------------------------------------------------------------------------- #
# C-30 — the command face states the same duty
# --------------------------------------------------------------------------- #

def test_c30_command_face_states_the_preflight_duty_before_the_how_to_call():
    text = _command_text()
    duty_at = text.find("pre-flight")
    how_at = text.find("follow its steps 1–9")
    assert duty_at != -1, (
        "templates/commands/implement.md MUST state the pre-flight duty in its "
        "Skill Delegation inputs (C-30)"
    )
    assert duty_at < how_at, (
        "the duty MUST appear BEFORE `follow its steps 1–9`, so a reader of the "
        "command alone meets the obligation before entering the skill"
    )


def test_c30_command_face_carries_the_same_obligation_shape():
    text = _command_text()
    m = re.search(r"(?ms)(pre-flight.*?)(?=follow its steps 1–9)", text)
    assert m, "the pre-flight duty paragraph must be locatable in the command face"
    duty = m.group(1)
    for root in GLOB_ROOTS:
        assert root in duty, f"the command face MUST name the glob root `{root}`"
    for cls in CLASSES:
        assert cls in duty, f"the command face MUST name the class `{cls}`"
    assert re.search(r"undecidable", duty) and re.search(r"first capture", duty, re.I), (
        "the command face MUST carry the undecidable-report and first-capture "
        "rules, not a summarized subset of the duty"
    )
