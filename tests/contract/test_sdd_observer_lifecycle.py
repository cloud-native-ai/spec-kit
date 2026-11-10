"""Contract tests for the observer lifecycle (Feature 096, wp03 T024).

Contracts: `contracts/observer-lifecycle.contract.md` C-01…C-12, the driver-side faces of
`contracts/observer-role.contract.md` C-09/C-10, and `contracts/observer-verification.contract.md`
C-03 (the two non-blocking fixtures and the doctored-gate red leg). The record-section shape is
owned by `SKILL.md` § SDD Observer; this module asserts the owner carries every lifecycle
obligation, that both failure fixtures reach the terminal stage without any stage verdict
depending on the observer, that the structural non-blocking predicate has teeth, and that the
digest field set still equals its frozen baseline. T032 extends this module with the US4
driver/digest-side boundary assertions.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_MD = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
REFERENCE = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "observer-lifecycle.md"
PROMPTS_MD = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "stage-prompts.md"
DIGEST = REPO_ROOT / "scripts" / "python" / "status-digest.py"
BASELINE = (REPO_ROOT / ".specify" / "specs" / "096-sdd-observer-agent"
            / "test-evidence" / "digest-fieldset-baseline.txt")
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "sdd-observer"

SECTION_TITLE = "## SDD Observer（观察者：启动、记录节与收束）"
RECORD_KEYS = ["state", "line_id", "run_id", "spec", "instance", "execution_label",
               "started_at", "reason"]

#: A line expressing "the observer gates the line" — subject + object + gate verb. The doctored
#: red leg below proves this predicate turns red when such a sentence enters the driver text.
GATE_SUBJECT = re.compile(r"observer|观察者", re.IGNORECASE)
GATE_OBJECT = re.compile(
    r"stage advance|stage gate|U4|checkpoint|review|merge|"
    r"阶段推进|阶段门|检查点|审查|合并", re.IGNORECASE)
GATE_VERB = re.compile(
    r"\bgate(s|d)?\b|\bblock(s|ed)?\b|\brequire(s|d)?\b|liveness|must wait|wait for|"
    r"depends? on|门前置|前置条件|阻塞|等待|依赖|门控|存活|门", re.IGNORECASE)
GATE_NEGATION = re.compile(
    r"MUST NOT|must not|never|不得|禁止|不成为|不构成|不改变|不影响|不阻塞|披露", re.IGNORECASE)


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def failure_builder():
    return _module("sdd_observer_failure_builder", FIXTURES / "failure_builder.py")


def line_builder():
    return _module("sdd_observer_line_builder_lifecycle", FIXTURES / "line_builder.py")


def observer_section() -> str:
    text = SKILL_MD.read_text(encoding="utf-8")
    start = text.find(SECTION_TITLE)
    assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
    end = text.find("\n## ", start + len(SECTION_TITLE))
    return text[start:end if end != -1 else len(text)]


def state_spine_section() -> str:
    text = PROMPTS_MD.read_text(encoding="utf-8")
    start = text.find("### 状态脊")
    assert start != -1, "stage-prompts.md lacks the § 状态脊 section"
    end = text.find("\n## ", start)
    return text[start:end if end != -1 else len(text)]


def gate_violations(text: str):
    """The structural non-blocking predicate: gating sentences not under a negation."""
    violations = []
    for line in text.splitlines():
        if not (GATE_SUBJECT.search(line) and GATE_OBJECT.search(line)
                and GATE_VERB.search(line)):
            continue
        if GATE_NEGATION.search(line):
            continue
        violations.append(line.strip())
    return violations


def _record_block(section: str) -> str:
    start = section.find("## Observer Record —")
    assert start != -1, "the section carries no record-section block"
    fence_start = section.rfind("```", 0, start)
    fence_end = section.find("```", start)
    assert fence_start != -1 and fence_end != -1, "the record block is not fenced"
    return section[fence_start + 3:fence_end]


def _block_keys(block: str):
    keys = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            keys.append(stripped[2:].partition(":")[0].strip())
    return keys


# --------------------------------------------------------------------------- #
# C-01 / C-03 — entry switch and recorded startup outcome
# --------------------------------------------------------------------------- #

def test_entry_switch_and_disabled_state():
    section = observer_section()
    assert "observer: on|off" in section, "the entry switch key is absent"
    assert "缺省 `on`" in section, "the default value `on` is not declared"
    assert "state: disabled" in section, "`off` is not recorded as state: disabled"
    assert "U6 收束报告" in section, "`off` is not disclosed in the U6 close-out report"
    assert "静默缺失" in section, "the never-a-silent-absence rule is absent"
    assert "started` / `failed` / `disabled`" in section, (
        "the startup outcome set is not declared"
    )


# --------------------------------------------------------------------------- #
# C-02 — startup point is the driver's and mechanically decidable
# --------------------------------------------------------------------------- #

def test_startup_point_is_driver_owned_and_decidable():
    section = observer_section()
    assert "line 已登记" in section, "the line-registration precondition is absent"
    assert "状态脊已建立" in section, "the spine precondition is absent"
    assert "U2 派发之前" in section, "the before-first-U2 boundary is absent"
    assert "机械判据" in section, "the mechanical criterion is not named"
    assert "MUST NOT 下放到任一 stage 命令内部" in section, (
        "the startup step is not reserved to the driver"
    )


# --------------------------------------------------------------------------- #
# C-04 — the record section shape is owned here
# --------------------------------------------------------------------------- #

def test_record_section_shape_is_owned_by_the_section():
    section = observer_section()
    keys = _block_keys(_record_block(section))
    assert keys == RECORD_KEYS, (
        "the owned record-section key set/order must be %r, got %r" % (RECORD_KEYS, keys)
    )
    assert "追加式" in section and "latest wins" in section, (
        "the append-only / latest-wins reading rule is absent"
    )
    assert "observer 自身 MUST NOT 写状态脊" in section, (
        "the observer's spine-write ban is absent"
    )


def test_fixture_record_matches_the_owned_shape(tmp_path):
    fixture = failure_builder().build_start_failure(tmp_path / "line")
    records = fixture["observer_records"]
    assert records, "the fixture spine carries no observer record"
    assert [key for key in records[-1] if key != "heading"] == RECORD_KEYS, (
        "the fixture record keys drift from the owner shape"
    )


# --------------------------------------------------------------------------- #
# C-05 / role C-09 — one dedicated instance, identity and creation duty
# --------------------------------------------------------------------------- #

def test_instance_identity_and_creation_duty():
    section = observer_section()
    assert "sdd-observer-<line_id>" in section, "the instance slug derivation is absent"
    assert "create-agent" in section, "instance creation is not delegated to create-agent"
    assert "MUST NOT 自行创建 observer 实例" in section, (
        "stage commands are not barred from creating instances"
    )
    assert "MUST NOT 注册为写线" in section, "the write-line exclusion is absent"
    assert "agent-write" in section, "the closed write-role set is not named"
    assert "MUST NOT 共享实例或 journal" in section, (
        "cross-line sharing is not forbidden"
    )


# --------------------------------------------------------------------------- #
# role C-10 — execution carrier and visibility
# --------------------------------------------------------------------------- #

def test_execution_carrier_is_external_only():
    section = observer_section()
    for token in ("run-agent", "fork", "stage-runner.sh", "subprocess"):
        assert token in section, "the carrier declaration lacks %r" % token
    assert "native" in section and "virtual" in section and "MUST NOT 承载" in section, (
        "native/virtual are not banned as carriers"
    )
    assert "`--sub-flow <label>=<triplet-dir>`" in section, (
        "visibility does not ride the existing supervision projection"
    )
    assert "三段约定" in section, "the three-segment label convention is absent"


# --------------------------------------------------------------------------- #
# C-06 / C-07 — bounded window, single live execution, restart at boundaries
# --------------------------------------------------------------------------- #

def test_bounded_execution_and_restart():
    section = observer_section()
    assert "至多一个未结算执行" in section, "the single-live-execution bound is absent"
    assert "flock" in section, "the single-writer protocol is absent"
    assert "阶段边界" in section, "the restart boundary is absent"
    assert "同一实例" in section, "the restart-from-same-instance rule is absent"
    assert "observer-gap" in section, "the restart gap row is absent"
    for token in ("重试次数", "超时判定", "完成哨兵判定"):
        assert token in section, "the restart non-change rule lacks %r" % token
    assert "MUST NOT 改变" in section, "the non-change rule is not normative"


# --------------------------------------------------------------------------- #
# C-08 — line-terminal close
# --------------------------------------------------------------------------- #

def test_terminal_close():
    section = observer_section()
    for token in ("--final", "line-terminal", "observer-settle", "observer-gap",
                  "state: closed"):
        assert token in section, "the terminal-close duty lacks %r" % token
    assert "state: failed" in section and "原因" in section, (
        "the failed-close record shape is absent"
    )
    assert "MUST NOT 被改写" in section, "the journal-is-never-rewritten rule is absent"
    assert "未闭合窗口" in section, "the named unclosed window is absent"


# --------------------------------------------------------------------------- #
# C-09 — non-blocking predicate and its doctored red leg
# --------------------------------------------------------------------------- #

def test_non_blocking_predicate_holds_on_the_driver_text():
    section = observer_section()
    assert "MUST NOT 成为任何阶段推进" in section, (
        "the non-blocking duty is not stated as a prohibition"
    )
    assert "披露是唯一的收束义务" in section or "唯一的收束义务" in section, (
        "disclosure is not declared the only close-out duty"
    )
    assert gate_violations(section) == [], (
        "the driver text states an observer gate: %r" % gate_violations(section)
    )


def test_doctored_gate_turns_the_predicate_red():
    section = observer_section()
    english = section + "\nStage advance requires observer liveness before U4.\n"
    chinese = section + "\n阶段推进（U4）以 observer 存活为前置条件。\n"
    assert gate_violations(english), "the predicate missed a doctored English stage gate"
    assert gate_violations(chinese), "the predicate missed a doctored Chinese stage gate"


# --------------------------------------------------------------------------- #
# C-10 — scope
# --------------------------------------------------------------------------- #

def test_scope_of_the_mechanism():
    section = observer_section()
    assert "嵌套运行" in section, "nested runs are not scoped in"
    assert "MUST NOT 观察外层团队运行" in section, "the inner/outer separation is absent"
    assert "非 SDD" in section and "MUST NOT 产生 observer 或 journal" in section, (
        "non-SDD runs are not scoped out"
    )


# --------------------------------------------------------------------------- #
# C-11 — the dispatch brief reference
# --------------------------------------------------------------------------- #

def test_dispatch_brief_reference_carries_its_obligations():
    assert REFERENCE.is_file(), "missing reference: %s" % REFERENCE
    text = REFERENCE.read_text(encoding="utf-8")
    for token in ("Assignment", "fast-fail", "Concurrency obligation", "Read domain",
                  "Write surface", "Forbidden", "未发现异常", "ANOMALY:"):
        assert token in text, "the dispatch brief lacks %r" % token
    assert "subagent-definitions.md" in text, "the concurrency-obligation pointer is absent"
    assert "effective-concurrency.yaml" in text, "the reading fields pointer is absent"
    assert "sdd-loop-driver" not in text, "the brief references the driver skill"
    for loop_token in ("U0", "U1", "U2", "U3", "U4", "U5"):
        assert loop_token not in text, (
            "the reference carries loop logic (%r)" % loop_token
        )


# --------------------------------------------------------------------------- #
# C-12 — the stage-prompts pointer, no key copy
# --------------------------------------------------------------------------- #

def test_stage_prompts_pointer_is_a_single_pointer():
    section = state_spine_section()
    pointer_lines = [line for line in section.splitlines() if "§ SDD Observer" in line]
    assert len(pointer_lines) == 1, (
        "§ 状态脊 must carry exactly one pointer line, got %d" % len(pointer_lines)
    )
    assert "SKILL.md" in pointer_lines[0], "the pointer does not name the owner file"
    for line in section.splitlines():
        assert not re.match(
            r"^- (state|line_id|run_id|spec|instance|execution_label|started_at|reason):",
            line.strip()), "§ 状态脊 copies record keys: %r" % line


# --------------------------------------------------------------------------- #
# SC-006 — digest field-set baseline comparison
# --------------------------------------------------------------------------- #

def _baseline_fields():
    top, rows, current = [], [], None
    for line in BASELINE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        if line.strip() and current == "top-level":
            top.append(line.strip())
        elif line.strip() and current and current.startswith("all_entries"):
            rows.append(line.strip())
    return sorted(top), sorted(rows)


def test_digest_field_set_matches_the_frozen_baseline():
    baseline_top, baseline_rows = _baseline_fields()
    assert baseline_top, "the frozen digest baseline carries no top-level keys"
    result = subprocess.run(
        [sys.executable, str(DIGEST), "--action", "digest", "--format", "json",
         "--workspace", "."],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, "status-digest failed: %s" % result.stderr[-800:]
    payload = json.loads(result.stdout)
    assert sorted(payload) == baseline_top, (
        "digest top-level field set drifted from the frozen baseline"
    )
    entries = payload.get("all_entries") or []
    if entries:
        current_rows = sorted({key for row in entries for key in row})
        assert current_rows == baseline_rows, (
            "digest row-key set drifted from the frozen baseline"
        )


# --------------------------------------------------------------------------- #
# SC-003 / C-03 — the two failure fixtures reach their terminal stage
# --------------------------------------------------------------------------- #

def _stage_verdict_files(fixture):
    """The declared stages' verdict carriers plus checkpoints — never the observer's own envelope."""
    state_dir, spec_dir = fixture["state_dir"], fixture["spec_dir"]
    files = []
    for stage in fixture["stages"]:
        files.append(state_dir / ("log-%s-%s.log" % (fixture["line_id"], stage)))
        files.append(state_dir / ("status-%s-%s" % (fixture["line_id"], stage)))
        files.append(state_dir / ("pid-%s-%s" % (fixture["line_id"], stage)))
        files.append(state_dir / ("heartbeat-%s-%s.log" % (fixture["line_id"], stage)))
    files.extend(sorted((spec_dir / "checkpoints").glob("*.md")))
    return files


def test_start_failure_fixture_reaches_the_terminal_stage(tmp_path):
    fixture = failure_builder().build_start_failure(tmp_path / "start-failure")
    sentinel = line_builder().sentinel_for(fixture["terminal_stage"], fixture["root"])
    terminal = fixture["state_dir"] / (
        "status-%s-%s" % (fixture["line_id"], fixture["terminal_stage"]))
    text = terminal.read_text(encoding="utf-8")
    assert "exit=0" in text and "sentinel=1" in text, "the terminal stage did not settle"
    log_tail = (fixture["state_dir"] / (
        "log-%s-%s.log" % (fixture["line_id"], fixture["terminal_stage"]))).read_text(
        encoding="utf-8").strip().splitlines()[-1]
    assert log_tail == sentinel, "the terminal sentinel is absent"

    records = fixture["observer_records"]
    assert len(records) == 1 and records[0]["state"] == "failed", (
        "the start failure is not recorded as state: failed"
    )
    assert records[0]["reason"] not in ("", "-"), "the failed record carries no reason"
    assert records[0]["execution_label"] == "-", "a start failure claims an execution label"

    envelope = fixture["status_envelope"].read_text(encoding="utf-8")
    assert "state=failed" in envelope and "reason=" in envelope, (
        "the failed status envelope is incomplete"
    )
    assert "exit=" not in envelope, "the envelope must stay unsettled (no exit record)"

    for path in _stage_verdict_files(fixture):
        assert "observer" not in path.read_text(encoding="utf-8").lower(), (
            "a stage verdict carrier mentions the observer: %s" % path
        )


def test_mid_run_kill_fixture_restarts_and_reaches_terminal(tmp_path):
    fixture = failure_builder().build_mid_run_kill(tmp_path / "mid-run-kill")
    records = fixture["observer_records"]
    assert [record["state"] for record in records] == ["started", "failed", "started"], (
        "the failed/restart record sequence is absent: %r" % records
    )
    assert records[0]["execution_label"] == records[1]["execution_label"], (
        "the failure record drifted from execution A"
    )
    assert records[2]["execution_label"] == fixture["restart_label"], (
        "the restart record does not name execution B"
    )
    assert records[2]["execution_label"] != records[1]["execution_label"], (
        "the restart reused the dead execution label"
    )
    assert len({record["instance"] for record in records}) == 1, (
        "the restart did not reuse the same instance"
    )
    assert records[1]["started_at"] < records[2]["started_at"], (
        "the restart does not land after the failure at a later boundary"
    )

    envelope = fixture["status_envelope"].read_text(encoding="utf-8")
    assert "state=failed" in envelope and "exit=137" in envelope, (
        "the killed execution left no failed status envelope"
    )
    assert fixture["reason"] in envelope, "the envelope carries no one-line reason"
    for label in (fixture["execution_label"], fixture["restart_label"]):
        status = (fixture["triplet_dir"] / ("%s.status" % label)).read_text(encoding="utf-8")
        assert "state=" in status, "the triplet status for %s is missing" % label

    terminal = fixture["state_dir"] / (
        "status-%s-%s" % (fixture["line_id"], fixture["terminal_stage"]))
    terminal_text = terminal.read_text(encoding="utf-8")
    assert "exit=0" in terminal_text and "sentinel=1" in terminal_text, (
        "the killed line did not reach its terminal stage"
    )
    for path in _stage_verdict_files(fixture):
        assert "observer" not in path.read_text(encoding="utf-8").lower(), (
            "a stage verdict carrier mentions the observer: %s" % path
        )
