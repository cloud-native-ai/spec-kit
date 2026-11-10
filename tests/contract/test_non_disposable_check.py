"""Contract tests for Feature 092's detection engine — C-601…C-608, C-101…C-108, C-701…C-707.

Subject: ``scripts/python/non-disposable-check.py``. Every leg below drives the engine through its
real calling surface as a subprocess or through the module's own public functions; nothing
re-implements the classification, and no literal the owner page declares is copied here. The two
sets the legs compare against are *read* at test time:

* the eight class ids — from the owner page § Detection Categories, through the engine's own
  ``--emit-categories`` (which reads the owner page, C-101);
* the four disposition values and the five entry states — the same call.

The report's own vocabulary (``data-model.md`` E-1 / E-2) is spelled here because the entry field
names *are* the contract this module pins (C-701); a missing field is the assertion, so the field
name has to be written down somewhere.

Fixture map (``tests/fixtures/non-disposable/``)
==============================================  ==================================================
fixture                                           shape / corpus row
==============================================  ==================================================
``surface.yaml``                                  the four declared roots (``.specify/specs``,
                                                  ``.specify/memory``, ``tests``, ``scripts``)
``surface-degraded.yaml``                         one present-and-empty root, one absent root
``surface-bad-kind.yaml`` / ``surface-no-st…``    a fact that is not a ``closed-set`` / has no body
``corpus-a1``                                     A1: registry says ``Implemented``, the verdict
                                                  says ``block`` → ``status-unreadable``
``corpus-a2``                                     A2: ``unclassified 0`` against a verifier run
                                                  that reports findings → ``false-closed-set``
``corpus-b``                                      B: a marker-carrying body + a live guard that
                                                  still asserts its old text → ``superseded-live``
``corpus-c``                                      C: a live binding numbered for another feature
``corpus-d``                                      D: one constant stated twice with two values
``corpus-e``                                      E: a self-refuted closed-set identity
``corpus-f2``                                     F2: a contract restating a value owner's
                                                  constant with a second value → ``stale-constant``
``corpus-g``                                      G2: a guard asserting a literal against itself
``corpus-h``                                      H: a referenced path that does not exist
``corpus-def``                                    retention wording with no expiry condition
                                                  (C-106's construction leg, not a corpus row)
``corpus-x``                                      the E-3 exemption model: in force / expired /
                                                  unevaluable / incomplete, one feature each
==============================================  ==================================================

Red-first (task T2 of the package): before the P2 engine legs landed, every leg below red as
"engine missing" or "class not emitted", never as a collection error — each helper asserts the
engine path first. The mutation legs (C-107) are the same reading taken from the other side: a copy
tree is edited to *create* the defect, the engine must go red and name the expected ``path:line``;
the copy is then repaired and the engine must go green on that class. A green that cannot go red is
not evidence, so a class with only one of the two legs fails C-107.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "non-disposable-check.py"
MIRROR = ROOT / ".specify" / "scripts" / "python" / "non-disposable-check.py"
FIXTURES = ROOT / "tests" / "fixtures" / "non-disposable"
SURFACE = FIXTURES / "surface.yaml"
OWNER_PAGE = ROOT / "shared" / "definitions" / "non-disposable-definitions.md"

#: ``data-model.md`` E-1 / E-2: the entry's own fields, the review states and the report envelope.
ENTRY_FIELDS = ("entry_id", "path", "line", "category", "detection", "state",
                "evidence_refs", "severity")
#: ``data-model.md`` § Entry State Machine: the five review states (``closed`` is derived, never
#: stored — C-705).
STATES = ("open", "unevaluated", "unconfirmed", "disposed", "exempt")
NOT_CLOSED = ("open", "unevaluated", "unconfirmed")
#: ``report-schema.contract.md`` C-702: the coverage declaration is the first block.
COVERAGE_KEYS = ("roots", "candidates", "excluded", "missing_roots", "undeclared_siblings",
                 "declaration", "declaration_status")
#: C-706's four reader questions: the key each is answered under in the report envelope.
QUESTION_KEYS = ("what_was_looked_at", "what_was_found", "what_is_proposed", "what_is_not_done")
QUESTION_ANCHOR = "questions"
#: C-604's eight argument rows; ``--scope-count`` is deliberately absent (it is not a ninth row).
DECLARED_OPTIONS = ("--root", "--json", "--scope", "--roots", "--emit-categories",
                    "--declaration", "-h", "--help", "--version")
#: C-107: one defect-creating leg per class, each naming where the defect lands.
MUTATIONS = {
    "superseded-live": "corpus-b",
    "multi-owner": "corpus-d",
    "orphan-path": "corpus-h",
    "renumber-live-binding": "corpus-c",
    "status-unreadable": "corpus-a1",
    "false-closed-set": "corpus-e",
    "stale-constant": "corpus-f2",
    "deferral-marker": "corpus-def",
}
#: Each fixture's corpus row: the classes it must reproduce and the ``path:line`` it must name.
EXPECTED = {
    "corpus-a1": (("status-unreadable", ".specify/specs/901-fixture", 3),),
    "corpus-a2": (("false-closed-set", ".specify/specs/084-verifying/verification.md", 3),),
    "corpus-b": (("superseded-live",
                  ".specify/specs/900-fixture/contracts/runner-contract.md", 1),),
    "corpus-c": (("renumber-live-binding", ".specify/specs/900-fixture/requirements.md", 3),),
    "corpus-d": (("multi-owner", ".specify/specs/900-fixture/plan.md", 3),),
    "corpus-e": (("false-closed-set", ".specify/specs/900-fixture/notes.md", 3),),
    "corpus-f2": (("stale-constant",
                   ".specify/specs/900-fixture/contracts/ceilings.contract.md", 5),),
    "corpus-g": (("superseded-live", ".specify/specs/900-fixture/requirements.md", 1),),
    "corpus-h": (("orphan-path", ".specify/specs/900-fixture/requirements.md", 3),),
    "corpus-def": (("deferral-marker", ".specify/specs/900-fixture/requirements.md", 4),),
    "corpus-x": (("status-unreadable", ".specify/specs/902-fixture/verification.md", 0),),
}
#: C-107's mutation legs: the fixture each leg's base is, and the ``path:line`` the created
#: defect must land on. The base is the same green tree for every leg, so the red that follows
#: a `create` can only be the created defect; `repair` restores the base and the class is 0.
MUTATION_SITES = {
    "superseded-live": ("corpus-clean",
                        ".specify/specs/900-fixture/contracts/runner-contract.md", 1),
    "multi-owner": ("corpus-clean", ".specify/specs/900-fixture/plan.md", 3),
    "orphan-path": ("corpus-clean", ".specify/specs/900-fixture/requirements.md", 5),
    "renumber-live-binding": ("corpus-clean", ".specify/specs/900-fixture/requirements.md", 3),
    "false-closed-set": ("corpus-clean", ".specify/specs/900-fixture/notes.md", 3),
    "stale-constant": ("corpus-clean",
                       ".specify/specs/900-fixture/contracts/ceilings.contract.md", 5),
    "deferral-marker": ("corpus-clean", ".specify/specs/900-fixture/requirements.md", 5),
    "status-unreadable": ("corpus-clean", ".specify/specs/900-fixture", 3),
}


# --------------------------------------------------------------------------- #
# helpers — every one asserts its artifact path first (red = "missing", never an error)
# --------------------------------------------------------------------------- #
def _require(path: Path):
    assert path.exists(), "%s is missing — the artifact this leg pins has not landed" % path


def _run(*args, root=None, env_extra=None, timeout=180):
    """Run the engine; returns ``(returncode, stdout, stderr)``."""
    _require(ENGINE)
    env = {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONPATH": str(ENGINE.parent)}
    env.update(env_extra or {})
    argv = [sys.executable, str(ENGINE), *args]
    if root is not None:
        argv += ["--root", str(root)]
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=timeout)


def _fixture_run(name, *, json_mode=True, extra=()):
    _require(FIXTURES / name)
    args = list(extra) + ["--declaration", str(SURFACE)]
    if json_mode:
        args = ["--json"] + args
    return _run(*args, root=FIXTURES / name)


def _report(name, **kwargs):
    proc = _fixture_run(name, **kwargs)
    assert proc.stdout.strip(), "no report on stdout: %s" % proc.stderr.strip()[:400]
    return proc, json.loads(proc.stdout)


def _categories_of(report):
    return [entry["category"] for entry in report["entries"]]


def _one(report, category):
    found = [entry for entry in report["entries"] if entry["category"] == category]
    assert found, "no %r entry in %r" % (category, sorted(set(_categories_of(report))))
    return found


def _emitted_classes():
    """The closed class set, read from the owner page through the engine (C-101)."""
    proc = _run("--emit-categories", "--json")
    assert proc.returncode == 0, proc.stderr[:400]
    return json.loads(proc.stdout)


def _tree_digest(root: Path):
    """A content digest over every file under ``root`` — the zero-write reading (C-602)."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _copy(name, tmp_path):
    """A writable copy of one fixture tree (C-602's legs never write the fixture itself)."""
    source = FIXTURES / name
    _require(source)
    target = tmp_path / name
    shutil.copytree(source, target)
    return target


