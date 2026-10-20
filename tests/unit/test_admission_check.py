"""Unit tests for skills/external/sdd-loop-driver/scripts/admission-check.py.

Red-first: the script does not exist yet; every test below fails at invocation.
The medium and large fixtures live in tests/fixtures/sdd_loop_efficiency/.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "admission-check.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency"

GIT = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com"]


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


def _init_repo(tmp_path, populate):
    project = tmp_path / ("project-%d" % len(list(tmp_path.iterdir())))
    project.mkdir()
    _git(project, "init")
    _git(project, "checkout", "-b", "012-medium")
    (project / "README.md").write_text("fixture base\n", encoding="utf-8")
    _git(project, "add", "-A")
    _git(project, "commit", "-m", "base")
    base = _git(project, "rev-parse", "HEAD")
    populate(project)
    _git(project, "add", "-A")
    _git(project, "commit", "-m", "fixture")
    return project, base


def _copy_fixture(tmp_path, name, spec_name):
    def populate(project):
        src = FIXTURES / name
        shutil.copytree(src, project, dirs_exist_ok=True)
    return _init_repo(tmp_path, populate)


def _run(project, base, expected_branch="012-medium", spec_name="012-medium",
         json_out=None, override=None):
    spec = project / ".specify" / "specs" / spec_name
    args = {
        "--project": str(project),
        "--base-ref": base,
        "--requirements": str(spec / "requirements.md"),
        "--tasks": str(spec / "tasks.md"),
        "--checklists": str(spec / "checklists" / "requirements.md"),
        "--entry-evidence": str(spec / "entry.md"),
        "--lines-manifest": str(spec / "lines.manifest"),
        "--expected-branch": expected_branch,
    }
    if override:
        args.update(override)
    cmd = [sys.executable, str(SCRIPT)]
    for key, value in args.items():
        cmd += [key, value]
    if json_out:
        cmd += ["--json-out", str(json_out)]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    payload = None
    if json_out and Path(json_out).exists():
        payload = json.loads(Path(json_out).read_text(encoding="utf-8"))
    return completed, payload


def _criteria(payload):
    return {item["id"]: item for item in payload["criteria"]}


def test_medium_fixture_admitted(tmp_path):
    project, base = _copy_fixture(tmp_path, "medium", "012-medium")
    out = tmp_path / "admission.json"
    completed, payload = _run(project, base, json_out=out)
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert payload["decision"] == "fast-lane"
    assert payload["measured"] == {"fr_count": 12, "task_count": 25}
    assert [item["id"] for item in payload["criteria"]] == list("abcdefg")
    assert all(item["verdict"] == "pass" for item in payload["criteria"])
    assert payload["checklist"] == "skipped(fast-lane)"


def test_large_fixture_denied(tmp_path):
    project, base = _copy_fixture(tmp_path, "large", "013-large")
    out = tmp_path / "admission.json"
    completed, payload = _run(project, base, expected_branch="013-large",
                              spec_name="013-large", json_out=out)
    assert completed.returncode == 1, completed.stderr
    assert payload["decision"] == "full-chain"
    assert payload["measured"]["task_count"] == 60
    assert _criteria(payload)["a"]["verdict"] == "fail"


@pytest.mark.parametrize("fr_count,task_count,admitted", [
    (8, 10, True), (30, 40, True), (7, 40, False), (31, 40, False),
    (12, 9, False), (12, 41, False),
])
def test_task_count_boundary_edges(tmp_path, fr_count, task_count, admitted):
    project, base = _init_repo(
        tmp_path, lambda root: _build_spec(root, fr_count=fr_count,
                                           task_count=task_count))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == (0 if admitted else 1)
    assert payload["decision"] == ("fast-lane" if admitted else "full-chain")
    assert payload["measured"]["fr_count"] == fr_count
    assert payload["measured"]["task_count"] == task_count


def test_narrow_task_pattern_only_for_admission(tmp_path):
    narrow_nine = ["- [ ] T%03d fixture" % i for i in range(1, 10)]
    narrow_nine += ["- [>] T010 claimed", "- [~] T011 deferred"]
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, task_lines=narrow_nine))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert payload["measured"]["task_count"] == 9, (
        "wide mode must not count [>]/[~] rows for admission")

    narrow_ten = ["- [ ] T%03d fixture" % i for i in range(1, 11)]
    narrow_ten += ["- [>] T011 claimed", "- [~] T012 deferred"]
    project2, base2 = _init_repo(tmp_path, lambda root: _build_spec(
        root, task_lines=narrow_ten))
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 0
    assert payload2["measured"]["task_count"] == 10


def test_fr_definition_pattern_pinned(tmp_path):
    seven = ["- **FR-%03d**: fixture" % i for i in range(1, 8)]
    seven += ["- **FR-008** no colon", "Some FR-009 mention", "- **FR-010** : spaced colon"]
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, fr_lines=seven))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert payload["measured"]["fr_count"] == 7

    eight = ["- **FR-%03d**: fixture" % i for i in range(1, 9)]
    project2, base2 = _init_repo(tmp_path, lambda root: _build_spec(
        root, fr_lines=eight))
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 0
    assert payload2["measured"]["fr_count"] == 8


def test_fr_count_excludes_sc_rows(tmp_path):
    eight = ["- **FR-%03d**: fixture" % i for i in range(1, 9)]
    eight += ["- **SC-%03d**: criterion" % i for i in range(1, 20)]
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, fr_lines=eight))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 0
    assert payload["measured"]["fr_count"] == 8


def test_missing_or_unparseable_tasks_fail_closed(tmp_path):
    project, base = _init_repo(tmp_path, lambda root: _build_spec(root))
    completed, _ = _run(project, base, override={
        "--tasks": str(tmp_path / "does-not-exist.md")})
    assert completed.returncode == 2

    project2, base2 = _init_repo(
        tmp_path, lambda root: _build_spec(root, task_lines=[]))
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 1
    assert payload2["decision"] == "full-chain"
    assert payload2["measured"]["task_count"] == 0


def test_missing_checklist_or_entry_fails_closed(tmp_path):
    project, base = _init_repo(tmp_path, lambda root: _build_spec(root))
    completed, _ = _run(project, base, override={
        "--checklists": str(tmp_path / "missing-checklist.md")})
    assert completed.returncode == 2

    project2, base2 = _init_repo(
        tmp_path, lambda root: _build_spec(root, entry="please use the fast lane\n"))
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 1
    assert payload2["decision"] == "full-chain"


def test_sensitive_or_engine_path_rejected(tmp_path):
    def engine(root):
        _build_spec(root)
        (root / "templates").mkdir()
        (root / "templates" / "fixture.md").write_text("x\n", encoding="utf-8")

    project, base = _init_repo(tmp_path, engine)
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert _criteria(payload)["c"]["verdict"] == "fail"

    def sensitive(root):
        _build_spec(root)
        (root / "docs" / "auth").mkdir(parents=True)
        (root / "docs" / "auth" / "notes.md").write_text("x\n", encoding="utf-8")

    project2, base2 = _init_repo(tmp_path, sensitive)
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 1
    assert _criteria(payload2)["d"]["verdict"] == "fail"

    def sensitive_content(root):
        _build_spec(root)
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs" / "notes.md").write_text("password = \"hunter2\"\n",
                                                encoding="utf-8")

    project3, base3 = _init_repo(tmp_path, sensitive_content)
    completed3, payload3 = _run(project3, base3, json_out=tmp_path / "c.json")
    assert completed3.returncode == 1
    assert _criteria(payload3)["d"]["verdict"] == "fail"


@pytest.mark.parametrize("manifest", [
    "# comment\n\n012-medium|012-medium\n",
    "012-medium|012-medium|extra\n",
    "012-medium | 012-medium\n",
    "012/medium|012-medium\n",
    "012-medium|012-medium\nother|other\n",
])
def test_lines_manifest_syntax_pinned(tmp_path, manifest):
    ok = manifest.startswith("# comment")
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, manifest=manifest))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    if ok:
        assert completed.returncode == 0
        assert _criteria(payload)["e"]["verdict"] == "pass"
    else:
        assert completed.returncode == 1
        assert _criteria(payload)["e"]["verdict"] == "fail"


def test_multiline_or_branch_mismatch_lines_manifest_rejected(tmp_path):
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, manifest="012-medium|another-branch\n"))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert _criteria(payload)["e"]["verdict"] == "fail"

    project2, base2 = _init_repo(tmp_path, lambda root: _build_spec(root))
    completed2, payload2 = _run(project2, base2, expected_branch="master",
                                json_out=tmp_path / "b.json")
    assert completed2.returncode == 1
    assert _criteria(payload2)["e"]["verdict"] == "fail"


def test_open_clarification_marker_rejected(tmp_path):
    def populate(root):
        _build_spec(root)
        spec = root / ".specify" / "specs" / "012-medium"
        text = (spec / "requirements.md").read_text(encoding="utf-8")
        text += "\n- [NEEDS CLARIFICATION: an open marker]\n"
        (spec / "requirements.md").write_text(text, encoding="utf-8")

    project, base = _init_repo(tmp_path, populate)
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert _criteria(payload)["f"]["verdict"] == "fail"


def test_unresolved_related_feature_rejected(tmp_path):
    project, base = _init_repo(tmp_path, lambda root: _build_spec(
        root, related="099", registry_feature="058"))
    completed, payload = _run(project, base, json_out=tmp_path / "a.json")
    assert completed.returncode == 1
    assert _criteria(payload)["f"]["verdict"] == "fail"

    def missing_detail(root):
        _build_spec(root)
        (root / ".specify" / "memory" / "features" / "058.md").unlink()

    project2, base2 = _init_repo(tmp_path, missing_detail)
    completed2, payload2 = _run(project2, base2, json_out=tmp_path / "b.json")
    assert completed2.returncode == 1
    assert _criteria(payload2)["f"]["verdict"] == "fail"


def test_exit_codes_0_1_2(tmp_path):
    project, base = _init_repo(tmp_path, lambda root: _build_spec(root))
    completed, _ = _run(project, base)
    assert completed.returncode == 0

    project2, base2 = _init_repo(tmp_path, lambda root: _build_spec(
        root, entry="no opt-in here\n"))
    completed2, _ = _run(project2, base2)
    assert completed2.returncode == 1

    project3, base3 = _init_repo(tmp_path, lambda root: _build_spec(root))
    completed3, _ = _run(project3, base3, override={
        "--lines-manifest": str(tmp_path / "no-manifest.txt")})
    assert completed3.returncode == 2
