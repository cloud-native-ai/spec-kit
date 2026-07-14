from __future__ import annotations

from tests.script_api import feedback_utils


# --------------------------------------------------------------------------- #
# unit_id validation (regex boundary)
# --------------------------------------------------------------------------- #
def test_validate_unit_id_accepts_speckit_and_skill():
    assert feedback_utils.validate_unit_id("/speckit.plan")
    assert feedback_utils.validate_unit_id("skill:analysis-project")
    assert feedback_utils.validate_unit_id("/speckit.feedback-mechanism")


def test_validate_unit_id_rejects_arbitrary_text():
    assert not feedback_utils.validate_unit_id("random text")
    assert not feedback_utils.validate_unit_id("")
    assert not feedback_utils.validate_unit_id("speckit.plan")  # missing leading slash
    assert not feedback_utils.validate_unit_id("skill analysis")  # space not allowed


# --------------------------------------------------------------------------- #
# unit_slug derivation
# --------------------------------------------------------------------------- #
def test_unit_slug_derivation():
    assert feedback_utils.unit_slug("/speckit.plan") == "speckit-plan"
    assert feedback_utils.unit_slug("skill:analysis-project") == "skill-analysis-project"
    assert feedback_utils.unit_slug("/speckit.implement") == "speckit-implement"


# --------------------------------------------------------------------------- #
# UTC timestamp formatting
# --------------------------------------------------------------------------- #
def test_now_iso_format():
    ts = feedback_utils.now_iso()
    # YYYY-MM-DDTHH:MM:SSZ
    assert len(ts) == 20 and ts.endswith("Z") and ts[10] == "T"


def test_timestamp_id_format():
    tid = feedback_utils.timestamp_id()
    # YYYYMMDDTHHMMSSZ
    assert len(tid) == 16 and tid.endswith("Z") and tid[8] == "T"


# --------------------------------------------------------------------------- #
# count_since_submission computation
# --------------------------------------------------------------------------- #
def test_count_since_submission_never_submitted_counts_all():
    entries = [
        {"created": "2026-07-13T10:00:00Z"},
        {"created": "2026-07-13T11:00:00Z"},
    ]
    assert feedback_utils.count_since_submission(entries, None) == 2


def test_count_since_submission_only_after_submitted():
    entries = [
        {"created": "2026-07-13T10:00:00Z"},
        {"created": "2026-07-13T12:00:00Z"},
        {"created": "2026-07-13T13:00:00Z"},
    ]
    submitted_at = "2026-07-13T11:00:00Z"
    assert feedback_utils.count_since_submission(entries, submitted_at) == 2


# --------------------------------------------------------------------------- #
# should_prompt = count >= threshold
# --------------------------------------------------------------------------- #
def test_should_prompt_boundary():
    assert feedback_utils.should_prompt(9, 10) is False
    assert feedback_utils.should_prompt(10, 10) is True
    assert feedback_utils.should_prompt(11, 10) is True


# --------------------------------------------------------------------------- #
# make_summary
# --------------------------------------------------------------------------- #
def test_make_summary_first_nonempty_line_capped():
    review = "\n\nFirst meaningful line.\nSecond line."
    assert feedback_utils.make_summary(review) == "First meaningful line."
    long = "x" * 300
    assert len(feedback_utils.make_summary(long)) == 200