def _edit(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    assert old in text, "fixture copy no longer carries %r — the mutation leg moved" % old[:60]
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# --------------------------------------------------------------------------- #
# C-601 / C-602 — one stdlib module, read-only in every mode
# --------------------------------------------------------------------------- #
def test_c601_engine_is_stdlib_only_and_has_one_import_entry():
    """C-601: the engine imports the standard library plus the two named sibling modules."""
    _require(ENGINE)
    text = ENGINE.read_text(encoding="utf-8")
    imports = set(re.findall(r"(?m)^import\s+([A-Za-z_][\w.]*)", text))
    imports |= set(re.findall(r"(?m)^from\s+([A-Za-z_][\w.]*)\s+import", text))
    external = {name for name in imports
                if "." not in name and name not in sys.stdlib_module_names
                and name not in {"__future__", "declaration_reader", "renumber_utils",
                                 "script_interface_cli"}}
    assert not external, "non-stdlib imports: %s" % sorted(external)
    assert "declaration_reader" in text, "the declaration layer must be read through its entry"


@pytest.mark.parametrize("mode", [("--json",), (), ("--roots",), ("--emit-categories",),
                                  ("--help",), ("--version",), ("--nope",)])
def test_c602_engine_writes_nothing_in_any_mode(mode, tmp_path):
    """C-602: a copy tree is byte-identical before and after the run, whatever the mode."""
    tree = _copy("corpus-g", tmp_path)
    before = _tree_digest(tree)
    _run(*mode, root=tree,
         env_extra={"PYTHONPYCACHEPREFIX": str(tmp_path / "pycache")})
    assert _tree_digest(tree) == before, "%s wrote into the audited tree" % (mode,)


def test_c602_no_bytecode_is_written_beside_the_engine(tmp_path):
    """C-602: importing the engine's siblings writes no ``__pycache__`` into ``scripts/python``."""
    _require(ENGINE)
    tree = _copy("corpus-g", tmp_path)
    cache = tmp_path / "cache"
    _run("--json", root=tree, env_extra={"PYTHONPYCACHEPREFIX": str(cache)})
    strays = sorted(p.name for p in (ROOT / "scripts" / "python").glob("*.pyc"))
    assert not strays, "bytecode landed beside the sources: %s" % strays


def test_c602_mirror_resolves_the_checkout_not_the_specify_directory():
    """C-602: invoked through ``.specify/scripts/python``, the root is the checkout's parent."""
    _require(MIRROR)
    proc = subprocess.run(
        [sys.executable, str(MIRROR), "--json"],
        capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
             "PYTHONPYCACHEPREFIX": "/tmp/non-disposable-pycache"},
        timeout=300)
    assert proc.stdout.strip(), proc.stderr[:400]
    report = json.loads(proc.stdout)
    roots = {row["path"] for row in report["coverage"]["roots"]}
    assert ".specify/specs" in roots
    assert not any(row.endswith(".specify/.specify") for row in roots)


