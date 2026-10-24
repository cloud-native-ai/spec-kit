"""Contract tests for ``scripts/python/doc-consistency-check.py`` (069a, T014).

Owns the command-surface / three-face assertions of
``.specify/specs/069a-flow-classification-docs-gates/contracts/doc-consistency-checker.md``
(C-1…C-4, C-6…C-9) that ``tasks.md`` T014 names:

* C-1  `--action verify` with `--spec-dir` / `--path` (both missing => exit 2),
       `--faces` defaulting to the four faces (unknown face => exit 2);
* C-2  the three scanned sets and the closed exclusion list (path level here;
       the line level lives in ``tests/unit/test_doc_consistency_rules.py``);
* C-3  the five ``evidence`` rules — grade/as-of pairing, as-of form, as-of
       freshness against the file's last commit, closed grade set, mandatory
       source — plus ``not-evaluated`` outside git (never "pass");
* C-4  the two-line reader declaration inside the first 40 non-empty lines;
* C-5  the SC-007 injections: an owner-text copy becomes ``duplicate-fact`` with
       both sides located;
* C-6  the count face is **delegated** (never re-implemented); an unavailable
       delegation is an explicit ``count_check.status = not-run`` and fails under
       ``--strict``;
* C-7  the JSON shape (action / checked_at / scope / faces / findings /
       count_check);
* C-8  exit codes — 0 never travels with a finding, 1 = findings or a strict
       ``not-evaluated``, 2 = input/parse error.

Annotation grammar (owner: ``shared/workflow/expression-gates.md`` § 证据分级与 as-of):
a line is an annotated assertion only when it carries the marker ``证据：``; the
grade is the token right after the marker, ``as-of`` is a ``YYYY-MM-DD`` value,
and ``source:`` is mandatory. Fixtures below use exactly that form.

Red-first discipline (Constitution IV): the engine does not exist yet, so ``_run``
asserts the script path first — red is "artifact missing / behaviour wrong",
never an import or collection error.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "python" / "doc-consistency-check.py"
CHECKER_REL = "scripts/python/doc-consistency-check.py"
OWNER_GUIDELINE = REPO_ROOT / "shared" / "guidelines" / "one-source-of-truth.md"

ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
EVIDENCE_RULES = (
    "grade-asof-unpaired",
    "as-of-malformed",
    "as-of-stale",
    "grade-invalid",
    "source-missing",
)

CLEAN_DOC = """# Clean Fixture

**Readers**: 迁移评审者，需要在合并前判断这份文档是否可用。
**Reading scenario**: 合并前核对读者声明与事实标注。

