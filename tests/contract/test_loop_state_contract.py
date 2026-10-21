"""Contract tests for loop-state.py (Feature 065 / Slice 065a).

One test cluster per contract clause of
`.specify/specs/065a-state-awareness/contracts/loop-state-cli.md`
(C-1..C-18, aliases LS-01..LS-18) and, from T008 on,
`contracts/snapshot-envelope.md` (C-19..C-32),
`contracts/stage-artifact-map.md` (C-50..C-60).

Red-first per tasks.md T003/T008: each batch lands before the code it
asserts; `notes/red-first-evidence.md` records the red runs.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"
REF = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "state-awareness.md"
SLICE_REQ = REPO_ROOT / ".specify" / "specs" / "065a-state-awareness" / "requirements.md"
SLICE_PLAN = REPO_ROOT / ".specify" / "specs" / "065a-state-awareness" / "plan.md"
SLICE_RESEARCH = REPO_ROOT / ".specify" / "specs" / "065a-state-awareness" / "research.md"
PARENT_REQ = REPO_ROOT / ".specify" / "specs" / "065-loop-interruption-recovery" / "requirements.md"

ALL_PARAMS = [
    "--line-id", "--stage", "--state-dir", "--spec-dir", "--repo", "--spine",
    "--probe", "--watch-script", "--out", "--start-grace", "--deadline-grace",
    "--heartbeat-max-age", "--retry-limit",
]

REQUIRED_TOP_LEVEL = [
    "schema_version", "line_id", "run_id", "stage", "loop_state", "verdict_source",
    "loop_state_reason", "watch_verdict", "recovery_action", "recovery_reason",
    "recovery_decision", "false_completion", "spine", "registry", "paths",
    "thresholds", "evidence", "interruptions", "missing_artifacts",
    "uncommitted_artifacts", "stale_signals", "evaluated_at",
]


def _run(args, cwd=None, timeout=120):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, timeout=timeout, cwd=cwd,
    )


def _run_json(args, cwd=None):
    proc = _run(args, cwd=cwd)
    assert proc.returncode == 0, f"snapshot failed: rc={proc.returncode}\n{proc.stderr}"
    return json.loads(proc.stdout)


def _write_spine(path: Path, state: str = "running", attempt: int = 1) -> None:
    path.write_text(
        "# Loop State Spine — demo-line\n\n"
        "<!-- loop-state:begin -->\n"
        "spine_schema: v1\n"
        f"spine_state: {state}\n"
        "stage_started_at: 1790000000\n"
        "stage_deadline_epoch: 1790005400\n"
        "stage_base_commit: abc1234\n"
        f"attempt: {attempt}\n"
        "retry_limit: 2\n"
        "<!-- loop-state:end -->\n",
        encoding="utf-8",
    )


def _make_fixture(tmp_path: Path, *, with_spine: bool = True):
    state_dir = tmp_path / "state" / "demo-line"
    state_dir.mkdir(parents=True)
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir()
    spine = state_dir / "spine.md"
    if with_spine:
        _write_spine(spine)
    return state_dir, spec_dir, spine


def _snapshot_args(state_dir, spec_dir, spine, line="demo-line", stage="plan"):
    return [
        "--action", "snapshot", "--line-id", line, "--state-dir", str(state_dir),
        "--spec-dir", str(spec_dir), "--repo", str(spec_dir), "--spine", str(spine),
        "--stage", stage, "--watch-script", str(REPO_ROOT / "no-such-watch.sh"),
    ]


# ---------------------------------------------------------------------------
# C-3 (LS-03): --help ladder + watcher-codes-as-data + full parameter face
# ---------------------------------------------------------------------------

def test_help_lists_actions_params_exit_ladder_and_watcher_data_note():
    assert SCRIPT.exists(), "loop-state.py missing (T004 not implemented)"
    proc = _run(["--help"])
    assert proc.returncode == 0
    text = proc.stdout
    for action in ("snapshot", "recover", "check-spine", "--self-test"):
        assert action in text, f"--help missing action {action}"
    for param in ALL_PARAMS:
        assert param in text, f"--help missing parameter {param}"
    assert "Exit codes:" in text, "--help missing exit-code ladder"
    ladder = text.split("Exit codes:", 1)[1]
    for code, keyword in (("0", "success"), ("1", "rejected"), ("2", "argument")):
        assert re_ladder(ladder, code, keyword), (
            f"--help ladder line for {code} ({keyword}) missing"
        )
    assert "DATA" in text and "10-16" in text, (
        "--help must state watcher verdict codes are data (never reused)"
    )


def re_ladder(ladder_text, code, keyword):
    for line in ladder_text.splitlines():
        if line.strip().startswith(code) and keyword in line:
            return True
    return False


# ---------------------------------------------------------------------------
# C-2 (LS-02): recover / check-spine structured refusal, per-action owner
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("action,owner", [("recover", "065c"), ("check-spine", "065b")])
def test_not_implemented_action_refusal_envelope(action, owner, tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    proc = _run(["--action", action, "--line-id", "demo-line",
                 "--state-dir", str(state_dir), "--spec-dir", str(spec_dir)])
    assert proc.returncode == 1, f"{action} refusal must exit 1, got {proc.returncode}"
    envelope = json.loads(proc.stdout)
    assert envelope["schema_version"] == 1
    assert envelope["action"] == action
    assert envelope["applied"] is False
    assert envelope["result"] == "failed"
    assert envelope["reason"] == "not-implemented-in-065a"
    assert envelope["owner"] == owner, f"{action} must declare owner={owner}"
    assert isinstance(envelope.get("steps"), list) and envelope["steps"] == []
    assert envelope.get("message"), "refusal envelope needs a user-readable message"


# ---------------------------------------------------------------------------
# C-20 (SN-02): top-level required fields + decision/top-level consistency
# ---------------------------------------------------------------------------

def test_snapshot_envelope_required_fields_and_decision_consistency(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    envelope = _run_json(_snapshot_args(state_dir, spec_dir, spine))
    for field in REQUIRED_TOP_LEVEL:
        assert field in envelope, f"top-level field missing: {field}"
    assert envelope["schema_version"] == 1
    decision = envelope["recovery_decision"]
    for key in ("action", "reason", "preconditions", "blocked_by"):
        assert key in decision, f"recovery_decision missing {key}"
    assert decision["action"] == envelope["recovery_action"]
    assert decision["reason"] == envelope["recovery_reason"]
    assert isinstance(decision["preconditions"], list)
    assert isinstance(decision["blocked_by"], list)


# ---------------------------------------------------------------------------
# C-20/C-23/C-39 (SN-02/SN-05/IA-07): nested spine.consistent, no flat alias
# ---------------------------------------------------------------------------

def test_spine_consistency_nested_only(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    envelope = _run_json(_snapshot_args(state_dir, spec_dir, spine))
    assert "consistent" in envelope["spine"], "spine.consistent must exist"
    assert "spine_consistent" not in envelope, (
        "flat top-level spine_consistent alias is forbidden"
    )


# ---------------------------------------------------------------------------
# C-10 (LS-10): --out atomic write + realpath boundary (state_dir / repo)
# ---------------------------------------------------------------------------

def test_out_side_effects_and_boundary(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    args = _snapshot_args(state_dir, spec_dir, spine)

    # baseline: --out outside both trees writes a file whose bytes == stdout
    out_ok = tmp_path / "outside" / "snap.json"
    out_ok.parent.mkdir()
    proc = _run(args + ["--out", str(out_ok)])
    assert proc.returncode == 0
    assert out_ok.read_text(encoding="utf-8") == proc.stdout, "--out content must equal stdout"

    # 1. target inside state_dir -> exit 2, no file
    bad1 = state_dir / "snap.json"
    proc = _run(args + ["--out", str(bad1)])
    assert proc.returncode == 2
    assert not bad1.exists()

    # 2. target inside repo -> exit 2, no file
    bad2 = spec_dir / "snap.json"
    proc = _run(args + ["--out", str(bad2)])
    assert proc.returncode == 2
    assert not bad2.exists()

    # 3. relative path resolved against cwd inside state_dir -> exit 2
    proc = _run(args + ["--out", "relative.json"], cwd=str(state_dir))
    assert proc.returncode == 2
    assert not (state_dir / "relative.json").exists()

    # 4. symlink outside pointing INTO state_dir -> exit 2, no leftover
    link = tmp_path / "link-into-state.json"
    os.symlink(state_dir / "evil.json", link)
    proc = _run(args + ["--out", str(link)])
    assert proc.returncode == 2
    assert not (state_dir / "evil.json").exists()
    assert not link.exists() or link.is_symlink()  # never materialized through the link

    # 5. no temp-file residue anywhere in state_dir / spec_dir
    leftovers = [p.name for p in list(state_dir.iterdir()) + list(spec_dir.iterdir())
                 if p.name.startswith((".", "tmp")) and p.name != "spine.md"]
    assert leftovers == [], f"temp-file residue: {leftovers}"


# ---------------------------------------------------------------------------
# C-10 / SA-4: snapshot is read-only — mtime audit over evidence trees
# ---------------------------------------------------------------------------

def test_snapshot_readonly_mtime_audit(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    state_dir.joinpath("pid-demo-line-plan").write_text(
        "pid=99999 start=123456 at=1790000001 line=demo-line stage=plan event=pid\n",
        encoding="utf-8",
    )
    log = state_dir / "log-demo-line-plan.log"
    log.write_text("working\n", encoding="utf-8")

    def mtimes():
        snap = {}
        for root in (state_dir, spec_dir):
            for base, _dirs, files in os.walk(root):
                for name in files:
                    p = Path(base) / name
                    st = p.stat()
                    snap[str(p)] = (st.st_mtime_ns, st.st_size)
        return snap

    before = mtimes()
    _run_json(_snapshot_args(state_dir, spec_dir, spine))
    after = mtimes()
    assert before == after, "snapshot must not write, touch mtimes, or create files"
    assert set(before) == set(after)


# ---------------------------------------------------------------------------
# FR-004 owner attribution: derived-mapping ownership is pinned to FR-004
# (slice requirements FR-004/FR-043, parent FR-004, research R-13, plan tree,
# references §Derived Mapping, loop-state.py). Any artifact claiming another
# owner — or claiming the reference/code owns the table — must fail here.
# ---------------------------------------------------------------------------

def test_derived_mapping_owner_is_fr004_everywhere():
    slice_text = SLICE_REQ.read_text(encoding="utf-8")
    # slice FR-004 declares itself the single owner of the derived table
    assert "本表的唯一 owner 是本条" in slice_text
    # slice FR-043 must NOT own the derived table
    assert "不在本条 owner 文档的拥有范围内" in slice_text

    parent_text = PARENT_REQ.read_text(encoding="utf-8")
    assert "唯一 owner" in parent_text and "FR-004" in parent_text, (
        "parent requirements must carry the FR-004 owner declaration"
    )

    research_text = SLICE_RESEARCH.read_text(encoding="utf-8")
    assert "FR-004" in research_text, "research R-13 must reference FR-004 as owner"
    assert "只做镜像" in research_text or "镜像" in research_text, (
        "research must state the reference/code mirror role"
    )

    plan_text = SLICE_PLAN.read_text(encoding="utf-8")
    assert "FR-004" in plan_text, "plan structure tree must point the mirror at FR-004"

    # owner reference: §Derived Mapping mirrors FR-004, never owns it
    assert REF.exists(), "references/state-awareness.md missing (T018)"
    ref_text = REF.read_text(encoding="utf-8")
    assert "## Derived Mapping" in ref_text or "## Derived Mapping（" in ref_text
    assert "FR-004" in ref_text, "reference must name FR-004 as the owner"
    assert "唯一 owner" in ref_text or "owner 为" in ref_text or "owner:" in ref_text

    # engine: mirrors the table, cites FR-004, never claims self-ownership
    assert SCRIPT.exists(), "loop-state.py missing (T004)"
    engine_text = SCRIPT.read_text(encoding="utf-8")
    assert "FR-004" in engine_text, "engine must cite FR-004 as the mapping owner"