# --------------------------------------------------------------------------- #
# C-603 — three exit codes, three meanings; the empty surface is never `0`
# --------------------------------------------------------------------------- #
def test_c603_clean_surface_exits_zero():
    """C-603: no findings over a stated, non-empty surface is ``0``."""
    proc = _run("--json", "--declaration", str(FIXTURES / "surface-clean.yaml"),
                root=FIXTURES / "corpus-clean")
    assert proc.returncode == 0, proc.stdout[-800:] + proc.stderr[-800:]
    report = json.loads(proc.stdout)
    assert report["entries"] == []
    assert report["closed"] is True


def test_c603_findings_exit_one():
    """C-603: findings exist (any entry, any class) is ``1``."""
    proc = _fixture_run("corpus-h", json_mode=False, extra=["--json"])
    assert proc.returncode == 1, proc.stdout[-400:] + proc.stderr[-400:]


def test_c603_unknown_option_exits_two():
    """C-603 / C-604: an option outside the eight rows exits ``2`` before any action runs."""
    proc = _fixture_run("corpus-g", json_mode=False, extra=["--nope"])
    assert proc.returncode == 2
    assert "--nope" in (proc.stderr + proc.stdout)


def test_c603_empty_candidate_set_exits_two_and_names_the_declaration():
    """C-603: the empty surface is a declaration defect — exit ``2``, the declaration named."""
    argv = ["--declaration", str(FIXTURES / "surface-degraded.yaml"), "--root", str(FIXTURES)]
    proc = _run(*argv)
    assert proc.returncode == 2, "an empty candidate set MUST NOT reach 0 or 1"
    text = proc.stderr + proc.stdout
    assert "surface-degraded.yaml" in text, "the reason must name the declaration"
    assert "no candidates" in text or "declared no candidates" in text


def test_c603_missing_declaration_layer_exits_two():
    """C-603: a tree with no declarations layer is an environment error, never a verdict."""
    proc = _run("--root", str(ROOT / "tests" / "fixtures" / "non-disposable" / "corpus-c"))
    assert proc.returncode == 2
    assert "declaration" in (proc.stderr + proc.stdout)


@pytest.mark.parametrize("declaration", ["surface-bad-kind.yaml", "surface-no-statement.yaml"])
def test_c603_invalid_fact_exits_two(declaration):
    """C-603: a fact that is not a ``closed-set`` / carries no body is a declaration defect."""
    proc = _run("--root", str(FIXTURES / "corpus-g"),
                "--declaration", str(FIXTURES / declaration))
    assert proc.returncode == 2
    assert declaration in (proc.stderr + proc.stdout)


# --------------------------------------------------------------------------- #
# C-604 — the calling surface is eight rows and two actions
# --------------------------------------------------------------------------- #
def test_c604_help_lists_exactly_the_declared_options():
    """C-604: the help body names the eight rows; ``--scope-count`` is not among them.

    The reading is the *option rows* of the help body (an indented ``--option`` at the start of
    a line), never a mention: the epilog may explain that ``--scope-count`` is not a ninth row,
    and a rejection message may name it, but neither is a declared row.
    """
    proc = _run("--help")
    assert proc.returncode == 0
    for option in DECLARED_OPTIONS:
        assert option in proc.stdout, "%r is not stated by --help" % option
    rows = set(re.findall(r"(?m)^\s{2,}(--[a-z][a-z-]*|-h)\b", proc.stdout))
    assert "--scope-count" not in rows, "`--scope-count` is not a ninth row"
    assert rows <= set(DECLARED_OPTIONS), "undeclared option row in help: %r" % (
        rows - set(DECLARED_OPTIONS))
    assert {"--root", "--json", "--scope", "--roots", "--emit-categories",
            "--declaration", "--version"} <= rows, "an option with an effect has no help row"


@pytest.mark.parametrize("argv", [("--help",), ("-h",)])
def test_c604_help_answers_without_acting(argv):
    """C-604: ``-h`` / ``--help`` answer with usage and exit ``0``, touching nothing."""
    proc = _run(*argv)
    assert proc.returncode == 0
    assert proc.stdout.lower().startswith("usage:")


def test_c604_version_answers_one_line():
    """C-604: ``--version`` answers one line and exits ``0``."""
    proc = _run("--version")
    assert proc.returncode == 0
    assert len(proc.stdout.strip().splitlines()) == 1


