"""Unit tests for skills/external/sdd-loop-driver/scripts/admission-check.py.

067 W2 (T004/T005, research R-2/R-3): the engine is loaded IN-PROCESS via importlib
and invoked through ``main(argv)`` — no per-case interpreter cold start. Exactly one
test (``test_exit_codes_0_1_2``) stays a true CLI subprocess invocation to pin the
exit-code (0/1/2) and argv/``--json-out`` contract surface. The engine module is
re-executed per case (see the ``admission_engine`` fixture): that reload IS the
explicit global-state reset between cases (FR-016 — admission-check.py declares only
immutable constants today, and re-execution guarantees a future mutable global cannot
become cross-case coupling). Repos come from module-scoped template repos built once
per module; every case works on a fresh ``git clone`` (copy-on-write), replacing the
per-case ``git init`` + two commits (the host hook tax is already gone via RC-07).

The medium and large fixtures live in tests/fixtures/sdd_loop_efficiency/.
"""

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "admission-check.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency"

ENGINE_MODULE_NAME = "_admission_check_engine_under_test"


def _git(project, *args):
    return subprocess.run(
        ["git", "-C", str(project), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.com", *args],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _build_spec(root, fr_count=12, task_count=25, fr_lines=None, task_lines=None,
                checklist_checked=True, entry="fast-lane=opt-in\n",
                manifest="012-medium|012-medium\n", clarifications=True,
                related="058", registry_feature="058", spec_name="012-medium"):
    spec = root / ".specify" / "specs" / spec_name
    spec.mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "memory" / "features").mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "memory" / "features.md").write_text(
        "# Feature Index\n\n| ID | Name | Status |\n|----|------|--------|\n"
        "| %s | fixture | Implemented |\n" % registry_feature, encoding="utf-8")
    (root / ".specify" / "memory" / "features" / ("%s.md" % related)).write_text(
        "# Feature %s\n" % related, encoding="utf-8")

    if fr_lines is None:
        fr_lines = ["- **FR-%03d**: fixture requirement %d" % (i, i)
                    for i in range(1, fr_count + 1)]
    if task_lines is None:
        task_lines = ["- [ ] T%03d fixture task" % i for i in range(1, task_count + 1)]
    parts = []
    if related:
        parts.append("**Related Feature**: %s\n" % related)
    parts.append("# Fixture Requirements\n")
    parts.extend(fr_lines)
    parts.append("\n- **SC-001**: fixture criterion")
    if clarifications:
        parts.append("\n## Clarifications\n\n### Session 2026-10-20\n\n- Q: fixture? → A: yes.\n")
    (spec / "requirements.md").write_text("\n".join(parts), encoding="utf-8")
    (spec / "tasks.md").write_text("\n".join(["# Fixture Tasks"] + task_lines) + "\n",
                                   encoding="utf-8")
    (spec / "checklists").mkdir(exist_ok=True)
    checked = "- [X]" if checklist_checked else "- [ ]"
    (spec / "checklists" / "requirements.md").write_text(
        "# Checklist\n\n- [X] CHK001 measurable\n%s CHK002 closed\n" % checked,
        encoding="utf-8")
    (spec / "entry.md").write_text("# Entry\n\n" + entry, encoding="utf-8")
    (spec / "lines.manifest").write_text(manifest, encoding="utf-8")
    return spec


# --- engine loading (in-process direct call, R-2) -------------------------------


