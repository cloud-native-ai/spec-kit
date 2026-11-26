"""Contract tests for the amended team-view program and its declaration surfaces (108, T019).

Pins `.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md`
C-101…C-109 and `contracts/view-labels.contract.md` C-401…C-408 — the clauses whose
subject is the closed reason set and exit map, the envelope shape, the single recognition
entry, the label vocabulary closure, the three-surface declarations and the containment
claims (no new third-party import, `goal-utils.py` zero modification, no shape change).
Behavioural rendering lives in `tests/integration/test_team_view_degradation.py`.

Strictly read-only: every assertion reads repository files, runs the program against a
pytest ``tmp_path`` fixture, or runs ``git show`` / ``git diff`` against the frozen
baseline commit read from the feature's implement-entry readings. FR-017, FR-019…FR-024.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.team_view_fixtures import build_team, default_frontmatter, snapshot

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"
UNIT_TEST = REPO_ROOT / "tests" / "unit" / "test_team_view_report_recognition.py"
INTEGRATION_TEST = REPO_ROOT / "tests" / "integration" / "test_team_view_degradation.py"
CONTRACT_TEST = Path(__file__).resolve()
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "commands" / "team.md"
SKILL_PAGE = REPO_ROOT / "skills" / "internal" / "view-team" / "SKILL.md"
PROGRAM_CONTRACT = "contracts/team-view-program.contract.md"
OWNER_PATH = ".specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md"
LABEL_CONTRACT = REPO_ROOT / ".specify" / "specs" / "108-team-view-degradation" / "contracts" / "view-labels.contract.md"
IMPLEMENT_READINGS = (
    REPO_ROOT / ".specify" / "specs" / "108-team-view-degradation"
    / "test-evidence" / "implement-entry-readings.txt"
)

BASELINE_COMMIT = "54c6efa8c"
REASONS = {"engine-degraded", "report-recognition-uncertain"}
EXIT_CODES = {0, 2, 3, 4, 5}
ENVELOPE_KEYS = {
    "tool", "version", "mode", "repo_root", "scope", "as_of",
    "overview", "team", "errors", "degraded",
}
INVENTORY_FIELDS = {
    "state", "reports", "shown", "omitted", "auxiliaries", "residue",
    "latest_path", "latest_token", "uncertain", "unreadable",
}
LOCAL_IMPORT_ROOTS = {"script_interface_cli", "pytest", "fixtures"}

pytestmark = pytest.mark.contract


def program_source() -> str:
    return PROGRAM.read_text(encoding="utf-8")


def load_program_module():
    spec = importlib.util.spec_from_file_location("team_view_program_contract", PROGRAM)
    module = importlib.util.module_from_spec(spec)
    sys.modules["team_view_program_contract"] = module
    spec.loader.exec_module(module)
    return module


team_view = load_program_module()


def run_program(*args):
    return subprocess.run(
        [sys.executable, str(PROGRAM), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120)


def implement_start_commit() -> str:
    text = IMPLEMENT_READINGS.read_text(encoding="utf-8")
    match = re.search(r"^implement_start_commit=([0-9a-f]{7,40})$", text, re.MULTILINE)
    assert match, "implement_start_commit= line missing from implement-entry readings"
    return match.group(1)


def clause_text(text: str, clause_id: str) -> str:
    match = re.search(
        r"\*\*%s\*\*(.*?)(?=\*\*C-\d+\*\*|\Z)" % re.escape(clause_id), text, re.S)
    assert match, "clause missing from the label contract: %s" % clause_id
    return match.group(1)


def leading_backtick_members(paragraph: str) -> list:
    members = []
    for segment in paragraph.split(" · "):
        match = re.search(r"`([^`]+)`", segment)
        if match:
            members.append(match.group(1))
    return members


def owner_label_members() -> set:
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    members = set()
    for clause in ("C-402", "C-403", "C-404"):
        members.update(leading_backtick_members(clause_text(text, clause)))
    for line in clause_text(text, "C-405").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: "):
            continue
        match = re.match(r"`([^`]+)`", cells[0])
        if match:
            members.add(match.group(1))
    return members


# --------------------------------------------------------------------------- #
# C-104 / SC-005 — closed reason set and the 2/2 exit mapping
# --------------------------------------------------------------------------- #
def test_reason_set_is_closed():
    source = program_source()
    codes = set(re.findall(r'"code":\s*"([^"]+)"', source))
    assert codes == REASONS, "emitted degradation code set drifted: %s" % sorted(codes)
    contract = (REPO_ROOT / ".specify" / "specs" / "108-team-view-degradation"
                / PROGRAM_CONTRACT).read_text(encoding="utf-8")
    for reason in REASONS:
        assert "`%s`" % reason in contract, "reason not owned by C-104: %s" % reason
    assert codes.isdisjoint({"缺失", "为空", "不可读", "未记录"}), (
        "a file-level state leaked into the degradation reason codes")
    assert tuple(team_view.APPROVED_EXIT_CODES) == (0, 2, 3, 4, 5), (
        "closed exit-code set changed: %r" % (team_view.APPROVED_EXIT_CODES,))


def test_exit_mapping_two_of_two(tmp_path):
    no_binding = default_frontmatter("no-binding")
    no_binding.pop("binding")
    build_team(tmp_path, "no-binding", frontmatter=no_binding)
    build_team(
        tmp_path,
        "residue-team",
        reports=[("2026-10-07-progress-snapshot.md", "Snapshot without a stamp.\n")],
    )
    build_team(tmp_path, "empty-history")
    build_team(tmp_path, "empty-runs")
    (tmp_path / ".specify" / "teams" / "empty-runs" / "runs").mkdir()

    observations = {}
    for slug in ("no-binding", "residue-team", "empty-history", "empty-runs"):
        result = run_program(slug, "--repo-root", str(tmp_path), "--json")
        payload = json.loads(result.stdout)
        observations[slug] = (result.returncode, [error["code"] for error in payload["errors"]])

    assert observations["no-binding"] == (5, ["engine-degraded"])
    assert observations["residue-team"] == (5, ["report-recognition-uncertain"])
    assert observations["empty-history"] == (0, [])
    assert observations["empty-runs"] == (0, [])
    assert {code for _rc, codes in observations.values() for code in codes} == REASONS
    assert all(rc in EXIT_CODES for rc, _codes in observations.values())


# --------------------------------------------------------------------------- #
# C-105 — envelope shape: ten top-level keys, nested additions only
# --------------------------------------------------------------------------- #
def test_envelope_keys_unchanged_with_nested_additions(tmp_path):
    build_team(
        tmp_path,
        "residue-team",
        reports=[
            ("2026-09-17T11-54-53Z-report.md", "# report\n"),
            ("2026-10-07-progress-snapshot.md", "Snapshot.\n"),
        ],
    )
    result = run_program("residue-team", "--repo-root", str(tmp_path), "--json")
    assert result.returncode == 5, result.stderr
    payload = json.loads(result.stdout)
    assert set(payload) == ENVELOPE_KEYS, (
        "top-level envelope keys drifted (no new key is allowed): %s" % sorted(payload))
    assert [error["code"] for error in payload["errors"]] == ["report-recognition-uncertain"]
    assert payload["degraded"] is True
    assert payload["as_of"]["latest_report_timestamp"] == "20260917T115453Z"
    assert INVENTORY_FIELDS <= set(payload["team"]["persistence"]["reports"]), (
        "the nested runs inventory is missing fields: %s"
        % sorted(INVENTORY_FIELDS - set(payload["team"]["persistence"]["reports"])))

    healthy = run_program("residue-team", "--repo-root", str(tmp_path))
    assert "report-recognition-uncertain" in healthy.stdout
    clean = run_program("--repo-root", str(tmp_path), "--json")
    clean_payload = json.loads(clean.stdout)
    assert set(clean_payload) == ENVELOPE_KEYS
    assert clean_payload["degraded"] is False
    assert clean_payload["errors"] == []
    assert clean_payload["as_of"]["latest_report_timestamp"] is None


# --------------------------------------------------------------------------- #
# C-102 — one engine, one recognition entry
# --------------------------------------------------------------------------- #
def test_single_recognition_entry_source_scan():
    source = program_source()
    assert source.count("def classify_runs(") == 1, (
        "exactly one `def classify_runs(` is allowed")
    assert source.count("STAMP_RE = re.compile(") == 1, (
        "exactly one compiled timestamp grammar is allowed")
    assert "REPORT_NAME_RE" not in source, "the narrow report-name template still exists"

    compiled = []
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "compile"):
            continue
        if node.args and isinstance(node.args[0], ast.Constant):
            value = node.args[0].value
            if isinstance(value, str) and (r"\d{8}T" in value or r"\d{4}-\d{2}-\d{2}" in value):
                compiled.append(value)
    assert len(compiled) == 1, (
        "timestamp grammars compiled in the source: %d" % len(compiled))

    tree = ast.parse(source)
    callers = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for inner in ast.walk(node):
            if (isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name)
                    and inner.func.id == "classify_runs"):
                callers.add(node.name)
    assert callers == {"build_persistence", "build_overview_row"}, (
        "classify_runs call sites drifted: %s" % sorted(callers))


# --------------------------------------------------------------------------- #
# C-103 / C-106 — closed CLI surface and the script interface
# --------------------------------------------------------------------------- #
def test_script_interface_stays_closed(tmp_path):
    build_team(tmp_path, "team-a")
    help_output = run_program("--help")
    assert help_output.returncode == 0
    for declared in ("--repo-root", "--scope", "--spec-dir", "--json", "--version"):
        assert declared in help_output.stdout, "help lacks %s" % declared
    assert "--target" not in help_output.stdout
    for label in ("usage", "side-effects:", "exit-codes:"):
        assert label in help_output.stdout.lower()

    target_attempt = run_program("team-a", "--target", "T-001", "--repo-root", str(tmp_path))
    assert target_attempt.returncode == 2
    assert "target" in (target_attempt.stderr + target_attempt.stdout).lower()

    for flag in ("-h", "--help", "--version"):
        before = snapshot(tmp_path)
        result = run_program(flag, "--repo-root", str(tmp_path))
        assert result.returncode == 0, (flag, result.stderr)
        assert snapshot(tmp_path) == before, "%s wrote to the tree" % flag


# --------------------------------------------------------------------------- #
# C-108 — no shape change; baseline-since equality of the naming owner and schema
# --------------------------------------------------------------------------- #
def test_report_naming_owner_and_schema_unchanged_since_baseline():
    exists = git("cat-file", "-e", BASELINE_COMMIT)
    assert exists.returncode == 0, "baseline commit object %s is missing" % BASELINE_COMMIT
    for path in (
        "skills/internal/create-team/SKILL.md",
        "skills/internal/create-team/references/create-mode.md",
    ):
        shown = git("show", "%s:%s" % (BASELINE_COMMIT, path))
        assert shown.returncode == 0, "git show failed for %s" % path
        assert (REPO_ROOT / path).read_text(encoding="utf-8") == shown.stdout, (
            "no-shape-change claim broken: %s differs from the baseline object" % path)
    assert team_view.classify_run_file("20260101T000000Z-report.md")["kind"] == "report", (
        "a previously conforming compact report name no longer classifies as a run report")


# --------------------------------------------------------------------------- #
# C-109 — three-surface consistency (pointer-shaped)
# --------------------------------------------------------------------------- #
def test_three_surfaces_cite_the_owner():
    docs = DOCS_PAGE.read_text(encoding="utf-8")
    view_section = docs[docs.index("## View Mode"):]
    following = re.search(r"^## ", view_section[len("## View Mode"):], re.MULTILINE)
    view_section = view_section[: len("## View Mode") + following.start()] if following else view_section
    skill = SKILL_PAGE.read_text(encoding="utf-8")
    help_output = run_program("--help")
    docstring = team_view.__doc__ or ""

    surfaces = {
        "docs View Mode": view_section,
        "skill": skill,
        "program --help": help_output.stdout,
        "program docstring": docstring,
    }
    for name, text in surfaces.items():
        for reason in REASONS:
            assert reason in text, "%s does not name reason %s" % (name, reason)
        assert OWNER_PATH in text, "%s does not cite the program contract owner" % name
    assert "5" in surfaces["program --help"] and "degrad" in surfaces["program --help"].lower()
    assert ".specify/specs/103-team-view/contracts/team-view-program.contract.md" not in skill
    assert ".specify/specs/103-team-view/contracts/team-view-program.contract.md" not in docstring


# --------------------------------------------------------------------------- #
# C-101 / RS-004 — only the three declared engine reads; goal-utils.py untouched
# --------------------------------------------------------------------------- #
def test_only_the_three_declared_engine_reads():
    tree = ast.parse(program_source())
    actions = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "engine_read"):
            continue
        literal_args = [
            arg.value for arg in node.args if isinstance(arg, ast.Constant)
            and isinstance(arg.value, str)
        ]
        assert literal_args, "engine_read call carries no literal action"
        actions.append(tuple(literal_args))
    assert sorted(actions) == [
        ("binding", "team"), ("list",), ("targets", "--list")], (
        "declared engine reads drifted: %r" % (actions,))
    source = program_source()
    assert "run-checks" not in source and "run_checks" not in source
    for write_action in ('"bind"', '"migrate"', '"--add"'):
        assert write_action not in source, (
            "a goal-utils write action is reachable from the view: %s" % write_action)


def test_goal_utils_is_untouched_since_baseline():
    baseline = implement_start_commit()
    assert git("cat-file", "-e", baseline).returncode == 0, (
        "implement baseline commit %s is missing" % baseline)
    diff = git("diff", "--name-only", "%s..HEAD" % baseline, "--", "scripts/python/goal-utils.py")
    assert diff.returncode == 0, diff.stderr
    assert diff.stdout.strip() == "", "goal-utils.py was modified: %s" % diff.stdout


# --------------------------------------------------------------------------- #
# DoD-2 dependency class (unit 2) — import-root audit
# --------------------------------------------------------------------------- #
def test_import_roots_are_stdlib_local_or_pytest():
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    if not stdlib:  # pragma: no cover - the pinned interpreter exposes the set
        stdlib = {
            "__future__", "ast", "datetime", "hashlib", "importlib", "json", "os",
            "pathlib", "re", "shutil", "subprocess", "sys",
        }
    allowed = stdlib | LOCAL_IMPORT_ROOTS
    offenders = {}
    for path in (PROGRAM, UNIT_TEST, CONTRACT_TEST, INTEGRATION_TEST):
        roots = set()
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
        extra = roots - allowed
        if extra:
            offenders[path.name] = sorted(extra)
    assert not offenders, "import roots outside stdlib/local/pytest: %r" % offenders


# --------------------------------------------------------------------------- #
# C-401…C-405 — label vocabulary closure, both directions
# --------------------------------------------------------------------------- #
EMITTING_SITES = {
    "缺失": "STATE_MISSING",
    "为空": "STATE_EMPTY",
    "不可读": "STATE_UNREADABLE",
    "未记录": "STATE_UNRECORDED",
    "已声明": "STATE_DECLARED",
    "未声明": "STATE_UNDECLARED",
    "定义损坏": "STATE_CORRUPT",
    "形态异常": "STATE_MALFORMED",
    "悬空（dangling）": "STATE_DANGLING",
    "已列出": "STATE_LISTED",
    "已聚合": "STATE_FOLDED",
    "本次无嵌套 SDD 调用": "NESTED_NONE",
    "未声明 → active": 'STATE_UNDECLARED + " → active"',
    "未识别（unrecognized）": "STATE_UNRECOGNIZED",
    "辅助产物（auxiliary）": "辅助产物（auxiliary）: 共 %d 份",
    "不可比对（not comparable）": "STATE_NOT_COMPARABLE",
    "按声明 pattern 不适用": "STATE_SPINE_BY_PATTERN",
    "适用性不可判定": "STATE_SPINE_UNDETERMINABLE",
    "goal 需归一为 anchor_slug": "STATE_GOAL_NORMALIZE",
    "降级（degraded）": "降级（degraded）:",
}


def test_label_closure_both_directions():
    owner = owner_label_members()
    assert len(owner) == 20, "owner table members drifted: %r" % sorted(owner)
    program_labels = {
        name: getattr(team_view, name)
        for name in dir(team_view)
        if re.fullmatch(r"STATE_[A-Z0-9_]+|NESTED_NONE", name)
        and isinstance(getattr(team_view, name), str)
    }
    assert len(program_labels) == 17, "state constant set drifted: %r" % sorted(program_labels)
    outside = {value for value in program_labels.values() if value not in owner}
    assert not outside, "labels emitted by the program outside the owner tables: %r" % outside

    source = program_source()
    missing_emitters = set()
    for member in sorted(owner):
        snippet = EMITTING_SITES.get(member)
        assert snippet is not None, "owner member has no registered emitting site: %s" % member
        if snippet not in source:
            missing_emitters.add(member)
    assert not missing_emitters, "owner members without an emitting site: %r" % sorted(
        missing_emitters)
    for name in program_labels:
        assert source.count(name) >= 2, (
            "constant %s is defined but never emitted" % name)


def test_missing_state_subset_members():
    owner = owner_label_members()
    subset = {"缺失", "为空", "不可读", "未记录"}
    assert subset <= owner
    assert {team_view.STATE_MISSING, team_view.STATE_EMPTY,
            team_view.STATE_UNREADABLE, team_view.STATE_UNRECORDED} == subset
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    for member in subset:
        assert "`%s`" % member in clause_text(text, "C-402")


def test_declaration_subset_members():
    owner = owner_label_members()
    assert {"已声明", "未声明"} <= owner
    assert team_view.STATE_DECLARED == "已声明"
    assert team_view.STATE_UNDECLARED == "未声明"
    rendered = team_view.STATE_UNDECLARED + team_view.DEFAULT_POINTER
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    assert rendered in clause_text(text, "C-403"), (
        "the declared pointer render is not the owner's rendered form: %r" % rendered)


def test_derived_label_members():
    expected = {
        "定义损坏", "形态异常", "悬空（dangling）", "已列出", "已聚合",
        "本次无嵌套 SDD 调用", "未声明 → active",
    }
    owner = owner_label_members()
    assert expected <= owner
    assert team_view.STATE_CORRUPT == "定义损坏"
    assert team_view.STATE_MALFORMED == "形态异常"
    assert team_view.STATE_DANGLING == "悬空（dangling）"
    assert team_view.STATE_LISTED == "已列出"
    assert team_view.STATE_FOLDED == "已聚合"
    assert team_view.NESTED_NONE == "本次无嵌套 SDD 调用"
    assert team_view.STATE_UNDECLARED + " → active" == "未声明 → active"


def test_new_derived_label_members():
    expected = {
        "未识别（unrecognized）", "辅助产物（auxiliary）", "不可比对（not comparable）",
        "按声明 pattern 不适用", "适用性不可判定", "goal 需归一为 anchor_slug",
        "降级（degraded）",
    }
    owner = owner_label_members()
    assert expected <= owner
    assert team_view.STATE_UNRECOGNIZED == "未识别（unrecognized）"
    assert team_view.STATE_NOT_COMPARABLE == "不可比对（not comparable）"
    assert team_view.STATE_SPINE_BY_PATTERN == "按声明 pattern 不适用"
    assert team_view.STATE_SPINE_UNDETERMINABLE == "适用性不可判定"
    assert team_view.STATE_GOAL_NORMALIZE == "goal 需归一为 anchor_slug"


# --------------------------------------------------------------------------- #
# C-406 / C-407 / C-408 — line forms and the substitution prohibition
# --------------------------------------------------------------------------- #
def test_residue_line_form_in_owner():
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    clause = clause_text(text, "C-406")
    assert "未识别（unrecognized）: 共 N 份；示例: <name>, …（省略 K）" in clause
    assert "未识别（unrecognized）—— 仅残留，最新不可确定" in clause
    source = program_source()
    assert "共 %d 份；示例: %s（省略 %d）" in source, (
        "the program's residue format no longer matches the owner's bounded form")
    assert team_view.RESIDUE_EXAMPLE_CAP <= 3


def test_roster_not_comparable_form_in_owner():
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    clause = clause_text(text, "C-407")
    assert "不可比对（not comparable）（原因：<reason>）" in clause
    assert "`未记录`" in clause
    source = program_source()
    assert '"- 名册差异（roster_delta）: %s（原因：%s）" % (' in source, (
        "the roster not-comparable line form drifted")
    assert 'STATE_NOT_COMPARABLE, delta["reason"]' in source


def test_no_substitute_label_or_empty_reason():
    text = LABEL_CONTRACT.read_text(encoding="utf-8")
    clause = clause_text(text, "C-408")
    assert "其他" in clause and "未知" in clause and "empty reason" in clause
    values = {
        getattr(team_view, name)
        for name in dir(team_view)
        if re.fullmatch(r"STATE_[A-Z0-9_]+", name)
        and isinstance(getattr(team_view, name), str)
    }
    assert "其他" not in values and "未知" not in values, (
        "a catch-all label stands for an enumerated state")
    source = program_source()
    assert "（原因：%s）" in source
    assert "（原因：）" not in source, "a reason-bearing line renders an empty reason"