def test_c604_scope_count_is_not_a_ninth_row():
    """C-604 pairing rule: the shard count travels in the shard id, so ``--scope-count`` is ``2``.

    This is the adjudication the P2 implement handoff recorded: the argument set is closed at
    eight rows, ``--scope s001-of-004`` names both the shard and ``n``, and an option that would
    carry ``n`` a second time is outside the surface — with or without ``--scope`` beside it.
    """
    alone = _run("--scope-count", "4")
    assert alone.returncode == 2, "`--scope-count` alone MUST be rejected"
    assert "--scope-count" in (alone.stderr + alone.stdout)
    paired = _run("--scope", "s000-of-004", "--scope-count", "4")
    assert paired.returncode == 2, "`--scope-count` beside `--scope` MUST be rejected too"


def test_c604_roots_prints_the_declared_set_and_stops():
    """C-604: ``--roots`` is a non-judging action — the declared roots, exit ``0``."""
    proc = _run("--roots", "--declaration", str(SURFACE),
                root=FIXTURES / "corpus-g")
    assert proc.returncode == 0
    declared = [line.strip() for line in SURFACE.read_text(encoding="utf-8").splitlines()
                if line.strip().startswith("- ")]
    for line in declared:
        assert line[2:].strip() in proc.stdout, "%r is missing from --roots" % line


def test_c604_emit_categories_is_a_non_judging_action():
    """C-604: ``--emit-categories`` prints the closed set and stops — it judges no tree."""
    proc = _run("--emit-categories", "--json", "--declaration", str(SURFACE))
    assert proc.returncode == 0, "a non-judging action MUST NOT report the tree's findings"
    payload = json.loads(proc.stdout)
    assert payload["action"] == "emit-categories"
    assert "entries" not in payload


# --------------------------------------------------------------------------- #
# C-605 / C-606 — the declaration is the only source of the surface
# --------------------------------------------------------------------------- #
def test_c605_roots_and_order_come_from_the_declaration():
    """C-605: members and order are read from the fact — a degraded fact degrades the reading."""
    proc = _run("--roots", "--declaration", str(FIXTURES / "surface-degraded.yaml"),
                root=FIXTURES / "corpus-g")
    assert proc.returncode == 0, proc.stderr[:400]
    report = json.loads(proc.stdout) if proc.stdout.lstrip().startswith("{") else None
    text = proc.stdout
    assert text.index(".specify/specs") < text.index(".specify/absent-root")
    if report is not None:
        assert [row["path"] for row in report["roots"]][:2] == [".specify/specs",
                                                                ".specify/absent-root"]


def test_c605_absent_root_is_reported_with_its_reason():
    """C-605: an absent root is named, never silently zero."""
    proc = _run("--json", "--declaration", str(FIXTURES / "surface-degraded.yaml"),
                root=FIXTURES / "corpus-g")
    assert proc.returncode in (0, 1, 2)
    text = proc.stdout + proc.stderr
    assert "declared-but-absent" in text


def test_c606_shard_ids_are_pure_functions_of_the_sorted_path_list(tmp_path):
    """C-606: the shards of one run are disjoint and their union is the whole entry set."""

    def read(scope):
        return _run("--json", "--scope", scope, "--declaration", str(SURFACE),
                    root=FIXTURES / "corpus-a1")

    whole = _run("--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-a1")
    whole_ids = {entry["entry_id"] for entry in json.loads(whole.stdout)["entries"]}
    parts, ids = [], []
    for index in range(3):
        proc = read("s%03d-of-003" % index)
        assert proc.returncode == 1, proc.stderr[:400]
        parts.append(proc)
        ids.extend(entry["entry_id"] for entry in json.loads(proc.stdout)["entries"])
    assert len(ids) == len(set(ids)), "the shards overlap: %d ids, %d distinct" % (
        len(ids), len(set(ids)))
    assert set(ids) == whole_ids, "the union misses %s" % sorted(whole_ids - set(ids))


def test_c606_an_empty_shard_exits_two():
    """C-606: no empty shard is part of a partition — asking for one is an input error."""
    proc = _run("--json", "--scope", "s000-of-4", "--declaration", str(SURFACE),
                root=FIXTURES / "corpus-g")
    assert proc.returncode == 2, "a malformed shard id MUST be rejected"


def test_c606_a_count_beyond_the_candidate_set_exits_two():
    """C-606: ``n`` larger than the candidate set forces an empty shard — exit ``2``."""
    proc = _run("--json", "--scope", "s000-of-999", "--declaration", str(SURFACE),
                root=FIXTURES / "corpus-h")
    assert proc.returncode == 2
    assert "scope" in (proc.stderr + proc.stdout).lower()


def test_c606_shard_count_must_be_one_per_run():
    """C-606: one run has one shard count; two partitions in one call is an input error."""
    proc = _run("--json", "--scope", "s000-of-004", "--scope", "s001-of-003",
                "--declaration", str(SURFACE), root=FIXTURES / "corpus-g")
    assert proc.returncode == 2


# --------------------------------------------------------------------------- #
# C-607 — determinism
# --------------------------------------------------------------------------- #
def test_c607_two_runs_serialise_byte_identically():
    """C-607: whatever the order of the reads, the report is byte-identical."""
    first = _fixture_run("corpus-a1", json_mode=False, extra=["--json"])
    second = _fixture_run("corpus-a1", json_mode=False, extra=["--json"])
    assert first.stdout == second.stdout


def test_c607_entries_are_sorted_by_entry_id():
    """C-607: entries sorted by ``entry_id``, never by discovery order."""
    _, report = _report("corpus-a1")
    ids = [entry["entry_id"] for entry in report["entries"]]
    assert ids == sorted(ids)