def _load_engine():
    spec = importlib.util.spec_from_file_location(ENGINE_MODULE_NAME, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[ENGINE_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def admission_engine():
    """Fresh engine module per case — the explicit between-case global-state reset (FR-016)."""
    engine = _load_engine()
    yield engine
    sys.modules.pop(ENGINE_MODULE_NAME, None)


# --- shared template repos + per-case clone (R-3) -------------------------------


def _make_template(base_dir, branch, populate):
    project = base_dir / "template"
    project.mkdir()
    _git(project, "init")
    _git(project, "checkout", "-b", branch)
    (project / "README.md").write_text("fixture base\n", encoding="utf-8")
    _git(project, "add", "-A")
    _git(project, "commit", "-m", "base")
    populate(project)
    _git(project, "add", "-A")
    _git(project, "commit", "-m", "fixture")
    return project


@pytest.fixture(scope="module")
def medium_template(tmp_path_factory):
    """One fully populated medium repo per module; cases clone instead of rebuilding."""
    return _make_template(tmp_path_factory.mktemp("admission-medium-template"),
                          "012-medium", lambda root: _build_spec(root))


@pytest.fixture(scope="module")
def large_template(tmp_path_factory):
    return _make_template(tmp_path_factory.mktemp("admission-large-template"),
                          "013-large",
                          lambda root: shutil.copytree(FIXTURES / "large", root,
                                                       dirs_exist_ok=True))


def _clone(template, tmp_path, name="project", mutate=None):
    """Cheap per-case repo: fresh clone of the frozen template, optional variant commit.

    Returns (project, base) where base = the template's frozen HEAD commit, so any
    variant commit lands in base..HEAD exactly like the old build-then-commit flow.
    """
    dest = tmp_path / name
    subprocess.run(["git", "clone", "--quiet", str(template), str(dest)],
                   check=True, capture_output=True, text=True)
    base = _git(dest, "rev-parse", "HEAD")
    if mutate is not None:
        mutate(dest)
        _git(dest, "add", "-A")
        _git(dest, "commit", "-m", "variant")
    return dest, base


# --- invocation helpers ----------------------------------------------------------


def _admission_args(project, base, expected_branch, spec_name, override):
    spec = project / ".specify" / "specs" / spec_name
    args = {
        "--project": str(project),
        "--base-ref": str(base),
        "--requirements": str(spec / "requirements.md"),
        "--tasks": str(spec / "tasks.md"),
        "--checklists": str(spec / "checklists" / "requirements.md"),
        "--entry-evidence": str(spec / "entry.md"),
        "--lines-manifest": str(spec / "lines.manifest"),
        "--expected-branch": expected_branch,
    }
    if override:
        args.update(override)
    argv = []
    for key, value in args.items():
        argv += [key, str(value)]
    return argv


def _run(engine, project, base, expected_branch="012-medium", spec_name="012-medium",
         override=None):
    """In-process admission check via engine.main(argv). Returns (exit_code, payload|None)."""
    argv = _admission_args(project, base, expected_branch, spec_name, override)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        code = engine.main(argv)
    out = stdout.getvalue()
    payload = json.loads(out) if out.strip() else None
    return code, payload


def _run_cli(project, base, expected_branch="012-medium", spec_name="012-medium",
             override=None, json_out=None):
    """True subprocess invocation — pins the CLI contract (argv, exit codes, --json-out file)."""
    argv = _admission_args(project, base, expected_branch, spec_name, override)
    cmd = [sys.executable, str(SCRIPT)]
    for token in argv:
        cmd.append(token)
    if json_out:
        cmd += ["--json-out", str(json_out)]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    payload = None
    if json_out and Path(json_out).exists():
        payload = json.loads(Path(json_out).read_text(encoding="utf-8"))
    return completed, payload


def _criteria(payload):
    return {item["id"]: item for item in payload["criteria"]}


# --- cases -----------------------------------------------------------------------


def test_medium_fixture_admitted(admission_engine, tmp_path, medium_template):
    project, base = _clone(medium_template, tmp_path)
    code, payload = _run(admission_engine, project, base)
    assert code == 0, payload and payload["reasons"]
    assert payload["decision"] == "fast-lane"
    assert payload["measured"] == {"fr_count": 12, "task_count": 25}
    assert [item["id"] for item in payload["criteria"]] == list("abcdefg")
    assert all(item["verdict"] == "pass" for item in payload["criteria"])
    assert payload["checklist"] == "skipped(fast-lane)"


def test_large_fixture_denied(admission_engine, tmp_path, large_template):
    project, base = _clone(large_template, tmp_path)
    code, payload = _run(admission_engine, project, base, expected_branch="013-large",
                         spec_name="013-large")
    assert code == 1, payload and payload["reasons"]
    assert payload["decision"] == "full-chain"
    assert payload["measured"]["task_count"] == 60
    assert _criteria(payload)["a"]["verdict"] == "fail"


@pytest.mark.parametrize("fr_count,task_count,admitted", [
    (8, 10, True), (30, 40, True), (7, 40, False), (31, 40, False),
    (12, 9, False), (12, 41, False),
    # 067 T005 sibling rows (same shape; every row keeps its own assertions and id):
    (30, 10, True),   # fr upper bound x task lower bound, both inside the window
    (7, 9, False),    # both counts below their lower bounds
])
def test_task_count_boundary_edges(admission_engine, tmp_path, medium_template,
                                   fr_count, task_count, admitted):
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, fr_count=fr_count, task_count=task_count))
    code, payload = _run(admission_engine, project, base)
    assert code == (0 if admitted else 1)
    assert payload["decision"] == ("fast-lane" if admitted else "full-chain")
    assert payload["measured"]["fr_count"] == fr_count
    assert payload["measured"]["task_count"] == task_count


