"""Contract tests for Feature 040 consumption observation (C-M1..C-M3, spec 035).

C-M1: feedback-step.md Reflect step carries the token-efficiency
self-assessment. C-M2: feedback-utils `list --contains` behavior.
C-M3: retrieval completeness over a fixture store.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
FEEDBACK_STEP = ROOT / "shared" / "workflow" / "feedback-step.md"
ENGINE = ROOT / "scripts" / "python" / "feedback-utils.py"
ENGINE_MIRROR = ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"


# --------------------------------------------------------------------------- #
# C-M1: feedback-step Reflect extension
# --------------------------------------------------------------------------- #
def test_cm1_reflect_carries_three_question_assessment():
    text = FEEDBACK_STEP.read_text(encoding="utf-8")
    for probe in ["原文转储", "代做确定性工作", "重复读取"]:
        assert probe in text, f"token self-assessment question missing: {probe}"


def test_cm1_marker_and_discipline_reference():
    text = FEEDBACK_STEP.read_text(encoding="utf-8")
    assert "token-efficiency" in text, "stable marker literal missing"
    assert "token-efficiency.md" in text, "discipline doc reference missing"


def test_cm1_clean_run_sentence_and_no_fabrication():
    text = FEEDBACK_STEP.read_text(encoding="utf-8")
    assert "No significant optimization points identified this run." in text
    assert "不编造" in text or "MUST NOT fabricate" in text, "no-fabrication rule missing"


def test_cm1_mirror_identical():
    mirror = ROOT / ".specify" / "shared" / "workflow" / "feedback-step.md"
    assert FEEDBACK_STEP.read_bytes() == mirror.read_bytes(), "feedback-step mirror drift"


def test_cm2_engine_mirror_identical():
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes(), "feedback-utils mirror drift"


# --------------------------------------------------------------------------- #
# C-M2 / C-M3: list --contains over a fixture store
# --------------------------------------------------------------------------- #
def run_engine(workspace: Path, *args: str) -> dict:
    cmd = [sys.executable, str(ENGINE), "--workspace-root", str(workspace), "--format", "json", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"engine failed: {proc.stderr}"
    return json.loads(proc.stdout)


@pytest.fixture()
def store(tmp_path: Path) -> Path:
    points = tmp_path / "p1.md"
    points.write_text(
        "- run had avoidable spend: whole-file dump observed. token-efficiency\n",
        encoding="utf-8",
    )
    run_engine(
        tmp_path, "--action", "record", "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", "fixture-run-1", "--review", "run with token observation",
        "--points-file", str(points),
    )
    points2 = tmp_path / "p2.md"
    points2.write_text("- unrelated improvement point\n", encoding="utf-8")
    run_engine(
        tmp_path, "--action", "record", "--unit-id", "/speckit.tasks", "--unit-type", "command",
        "--run-id", "fixture-run-2", "--review", "clean run",
        "--points-file", str(points2),
    )
    return tmp_path


def test_cm2_contains_filters_to_marked_entries(store):
    out = run_engine(store, "--action", "list", "--contains", "token-efficiency", "--limit", "10")
    assert out["count"] == 1
    assert out["matches"][0]["unit_id"] == "/speckit.plan"


def test_cm2_contains_case_insensitive(store):
    out = run_engine(store, "--action", "list", "--contains", "Token-Efficiency", "--limit", "10")
    assert out["count"] == 1


def test_cm2_contains_combines_and_with_unit_filter(store):
    out = run_engine(
        store, "--action", "list", "--contains", "token-efficiency",
        "--unit-id", "/speckit.tasks", "--limit", "10",
    )
    assert out["count"] == 0, "--contains must AND with --unit-id"


def test_cm2_no_match_returns_empty_exit_zero(store):
    out = run_engine(store, "--action", "list", "--contains", "no-such-marker-anywhere")
    assert out["count"] == 0 and out["matches"] == []


def test_cm2_output_stays_summary_level(store):
    out = run_engine(store, "--action", "list", "--contains", "token-efficiency", "--limit", "10")
    entry = out["matches"][0]
    assert "summary" in entry and "path" in entry
    assert "body" not in entry and "points" not in entry, "list output must stay summary-level"


def test_cm2_omitting_contains_keeps_existing_behavior(store):
    out = run_engine(store, "--action", "list", "--limit", "10")
    assert out["count"] == 2


def test_cm3_limit_zero_returns_all_marked(store):
    out = run_engine(store, "--action", "list", "--contains", "token-efficiency", "--limit", "0")
    assert out["count"] == 1 and len(out["matches"]) == 1