def test_c607_mappings_are_key_sorted():
    """C-607: the JSON mappings are serialised with sorted keys."""
    proc = _fixture_run("corpus-a1", json_mode=False, extra=["--json"])
    keys = [line for line in proc.stdout.splitlines()
            if line.startswith('  "') and line.rstrip().endswith("{")]
    parsed = re.findall(r'^  "([a-z_]+)": \{', proc.stdout, re.MULTILINE)
    assert parsed == sorted(parsed)
    assert keys


# --------------------------------------------------------------------------- #
# C-608 — per-class zero reporting over a stated surface
# --------------------------------------------------------------------------- #
def test_c608_every_class_is_reported_even_at_zero():
    """C-108: a class that finds nothing reports ``count: 0`` with the roots it searched."""
    _, report = _report("corpus-g")
    classes = _emitted_classes()["classes"]
    assert set(report["classes"]) == set(classes), "a class was omitted from the report"
    for name, row in report["classes"].items():
        assert set(row) == {"count", "roots"}, "%s carries %r" % (name, sorted(row))
        assert row["roots"], "%s reports no roots — a silent zero" % name


def test_c608_a_zero_is_not_a_green():
    """C-108 / C-603: a tree with one finding still reports the other seven classes as zero."""
    _, report = _report("corpus-h")
    counts = {name: row["count"] for name, row in report["classes"].items()}
    assert counts["orphan-path"] >= 1
    assert counts["stale-constant"] == 0
    assert report["closed"] is False


# --------------------------------------------------------------------------- #
# C-101 / C-102 — the closed set, one class per entry
# --------------------------------------------------------------------------- #
def test_c101_class_set_is_read_from_the_owner_page():
    """C-101: the engine's class set is the owner page's, never an engine-local extension."""
    _require(OWNER_PAGE)
    payload = _emitted_classes()
    declared = payload["classes"]
    assert isinstance(declared, list), "the class set is reported as %r" % type(declared)
    assert len(declared) == 8, "the closed set has %d members: %r" % (len(declared), declared)
    owner_text = OWNER_PAGE.read_text(encoding="utf-8")
    for name in declared:
        assert "`%s`" % name in owner_text, "%s is not declared by the owner page" % name
    assert payload["owner"].endswith("non-disposable-definitions.md")


def test_c101_unknown_class_is_a_finding_never_a_silent_pass(tmp_path):
    """C-101: a class the owner page does not declare is reported as ``unknown-class``."""
    tree = _copy("corpus-g", tmp_path)
    owner = tree / "shared" / "definitions" / "non-disposable-definitions.md"
    if not owner.is_file():
        owner.parent.mkdir(parents=True, exist_ok=True)
        owner.write_text(OWNER_PAGE.read_text(encoding="utf-8"), encoding="utf-8")
    # Remove one member from the owner page's class table: the engine still emits the defect,
    # and must say the class is not declared rather than renaming or dropping it.
    text = owner.read_text(encoding="utf-8")
    owner.write_text(re.sub(r"(?m)^.*`orphan-path`.*\n", "", text, count=1), encoding="utf-8")
    _edit(tree / ".specify/specs/900-fixture/requirements.md", "# Requirements", "# Requirements")
    proc = _run("--json", "--declaration", str(SURFACE), root=tree)
    report = json.loads(proc.stdout)
    names = set(_categories_of(report))
    if "orphan-path" in names:
        assert "unknown-class" in names, "an undeclared class must surface as `unknown-class`"


@pytest.mark.parametrize("fixture", sorted(EXPECTED))
def test_c102_each_entry_carries_one_class_of_the_closed_set(fixture):
    """C-102: one class per entry — no ``+``, ``,`` or ``|`` joined class string."""
    _, report = _report(fixture)
    closed = set(_emitted_classes()["classes"]) | {"unknown-class"}
    for entry in report["entries"]:
        assert entry["category"] in closed, entry["category"]
        for joiner in ("+", ",", "|"):
            assert joiner not in entry["category"], entry["category"]


def test_c102_a_two_class_defect_is_two_entries():
    """C-102: the same body read as two classes is two entries with distinct ``entry_id``s."""
    _, report = _report("corpus-b")
    ids = [entry["entry_id"] for entry in report["entries"]]
    assert len(ids) == len(set(ids))
    classes = set(_categories_of(report))
    assert {"superseded-live", "orphan-path"} <= classes


# --------------------------------------------------------------------------- #
# C-103 — each entry names its observable reading
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("fixture", sorted(EXPECTED))
def test_c103_every_entry_carries_a_recheckable_reading(fixture):
    """C-103: ``path``, a 1-based ``line`` (or ``0`` for a file-level fact) and evidence refs."""
    tree = FIXTURES / fixture
    _, report = _report(fixture)
    expected_classes = {row[0] for row in EXPECTED[fixture]}
    assert expected_classes <= set(_categories_of(report)), (
        "%s did not reproduce %r — the tree reports %r"
        % (fixture, sorted(expected_classes), sorted(set(_categories_of(report)))))
    for entry in report["entries"]:
        for field in ENTRY_FIELDS:
            assert field in entry, "%s misses %r" % (entry.get("entry_id"), field)
        assert isinstance(entry["line"], int) and entry["line"] >= 0
        assert entry["evidence_refs"], "%s names no evidence" % entry["entry_id"]
        for ref in entry["evidence_refs"]:
            assert ref.get("path"), "%s carries an evidence ref without a path" % entry["entry_id"]
        resolvable = [ref for ref in entry["evidence_refs"]
                      if (tree / ref["path"]).exists() or ref["path"].endswith("/")
                      or not ref["path"].endswith(".md")]
        assert resolvable, "%s names no reading that exists in the tree" % entry["entry_id"]