def test_narrow_task_pattern_only_for_admission(admission_engine, tmp_path, medium_template):
    narrow_nine = ["- [ ] T%03d fixture" % i for i in range(1, 10)]
    narrow_nine += ["- [>] T010 claimed", "- [~] T011 deferred"]
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, task_lines=narrow_nine))
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert payload["measured"]["task_count"] == 9, (
        "wide mode must not count [>]/[~] rows for admission")

    narrow_ten = ["- [ ] T%03d fixture" % i for i in range(1, 11)]
    narrow_ten += ["- [>] T011 claimed", "- [~] T012 deferred"]
    project2, base2 = _clone(medium_template, tmp_path, "project-2", lambda root: _build_spec(
        root, task_lines=narrow_ten))
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 0
    assert payload2["measured"]["task_count"] == 10


def test_fr_definition_pattern_pinned(admission_engine, tmp_path, medium_template):
    seven = ["- **FR-%03d**: fixture" % i for i in range(1, 8)]
    seven += ["- **FR-008** no colon", "Some FR-009 mention", "- **FR-010** : spaced colon"]
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, fr_lines=seven))
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert payload["measured"]["fr_count"] == 7

    eight = ["- **FR-%03d**: fixture" % i for i in range(1, 9)]
    project2, base2 = _clone(medium_template, tmp_path, "project-2", lambda root: _build_spec(
        root, fr_lines=eight))
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 0
    assert payload2["measured"]["fr_count"] == 8


def test_fr_count_excludes_sc_rows(admission_engine, tmp_path, medium_template):
    eight = ["- **FR-%03d**: fixture" % i for i in range(1, 9)]
    eight += ["- **SC-%03d**: criterion" % i for i in range(1, 20)]
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, fr_lines=eight))
    code, payload = _run(admission_engine, project, base)
    assert code == 0
    assert payload["measured"]["fr_count"] == 8


def test_missing_or_unparseable_tasks_fail_closed(admission_engine, tmp_path, medium_template):
    project, base = _clone(medium_template, tmp_path)
    code, _ = _run(admission_engine, project, base, override={
        "--tasks": str(tmp_path / "does-not-exist.md")})
    assert code == 2

    project2, base2 = _clone(medium_template, tmp_path, "project-2", lambda root: _build_spec(
        root, task_lines=[]))
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 1
    assert payload2["decision"] == "full-chain"
    assert payload2["measured"]["task_count"] == 0


def test_missing_checklist_or_entry_fails_closed(admission_engine, tmp_path, medium_template):
    project, base = _clone(medium_template, tmp_path)
    code, _ = _run(admission_engine, project, base, override={
        "--checklists": str(tmp_path / "missing-checklist.md")})
    assert code == 2

    project2, base2 = _clone(medium_template, tmp_path, "project-2", lambda root: _build_spec(
        root, entry="please use the fast lane\n"))
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 1
    assert payload2["decision"] == "full-chain"


