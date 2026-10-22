"""Contract tests for loop-state.py (Feature 065 / Slice 065a).

One test cluster per contract clause of
`.specify/specs/065a-state-awareness/contracts/loop-state-cli.md`
(C-1..C-18, aliases LS-01..LS-18) and, from T008 on,
`contracts/snapshot-envelope.md` (C-19..C-32),
`contracts/stage-artifact-map.md` (C-50..C-60).

Red-first per tasks.md T003/T008: each batch lands before the code it
asserts; `notes/red-first-evidence.md` records the red runs.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

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
    # C-3 pins the *semantics* of each rung, not one spelling of the keyword:
    # rung 0 = evaluation succeeded (either "success" or "succeeded" is valid),
    # rung 1 = rejected/validation failed, rung 2 = argument error.
    for code, keywords in (
        ("0", ("success", "succeeded")),
        ("1", ("rejected", "refused")),
        ("2", ("argument", "usage")),
    ):
        assert re_ladder(ladder, code, keywords), (
            f"--help ladder line for {code} ({keywords}) missing"
        )
    assert "DATA" in text and "10-16" in text, (
        "--help must state watcher verdict codes are data (never reused)"
    )


def re_ladder(ladder_text, code, keywords):
    if isinstance(keywords, str):
        keywords = (keywords,)
    for line in ladder_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(code) and any(k in line for k in keywords):
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


# ---------------------------------------------------------------------------
# T008 / C-11..C-13: --probe acceptance, refusals and local-evidence isolation
# ---------------------------------------------------------------------------

def _probe_minimal_a():
    """Shape (a): a snapshot envelope with watch_verdict + evidence."""
    return {
        "schema_version": 1,
        "line_id": "demo-line",
        "watch_verdict": {
            "present": False, "status": "na", "value_state": "na",
            "verdict": None, "reason": None, "exit_code": None,
            "attribution": None, "detail": None,
        },
        "evidence": {
            "evidence_source": "probe",
            "pid": {"status": "missing", "value_state": "na", "path": None},
            "status": {"status": "missing", "value_state": "na", "path": None},
            "log": {"status": "missing", "value_state": "na", "path": None},
            "heartbeat": {"status": "missing", "value_state": "na", "path": None},
            "watchbeat": {"status": "missing", "value_state": "na", "path": None},
            "hook": {"status": "na", "value_state": "na", "path": None,
                     "observed_at": None},
            "artifacts": {"status": "missing", "value_state": "na",
                          "stage": None, "complete": None,
                          "commit_required": None, "no_change_allowed": None,
                          "items": []},
            "commits": {"status": "missing", "value_state": "na", "base": None,
                        "pathspec": [], "commits": [], "touching": None},
        },
    }


def _probe_snapshot_run(tmp_path, payload, name="probe.json"):
    probe = tmp_path / name
    probe.write_text(json.dumps(payload), encoding="utf-8")
    return probe, _run(["--action", "snapshot", "--line-id", "demo-line",
                        "--probe", str(probe)])


def test_probe_shapes_a_and_b_are_accepted(tmp_path):
    probe, proc = _probe_snapshot_run(tmp_path, _probe_minimal_a())
    assert proc.returncode == 0, proc.stderr
    envelope = json.loads(proc.stdout)
    assert envelope["evidence"]["evidence_source"] == "probe"
    assert envelope["paths"]["probe"] == str(probe)

    _, proc = _probe_snapshot_run(
        tmp_path, {"schema_version": 1, "reachable": False, "reason": "ssh-255"},
        name="probe-b.json")
    assert proc.returncode == 0, proc.stderr
    envelope = json.loads(proc.stdout)
    assert envelope["loop_state"] == "STALLED"
    assert envelope["loop_state_reason"] == "remote-unreachable"
    assert envelope["recovery_action"] == "stop"


@pytest.mark.parametrize("payload,label", [
    ("{not json", "unparseable"),
    ({"schema_version": 2, "watch_verdict": {}, "evidence": {}}, "wrong-schema"),
    ({"schema_version": 1, "reachable": True, "reason": "x"}, "reachable-true"),
    ({"schema_version": 1, "watch_verdict": {}, "evidence": {}, "line_id": "other"},
     "line-mismatch"),
])
def test_probe_rejections_exit_2(tmp_path, payload, label):
    probe = tmp_path / ("probe-%s.json" % label)
    probe.write_text(payload if isinstance(payload, str) else json.dumps(payload),
                     encoding="utf-8")
    proc = _run(["--action", "snapshot", "--line-id", "demo-line",
                 "--probe", str(probe)])
    assert proc.returncode == 2, f"{label}: expected exit 2, got {proc.returncode}"

    missing = _run(["--action", "snapshot", "--line-id", "demo-line",
                    "--probe", str(tmp_path / "nope.json")])
    assert missing.returncode == 2, "an unreadable --probe file is exit 2"


@pytest.mark.parametrize("flag", [
    "--spine", "--state-dir", "--spec-dir", "--repo", "--watch-script",
])
def test_probe_is_mutually_exclusive_with_local_paths(tmp_path, flag):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    probe = tmp_path / "probe.json"
    probe.write_text(json.dumps(_probe_minimal_a()), encoding="utf-8")
    targets = {
        "--spine": str(spine), "--state-dir": str(state_dir),
        "--spec-dir": str(spec_dir), "--repo": str(spec_dir),
        "--watch-script": str(REPO_ROOT / "no-such-watch.sh"),
    }
    proc = _run(["--action", "snapshot", "--line-id", "demo-line",
                 "--probe", str(probe), flag, targets[flag]])
    assert proc.returncode == 2, (
        f"{flag} together with --probe must exit 2 (mutual exclusion)"
    )


def test_probe_does_not_read_local_evidence(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    state_dir.joinpath("log-demo-line-plan.log").write_text(
        "TASKS-DONE\n", encoding="utf-8")  # local completion evidence
    probe = tmp_path / "probe.json"
    probe.write_text(json.dumps({"schema_version": 1, "reachable": False,
                                 "reason": "ssh-255"}), encoding="utf-8")
    proc = _run(["--action", "snapshot", "--line-id", "demo-line",
                 "--probe", str(probe)])
    assert proc.returncode == 0, proc.stderr
    envelope = json.loads(proc.stdout)
    assert envelope["loop_state"] == "STALLED", (
        "local completion evidence must never be mixed into probe evaluation"
    )
    assert envelope["evidence"]["log"]["status"] == "missing"


# ---------------------------------------------------------------------------
# T008 / C-4/C-6: required-input vs evidence-source matrix
# ---------------------------------------------------------------------------

def test_missing_line_id_exits_2():
    proc = _run(["--action", "snapshot"])
    assert proc.returncode == 2, "--line-id is a required input (exit 2)"


def test_unreadable_evidence_sources_missing_but_exit_0(tmp_path):
    state_dir = tmp_path / "state" / "demo-line"
    state_dir.mkdir(parents=True)
    state_dir.joinpath("log-demo-line-plan.log").write_text(
        "TASKS-DONE\n", encoding="utf-8")  # dispatch evidence, spine absent
    proc = _run([
        "--action", "snapshot", "--line-id", "demo-line", "--stage", "plan",
        "--spine", str(tmp_path),            # a directory: unreadable as a file
        "--state-dir", str(state_dir),
        "--spec-dir", str(tmp_path / "no-spec"),
        "--repo", str(tmp_path / "no-repo"),
    ])
    assert proc.returncode == 0, proc.stderr
    envelope = json.loads(proc.stdout)
    assert envelope["spine"]["status"] == "missing"
    assert envelope["registry"]["status"] == "missing"
    assert envelope["loop_state"] == "UNKNOWN"
    assert envelope["recovery_action"] == "stop"


# ---------------------------------------------------------------------------
# T008 / C-17: --self-test output contract
# ---------------------------------------------------------------------------

def test_self_test_output_contract():
    proc = _run(["--self-test"])
    assert proc.returncode in (0, 1), proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines, "--self-test produced no output"
    summary = re.match(r"^SELF-TEST: (\d+) passed, (\d+) failed$", lines[-1])
    assert summary, f"last line must be the summary, got: {lines[-1]!r}"
    passed, failed = int(summary.group(1)), int(summary.group(2))
    assert passed + failed > 0
    for line in lines[:-1]:
        assert line.startswith("ok ") or re.match(r"^FAIL .+ — .+$", line), (
            f"per-case line must be 'ok <case>' or 'FAIL <case> — <detail>': {line!r}"
        )
    assert proc.returncode == (0 if failed == 0 else 1), (
        "exit 0 when all cases pass, 1 when any fails"
    )


# ---------------------------------------------------------------------------
# T008 / C-32: determinism (only evaluated_at may diff)
# ---------------------------------------------------------------------------

def test_two_runs_differ_only_in_evaluated_at(tmp_path):
    state_dir, spec_dir, spine = _make_fixture(tmp_path)
    args = _snapshot_args(state_dir, spec_dir, spine)
    first = _run(args)
    second = _run(args)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    left = json.loads(first.stdout)
    right = json.loads(second.stdout)
    assert left["evaluated_at"].endswith("Z")
    assert {k: v for k, v in left.items() if k != "evaluated_at"} == {
        k: v for k, v in right.items() if k != "evaluated_at"}
    assert "age_seconds" not in first.stdout, (
        "age-like derived numbers are forbidden (only raw at/mtime_ns)"
    )


# ---------------------------------------------------------------------------
# T008 / C-50 (AM-01): STAGE_ARTIFACTS vs reference §Stage Artifact Map
# ---------------------------------------------------------------------------

STAGES = ["requirements", "clarify", "plan", "tasks", "checklist", "analyze",
          "implement", "review"]
STATES = ("RUNNING|DONE|INCOMPLETE|ANOMALY|FAILED|DEAD|TIMEOUT|NO_SIGNAL|"
          "STALLED|REENTRY_REQUIRED|UNKNOWN")


def _load_engine_module():
    assert SCRIPT.exists(), "loop-state.py missing (T004)"
    spec = importlib.util.spec_from_file_location("loop_state_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["loop_state_contract"] = module
    spec.loader.exec_module(module)
    return module


def _section(text, heading):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("#") and heading in line:
            start = index + 1
            break
    assert start is not None, f"section {heading!r} missing"
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def _table_rows(body):
    rows = []
    for line in body:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def _backticked(cell):
    return re.findall(r"`([^`]+)`", cell)


def _as_bool(cell):
    value = cell.strip().strip("`").lower()
    if value in ("true", "yes", "是"):
        return True
    if value in ("false", "no", "否"):
        return False
    raise AssertionError(f"not a boolean cell: {cell!r}")


def test_stage_artifacts_match_reference_five_dimensions():
    module = _load_engine_module()
    table = getattr(module, "STAGE_ARTIFACTS", None)
    assert isinstance(table, dict), (
        "STAGE_ARTIFACTS is the runtime owner of the stage artifact map (T011)"
    )
    assert sorted(table) == sorted(STAGES), (
        f"STAGE_ARTIFACTS must cover the eight stages, got {sorted(table)}"
    )

    assert REF.exists(), "references/state-awareness.md missing (T018)"
    rows = _table_rows(_section(REF.read_text(encoding="utf-8"),
                                "Stage Artifact Map"))
    assert rows, "§Stage Artifact Map must contain the mirror table"
    reference = {}
    for cells in rows[1:]:
        name = (_backticked(cells[0]) or [cells[0].strip()])[0]
        if name not in STAGES:
            continue
        reference[name] = {
            "artifacts": sorted(_backticked(cells[1])),
            "owned_paths": sorted(_backticked(cells[2])),
            "commit_required": _as_bool(cells[3]),
            "no_change_allowed": _as_bool(cells[4]),
        }
    assert sorted(reference) == sorted(STAGES), (
        f"reference table must cover the eight stages, got {sorted(reference)}"
    )

    for stage in STAGES:
        entry = table[stage]
        assert sorted(entry["artifacts"]) == reference[stage]["artifacts"], stage
        assert sorted(entry["owned_paths"]) == reference[stage]["owned_paths"], stage
        assert entry["commit_required"] is reference[stage]["commit_required"], stage
        assert entry["no_change_allowed"] is reference[stage]["no_change_allowed"], stage


# ---------------------------------------------------------------------------
# T008: script derived table == reference §Derived Mapping == FR-004 table
# ---------------------------------------------------------------------------

def _clause_states():
    """FR-004 is the owner: derive the expected (order -> states) from it."""
    text = SLICE_REQ.read_text(encoding="utf-8")
    line = next(l for l in text.splitlines() if l.startswith("- **FR-004**"))
    marks = [(m.start(), int(m.group(1)))
             for m in re.finditer(r"\((\d+)\)", line)]
    assert [num for _pos, num in marks] == list(range(1, 9)), (
        "FR-004 must carry its eight numbered priority clauses"
    )
    clauses = {}
    for index, (pos, number) in enumerate(marks):
        end = marks[index + 1][0] if index + 1 < len(marks) else len(line)
        clause = line[pos:end].split("。", 1)[0]
        found = re.findall(r"\b(%s)\b" % STATES, clause)
        clauses[number] = [s for i, s in enumerate(found)
                           if i == 0 or found[i - 1] != s]
    return clauses


def _group(rows):
    grouped = {}
    for order, state in rows:
        grouped.setdefault(order, []).append(state)
    return grouped


def test_derived_mapping_is_three_way_identical():
    expected = _clause_states()

    module = _load_engine_module()
    script_rows = getattr(module, "DERIVED_MAPPING", None)
    assert isinstance(script_rows, list) and script_rows, (
        "loop-state.py must expose DERIVED_MAPPING (order, state) rows mirroring "
        "FR-004 (T013)"
    )
    script_grouped = _group(
        (row["order"], row.get("state") or row["loop_state"]) for row in script_rows)
    assert script_grouped == expected, (
        "script derived table must mirror FR-004 clause by clause"
    )

    assert REF.exists(), "references/state-awareness.md missing (T018)"
    rows = _table_rows(_section(REF.read_text(encoding="utf-8"), "Derived Mapping"))
    assert rows, "§Derived Mapping must contain the mirror table"
    reference_grouped = {}
    for cells in rows[1:]:
        match = re.match(r"^(\d+)$", (_backticked(cells[0]) or [cells[0].strip()])[0])
        if not match:
            continue
        order = int(match.group(1))
        found = re.findall(r"\b(%s)\b" % STATES, " | ".join(cells[1:]))
        deduped = [s for i, s in enumerate(found) if i == 0 or found[i - 1] != s]
        reference_grouped[order] = deduped
    assert reference_grouped == expected, (
        "reference §Derived Mapping must mirror FR-004 clause by clause"
    )


# ---------------------------------------------------------------------------
# T021 / C-33 (LS-13) + C-43/C-44: distribution surface — SKILL.md and the
# docs page must carry the entry, the call forms and the watcher/Registry
# relationship, with values that agree with `--help` and the engine data.
# ---------------------------------------------------------------------------

SKILL_MD = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
DOCS_MD = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"


def _numbered_items(body):
    items = {}
    current = None
    for line in body:
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if match:
            current = int(match.group(1))
            items[current] = [match.group(2)]
        elif current is not None and line.strip():
            items[current].append(line.strip())
    return {number: " ".join(parts) for number, parts in items.items()}


def test_skill_references_state_awareness_reference():
    assert SKILL_MD.exists(), "skills/external/sdd-loop-driver/SKILL.md missing"
    body = _section(SKILL_MD.read_text(encoding="utf-8"), "References")
    hits = [line for line in body if "references/state-awareness.md" in line]
    assert hits, (
        "SKILL.md §References must carry a `references/state-awareness.md` line "
        "(T022); other references point at its sections instead of copying tables"
    )


def test_skill_hard_requirement_snapshot_is_read_only():
    body = _section(SKILL_MD.read_text(encoding="utf-8"), "Hard Requirements")
    items = _numbered_items(body)
    hits = [number for number, text in items.items() if "loop-state.py" in text]
    assert hits, (
        "a Hard Requirement must name `scripts/loop-state.py` so the read-only "
        "boundary is not only a reference note (T022)"
    )
    item = items[hits[0]]
    for literal in ("只读", "写状态脊", "杀进程"):
        assert literal in item, (
            "the loop-state Hard Requirement must state %r; snapshot is read-only "
            "and never writes the spine or kills processes" % literal
        )
    assert "MUST NOT" in item, "the hard requirement must be normative (MUST NOT)"


def test_docs_page_documents_entry_call_forms_and_relationships():
    assert DOCS_MD.exists(), "docs/reference/skills/sdd-loop-driver.md missing"
    text = DOCS_MD.read_text(encoding="utf-8")
    assert "scripts/loop-state.py" in text, "the docs page must name the entry"
    for form in ("--action snapshot", "--probe", "--self-test"):
        assert form in text, "the docs page must document the %r call form" % form
    assert "references/state-awareness.md" in text, (
        "the docs page must point at the owner reference instead of restating it"
    )
    assert "watch-target.sh" in text and "references/watch-model.md" in text, (
        "the docs page must state the relationship to the watcher and its owner"
    )
    assert "line-registry.py" in text, (
        "the docs page must state the relationship to the Line Registry"
    )


def test_docs_values_agree_with_help_and_engine_data():
    proc = _run(["--help"])
    assert proc.returncode == 0, proc.stderr
    choices = re.search(r"--action \{([^}]+)\}", proc.stdout)
    assert choices, "`--help` must publish the --action choice list"
    actions = [item.strip() for item in choices.group(1).split(",")]
    assert actions == ["snapshot", "recover", "check-spine"], actions

    docs = DOCS_MD.read_text(encoding="utf-8")
    for action in actions:
        assert action in docs, "docs must document the %r action from --help" % action

    ladder = re.findall(r"(?m)^\s{2}([12])\s\s", proc.stdout)
    assert "0" in proc.stdout.split("Exit codes:", 1)[1], "help must keep the exit ladder"
    assert "1" in ladder and "2" in ladder, ladder
    exit_line = next((line for line in docs.splitlines()
                      if line.startswith("- **退出码**")), None)
    assert exit_line, "the docs page must state the exit-code boundary"
    for code in ("0", "1", "2"):
        assert code in exit_line, "the docs exit ladder must carry %r" % code

    module = _load_engine_module()
    assert getattr(module, "SCHEMA_VERSION", None) == 1
    assert "schema_version" in docs and "1" in docs, (
        "the docs page must state the schema_version=1 envelope"
    )
    assert "schema_version=1" in docs or "`schema_version`" in docs, (
        "the docs page must name the envelope schema field"
    )