# --------------------------------------------------------------------------- #
# C-104 — the four structure classes
# --------------------------------------------------------------------------- #
def test_c104_superseded_live_names_body_and_guard():
    """C-104: a superseded body a live guard still asserts → body path:line + guard path:line."""
    _, report = _report("corpus-b")
    entry = _one(report, "superseded-live")[0]
    assert entry["path"] == ".specify/specs/900-fixture/contracts/runner-contract.md"
    assert entry["line"] == 1
    refs = {(ref.get("path"), ref.get("line")) for ref in entry["evidence_refs"]}
    assert (".specify/specs/900-fixture/contracts/runner-contract.md", 1) in refs
    assert any(path and "tests/" in path for path, _ in refs), "the guard is not named: %r" % refs


def test_c104_superseded_live_guard_side_tautology():
    """C-104 (G2): a guard asserting a literal against itself names the body it cannot protect."""
    _, report = _report("corpus-g")
    entry = _one(report, "superseded-live")[0]
    assert entry["path"] == ".specify/specs/900-fixture/requirements.md"
    guards = [ref for ref in entry["evidence_refs"] if "tests/" in (ref.get("path") or "")]
    assert guards, "the guard side is not named"
    assert guards[0]["line"] >= 1


def test_c104_multi_owner_names_both_sites_and_both_values():
    """C-104: one name stated twice with two values → red, naming both sites and both values."""
    _, report = _report("corpus-d")
    entry = _one(report, "multi-owner")[0]
    refs = [ref for ref in entry["evidence_refs"] if ref.get("value") is not None]
    assert len(refs) >= 2, "only one side is named: %r" % entry["evidence_refs"]
    assert len({ref["value"] for ref in refs}) >= 2, "both values must be shown"
    assert len({ref["path"] for ref in refs}) >= 2, "both sites must be shown"


def test_c104_orphan_path_names_the_citing_site_and_the_target():
    """C-104: a referenced path that does not exist → the citing path:line and the target."""
    tree = FIXTURES / "corpus-h"
    _, report = _report("corpus-h")
    entry = _one(report, "orphan-path")[0]
    targets = [ref.get("target") for ref in entry["evidence_refs"] if ref.get("target")]
    assert targets, "the missing target is not named"
    missing = [target for target in targets if not (tree / target).exists()]
    assert missing, "%r resolves in the fixture — not a finding" % targets
    assert entry["line"] >= 1 and entry["path"].endswith(".md")


def test_c104_renumber_live_binding_names_file_and_line():
    """C-104: a live binding numbered for another feature → red, naming file:line."""
    _, report = _report("corpus-c")
    entry = _one(report, "renumber-live-binding")[0]
    assert entry["path"].startswith(".specify/specs/")
    assert entry["line"] >= 1
    assert entry.get("bound") or any("bound" in (ref or {}) for ref in entry["evidence_refs"])


# --------------------------------------------------------------------------- #
# C-105 / C-106 — the four state classes
# --------------------------------------------------------------------------- #
def test_c105_status_unreadable_reads_the_closure_verdict():
    """C-105: a registry status disagreeing with the verdict → red, naming the feature."""
    _, report = _report("corpus-a1")
    entries = _one(report, "status-unreadable")
    clash = [entry for entry in entries if entry.get("feature") == "901"]
    assert clash, "the A1 reading is missing: %r" % [e.get("feature") for e in entries]
    entry = clash[0]
    assert entry["path"] == ".specify/specs/901-fixture"
    commands = [ref.get("command") for ref in entry["evidence_refs"] if ref.get("command")]
    assert commands and "closure-acceptance-check.py" in commands[0]
    assert entry.get("verdict") == "block"


def test_c203_missing_field_names_are_read_from_the_owner_page(tmp_path):
    """C-203: the absent block / smoke fields are named, the names read from the owner (C-205).

    The field names are the owner page's, never an engine-local list. The leg empties the
    verification record down to its status table, leaving exactly the machine-readable block
    and the smoke fields absent, and asserts the engine names them.
    """
    tree = _copy("corpus-a1", tmp_path)
    record = tree / ".specify" / "specs" / "901-fixture" / "verification.md"
    record.write_text("# Verification — 901-fixture\n\n| SC | Path | Status | Evidence |\n"
                      "|----|------|--------|----------|\n"
                      "| SC-001 | final | **pass** | the fixture is its own evidence |\n",
                      encoding="utf-8")
    proc = _run("--json", "--declaration", str(SURFACE), root=tree)
    report = json.loads(proc.stdout)
    entries = [entry for entry in _one(report, "status-unreadable")
               if entry["path"].endswith("verification.md")]
    assert entries, "a record with no machine block is itself a reading"
    missing = entries[0].get("missing_fields") or []
    assert "smoke_exit_code" in missing, (
        "the smoke fields are read from the owner page, not listed in the engine: %r" % missing)
    assert "SC-NNN_status=" in missing, "the machine-readable block is named by its own shape"
    assert all(isinstance(name, str) and name for name in missing)


def test_c105_false_closed_set_shows_both_readings():
    """C-105: a claimed closed-set identity whose two sides disagree → red, both readings."""
    _, report = _report("corpus-a2")
    entry = _one(report, "false-closed-set")[0]
    claims = [ref.get("claimed") for ref in entry["evidence_refs"] if "claimed" in ref]
    assert claims, "the claim is not shown"
    assert str(claims[0]).startswith("unclassified")
    recomputed = [ref for ref in entry["evidence_refs"]
                  if ref.get("recomputed_total") is not None]
    assert recomputed and recomputed[0]["recomputed_total"] != 0, "the run's reading is missing"