def test_sensitive_or_engine_path_rejected(admission_engine, tmp_path, medium_template):
    def engine(root):
        _build_spec(root)
        (root / "templates").mkdir()
        (root / "templates" / "fixture.md").write_text("x\n", encoding="utf-8")

    project, base = _clone(medium_template, tmp_path, mutate=engine)
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert _criteria(payload)["c"]["verdict"] == "fail"

    def sensitive(root):
        _build_spec(root)
        (root / "docs" / "auth").mkdir(parents=True)
        (root / "docs" / "auth" / "notes.md").write_text("x\n", encoding="utf-8")

    project2, base2 = _clone(medium_template, tmp_path, "project-2", mutate=sensitive)
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 1
    assert _criteria(payload2)["d"]["verdict"] == "fail"

    def sensitive_content(root):
        _build_spec(root)
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs" / "notes.md").write_text("password = \"hunter2\"\n",
                                                encoding="utf-8")

    project3, base3 = _clone(medium_template, tmp_path, "project-3",
                             mutate=sensitive_content)
    code3, payload3 = _run(admission_engine, project3, base3)
    assert code3 == 1
    assert _criteria(payload3)["d"]["verdict"] == "fail"


@pytest.mark.parametrize("manifest", [
    "# comment\n\n012-medium|012-medium\n",
    "012-medium|012-medium|extra\n",
    "012-medium | 012-medium\n",
    "012/medium|012-medium\n",
    "012-medium|012-medium\nother|other\n",
])
def test_lines_manifest_syntax_pinned(admission_engine, tmp_path, medium_template, manifest):
    ok = manifest.startswith("# comment")
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, manifest=manifest))
    code, payload = _run(admission_engine, project, base)
    if ok:
        assert code == 0
        assert _criteria(payload)["e"]["verdict"] == "pass"
    else:
        assert code == 1
        assert _criteria(payload)["e"]["verdict"] == "fail"


def test_multiline_or_branch_mismatch_lines_manifest_rejected(admission_engine, tmp_path,
                                                              medium_template):
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, manifest="012-medium|another-branch\n"))
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert _criteria(payload)["e"]["verdict"] == "fail"

    project2, base2 = _clone(medium_template, tmp_path, "project-2")
    code2, payload2 = _run(admission_engine, project2, base2, expected_branch="master")
    assert code2 == 1
    assert _criteria(payload2)["e"]["verdict"] == "fail"


def test_open_clarification_marker_rejected(admission_engine, tmp_path, medium_template):
    def populate(root):
        _build_spec(root)
        spec = root / ".specify" / "specs" / "012-medium"
        text = (spec / "requirements.md").read_text(encoding="utf-8")
        text += "\n- [NEEDS CLARIFICATION: an open marker]\n"
        (spec / "requirements.md").write_text(text, encoding="utf-8")

    project, base = _clone(medium_template, tmp_path, mutate=populate)
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert _criteria(payload)["f"]["verdict"] == "fail"


def test_unresolved_related_feature_rejected(admission_engine, tmp_path, medium_template):
    project, base = _clone(medium_template, tmp_path, mutate=lambda root: _build_spec(
        root, related="099", registry_feature="058"))
    code, payload = _run(admission_engine, project, base)
    assert code == 1
    assert _criteria(payload)["f"]["verdict"] == "fail"

    def missing_detail(root):
        _build_spec(root)
        (root / ".specify" / "memory" / "features" / "058.md").unlink()

    project2, base2 = _clone(medium_template, tmp_path, "project-2", mutate=missing_detail)
    code2, payload2 = _run(admission_engine, project2, base2)
    assert code2 == 1
    assert _criteria(payload2)["f"]["verdict"] == "fail"


def test_exit_codes_0_1_2(tmp_path, medium_template):
    """CLI contract pin (T004 / R-2): the only true subprocess cases in this file.

    The 0/1/2 exit-code semantics of the original test are preserved verbatim; the
    exit-0 invocation additionally pins the ``--json-out`` file surface.
    """
    project, base = _clone(medium_template, tmp_path)
    completed, payload = _run_cli(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 0
    assert payload is not None and payload["decision"] == "fast-lane"

    project2, base2 = _clone(medium_template, tmp_path, "project-2", lambda root: _build_spec(
        root, entry="no opt-in here\n"))
    completed2, _ = _run_cli(project2, base2)
    assert completed2.returncode == 1

    project3, base3 = _clone(medium_template, tmp_path, "project-3")
    completed3, _ = _run_cli(project3, base3, override={
        "--lines-manifest": str(tmp_path / "no-manifest.txt")})
    assert completed3.returncode == 2
