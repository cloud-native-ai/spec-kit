"""Contract tests for the six expression faces (069b, T016).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md``
C-11…C-13 that ``tasks.md`` T016 names:

* C-11 ``--action faces`` parses ``shared/workflow/expression-gates.md`` § 六面:
  exactly six data rows, unique face ids, exactly **one** ``owner_pointer`` cell
  per row (a cell joining several paths with ``+`` is still one binding), every
  path resolvable in the source root or the ``.specify/`` mirror, and every
  ``§ <anchor>`` matching a heading of that file. Violations are
  ``faces-count`` / ``faces-duplicate`` / ``faces-pointer-missing`` /
  ``faces-unresolvable``; the JSON top level carries ``faces``.
* C-12 no file outside the six-face table pairs ≥3 face ids with owner paths
  (a second binding table) — ``faces-second-table``.
* C-13 the criterion-text copy count is measured by the existing
  ``doc-consistency-check.py --faces duplicate`` with the comparison side
  narrowed to the classification owner (``--owner-path``) over the declared
  subject surface — ``shared/`` + ``templates/commands/`` + ``skills/`` +
  ``docs/`` + this spec's formal artifacts — and must be ``[]``. Copies in a
  command template, a skill or the docs tree turn it red (injected below); the
  earlier "owner + spec artifacts only" scope could not see them. The default
  S3 owner set (nine owner paths, six binding cells) stays the comparison side
  for every other consumer, and ``shared/workflow/expression-gates.md`` belongs
  to it — it MUST NOT become the classification owner's subject.

Injection fixtures live in ``tmp_path`` (delete a row, duplicate a row, an
unresolvable path, an empty pointer cell, a mismatched anchor, a second table).
Red-first (Constitution IV): 069a's engine has no ``faces`` action yet, so the
engine assertions red as "action missing" — never as an import or collection
error. ``_run`` asserts the script path first.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
GATES = REPO_ROOT / "shared" / "workflow" / "expression-gates.md"
OWNER = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"
DOC_CHECK = REPO_ROOT / "scripts" / "python" / "doc-consistency-check.py"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "069b-isomorphism-migration-metrics"

GATES_REL = Path("shared") / "workflow" / "expression-gates.md"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
COMMANDS_REL = Path("templates") / "commands"

FACE_SECTION_KEYWORD = "六面"
FACE_TABLE_HEADER = ("面（中文）", "face id", "owner_pointer")
FACES = (
    "requirements-clarity",
    "reader-purpose",
    "evidence-asof",
    "structure-links-build",
    "fact-consistency",
    "review",
)
BACKTICK_RE = re.compile(r"`([^`]+)`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected from 069a. "
        "Red is the intended pre-implementation state for 069b T016."
        % ENGINE.relative_to(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _faces(root: Path):
    proc = _run("--action", "faces", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def _kinds(record: dict) -> list[str]:
    return [finding.get("kind") for finding in record.get("findings", [])]


def _face_rows(text: str) -> list[list[str]]:
    """Data rows of the first table inside § 六面 (independent oracle)."""
    lines = text.splitlines()
    body: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = FACE_SECTION_KEYWORD in line
            continue
        if inside:
            body.append(line)
    header = None
    rows: list[list[str]] = []
    for line in body:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if header and len(cells) == len(header):
            rows.append(cells)
    return rows


def _pointer_paths(cell: str) -> list[tuple[str, str | None]]:
    """Split one owner_pointer cell into (path, anchor) pairs.

    A cell joins several paths with ``+``; each segment carries its own optional
    ``§ <anchor>`` (C-11: the whole cell is still one binding).
    """
    pairs: list[tuple[str, str | None]] = []
    for segment in cell.split("+"):
        match = BACKTICK_RE.search(segment)
        if not match:
            continue
        path = match.group(1).strip()
        anchor = None
        if "§" in segment:
            tail = segment.split("§", 1)[1]
            anchor = tail.split("+", 1)[0]
            anchor = BACKTICK_RE.sub("", anchor)
            anchor = re.sub(r"[（(].*?[）)]", "", anchor).strip()
            anchor = anchor.strip("` ").strip()
        pairs.append((path, anchor or None))
    return pairs


def _resolves(root: Path, rel: str) -> Path | None:
    for candidate in (root / rel, root / ".specify" / rel):
        if candidate.is_file():
            return candidate
    return None


def _anchor_matches(path: Path, anchor: str) -> bool:
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match and anchor in match.group(2):
            return True
    return False


def _gates_doc(rows: list[tuple[str, str, str]]) -> str:
    lines = [
        "# Expression Gates (069b faces fixture)",
        "",
        "fixture: the only file that may carry the six-face table.",
        "",
        "## 六面（封闭集）",
        "",
        "| " + " | ".join(FACE_TABLE_HEADER) + " |",
        "| " + " | ".join("---" for _ in FACE_TABLE_HEADER) + " |",
    ]
    for label, face_id, pointer in rows:
        lines.append("| %s | %s | %s |" % (label, face_id, pointer))
    lines.extend(["", "## 阶段算子表", "", "fixture: no operator rows.", ""])
    return "\n".join(lines)


def _valid_rows() -> list[tuple[str, str, str]]:
    return [
        ("需求清晰度", "requirements-clarity", "`shared/guidelines/a.md` § Section A"),
        ("读者/目的/边界", "reader-purpose", "`shared/guidelines/b.md` § Section B"),
        ("证据分级与 as-of", "evidence-asof", "`shared/workflow/expression-gates.md` § 阶段算子表"),
        (
            "结构/链接/构建",
            "structure-links-build",
            "`shared/guidelines/a.md` + `shared/guidelines/b.md`",
        ),
        ("事实一致性", "fact-consistency", "`shared/guidelines/c.md`"),
        ("评审", "review", "`shared/guidelines/mirror-only.md` § Mirror Section"),
    ]


def _build_faces_repo(root: Path, rows: list[tuple[str, str, str]] | None = None) -> None:
    used = _valid_rows() if rows is None else rows
    _write(root / GATES_REL, _gates_doc(used))
    _write(root / "templates" / "commands" / "docs.md", "# /speckit.docs\n\nfixture template\n")
    _write(root / "shared" / "guidelines" / "a.md", "# A\n\n## Section A\n\nfixture\n")
    _write(root / "shared" / "guidelines" / "b.md", "# B\n\n## Section B\n\nfixture\n")
    _write(root / "shared" / "guidelines" / "c.md", "# C\n\nfixture prose only\n")
    # Mirror-only resolution: the source-root path does not exist.
    _write(root / ".specify" / "shared" / "guidelines" / "mirror-only.md", "# M\n\n## Mirror Section\n\nfixture\n")


# --------------------------------------------------------------------------- #
# real tree: six rows, unique ids, one pointer cell each, all resolvable
# --------------------------------------------------------------------------- #
def test_real_face_table_has_exactly_six_unique_bindings():
    text = GATES.read_text(encoding="utf-8")
    rows = _face_rows(text)
    assert len(rows) == 6, "§ 六面 MUST carry exactly six data rows (C-11); got %d" % len(rows)
    ids = [row[1] for row in rows]
    assert len(set(ids)) == 6, "face ids MUST be unique (C-11); got %r" % ids
    assert set(ids) == set(FACES), "unexpected face id set: %r" % sorted(ids)
    for row in rows:
        pointer_cells = [cell for cell in row[2:] if cell.strip()]
        assert len(row) == 3 and len(pointer_cells) == 1, (
            "each face row MUST carry exactly one owner_pointer cell (C-11); got %r" % (row,)
        )
        assert _pointer_paths(row[2]), "empty owner_pointer for %r (C-11)" % row[1]


def test_real_face_paths_and_anchors_resolve():
    for row in _face_rows(GATES.read_text(encoding="utf-8")):
        face_id, cell = row[1], row[2]
        for rel, anchor in _pointer_paths(cell):
            resolved = _resolves(REPO_ROOT, rel)
            assert resolved is not None, (
                "face %r points at an unresolvable path %r (C-11)" % (face_id, rel)
            )
            if anchor:
                assert _anchor_matches(resolved, anchor), (
                    "face %r anchor %r has no matching heading in %s (C-11)"
                    % (face_id, anchor, rel)
                )


def test_faces_action_reports_six_faces_and_zero_findings():
    proc, record = _faces(REPO_ROOT)
    assert proc.returncode == 0, (
        "faces on the real tree must exit 0; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None
    assert record.get("faces") == 6, (
        "the JSON top level MUST carry `faces` = 6 (C-11); got %r" % record.get("faces")
    )
    assert record.get("findings") == [], "the real face table must be defect-free (C-11)"


# --------------------------------------------------------------------------- #
# C-13: the duplicate face over the closed subject set
# --------------------------------------------------------------------------- #
# C-13: the declared subject surface. A copy in a command template, a skill or
# the docs tree is exactly what the criterion must be able to see — the earlier
# "owner + spec artifacts" scope could not (review F4).
DECLARED_SUBJECT_ROOTS = ("shared", "templates/commands", "skills", "docs")


def _run_duplicate(*paths: str) -> tuple[subprocess.CompletedProcess, dict]:
    args = [
        sys.executable,
        str(DOC_CHECK),
        "--action",
        "verify",
        "--faces",
        "duplicate",
        "--owner-path",
        OWNER_REL.as_posix(),
    ]
    for path in paths:
        args.extend(["--path", path])
    args.extend(["--spec-dir", str(SPEC_DIR), "--format", "json"])
    proc = subprocess.run(args, cwd=str(REPO_ROOT), capture_output=True, text=True)
    assert proc.stdout.strip(), (
        "doc-consistency-check must print JSON; stderr=%r" % proc.stderr
    )
    return proc, json.loads(proc.stdout)


def _longest_owner_line(min_length: int = 48) -> str:
    """A distinctive criterion line that the duplicate face can compare."""
    best = ""
    for raw in OWNER.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("|") or stripped.startswith("#"):
            continue
        if len(re.sub(r"\s+", " ", stripped)) < min_length:
            continue
        if len(stripped) > len(best):
            best = stripped
    assert best, "the owner must carry at least one long prose line"
    return best


def test_duplicate_face_is_clean_over_the_declared_wide_scope():
    proc, record = _run_duplicate(*DECLARED_SUBJECT_ROOTS)
    assert record.get("findings") == [], (
        "the criterion-text copy count must be zero over the declared subject "
        "surface (C-13: shared/ + templates/commands/ + skills/ + docs/ + this "
        "spec); got %r" % record.get("findings")
    )
    assert proc.returncode == 0
    scanned = record.get("scope", {}).get("files_scanned", 0)
    assert scanned > 100, (
        "the declared scope must actually scan the command/skill/docs surfaces; "
        "only %d files were scanned" % scanned
    )
    assert record["scope"].get("owners") == [OWNER_REL.as_posix()], (
        "the comparison side must be the classification owner itself; got %r"
        % record["scope"].get("owners")
    )


def test_a_copied_criterion_line_in_each_surface_turns_red(tmp_path):
    """A copy placed in templates/commands, skills or docs must not stay green."""
    line = _longest_owner_line()
    surfaces = {
        "templates/commands": tmp_path / "templates" / "commands" / "copy.md",
        "skills": tmp_path / "skills" / "external" / "copy" / "SKILL.md",
        "docs": tmp_path / "docs" / "copy.md",
    }
    for label, path in surfaces.items():
        _write(path, "# copied criterion\n\n%s\n" % line)
        proc, record = _run_duplicate(str(path.parent))
        assert proc.returncode == 1, (
            "a criterion copy under %s must turn the duplicate face red; got "
            "findings=%r" % (label, record.get("findings"))
        )
        hits = [
            finding
            for finding in record.get("findings", [])
            if finding.get("path", "").endswith(path.name)
            or (finding.get("counterpart") or "").startswith(str(path))
        ]
        assert hits, (
            "the finding must point at the copy under %s; got %r"
            % (label, record.get("findings"))
        )


def test_s3_owner_set_is_the_comparison_side_not_a_subject():
    module = _load_module(DOC_CHECK, "doc_consistency_check_069b")
    owner_paths = list(getattr(module, "OWNER_PATHS"))
    assert len(owner_paths) == 9, (
        "the S3 comparison set MUST stay the nine declared owner paths (C-13); got %d: %r"
        % (len(owner_paths), owner_paths)
    )
    assert "shared/workflow/expression-gates.md" in owner_paths
    assert OWNER_REL.as_posix() not in owner_paths, (
        "the classification owner MUST be a subject, never a comparison-side owner (C-13)"
    )


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- #
# injections
# --------------------------------------------------------------------------- #
def test_valid_fixture_is_green(tmp_path):
    _build_faces_repo(tmp_path)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 0, (
        "a well-formed six-row fixture must exit 0; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None
    assert record.get("faces") == 6
    assert record.get("findings") == []


def test_deleted_row_reports_faces_count(tmp_path):
    rows = _valid_rows()[:-1]
    _build_faces_repo(tmp_path, rows)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1, "a five-row face table must exit 1"
    assert record is not None
    assert "faces-count" in _kinds(record), (
        "five rows MUST be `faces-count` (C-11); got %r" % _kinds(record)
    )


def test_duplicated_row_reports_faces_duplicate(tmp_path):
    rows = _valid_rows() + [_valid_rows()[0]]
    _build_faces_repo(tmp_path, rows)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-duplicate" in _kinds(record), (
        "a repeated face id MUST be `faces-duplicate` (C-11); got %r" % _kinds(record)
    )


def test_unresolvable_path_reports_faces_unresolvable(tmp_path):
    rows = _valid_rows()
    rows[0] = (rows[0][0], rows[0][1], "`shared/guidelines/does-not-exist.md` § Section A")
    _build_faces_repo(tmp_path, rows)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-unresolvable" in _kinds(record), (
        "a nonexistent pointer path MUST be `faces-unresolvable` (C-11); got %r"
        % _kinds(record)
    )


def test_unmatched_anchor_reports_faces_unresolvable(tmp_path):
    rows = _valid_rows()
    rows[0] = (rows[0][0], rows[0][1], "`shared/guidelines/a.md` § Section Not There")
    _build_faces_repo(tmp_path, rows)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-unresolvable" in _kinds(record), (
        "an anchor without a matching heading MUST be `faces-unresolvable` (C-11); got %r"
        % _kinds(record)
    )


def test_empty_pointer_cell_reports_faces_pointer_missing(tmp_path):
    rows = _valid_rows()
    rows[2] = (rows[2][0], rows[2][1], "")
    _build_faces_repo(tmp_path, rows)
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-pointer-missing" in _kinds(record), (
        "an empty owner_pointer cell MUST be `faces-pointer-missing` (C-11); got %r"
        % _kinds(record)
    )


def test_second_binding_table_reports_faces_second_table(tmp_path):
    _build_faces_repo(tmp_path)
    _write(
        tmp_path / "shared" / "definitions" / "second-face-table.md",
        "\n".join(
            [
                "# Second binding table (fixture)",
                "",
                "| face | owner |",
                "| --- | --- |",
                "| requirements-clarity | `shared/guidelines/a.md` |",
                "| reader-purpose | `shared/guidelines/b.md` |",
                "| evidence-asof | `shared/guidelines/c.md` |",
                "",
            ]
        ),
    )
    proc, record = _faces(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "faces-second-table" in _kinds(record), (
        "a ≥3-row face/path table outside § 六面 MUST be `faces-second-table` (C-12); "
        "got %r" % _kinds(record)
    )


def test_faces_is_read_only(tmp_path):
    import hashlib

    _build_faces_repo(tmp_path)
    before = {
        path.relative_to(tmp_path).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(tmp_path.rglob("*"))
        if path.is_file()
    }
    _faces(tmp_path)
    after = {
        path.relative_to(tmp_path).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(tmp_path.rglob("*"))
        if path.is_file()
    }
    assert before == after, "faces MUST NOT write, cache or create files (C-15)"


def test_faces_on_a_payload_root_is_framework_source_required(tmp_path):
    payload = tmp_path / "project"
    _write(payload / ".specify" / GATES_REL, _gates_doc(_valid_rows()))
    _write(
        payload / ".specify" / OWNER_REL,
        "\n".join(
            [
                "# fixture owner",
                "",
                "## 逐流程台账",
                "",
                "**台账版本**: 1（2026-10-25）",
                "",
                "| unit_id | flow_class | basis | neutral | notes |",
                "| --- | --- | --- | --- | --- |",
                "",
            ]
        ),
    )
    proc, record = _faces(payload)
    assert proc.returncode == 2, "a payload root MUST exit 2 (C-14)"
    assert record is not None
    assert record.get("findings") == []
    assert (record.get("error") or {}).get("label") == "framework-source-required", (
        "expected framework-source-required; got %r" % (record.get("error"),)
    )