该切片把两个引擎放在框架源里（证据：实测，as-of 2026-10-24，source: `python3 scripts/python/flow-class-check.py --action check` exit 0）。
"""


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    assert CHECKER.is_file(), (
        "doc-consistency checker missing: %s — expected at T020/T021 (069a). "
        "Red is the intended pre-implementation state for T014." % CHECKER_REL
    )
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON document on stdout, got empty output (stderr: %r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _verify(*args: str, cwd: Path | None = None) -> tuple[subprocess.CompletedProcess, dict]:
    proc = _run("--action", "verify", "--format", "json", *args, cwd=cwd)
    return proc, (_json(proc) if proc.stdout.strip() else {})


def _findings(doc: dict) -> list[dict]:
    findings = doc.get("findings")
    assert isinstance(findings, list), "JSON output lacks a findings[] list: %r" % doc
    return findings


def _rules(doc: dict) -> list[str]:
    return [finding.get("rule", "") for finding in _findings(doc)]


def _facet(doc: dict, face: str) -> str:
    faces = doc.get("faces")
    assert isinstance(faces, dict), "JSON output lacks a faces object: %r" % doc
    assert face in faces, "faces object lacks the %r face: %r" % (face, faces)
    return str(faces[face])


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args], cwd=str(repo), check=True, capture_output=True, text=True
    )


def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    return path


def _git_commit_all(repo: Path, message: str = "fixture") -> None:
    _git(repo, "add", "-A")
    _git(
        repo,
        "-c", "user.email=t@t",
        "-c", "user.name=t",
        "commit", "-q", "-m", message,
    )


def _spec_dir(root: Path) -> Path:
    """A minimal, count-consistent spec dir (3 FR / 2 SC / 3 tasks)."""
    spec = root / "specs" / "001-fixture"
    _write(
        spec / "requirements.md",
        "# Requirements\n\n"
        "- **FR-001**: first requirement.\n"
        "- **FR-002**: second requirement.\n"
        "- **FR-003**: third requirement.\n"
        "- **SC-001**: first criterion.\n"
        "- **SC-002**: second criterion.\n",
    )
    _write(spec / "plan.md", "# Plan\n\nNo count claim here.\n")
    _write(
        spec / "tasks.md",
        "# Tasks\n\n- [ ] T001 first task\n- [ ] T002 second task\n- [ ] T003 third task\n",
    )
    return spec


# --------------------------------------------------------------------------- #
# C-1 — command surface
# --------------------------------------------------------------------------- #
def test_c01_requires_a_scope_and_rejects_unknown_faces(tmp_path):
    proc = _run("--action", "verify")
    assert proc.returncode == 2, (
        "no --spec-dir and no --path must be an input error (exit 2), got %d (stderr: %r)"
        % (proc.returncode, proc.stderr)
    )
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    proc = _run("--action", "verify", "--path", str(doc), "--faces", "reader,nonsense")
    assert proc.returncode == 2, "an unknown face name must be an input error (exit 2)"


def test_c01_default_faces_are_the_four_registered_faces(tmp_path):
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    spec = _spec_dir(tmp_path)
    proc, payload = _verify("--spec-dir", str(spec), "--path", str(doc))
    assert proc.returncode == 0, "clean fixture must exit 0 (stderr: %r)" % proc.stderr
    assert set(payload["faces"]) == {"reader", "evidence", "duplicate", "count"}, (
        "the default face set must be reader,evidence,duplicate,count; got %r"
        % sorted(payload["faces"])
    )


# --------------------------------------------------------------------------- #
# C-2 — clean run and JSON shape
# --------------------------------------------------------------------------- #
def test_c02_clean_fixture_passes_with_no_findings(tmp_path):
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    spec = _spec_dir(tmp_path)
    proc, payload = _verify(
        "--spec-dir", str(spec), "--path", str(doc), "--faces", "reader,evidence,count"
    )
    assert proc.returncode == 0, (
        "clean fixture must exit 0, got %d (stdout: %r / stderr: %r)"
        % (proc.returncode, proc.stdout[:600], proc.stderr)
    )
    assert _findings(payload) == [], "clean fixture must report zero findings"
    assert _facet(payload, "reader") == "pass"
    # Outside git, the as-of freshness rule is not-evaluable — explicit, never a finding.
    assert _facet(payload, "evidence") in {"pass", "not-evaluated"}


def test_c07_json_shape(tmp_path):
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    spec = _spec_dir(tmp_path)
    proc, payload = _verify("--spec-dir", str(spec), "--path", str(doc))
    assert proc.returncode == 0, "clean fixture must exit 0"
    assert payload["action"] == "verify"
    assert ISO_Z_RE.match(payload["checked_at"]), (
        "checked_at must be ISO-8601 Z, got %r" % payload.get("checked_at")
    )
    scope = payload["scope"]
    assert set(scope) >= {"spec_dir", "paths", "files_scanned"}, "scope lacks required fields: %r" % scope
    assert isinstance(scope["files_scanned"], int) and scope["files_scanned"] >= 1
    count_check = payload["count_check"]
    assert set(count_check) >= {"status", "reason"}, "count_check lacks status/reason: %r" % count_check
    assert count_check["status"] in {"delegated", "not-run"}
    assert count_check["status"] == "delegated", (
        "with a complete spec dir the count face must delegate, got %r (reason: %r)"
        % (count_check["status"], count_check.get("reason"))
    )


# --------------------------------------------------------------------------- #
# C-4 — reader declaration
# --------------------------------------------------------------------------- #
def test_c03_reader_declaration_missing_is_blocking(tmp_path):
    doc = _write(tmp_path / "doc.md", "# Doc\n\n没有任何读者声明。\n")
    proc, payload = _verify("--path", str(doc), "--faces", "reader")
    assert proc.returncode == 1, "a missing reader declaration must fail (exit 1)"
    assert "reader-declaration-missing" in _rules(payload), (
        "expected reader-declaration-missing, got %r" % _rules(payload)
    )
    assert _facet(payload, "reader") == "fail"


def test_c03_reader_declaration_with_empty_value_is_blocking(tmp_path):
    doc = _write(
        tmp_path / "doc.md",
        "# Doc\n\n**Readers**:\n**Reading scenario**: 合并前核对。\n",
    )
    proc, payload = _verify("--path", str(doc), "--faces", "reader")
    assert proc.returncode == 1, "an empty declared value must fail (exit 1)"
    assert "reader-declaration-missing" in _rules(payload)


def test_c03_reader_declaration_after_40_non_empty_lines_is_blocking(tmp_path):
    filler = "\n".join("第 %d 行填充内容，用于把声明挤出前 40 行。" % i for i in range(1, 45))
    doc = _write(
        tmp_path / "doc.md",
        "# Doc\n\n" + filler + "\n\n"
        "**Readers**: 迁移评审者。\n**Reading scenario**: 合并前核对。\n",
    )
    proc, payload = _verify("--path", str(doc), "--faces", "reader")
    assert proc.returncode == 1, "a declaration beyond the first 40 non-empty lines must fail"
    assert "reader-declaration-missing" in _rules(payload)


def test_c03_reader_declaration_present_within_40_passes(tmp_path):
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    proc, payload = _verify("--path", str(doc), "--faces", "reader")
    assert proc.returncode == 0, "a valid declaration must pass (stderr: %r)" % proc.stderr
    assert _facet(payload, "reader") == "pass"


def test_c03_reader_face_is_not_applicable_without_paths(tmp_path):
    spec = _spec_dir(tmp_path)
    proc, payload = _verify("--spec-dir", str(spec), "--faces", "reader")
    assert proc.returncode == 0, "no --path leaves the reader face not applicable"
    assert _facet(payload, "reader") == "not-applicable", (
        "the reader face must be explicitly not-applicable when no --path is given"
    )


# --------------------------------------------------------------------------- #
# C-3 — evidence rules
# --------------------------------------------------------------------------- #
def _evidence_doc(tmp_path: Path, annotation: str, name: str = "doc.md") -> Path:
    return _write(
        tmp_path / name,
        "# Doc\n\n**Readers**: 迁移评审者。\n**Reading scenario**: 合并前核对。\n\n"
        "该切片把两个引擎放在框架源里（证据：%s）。\n" % annotation,
    )


def test_c04_evidence_grade_asof_unpaired(tmp_path):
    doc = _evidence_doc(tmp_path, "实测，source: `pytest -q` exit 0")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "grade-asof-unpaired" in _rules(payload), (
        "a grade without as-of must report grade-asof-unpaired, got %r" % _rules(payload)
    )


def test_c04_evidence_asof_malformed(tmp_path):
    doc = _evidence_doc(tmp_path, "实测，as-of 2026/10/24，source: `pytest -q` exit 0")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "as-of-malformed" in _rules(payload)


def test_c04_evidence_grade_invalid(tmp_path):
    doc = _evidence_doc(tmp_path, "观察，as-of 2026-10-24，source: `pytest -q` exit 0")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "grade-invalid" in _rules(payload), (
        "a grade outside 实测/推断/引用 must report grade-invalid, got %r" % _rules(payload)
    )


def test_c04_evidence_source_missing(tmp_path):
    doc = _evidence_doc(tmp_path, "实测，as-of 2026-10-24")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "source-missing" in _rules(payload), (
        "an annotation without source must report source-missing, got %r" % _rules(payload)
    )


def test_c04_evidence_source_empty_value(tmp_path):
    doc = _evidence_doc(tmp_path, "实测，as-of 2026-10-24，source: ")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "source-missing" in _rules(payload), "an empty source value is source-missing"


def test_c04_evidence_asof_stale_against_last_commit(tmp_path):
    repo = _git_repo(tmp_path / "repo")
    doc = _evidence_doc(repo, "实测，as-of 2000-01-01，source: `pytest -q` exit 0")
    _git_commit_all(repo)
    # The working tree is clean and the last commit is today; an as-of in 2000 is stale.
    proc, payload = _verify("--path", "doc.md", "--faces", "evidence", cwd=repo)
    assert proc.returncode == 1, (
        "an as-of older than the file's last commit must fail (stdout: %r)" % proc.stdout[:600]
    )
    assert "as-of-stale" in _rules(payload), (
        "expected as-of-stale, got %r" % _rules(payload)
    )


def test_c04_evidence_asof_fresh_against_last_commit(tmp_path):
    repo = _git_repo(tmp_path / "repo")
    doc = _evidence_doc(repo, "实测，as-of 2026-10-24，source: `pytest -q` exit 0")
    _git_commit_all(repo)
    commit_date = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", "doc.md"],
        cwd=str(repo), check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", commit_date), (
        "fixture precondition: the doc must have a commit date, got %r" % commit_date
    )
    # Rewrite the annotation to the file's last commit date: equal is fresh.
    _evidence_doc(repo, "实测，as-of %s，source: `pytest -q` exit 0" % commit_date)
    proc, payload = _verify("--path", "doc.md", "--faces", "evidence", cwd=repo)
    assert "as-of-stale" not in _rules(payload), (
        "an as-of equal to the last commit date is fresh; got %r" % _rules(payload)
    )
    assert _facet(payload, "evidence") == "pass", (
        "a fresh, fully annotated line must pass the evidence face (stdout: %r)"
        % proc.stdout[:600]
    )


def test_c04_evidence_asof_stale_not_evaluated_outside_git(tmp_path):
    doc = _evidence_doc(tmp_path, "实测，as-of 2000-01-01，source: `pytest -q` exit 0")
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert "as-of-stale" not in _rules(payload), (
        "outside git the staleness rule must not fire as a finding"
    )
    assert _facet(payload, "evidence") == "not-evaluated", (
        "outside git the evidence face must be explicitly not-evaluated, never pass"
    )
    assert proc.returncode == 0, "non-strict not-evaluated does not change the exit code"
    strict = _run(
        "--action", "verify", "--format", "json",
        "--path", str(doc), "--faces", "evidence", "--strict",
    )
    assert strict.returncode == 1, "--strict must upgrade a not-evaluated evidence face to exit 1"


def test_c04_evidence_clean_annotation_passes(tmp_path):
    repo = _git_repo(tmp_path / "repo")
    _evidence_doc(repo, "实测，as-of 2026-10-24，source: `pytest -q` exit 0")
    _git_commit_all(repo)
    commit_date = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", "doc.md"],
        cwd=str(repo), check=True, capture_output=True, text=True,
    ).stdout.strip()
    _evidence_doc(repo, "实测，as-of %s，source: `pytest -q` exit 0" % commit_date)
    proc, payload = _verify("--path", "doc.md", "--faces", "evidence", cwd=repo)
    assert proc.returncode == 0, (
        "a complete three-piece annotation must pass (stdout: %r)" % proc.stdout[:600]
    )
    assert _facet(payload, "evidence") == "pass"


# --------------------------------------------------------------------------- #
# C-5 — duplicate fact (SC-007 injection 1)
# --------------------------------------------------------------------------- #
def _owner_sentence() -> str:
    for line in OWNER_GUIDELINE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if len(stripped) >= 80 and not stripped.startswith("#") and not stripped.startswith("|"):
            return stripped
    raise AssertionError("fixture precondition: no >= 80 char sentence found in the owner")


def test_c05_copied_owner_text_is_reported_as_duplicate_fact(tmp_path):
    sentence = _owner_sentence()
    doc = _write(
        tmp_path / "doc.md",
        "# Doc\n\n**Readers**: 迁移评审者。\n**Reading scenario**: 合并前核对。\n\n"
        + sentence + "\n",
    )
    proc, payload = _verify("--path", str(doc), "--faces", "duplicate")
    assert proc.returncode == 1, "a copied owner sentence must fail the duplicate face"
    findings = [f for f in _findings(payload) if f.get("rule") == "duplicate-fact"]
    assert findings, "expected duplicate-fact, got %r" % _rules(payload)
    hit = next(f for f in findings if f.get("path", "").endswith("doc.md"))
    assert hit.get("line"), "the finding must locate the copied line"
    assert hit.get("counterpart"), "the finding must locate the other side (counterpart)"
    assert "one-source-of-truth.md" in str(hit.get("counterpart")) or (
        "one-source-of-truth.md" in str(hit.get("path"))
    ), "the counterpart must point at the owner document: %r" % hit
    assert hit.get("fix_direction"), "duplicate findings must carry a fix direction"


def test_c05_s3_owner_set_is_the_reference_side_only(tmp_path):
    """S3 is the *counterpart* side (C-2), never a subject of its own comparison.

    The face owners legitimately share machine-regenerated blocks (the compiled
    Wrap-up step list is one registry projection appearing in several skills);
    auditing S3 against itself would report them as hand-written copies. A clean
    spec dir scanned with the duplicate face must therefore stay silent.
    """
    spec = _spec_dir(tmp_path)
    proc, payload = _verify("--spec-dir", str(spec), "--faces", "duplicate")
    findings = _duplicates(payload)
    assert findings == [], (
        "the face-owner set is the comparison side; its own shared/generated blocks "
        "must not be reported as duplicates: %r" % findings[:3]
    )
    assert proc.returncode == 0


# --------------------------------------------------------------------------- #
# C-6 — count face is delegated (SC-007 injection 3)
# --------------------------------------------------------------------------- #
def test_c06_injected_count_mismatch_is_reported(tmp_path):
    spec = _spec_dir(tmp_path)
    plan = spec / "plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8") + "\nThis plan asserts 5 FR in total.\n",
        encoding="utf-8",
    )
    proc, payload = _verify("--spec-dir", str(spec), "--faces", "count")
    assert proc.returncode == 1, (
        "a hand-written count that disagrees with the definitions must fail "
        "(stdout: %r)" % proc.stdout[:600]
    )
    assert "count-mismatch" in _rules(payload), (
        "expected count-mismatch via delegation, got %r" % _rules(payload)
    )
    assert payload["count_check"]["status"] == "delegated"


def test_c06_unavailable_delegation_is_explicit_not_run(tmp_path):
    spec = tmp_path / "specs" / "001-incomplete"
    _write(spec / "requirements.md", "# Requirements\n\n- **FR-001**: only one.\n")
    proc, payload = _verify("--spec-dir", str(spec), "--faces", "count")
    assert proc.returncode == 0, "non-strict not-run does not change the exit code"
    count_check = payload["count_check"]
    assert count_check["status"] == "not-run", (
        "an unavailable delegation must be explicitly not-run, got %r" % count_check
    )
    assert count_check.get("reason"), "not-run must carry a reason"
    strict = _run(
        "--action", "verify", "--format", "json",
        "--spec-dir", str(spec), "--faces", "count", "--strict",
    )
    assert strict.returncode == 1, "--strict must treat an unavailable count face as a failure"


# --------------------------------------------------------------------------- #
# C-8 — exit codes
# --------------------------------------------------------------------------- #
def test_c08_exit_zero_never_carries_a_finding(tmp_path):
    doc = _write(tmp_path / "doc.md", "# Doc\n\n没有任何读者声明。\n")
    proc, payload = _verify("--path", str(doc), "--faces", "reader")
    assert _findings(payload), "fixture must produce at least one finding"
    assert proc.returncode == 1, "findings must never exit 0"


def test_c02_unreadable_path_is_an_input_error(tmp_path):
    proc = _run(
        "--action", "verify", "--format", "json",
        "--path", str(tmp_path / "missing.md"), "--faces", "reader",
    )
    assert proc.returncode == 2, "an unreadable --path is an input error (exit 2)"


def test_c02_checker_is_read_only(tmp_path):
    doc = _write(tmp_path / "doc.md", CLEAN_DOC)
    before = hashlib.sha256(doc.read_bytes()).hexdigest()
    _run("--action", "verify", "--format", "json", "--path", str(doc), "--faces", "reader,evidence")
    after = hashlib.sha256(doc.read_bytes()).hexdigest()
    assert before == after, "the checker must never modify the checked document"
    assert not (tmp_path / "doc.md.json").exists()