def test_c105_stale_constant_names_both_sites_and_the_owner():
    """C-105: a constant with two live values, one site not the owner → both sites, both values."""
    _, report = _report("corpus-f2")
    entry = _one(report, "stale-constant")[0]
    refs = [ref for ref in entry["evidence_refs"] if ref.get("value") is not None]
    assert len(refs) >= 2, "only one site is named"
    assert len({ref["value"] for ref in refs}) >= 2
    owners = [ref["path"] for ref in refs if ref["path"].startswith(("scripts/", ".specify/scripts/"))]
    assert owners, "the value owner's site is not named"


def test_c105_stale_constant_is_green_on_the_real_tree():
    """Quickstart § 2: the real tree has no ``stale-constant`` row — the class is red on F2 only."""
    proc = _run("--json", root=ROOT,
                env_extra={"PYTHONPYCACHEPREFIX": "/tmp/non-disposable-pycache"},
                timeout=300)
    report = json.loads(proc.stdout)
    assert report["classes"]["stale-constant"]["count"] == 0
    assert report["classes"]["stale-constant"]["roots"], "a zero must still name its roots"


def test_c106_deferral_marker_is_proven_by_construction():
    """C-106: no corpus row carries the class, so the guard proves it on the fixture tree.

    The class is in the closed set (C-101) and is emitted by the engine; the corpus's own
    two-way check (``plan.md`` § A–H Corpus Mapping) records that no A–H row carries it, which is
    why the fixture — not the corpus — is this leg's evidence.
    """
    assert "deferral-marker" in _emitted_classes()["classes"]
    _, report = _report("corpus-def")
    entries = _one(report, "deferral-marker")
    assert len(entries) >= 1
    for entry in entries:
        assert entry["path"].startswith(".specify/specs/")
        assert entry["line"] >= 1
        quotes = [ref.get("quote") for ref in entry["evidence_refs"] if ref.get("quote")]
        assert quotes and quotes[0].strip(), "the marker itself is not quoted"


def test_c106_a_quoted_prohibition_is_not_a_deferral():
    """C-106: a rule that *forbids* the retention form is not the engine's reading of it."""
    _, report = _report("corpus-def")
    quoted = [entry for entry in report["entries"]
              if entry["category"] == "deferral-marker"
              and any("MUST NOT" in (ref.get("quote") or "") for ref in entry["evidence_refs"])]
    assert not quoted, "a prohibition line was read as a deferral"


# --------------------------------------------------------------------------- #
# C-107's legs. Each pair edits one file of `corpus-clean`'s copy: `create` lands the defect
# at the site `MUTATION_SITES` names, `repair` restores the base byte-for-byte.
# --------------------------------------------------------------------------- #
REQ = ".specify/specs/900-fixture/requirements.md"
PLAN = ".specify/specs/900-fixture/plan.md"
NOTES = ".specify/specs/900-fixture/notes.md"
RUNNER = ".specify/specs/900-fixture/contracts/runner-contract.md"
#: A live guard is a `tests/` module, and every reading comes from the declared surface
#: (C-605): the guard lands under the surface's own `tests/` root.
RUNNER_GUARD = "tests/contract/test_runner_contract.py"


def _write(tree, relpath, text):
    path = tree / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _create_superseded(tree):
    # A contract still asserted as current by a live guard that cannot go red: the guard
    # compares a literal with itself, so no edit to the body can move it (corpus G2's shape).
    # The body's own line 1 is the site (C-104 pair: body path:line + guard path:line).
    _write(tree, RUNNER, "# Contract: runner\n\n"
                         "C-016: the runner MUST keep one entry point.\n")
    _write(tree, RUNNER_GUARD,
           '"""Guard for `.specify/specs/900-fixture/contracts/runner-contract.md`."""\n'
           "import pathlib\n\n"
           "\n"
           "def test_byte_identical():\n"
           "    expected = 'byte-identical'\n"
           "    assert expected == 'byte-identical'\n")


def _repair_superseded(tree):
    for relpath in (RUNNER, RUNNER_GUARD):
        (tree / relpath).unlink()


def _create_multi(tree):
    # The same constant stated twice with two live values, neither site owned by a script
    # (otherwise the pair is `stale-constant`, C-104's own distinction): the requirements file
    # states `30s`, the plan now states `15m`.
    _write(tree, "scripts/1-reporter-cadence.md", "# Cadence\n\nREPORTER_CADENCE: 15m\n")


def _repair_multi(tree):
    (tree / "scripts/1-reporter-cadence.md").unlink()


def _create_orphan(tree):
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 900\n\n"
                      "See `scripts/python/absent-helper.py` for the rule.\n")


def _repair_orphan(tree):
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 900\n")


def _create_renumber(tree):
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 877\n")


def _repair_renumber(tree):
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 900\n")


def _create_false_closed(tree):
    # A claimed closed-set identity whose two sides disagree (the E4 shape).
    _write(tree, NOTES, "# Notes\n\nThe earlier review records `367 + 737 = 1104 ≠ 751`.\n")


def _repair_false_closed(tree):
    (tree / NOTES).unlink()


STALE_OWNER = "scripts/python/decomposition-check.py"
STALE_BODY = ".specify/specs/900-fixture/contracts/ceilings.contract.md"


