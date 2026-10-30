"""Unit tests for the ``spec:`` key family of ``scripts/python/flow-class-check.py`` (077, T002).

Owns the engine-side details of
``.specify/specs/077-doc-sdd-integration/contracts/class-resolution.md`` that a
whole-repository contract test cannot isolate:

* key grammar ``^spec:[a-z0-9][a-z0-9-]*$`` — a bare directory name,
  ``feature:<ID>`` and any ``/``-bearing path form stay exit code 2 and never
  yield a decided class;
* resolution location — ``<repo>/.specify/specs/<name>/requirements.md``, with
  the second hat (``--repo`` naming ``.specify`` itself) degrading to
  ``<repo>/specs/<name>/requirements.md``;
* a missing spec directory (or a directory without ``requirements.md``) is exit
  code 2, never a silently-typed class;
* the record is **field-for-field identical** to a unit-key record: ten keys
  (``action`` / ``checked_at`` / ``unit_id`` / ``flow_class`` / ``source`` /
  ``marker`` / ``basis`` / ``neutral`` / ``error``); ``unit_id`` is the key
  verbatim; ``source`` is ``declaration`` or ``default`` (never ``ledger``);
  ``basis`` is ``null`` and ``neutral`` is ``false``;
* the three exit-code segments: 0 = resolved (declared, or undeclared on the
  default), 1 = declared value outside the closed set, 2 = invalid key / missing
  spec directory / unparsable owner — 1 and 2 are never merged;
* every exit-2 outcome of an in-family ``spec:`` key carries the one closed
  ``owner-unavailable`` label and ``flow_class: null`` (``contracts/
  class-resolution.md`` C-003 / C-006 / C-007): a missing spec directory or an
  unreadable ``requirements.md`` must never read as ``invalid-unit-id`` (the key
  is legal) nor hand a consumer a decided class; the distinguishing cause lives
  in ``error.detail``;
* owner resolution precedes key-grammar matching (the registered change in
  ``requirements.md`` FR-011 exemption ①): with the owner unavailable, *any* key
  exits 2 with the same ``owner-unavailable`` label;
* a spec declaration never enters the per-unit ledger (the owner document is
  byte-identical after a ``spec:`` lookup, and the answer is never
  ``source: ledger``);
* both actions remain read-only.

Fixtures are built from scratch in ``tmp_path`` with literal text; no test
touches the real owner, the real ledger or the real ``.specify/specs/`` tree.
Red-first (Constitution IV): the engine does not understand ``spec:`` keys yet —
``spec:<dir>`` exits 2 with ``invalid-unit-id`` today (see
``test-evidence/plan-resolution-baseline.txt``), so the declaration group below
is the intended pre-implementation red.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"

# requirements.md § Shared Strings (pinned copies; the test may pin literals).
DEFAULT_MARKER = "未声明·按默认"   # 069 § Shared Strings, [[STR-004]]
RECORD_FIELDS = {
    "action",
    "checked_at",
    "unit_id",
    "flow_class",
    "flow_type",
    "source",
    "marker",
    "basis",
    "neutral",
    "error",
}
EXIT_2_LABELS = {"invalid-unit-id", "owner-unavailable"}
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

# A minimal but parsable owner document: one ledger row, the four required
# columns (unit_id / flow_class / basis / neutral) and the version declaration.
OWNER_TEXT = """# Flow Class Definitions (unit-test fixture)

本文件是 077 单元测试的临时夹具，不是仓库所有者。

## 逐流程台账

**台账版本**: 1（2026-10-30）