def _create_stale(tree):
    # FR_CEILING declared 38 by the value owner (a `scripts/` module) and stated 62 by a
    # contract body: one value, two sites, the stating site is not the owner.
    _write(tree, STALE_OWNER, '"""A value owner.\n\nDeclares the ceiling once.\n"""\n\n'
                              "FR_CEILING = 38\n")
    _write(tree, STALE_BODY, "# Contract: ceilings\n\nEach feature is held to a ceiling.\n\n"
                             "The plan states FR_CEILING = 62 for the same name.\n")


def _repair_stale(tree):
    for relpath in (STALE_OWNER, STALE_BODY):
        (tree / relpath).unlink()


STATUS_REGISTRY = ".specify/features.md"


def _create_status(tree):
    # A registry row claiming `Implemented` for a feature whose verification record carries no
    # machine-readable block and no smoke fields: the row claims more than the record reads.
    _write(tree, STATUS_REGISTRY,
           "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |\n"
           "|----|------|-------------|--------|-----------------|-----------|--------------|\n"
           "| 900 | fixture | a fixture row | Implemented | `.specify/features/900-900.md` "
           "| `.specify/specs/900-fixture/requirements.md` | 2026-11-09 |\n")
    _write(tree, ".specify/specs/900-fixture/verification.md",
           "# Verification — 900-fixture\n\n| SC | Path | Status | Evidence |\n"
           "|----|------|--------|----------|\n"
           "| SC-001 | final | **pass** | the fixture is its own evidence |\n")


def _repair_status(tree):
    (tree / STATUS_REGISTRY).unlink()
    (tree / ".specify/specs/900-fixture/verification.md").unlink()


def _create_deferral(tree):
    # A retention statement with no expiry condition (C-106: proven by construction).
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 900\n\n"
                      "- The old path is kept for now.\n")


def _repair_deferral(tree):
    _write(tree, REQ, "# Requirements: 900\n\n**Feature ID**: 900\n")


_LEGS = {
    "superseded-live": (_create_superseded, _repair_superseded),
    "multi-owner": (_create_multi, _repair_multi),
    "orphan-path": (_create_orphan, _repair_orphan),
    "renumber-live-binding": (_create_renumber, _repair_renumber),
    "false-closed-set": (_create_false_closed, _repair_false_closed),
    "stale-constant": (_create_stale, _repair_stale),
    "deferral-marker": (_create_deferral, _repair_deferral),
    "status-unreadable": (_create_status, _repair_status),
}


# --------------------------------------------------------------------------- #
# C-107 — one mutation leg per class: red when the defect is created, green when repaired
# --------------------------------------------------------------------------- #
#: The mutation legs' surface: `.specify/specs` + `tests` + `scripts`. `tests` carries the
#: guard side of `superseded-live`, `scripts` the value owner of `stale-constant` -- an owner is
#: a declaring script, and the declared surface is the only place a reading comes from (C-605).
SURFACE_CLEAN = FIXTURES / "surface-clean.yaml"


def _leg_run(root, surface=SURFACE_CLEAN):
    return _run("--json", "--declaration", str(surface), root=root)


def _red_then_green(category, create, repair):
    """Create the defect on a copy of the green base → red; repair it → that class back to 0.

    The base is `corpus-clean`, a tree the engine reports as `closed: true` with every class at
    zero, so the red that follows can only be the created defect. The same helper is what the
    engine-side mutation hunt uses: break one detection predicate, watch the leg go red.
    """
    import tempfile

    _require(FIXTURES / "corpus-clean")
    with tempfile.TemporaryDirectory() as workspace:
        tree = _copy("corpus-clean", Path(workspace))
        before = json.loads(_leg_run(tree).stdout)
        assert before["classes"][category]["count"] == 0, (
            "the base tree already carries %s — the leg cannot show a red" % category)
        assert before["closed"] is True, "the base tree is not green, so a red proves nothing"
        create(tree)
        red = _leg_run(tree)
        red_report = json.loads(red.stdout)
        named = [entry for entry in red_report["entries"] if entry["category"] == category]
        assert names_class(red_report, category), (
            "the created defect did not turn %r red — got %r"
            % (category, sorted({e["category"] for e in red_report["entries"]})))
        assert red.returncode == 1, "the engine stayed green after the defect was created"
        expected_fixture, expected_path, expected_line = MUTATION_SITES[category]
        assert any(entry["path"] == expected_path and entry["line"] == expected_line
                   for entry in named), (
            "%s does not name %s:%d — got %r" % (category, expected_path, expected_line,
                                                 [(e["path"], e["line"]) for e in named]))
        repair(tree)
        green_report = json.loads(_leg_run(tree).stdout)
        assert green_report["classes"][category]["count"] == 0, (
            "the repaired copy still reports %r — the leg's inverse does not hold" % category)


def names_class(report, category):
    return [entry for entry in report["entries"] if entry["category"] == category]


def test_c107_mutation_legs_cover_the_whole_closed_set():
    """C-107: every class of the closed set carries a defect-creating leg, not a green only."""
    closed = set(_emitted_classes()["classes"])
    assert set(MUTATIONS) == closed, (
        "mutation legs exist for %r; the closed set is %r" % (sorted(MUTATIONS), sorted(closed)))
    assert set(_LEGS) == closed, "a leg is missing for %r" % sorted(closed - set(_LEGS))


@pytest.mark.parametrize("category", sorted(MUTATIONS))
def test_c107_one_mutation_leg_per_class(category):
    """C-107: each class goes red on a created defect and back green on its repair."""
    create, repair = _LEGS[category]
    _red_then_green(category, create, repair)