| unit_id | flow_class | basis | neutral |
|---------|------------|-------|---------|
| /speckit.implement | execution | mixed-oracle | |
"""

DECLARED = "# fixture spec\n\n**Flow Class**: expression\n\n## Related Feature *(mandatory)*\n\n**Feature ID**: 999\n"
UNDECLARED = "# fixture spec\n\n## Related Feature *(mandatory)*\n\n**Feature ID**: 999\n"
INVALID_VALUE = "# fixture spec\n\n**Flow Class**: expressive\n\n## Related Feature *(mandatory)*\n"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s" % ENGINE.relative_to(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _lookup(repo: Path, unit_id: str) -> subprocess.CompletedProcess:
    return _run("--repo", str(repo), "--action", "lookup", "--unit-id", unit_id,
                "--format", "json")


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON record on stdout, got empty output (stderr: %r)"
        % proc.stderr
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


def _make_repo(tmp_path: Path, *, with_owner: bool = True) -> Path:
    """Materialise a repo covering both hats (source root and payload root)."""
    repo = tmp_path / "repo"
    (repo / "templates" / "commands").mkdir(parents=True, exist_ok=True)
    if with_owner:
        _write(repo / "shared" / "definitions" / "flow-class-definitions.md", OWNER_TEXT)
        _write(
            repo / ".specify" / "shared" / "definitions" / "flow-class-definitions.md",
            OWNER_TEXT,
        )
    return repo


def _add_spec(repo: Path, name: str, text: str) -> Path:
    directory = repo / ".specify" / "specs" / name
    _write(directory / "requirements.md", text)
    return directory


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


# --------------------------------------------------------------------------- #
# A. key grammar — the two existing families keep working, spec: is exact
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "unit_id",
    [
        "077-doc-sdd-integration",          # bare directory name
        "feature:077",                      # Feature key is never a line key
        "spec:077-doc-sdd-integration/requirements",  # path form
        "spec:../077-doc-sdd-integration",  # traversal form
        "spec:",                            # empty
        "spec:-leading-hyphen",             # grammar starts with [a-z0-9]
        "spec:Uppercase",                   # grammar is lower-case
        "spec:under_score",                 # underscore is not in the grammar
        "Spec:077",                         # prefix is case sensitive
    ],
)
def test_key_grammar_rejects_bare_feature_and_path_forms(tmp_path, unit_id):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "077-doc-sdd-integration", DECLARED)

    proc = _lookup(repo, unit_id)

    assert proc.returncode == 2, (
        "%r must not be accepted as a spec key (stdout=%r)"
        % (unit_id, proc.stdout)
    )
    record = _json(proc)
    assert record["unit_id"] == unit_id
    assert record["source"] == "default"
    assert record["flow_class"] != "expression"
    assert record["marker"] is None, (
        "the undeclared marker is reserved for a parsed-but-absent declaration"
    )
    assert record["error"] and record["error"]["label"] in EXIT_2_LABELS


def test_existing_unit_key_still_resolves_from_the_ledger(tmp_path):
    repo = _make_repo(tmp_path)

    proc = _lookup(repo, "/speckit.implement")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "execution"
    assert record["source"] == "ledger"
    assert record["basis"] == "mixed-oracle"


def test_valid_spec_key_is_not_rejected_as_an_invalid_unit_id(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)

    proc = _lookup(repo, "spec:fx-declared")

    assert proc.returncode != 2, (
        "a well-formed spec: key pointing at an existing spec directory must "
        "resolve (stderr=%r)" % proc.stderr
    )
    record = _json(proc)
    assert (record.get("error") or {}).get("label") != "invalid-unit-id"


# --------------------------------------------------------------------------- #
# B. resolution location — two hats, and a spec directory that must exist
# --------------------------------------------------------------------------- #
def test_resolves_under_the_dot_specify_specs_directory(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)

    proc = _lookup(repo, "spec:fx-declared")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "expression"
    assert record["source"] == "declaration"


def test_resolves_when_repo_names_dot_specify_itself(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)

    source_hat = _lookup(repo, "spec:fx-declared")
    payload_hat = _lookup(repo / ".specify", "spec:fx-declared")

    assert source_hat.returncode == 0, source_hat.stderr
    assert payload_hat.returncode == 0, payload_hat.stderr
    assert _json(source_hat)["flow_class"] == _json(payload_hat)["flow_class"]
    assert _json(source_hat)["source"] == _json(payload_hat)["source"]
    assert _json(source_hat)["unit_id"] == _json(payload_hat)["unit_id"] == "spec:fx-declared"


def test_missing_spec_directory_exits_2_without_a_decided_class(tmp_path):
    """C-003 / C-006: exit 2, no class value, the closed degradation label.

    A later review round found this path labelled ``invalid-unit-id`` with a
    decided ``flow_class: execution`` — the key is well formed, so the label
    pointed at the wrong thing, and the class contradicted C-003's "MUST NOT
    return any class value". Both halves are asserted here: the record carries
    no class, and the label is the one the dispatch payload's closed domain
    (``{owner-unavailable, -}``) can carry.
    """
    repo = _make_repo(tmp_path)

    proc = _lookup(repo, "spec:does-not-exist")

    assert proc.returncode == 2, (
        "a spec key whose directory is absent must exit 2 (stdout=%r)"
        % proc.stdout
    )
    record = _json(proc)
    assert record["source"] == "default"
    assert record["marker"] is None
    assert record["flow_class"] is None, (
        "C-003: exit 2 MUST NOT return any class value — a misspelled spec key "
        "must not read as a firm `execution`; got %r"
        % (record["flow_class"],)
    )
    assert record["error"] and record["error"]["label"] == "owner-unavailable", (
        "a missing spec input is the same degradation branch as an absent owner "
        "(FR-009 class ③) and must stay inside the payload's two-value error "
        "domain; label=%r" % ((record["error"] or {}).get("label"),)
    )
    assert "spec input not found" in record["error"]["detail"], (
        "the distinguishing cause belongs in detail: %r"
        % record["error"]["detail"]
    )
    assert proc.stderr.startswith("owner-unavailable:"), (
        "the stage card prints the label verbatim, so stderr must carry it: %r"
        % proc.stderr
    )


def test_existing_spec_directory_without_requirements_exits_2(tmp_path):
    repo = _make_repo(tmp_path)
    (repo / ".specify" / "specs" / "fx-empty").mkdir(parents=True)

    proc = _lookup(repo, "spec:fx-empty")

    assert proc.returncode == 2
    record = _json(proc)
    assert record["error"] is not None
    assert record["flow_class"] is None, (
        "C-003 holds on every exit-2 input path, not only on the missing-dir one"
    )


def test_spec_key_without_an_existing_directory_never_reads_the_ledger(tmp_path):
    """A missing spec dir must not fall back to a ledger row of the same name."""
    repo = _make_repo(tmp_path)
    _write(
        repo / "shared" / "definitions" / "flow-class-definitions.md",
        OWNER_TEXT.replace(
            "| /speckit.implement | execution | mixed-oracle | |",
            "| spec:ghost | expression | reader-oracle | |",
        ),
    )
    _write(
        repo / ".specify" / "shared" / "definitions" / "flow-class-definitions.md",
        OWNER_TEXT.replace(
            "| /speckit.implement | execution | mixed-oracle | |",
            "| spec:ghost | expression | reader-oracle | |",
        ),
    )

    proc = _lookup(repo, "spec:ghost")

    assert proc.returncode == 2, (
        "a spec key is never answered from the ledger (stdout=%r)" % proc.stdout
    )
    assert _json(proc)["source"] != "ledger"


# --------------------------------------------------------------------------- #
# C. record shape — nine fields, unit-key identical
# --------------------------------------------------------------------------- #
def test_record_carries_exactly_the_ten_unit_key_fields(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-absent", UNDECLARED)

    proc = _lookup(repo, "spec:fx-absent")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert set(record) == RECORD_FIELDS, (
        "the spec record must be field-for-field identical to a unit-key "
        "record: extra=%r missing=%r"
        % (sorted(set(record) - RECORD_FIELDS), sorted(RECORD_FIELDS - set(record)))
    )
    assert record["action"] == "lookup"
    assert ISO_Z_RE.match(record["checked_at"]), record["checked_at"]
    assert record["unit_id"] == "spec:fx-absent"
    assert record["flow_class"] == "execution"
    assert record["source"] == "default"
    assert record["marker"] == DEFAULT_MARKER
    assert record["basis"] is None
    assert record["neutral"] is False
    assert record["error"] is None or set(record["error"]) == {"label", "detail"}


def test_declared_record_keeps_basis_null_and_neutral_false(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)

    record = _json(_lookup(repo, "spec:fx-declared"))

    assert record["basis"] is None, "the basis is the declaration line, not a ledger column"
    assert record["neutral"] is False, "the neutral list registers framework skills only"


def test_a_spec_answer_is_never_sourced_from_the_ledger(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)
    owner = repo / "shared" / "definitions" / "flow-class-definitions.md"
    before = owner.read_bytes()

    record = _json(_lookup(repo, "spec:fx-declared"))

    assert record["source"] in {"declaration", "default"}
    assert owner.read_bytes() == before, (
        "the spec declaration must never be written into the per-unit ledger"
    )


# --------------------------------------------------------------------------- #
# D. exit-code segments
# --------------------------------------------------------------------------- #
def test_declared_expression_exits_0_with_declaration_source(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)

    proc = _lookup(repo, "spec:fx-declared")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "expression"
    assert record["source"] == "declaration"
    assert record["marker"] is None, (
        "the default marker is mutually exclusive with source: declaration"
    )


def test_undeclared_spec_exits_0_with_the_default_marker(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-absent", UNDECLARED)

    proc = _lookup(repo, "spec:fx-absent")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "execution"
    assert record["source"] == "default"
    assert record["marker"] == DEFAULT_MARKER


def test_invalid_class_value_exits_1_not_2(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-bad", INVALID_VALUE)

    proc = _lookup(repo, "spec:fx-bad")

    assert proc.returncode == 1, (
        "an author typo must be exit 1 (blocking), never the exit-2 "
        "degradation path (stdout=%r stderr=%r)" % (proc.stdout, proc.stderr)
    )
    record = _json(proc)
    assert record["flow_class"] is None, (
        "exit-1 records carry no class value — a consumer that reads only the "
        "record must not see a decided class"
    )
    assert record["source"] == "declaration"
    assert "invalid-class" in proc.stderr
    assert "fx-bad" in proc.stderr and "requirements.md" in proc.stderr
    assert "expressive" in proc.stderr


def test_owner_resolution_precedes_key_grammar(tmp_path):
    repo = _make_repo(tmp_path, with_owner=False)
    _add_spec(repo, "fx-declared", DECLARED)

    spec_proc = _lookup(repo, "spec:fx-declared")
    junk_proc = _lookup(repo, "definitely-not-a-unit")

    assert spec_proc.returncode == 2
    assert junk_proc.returncode == 2
    spec_record = _json(spec_proc)
    junk_record = _json(junk_proc)
    assert spec_record["error"]["label"] == "owner-unavailable", (
        "with the owner unavailable, every key takes the same degradation label "
        "(the registered ordering change — requirements FR-011 exemption ①)"
    )
    assert junk_record["error"]["label"] == "owner-unavailable", (
        "the old order reported invalid-unit-id here; the registered change "
        "reports owner-unavailable — same exit code, same gate set"
    )
    assert spec_proc.stderr.startswith("owner-unavailable:")
    assert junk_proc.stderr.startswith("owner-unavailable:")


# --------------------------------------------------------------------------- #
# E. read-only
# --------------------------------------------------------------------------- #
def test_spec_lookup_is_read_only(tmp_path):
    repo = _make_repo(tmp_path)
    _add_spec(repo, "fx-declared", DECLARED)
    _add_spec(repo, "fx-absent", UNDECLARED)
    before = _tree_digest(repo)

    _lookup(repo, "spec:fx-declared")
    _lookup(repo, "spec:fx-absent")
    _lookup(repo, "spec:missing")

    assert _tree_digest(repo) == before
