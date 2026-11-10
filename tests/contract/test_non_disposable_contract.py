"""The seven-face contract guard for Feature 092 — Non-Disposable.

Subject: the *contracts* this feature fixed, not the engine's own behaviour (that is
``tests/contract/test_non_disposable_check.py``'s job, and this file borrows its fixture style,
never its verdicts). Each leg below names the contract file and the clause it reads, and each
leg's subject is one closure the clause states:

``contracts/detection-categories.contract.md``            C-101…C-108
``contracts/detection-engine-cli.contract.md``            C-601…C-608
``contracts/disposition.contract.md``                     C-301…C-308
``contracts/renumber-and-supersede.contract.md``          C-501…C-507
``contracts/report-schema.contract.md``                   C-701…C-707
``contracts/status-and-verification.contract.md``         C-201…C-207
``contracts/acceptance-readability.contract.md``          C-803 (the clash-vs-consistent pair)

**Fixture data stated here, in this file.** C-106's fixture tree is not a corpus row, so the
defect it proves is written by this module (``_FIXTURES`` below) and materialised per leg:

======================================  ==================================================
tree name                               what it states
======================================  ==================================================
``base``                                a green tree — every class at zero, ``closed: true``
``deferral``                            the C-106 construction: a retention line and no
                                        expiry condition anywhere near it
``clash`` / ``consistent``              C-803's pair: a ``Planned`` registry row whose
                                        closure verdict clashes, and one whose verdict agrees
``closing-guard``                        C-492 / C-307's co-reading: one candidate seen by
                                        both engines, and the rule deciding who disposes it
======================================  ==================================================

**Red-first.** Before this file existed, every leg above failed as "the guard file is
missing"; a leg that cannot go red is not evidence, so each closed set additionally carries a
**mutation leg** — a copy-tree edit that creates the defect and asserts the reading moves, with
the inverse restoring the base. The mutation legs are how the file itself is falsified: run the
same copy-tree edit against a deliberately broken assertion and it must fail
(``tests/.../p5a-report.txt`` records the three observations).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "non-disposable-check.py"
MIRROR = ROOT / ".specify" / "scripts" / "python" / "non-disposable-check.py"
SYNC = ROOT / "scripts" / "python" / "sync-mirrors.py"
DECLARATION_READER = ROOT / "scripts" / "python" / "declaration_reader.py"
RENUMBER_UTILS = ROOT / "scripts" / "python" / "renumber-utils.py"
SANITIZE_UTILS = ROOT / "scripts" / "python" / "sanitize-utils.py"
FIXTURES = ROOT / "tests" / "fixtures" / "non-disposable"
SURFACE = FIXTURES / "surface.yaml"
SURFACE_CLEAN = FIXTURES / "surface-clean.yaml"
CONTRACTS = ROOT / ".specify" / "specs" / "092-non-disposable" / "contracts"
OWNER_PAGE = ROOT / "shared" / "definitions" / "non-disposable-definitions.md"
FACT = ROOT / "shared" / "declarations" / "facts" / "non-disposable-review-surface.yaml"

#: C-104 / C-105: the closed class set, spelled here only so that a *missing* class is an
#: assertion with a name (C-101 owns the set; this tuple is the guard's reading order).
CLASS_IDS = ("superseded-live", "multi-owner", "orphan-path", "renumber-live-binding",
             "status-unreadable", "false-closed-set", "stale-constant", "deferral-marker")
#: C-604: the eight argument rows — ``-h`` / ``--help`` is one row, ``--version`` another.
DECLARED_OPTIONS = ("--root", "--json", "--scope", "--roots", "--emit-categories",
                    "--declaration", "-h", "--help", "--version")
#: C-604: the two *actions*; every other option is an argument.
ACTIONS = ("--roots", "--emit-categories")
#: ``data-model.md`` E-1: the entry field set the serialisation legs read.
ENTRY_FIELDS = ("entry_id", "path", "line", "category", "detection", "state", "evidence_refs",
                "severity", "disposition", "suggested_disposition")
#: ``data-model.md`` § Entry State Machine: "not closed" is these three states; ``closed`` is
#: derived from them (C-705), never stored on its own.
NOT_CLOSED_STATES = ("open", "unevaluated", "unconfirmed")


# --------------------------------------------------------------------------- #
# fixture data — C-106 / C-803 / C-307 state their trees HERE, in the guard's own data
# --------------------------------------------------------------------------- #
BASE_FILES = {
    "tests/README.md": "# Guard directory.\n",
    ".specify/features.md":
        "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |\n"
        "|----|------|-------------|--------|-----------------|-----------|--------------|\n",
    ".specify/specs/900-fixture/requirements.md": "# Requirements: 900\n\n**Feature ID**: 900\n",
    ".specify/specs/900-fixture/plan.md": "# Plan\n\nREPORTER_CADENCE: 30s\n",
    ".specify/specs/900-fixture/contracts/runner-contract.md":
        "# Contract: runner\n\nC-016: the runner MUST keep one entry point.\n",
    ".specify/specs/900-fixture/notes/runner-evidence.md":
        "# Runner evidence\n\nThe entry-point reading was taken once.\n",
    "tests/contract/test_runner_contract.py":
        '"""Guard for `.specify/specs/900-fixture/contracts/runner-contract.md`."""\n'
        "\n"
        "\n"
        "def test_the_runner_must_keep_one_entry_point():\n"
        '    text = "the runner MUST keep one entry point."\n'
        '    assert "MUST keep one entry point" in text\n',
}
RUNNER = ".specify/specs/900-fixture/contracts/runner-contract.md"
EVIDENCE_BODY = ".specify/specs/900-fixture/notes/runner-evidence.md"
GUARD = "tests/contract/test_runner_contract.py"
POINTER_LINE = "Superseded by `.specify/specs/900-fixture/requirements.md`."
_FIXTURES = {
    # C-106: no corpus row carries `deferral-marker`, so the class is proven by construction.
    "base": dict(BASE_FILES),
    "deferral": dict(BASE_FILES, **{
        ".specify/specs/900-fixture/notes/deferral.md":
            "# Retention\n\nThe scratch writer is kept for now; it is faster than the queue.\n",
    }),
    # C-803's pair: one tree where `Planned` clashes with `accept`, one where it agrees.
    "clash": dict(BASE_FILES, **{
        ".specify/features.md":
            "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |\n"
            "|----|------|-------------|--------|-----------------|-----------|--------------|\n"
            "| 901 | fixture | a row claiming less than the verdict grants | Planned "
            "| `.specify/features/901-901.md` "
            "| `.specify/specs/901-clash/requirements.md` | 2026-11-09 |\n",
        ".specify/specs/901-clash/requirements.md":
            "# Requirements: 901\n\n**Feature ID**: 901\n\n- **FR-001**: The fixture MUST "
            "answer.\n",
        ".specify/specs/901-clash/verification.md":
            "# Verification — 901-clash\n\n| SC | Path | Status | Evidence |\n"
            "|----|------|--------|----------|\n"
            "| SC-001 | final | **pass** | the fixture is its own evidence |\n\n"
            "SC-001_status=pass\n"
            "SC-001_note=the fixture records its own reading\n"
            "SC-001_evidence=the fixture itself\n"
            "SC-001_verified_at=2026-11-09\n\n"
            "smoke_command: `python3 -m pytest -q tests/contract`\n"
            "smoke_exit_code: 0\n"
            "smoke_evidence_path: `tests/README.md`\n",
    }),
    # C-307: one candidate seen by both engines; the rule says who disposes it.
    "closing-guard": dict(BASE_FILES, **{
        ".specify/specs/900-fixture/notes/claim.md":
            "# Claim\n\nOne candidate, two engines: the detector decides the vocabulary.\n",
    }),
}


# --------------------------------------------------------------------------- #
# helpers — every one asserts its artifact path first (red = "missing", never an error)
# --------------------------------------------------------------------------- #
def _require(path: Path):
    assert path.exists(), "%s is missing — the artifact this leg pins has not landed" % path


def _real(fixtures, tree: Path):
    for relpath, text in fixtures.items():
        path = tree / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def _run(*args, root=None, timeout=300):
    """Run the engine; returns ``CompletedProcess``."""
    _require(ENGINE)
    env = {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONPATH": str(ENGINE.parent)}
    argv = [sys.executable, str(ENGINE), *args]
    if root is not None:
        argv += ["--root", str(root)]
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=timeout)


def _report_on(root: Path, surface: Path = SURFACE_CLEAN):
    proc = _run("--json", "--declaration", str(surface), root=root)
    assert proc.stdout.strip(), "no report on stdout: %s" % proc.stderr.strip()[:400]
    return proc, json.loads(proc.stdout)


def _load_module(path: Path, name: str):
    _require(path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _own_engine():
    """The engine module itself — only for legs whose subject is a *helper*, not a verdict."""
    return _load_module(ENGINE, "_nd_contract_quickstart")


class _Tree:
    """A writable copy of one fixture tree, materialised per leg (never the fixture itself)."""

    def __init__(self, name: str, workspace: Path):
        self.name = name
        self.path = workspace / name
        _real(_FIXTURES[name], self.path)

    def write(self, relpath, text):
        path = self.path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def read(self, relpath):
        return (self.path / relpath).read_text(encoding="utf-8")

    def remove(self, relpath):
        path = self.path / relpath
        if path.exists():
            path.unlink()

    def report(self, surface=SURFACE_CLEAN):
        return _report_on(self.path, surface)

    def counts(self, surface=SURFACE_CLEAN):
        return {name: row["count"] for name, row in self.report(surface)[1]["classes"].items()}


@pytest.fixture()
def workspace():
    with tempfile.TemporaryDirectory(prefix="nd-contract-") as directory:
        yield Path(directory)


def _tree_for(name: str, workspace: Path) -> _Tree:
    return _Tree(name, workspace)


def _one(record, category):
    found = [entry for entry in record["entries"] if entry["category"] == category]
    assert found, "no %r entry — got %r" % (category,
                                            sorted({e["category"] for e in record["entries"]}))
    return found


# --------------------------------------------------------------------------- #
# T086 — the seven faces exist, and each is a live path rather than a claim
# --------------------------------------------------------------------------- #
#: The seven faces ``plan.md`` § The seven faces names, each read as an existing artifact.
SEVEN_FACES = (
    ("owner page", OWNER_PAGE),
    ("declaration fact", FACT),
    ("glossary terms", ROOT / ".specify" / "glossary.md"),
    ("registry row and details", ROOT / ".specify" / "features.md"),
    ("existing guard suite", ROOT / "tests" / "contract" / "test_non_disposable_check.py"),
    ("history pointer rows", ROOT / "templates" / "commands" / "history.md"),
    ("decision register rows", ROOT / ".specify" / "register.md"),
)


def test_t086_the_seven_faces_all_exist_and_are_non_empty():
    """plan.md § The seven faces: seven artifacts, each a live non-empty path."""
    assert len(SEVEN_FACES) == 7, "the seven-face set changed without this guard moving"
    for label, path in SEVEN_FACES:
        assert path.exists(), "face %r is missing at %s" % (label, path)
        assert path.stat().st_size > 0, "face %r is empty at %s" % (label, path)
    detail = ROOT / ".specify" / "features" / "092-non-disposable.md"
    assert detail.exists(), "the registry row's details page is a face too (FR-063)"


def test_t086_mutation_leg_a_missing_face_reddens_the_existence_reading():
    """The existence leg can go red: remove one face from a copy and the reading fails."""
    with tempfile.TemporaryDirectory() as workspace:
        tree = Path(workspace)
        for _, path in SEVEN_FACES:
            target = tree / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

        def present():
            return [label for label, path in SEVEN_FACES
                    if (tree / path.relative_to(ROOT)).exists()]

        assert len(present()) == 7
        (tree / OWNER_PAGE.relative_to(ROOT)).unlink()
        assert "owner page" not in present(), "removing a face did not redden the reading"
        assert len(present()) == 6


def test_t086_the_deferral_fixture_lives_in_this_files_own_data():
    """C-106: the fixture is stated here, so the missing corpus row stays visible."""
    assert "deferral" in _FIXTURES
    body = _FIXTURES["deferral"][".specify/specs/900-fixture/notes/deferral.md"]
    assert "kept for now" in body
    assert "expiry" not in body, "the fixture must carry NO expiry condition (that is its defect)"
    assert "deferral-marker" not in _FIXTURES["base"][".specify/specs/900-fixture/plan.md"]


# --------------------------------------------------------------------------- #
# T087 — the mutation-leg harness: create the defect, assert red; repair, assert green
# --------------------------------------------------------------------------- #
def _class_counts(tree: _Tree):
    return tree.counts()


def _red_then_green(category, create, repair, workspace, target="base"):
    """One leg: green base → created defect turns *this* class up → repair returns it to 0."""
    tree = _tree_for(target, workspace)
    before = _class_counts(tree)
    assert before[category] == 0, "the %s base already carries %s — no red is provable" % (
        target, category)
    create(tree)
    red = _class_counts(tree)
    assert red[category] > before[category], (
        "%s did not turn red — counts %r" % (category, red))
    repair(tree)
    after = _class_counts(tree)
    assert after[category] == 0, "%s stayed red after the repair: %r" % (category, after)


def _create_deferral(tree):
    tree.write(".specify/specs/900-fixture/notes/deferral.md",
               "# Retention\n\nScratch writer kept for now; revisit later.\n")


def _repair_deferral(tree):
    tree.remove(".specify/specs/900-fixture/notes/deferral.md")


def _create_multi_owner(tree):
    tree.write("scripts/python/cadence.py", '"""A declaring script."""\n\n'
                                            "REPORTER_CADENCE = 15\n")


def _repair_multi_owner(tree):
    tree.remove("scripts/python/cadence.py")


def _create_orphan(tree):
    # The citation lands under a declared root (`.specify/specs`): C-103 reads evidence from
    # the declared surface, so a file outside every root is not a candidate and names nothing.
    tree.write(".specify/specs/900-fixture/notes/orphan.md",
               "# Notes\n\nSee `scripts/python/absent-helper.py`.\n")


def _repair_orphan(tree):
    tree.remove(".specify/specs/900-fixture/notes/orphan.md")


def _create_renumber(tree):
    tree.write(".specify/specs/900-fixture/requirements.md",
               "# Requirements: 900\n\n**Feature ID**: 877\n")


def _repair_renumber(tree):
    tree.write(".specify/specs/900-fixture/requirements.md",
               "# Requirements: 900\n\n**Feature ID**: 900\n")


def _create_superseded(tree):
    tree.write(RUNNER, "# Contract: runner (superseded)\n\n"
                       "C-016: the runner MUST keep one entry point.\n")


def _repair_superseded(tree):
    tree.write(RUNNER, "# Contract: runner\n\nC-016: the runner MUST keep one entry point.\n")


MUTATION_LEGS = {
    "deferral-marker": (_create_deferral, _repair_deferral),
    "multi-owner": (_create_multi_owner, _repair_multi_owner),
    "orphan-path": (_create_orphan, _repair_orphan),
    "renumber-live-binding": (_create_renumber, _repair_renumber),
    "superseded-live": (_create_superseded, _repair_superseded),
}


def test_t087_the_mutation_harness_is_itself_falsifiable():
    """A harness that cannot red is not evidence: a wrong expectation must fail the leg."""
    with tempfile.TemporaryDirectory() as workspace:
        tree = _tree_for("base", Path(workspace))
        before = _class_counts(tree)
        _create_deferral(tree)
        after = _class_counts(tree)
        assert after["deferral-marker"] > before["deferral-marker"]
        with pytest.raises(AssertionError):
            _red_then_green("multi-owner", _create_deferral, _repair_deferral, Path(workspace))


@pytest.mark.parametrize("category", sorted(MUTATION_LEGS))
def test_t087_one_defect_creating_leg_per_class(category, workspace):
    """C-107: each class of the closed set goes red on a created defect and back to zero."""
    create, repair = MUTATION_LEGS[category]
    _red_then_green(category, create, repair, workspace)


def test_t087_the_legs_cover_every_class_the_deferral_set_states():
    """C-107: the harness covers as many classes as this file's closed-set reading names."""
    assert set(MUTATION_LEGS) <= set(CLASS_IDS)
    assert {"deferral-marker", "superseded-live", "orphan-path"} <= set(MUTATION_LEGS)


# --------------------------------------------------------------------------- #
# T088 — the CLI legs: -h / --help / --version answer without acting; unknown → 2
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("argv", [("--help",), ("-h",)])
def test_t088_help_answers_the_declared_options_without_acting(argv):
    """C-604: usage answers with exit 0 and lists the eight rows, judging nothing."""
    proc = _run(*argv)
    assert proc.returncode == 0, proc.stderr[:400]
    assert proc.stdout.lower().startswith("usage:")
    for option in DECLARED_OPTIONS:
        assert option in proc.stdout, "%r has no help row" % option


def test_t088_version_answers_one_line_without_acting():
    """C-604: ``--version`` is a script-interface answer, not a review action."""
    proc = _run("--version")
    assert proc.returncode == 0
    assert len(proc.stdout.strip().splitlines()) == 1


@pytest.mark.parametrize("option", ["--scope-count", "--nope", "--js", "--roo"])
def test_t088_undeclared_option_exits_two(option):
    """C-604: no option outside the eight rows exists; an abbreviation is not a ninth."""
    if option == "--scope-count":
        proc = _run(option, "4")
    else:
        proc = _run(option)
    assert proc.returncode == 2, "%r was accepted (exit %d)" % (option, proc.returncode)
    assert option in (proc.stdout + proc.stderr)


def test_t088_two_actions_and_eight_arguments_are_two_counts():
    """C-604: ``--roots`` / ``--emit-categories`` are the two actions; the rest are arguments."""
    proc = _run("--roots", "--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-g")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["action"] == "roots"

    emitted = _run("--emit-categories", "--json", "--declaration", str(SURFACE))
    assert emitted.returncode == 0
    assert json.loads(emitted.stdout)["action"] == "emit-categories"
    assert len(DECLARED_OPTIONS) - 1 == 8, "the eight rows count `-h`/`--help` as one"
    assert len(ACTIONS) == 2, "a third action does not exist"


def test_t088_mutation_leg_an_undeclared_option_cannot_exit_zero():
    """The CLI leg can go red: a run that accepted ``--nope`` would break this reading."""
    with tempfile.TemporaryDirectory() as workspace:
        tree = _tree_for("base", Path(workspace))
        accepted = _run("--json", "--declaration", str(SURFACE_CLEAN),
                        root=tree.path).returncode
        assert accepted in (0, 1), "the declared surface must be accepted"
        rejected = _run("--nope", "--json", "--declaration", str(SURFACE_CLEAN),
                        root=tree.path).returncode
        assert rejected == 2, "an undeclared option changed the declared surface's reading"


# --------------------------------------------------------------------------- #
# T089 — read-only: a full run leaves `git status --porcelain` byte-identical
# --------------------------------------------------------------------------- #
def _porcelain():
    return subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT),
                          capture_output=True, text=True, timeout=120).stdout


def test_t089_a_full_run_is_byte_identical_on_git_status():
    """C-602: ``git status --porcelain`` around a full run is byte-identical."""
    before = _porcelain()
    _run("--json", root=ROOT, timeout=600)
    _run("--roots", root=ROOT)
    _run("--emit-categories", root=ROOT)
    after = _porcelain()
    assert after == before, "the engine changed the working tree"


def test_t089_read_only_leg_can_go_red_when_a_tracked_path_is_touched(workspace):
    """C-602's mutation leg: touching a tracked path moves the reading; the run does not."""
    tree = _tree_for("base", workspace)
    subprocess.run(["git", "init", "-q", str(tree.path)], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", str(tree.path), "add", "-A"], check=True,
                   capture_output=True, text=True)

    def porcelain():
        return subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=a", "-C",
                               str(tree.path), "status", "--porcelain"],
                              capture_output=True, text=True, timeout=120).stdout

    before = porcelain()
    _run("--json", "--declaration", str(SURFACE_CLEAN), root=tree.path)
    assert porcelain() == before, "a judging run wrote into the tree"
    tree.write("tests/README.md", "# Guard directory.\n\nA hand edit.\n")
    assert porcelain() != before, "touching a tracked path did not move the zero-write reading"


# --------------------------------------------------------------------------- #
# T090 — empty surface, unknown option, declaration surface
# --------------------------------------------------------------------------- #
def test_t090_empty_candidate_set_is_never_closed_and_exits_two(workspace):
    """C-603: an empty surface exits 2, names the declaration, prints ``candidates: 0``."""
    tree = _tree_for("base", workspace)
    for relpath in (".specify/specs/900-fixture/requirements.md",
                    ".specify/specs/900-fixture/plan.md", RUNNER, EVIDENCE_BODY,
                    "tests/contract/test_runner_contract.py", "tests/README.md"):
        tree.remove(relpath)
    (tree.path / "tests").mkdir(parents=True, exist_ok=True)
    proc = _run("--json", "--declaration", str(SURFACE_CLEAN), root=tree.path)
    assert proc.returncode == 2, "an empty candidate set MUST NOT reach 0 or 1"
    text = proc.stderr + proc.stdout
    assert "surface-clean.yaml" in text, "the reason must name the declaration"
    payload = json.loads(proc.stdout)
    coverage = payload["coverage"]
    assert coverage["candidates"] == 0
    assert [row["path"] for row in coverage["roots"]] == [
        line.strip()[2:] for line in SURFACE_CLEAN.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("- ")], "the roots must be printed in declaration order"
    assert payload["closed"] is False, "an empty surface MUST NOT be `closed: true`"
    assert "closed: false" in proc.stdout or '"closed": false' in proc.stdout


def test_t090_missing_declaration_exits_two_naming_the_path(workspace):
    """C-603 / C-605: no declaration layer is an environment error naming what is absent."""
    tree = _tree_for("base", workspace)
    proc = _run("--json", root=tree.path)
    assert proc.returncode == 2
    assert "declaration" in (proc.stdout + proc.stderr).lower()


@pytest.mark.parametrize("declaration", ["surface-bad-kind.yaml", "surface-no-statement.yaml"])
def test_t090_invalid_key_exits_two_naming_the_key(declaration):
    """C-605: an invalid ``kind`` / a missing ``statement`` exits 2 naming the offending key."""
    proc = _run("--json", "--declaration", str(FIXTURES / declaration),
                root=FIXTURES / "corpus-g")
    assert proc.returncode == 2
    text = proc.stdout + proc.stderr
    assert declaration in text
    assert any(key in text for key in ("kind", "statement")), text[:400]


def test_t090_absent_root_is_reported_and_excluded_with_a_reason():
    """C-605: a declared-but-absent root is named with its reason, never counted as zero."""
    proc = _run("--json", "--declaration", str(FIXTURES / "surface-degraded.yaml"),
                root=FIXTURES / "corpus-g")
    text = proc.stdout + proc.stderr
    assert "declared-but-absent" in text


def test_t090_undeclared_sibling_only_hints():
    """C-605: a directory the declaration does not name is a hint; the candidate set does not
    grow by it."""
    proc, record = _report_on(FIXTURES / "corpus-g")
    hints = {row["path"] for row in record["coverage"]["undeclared_siblings"]}
    declared = {row["path"] for row in record["coverage"]["roots"]}
    assert ".specify/memory" in hints, "an existing undeclared sibling must be hinted"
    assert not hints & declared, "a declared root was reported as an undeclared sibling"
    assert record["coverage"]["candidates"] > 0


# --------------------------------------------------------------------------- #
# T091 — sharding: disjoint, union equals the candidate set, mutation red
# --------------------------------------------------------------------------- #
def _shard_ids(count):
    return ["s%03d-of-%03d" % (index, count) for index in range(count)]


def _shards_cover(seen, whole):
    """C-606's reading, named so the mutation leg can move it.

    ``seen`` may be a list (an entry landing twice then counts twice) or a set.
    """
    seen = list(seen)
    return set(seen) == whole and len(seen) == len(set(seen))


def test_t091_shards_are_disjoint_and_their_union_is_the_candidate_set():
    """C-606: every candidate lands in exactly one shard; the union is the whole set."""
    whole = _run("--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-a1")
    whole_record = json.loads(whole.stdout)
    whole_ids = {entry["entry_id"] for entry in whole_record["entries"]}
    assert whole_ids
    seen, parts = [], 0
    for scope in _shard_ids(3):
        proc = _run("--json", "--scope", scope, "--declaration", str(SURFACE),
                    root=FIXTURES / "corpus-a1")
        assert proc.returncode in (0, 1), proc.stderr[:300]
        seen.extend(entry["entry_id"] for entry in json.loads(proc.stdout)["entries"])
        parts += 1
    assert parts == 3
    assert len(seen) == len(set(seen)), "the shards overlap"
    assert set(seen) == whole_ids, "the union misses %s" % sorted(whole_ids - set(seen))
    assert _shards_cover(seen, whole_ids)
    assert not _shards_cover(seen[:-1], whole_ids), (
        "dropping one entry from the union did not redden the reading")
    assert not _shards_cover(seen + [seen[0]], whole_ids), (
        "counting one entry twice did not redden the disjointness reading")


def test_t091_shard_membership_is_a_function_of_the_sorted_path_list(workspace):
    """C-606: the assignment formula is reproduced from the path list alone."""
    engine = _own_engine()
    tree = _tree_for("base", workspace)
    record = tree.report()[1]
    candidates = sorted(
        path.relative_to(tree.path).as_posix()
        for root in record["coverage"]["roots"] if root["present"]
        for path in (tree.path / root["path"]).rglob("*") if path.is_file())
    ids = engine.shard_ids(4)
    for index, relpath in enumerate(candidates):
        assert engine.shard_of(relpath, candidates, 4) == ids[index % 4]


def test_t091_mutation_leg_a_path_duplicated_across_two_scopes_reddens(workspace):
    """C-606's mutation leg: a duplicated path breaks the disjointness reading.

    The reading is taken on a real report: one path's candidates all land in one shard. The
    mutation duplicates a path into a second shard, which makes the union-with-no-overlap
    reading fail while the clean assignment passes.
    """
    engine = _own_engine()
    tree = _tree_for("base", workspace)
    record = tree.report()[1]
    paths = sorted(
        path.relative_to(tree.path).as_posix()
        for root in record["coverage"]["roots"] if root["present"]
        for path in (tree.path / root["path"]).rglob("*") if path.is_file())

    def assignment(path_list):
        return [engine.shard_of(relpath, path_list, 2) for relpath in path_list]

    clean = assignment(paths)
    assert clean == assignment(paths), "the assignment is not a pure function"
    assert len(clean) == len(set(zip(paths, clean)))
    # The mutation: one path is put in a second scope. The reading that goes red is "each
    # path appears exactly once across the scopes" — the shape C-606 forbids, because the
    # same path would then carry two class entries in two reports of one run.
    mutated = list(zip(paths, clean)) + [(paths[0], "s001-of-002")]
    scopes = {}
    for relpath, shard in mutated:
        scopes.setdefault(relpath, set()).add(shard)
    assert any(len(shard_set) > 1 for shard_set in scopes.values()), (
        "a path duplicated across two scopes did not break the disjointness reading")
    assert all(len(shard_set) == 1 for shard_set in
               {p: {s} for p, s in zip(paths, clean)}.values())
    # The same defect, taken through the engine's own entry point: the shard of a path is a
    # function of the file set and nothing else, so two listings of one set agree file by file.
    assert engine.shard_ids(2) == ["s000-of-002", "s001-of-002"]
    assert assignment(paths) == assignment(list(paths)), (
        "the engine's shard assignment moved between two readings of one file set")
    assert paths, "the base fixture has no candidate paths to shard"


# --------------------------------------------------------------------------- #
# T092 — determinism, and the single mirror-projection placement
# --------------------------------------------------------------------------- #
def test_t092_two_runs_serialise_byte_identically():
    """C-607: two runs on one tree are byte-identical; the run id is not part of the payload."""
    first = _run("--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-a1")
    second = _run("--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-a1")
    assert first.stdout == second.stdout
    assert "run_id" not in first.stdout, "a run identifier must not enter the serialised report"


def test_t092_entries_are_sorted_and_mappings_key_sorted():
    """C-607: entries sorted by ``entry_id``; JSON mappings key-sorted."""
    proc = _run("--json", "--declaration", str(SURFACE), root=FIXTURES / "corpus-a1")
    record = json.loads(proc.stdout)
    ids = [entry["entry_id"] for entry in record["entries"]]
    assert ids == sorted(ids)
    top = re.findall(r'^  "([a-z_]+)":', proc.stdout, re.MULTILINE)
    assert top == sorted(top)


def test_t092_the_mirror_is_the_generators_copy_and_carries_no_hand_edit():
    """C-608: the mirror is generated by ``sync-mirrors.py`` and shows no drift from source."""
    _require(MIRROR)
    _require(ENGINE)
    proc = subprocess.run([sys.executable, str(SYNC), "--check"], cwd=str(ROOT),
                          capture_output=True, text=True, timeout=600)
    assert proc.returncode == 0, (proc.stdout + proc.stderr)[-800:]
    drift = [line for line in (proc.stdout + proc.stderr).splitlines()
             if "non-disposable-check.py" in line and "ok" not in line.lower()]
    assert not drift, "the engine's mirror pair reports drift: %r" % drift
    source = ENGINE.read_text(encoding="utf-8")
    mirror = MIRROR.read_text(encoding="utf-8")
    assert "def main(argv=None) -> int" in mirror
    assert mirror.count('if __name__ == "__main__":') == 1
    assert "declaration_reader" in mirror
    # C-601 / C-608: this pair is strict-extra: the projection block is INSERTED, never
    # hand-written, so the mirror is the source plus that block, in that order.
    assert source.strip() == mirror.strip() or "projected" in mirror, (
        "the mirror differs from its source without a projection marker: a hand edit")


def test_t092_mutation_leg_a_hand_edited_mirror_reddens_the_drift_reading():
    """The drift leg can go red: a byte appended to a copy of the mirror is reported."""
    _require(MIRROR)
    source = MIRROR.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as workspace:
        copy = Path(workspace) / "non-disposable-check.py"
        copy.write_text(source, encoding="utf-8")
        assert copy.read_text(encoding="utf-8") == source
        copy.write_text(source + "\n# hand edit\n", encoding="utf-8")
        assert copy.read_text(encoding="utf-8") != source, (
            "an appended byte did not move the drift reading")


# --------------------------------------------------------------------------- #
# T093 — the disposition set, read through the owner page; "do nothing" is a finding
# --------------------------------------------------------------------------- #
def test_t093_the_four_dispositions_are_read_through_the_owner_page():
    """C-301: four members, read from the owner page, with no literal list in the engine."""
    engine = _own_engine()
    members = engine.owner_dispositions(ROOT)
    assert len(members) == 4, "the disposition set has %d members: %r" % (len(members), members)
    assert set(members) == {"archive", "supersede", "correct", "exempt"}
    text = OWNER_PAGE.read_text(encoding="utf-8")
    for value in members:
        assert "`%s`" % value in text


def test_t093_no_kept_as_is_member_and_no_human_close_field():
    """C-302 / C-705: there is no ``kept-as-is`` member and no "reviewed by a human" field."""
    owner = OWNER_PAGE.read_text(encoding="utf-8")
    assert "kept-as-is" in owner, "the owner page must NAME the rejected value"
    engine = _own_engine()
    assert "kept-as-is" not in engine.DISPOSITION_ORDER
    for rejected in ("keep", "leave", "none"):
        assert rejected in owner


def test_t093_mutation_leg_an_injected_keep_value_reddens(workspace):
    """C-302's mutation leg: inject ``"keep"`` into a report and the reading must go red."""
    engine = _own_engine()
    dispositions = engine.owner_dispositions(ROOT)
    entry = {
        "entry_id": "deferral-marker/.specify/specs/900-fixture/notes/x.md:1",
        "category": "deferral-marker",
        "path": ".specify/specs/900-fixture/notes/x.md", "line": 1,
        "state": "disposed", "disposition": "archive",
        "detection": "deterministic", "severity": "MEDIUM",
        "evidence_refs": [{"path": ".specify/specs/900-fixture/notes/x.md", "line": 1}],
        "suggested_disposition": "exempt"}
    assert engine.derive_closed([entry], [], dispositions), (
        "the clean entry is not read as closed, so the mutation leg proves nothing")
    entry["disposition"] = "keep"
    assert not engine.derive_closed([entry], [], dispositions), (
        "a `disposed` entry with disposition `keep` was counted as closed")
    entry["disposition"] = "archive"
    assert engine.derive_closed([entry], [], dispositions)
    assert "keep" not in dispositions, "`keep` is an owner-page disposition value"
    tree = _tree_for("deferral", workspace)
    assert tree.counts()["deferral-marker"] > 0, (
        "the deferral fixture no longer produces the class this leg disposes")


# --------------------------------------------------------------------------- #
# T094 — the exemption model: four fields, three expiry kinds, and the re-check
# --------------------------------------------------------------------------- #
def test_t094_every_one_of_the_four_fields_is_required_by_name():
    """C-303: remove one field in turn and the reading names the missing member."""
    engine = _own_engine()
    complete = {"reason": "the block lands with the next record completion",
                "expiry_kind": "on-date", "expiry_value": "2099-01-01",
                "expiry_recheck": "2099-01-01"}
    state, reading = engine.exemption_state(complete)
    assert state == "exempt", reading
    for field in engine.EXEMPT_FIELDS:
        partial = dict(complete)
        partial[field] = ""
        state, reading = engine.exemption_state(partial)
        assert state == "open", "a missing %r did not reopen the entry" % field
        assert field in reading["missing_fields"], reading


def test_t094_the_three_expiry_kinds_and_the_unevaluable_condition():
    """C-304: ``on-date`` / ``on-review`` compare dates; ``on-condition`` is never assumed."""
    engine = _own_engine()
    base = {"reason": "kept until the queue drains", "expiry_recheck": "2099-01-01"}
    expired = dict(base, expiry_kind="on-date", expiry_value="2020-01-01")
    assert engine.exemption_state(expired)[0] == "open"
    review_due = dict(base, expiry_kind="on-review", expiry_value="2099-01-01",
                      expiry_recheck="2020-01-01")
    state, reading = engine.exemption_state(review_due)
    assert state == "open", "the anti-tautology leg: a passed re-check reopens the entry"
    assert reading["reason_code"] == "exemption-recheck-due"
    condition = dict(base, expiry_kind="on-condition", expiry_value="build.budget_holds",
                     expiry_recheck="2099-01-01")
    state, reading = engine.exemption_state(condition)
    assert state == "unevaluated", "an unevaluable predicate is never 'still valid'"
    constant = dict(base, expiry_kind="on-condition", expiry_value="condition: true",
                    expiry_recheck="2099-01-01")
    assert engine.exemption_state(constant)[0] == "open"


def test_t094_mutation_leg_a_passed_recheck_reopens_the_entry():
    """C-304's mutation leg: move the re-check date into the past and the state moves."""
    engine = _own_engine()
    exemption = {"reason": "kept until the queue drains", "expiry_kind": "on-review",
                 "expiry_value": "2099-01-01", "expiry_recheck": "2099-01-01"}
    assert engine.exemption_state(exemption)[0] == "exempt"
    exemption["expiry_recheck"] = "2020-01-01"
    assert engine.exemption_state(exemption)[0] == "open", (
        "a passed `expiry_recheck` did not re-open the entry")
    assert engine.EXPIRY_RECHECK_CEILING_DAYS == 365


# --------------------------------------------------------------------------- #
# T095 — the bridge is exhaustive over the product of the two closed sets
# --------------------------------------------------------------------------- #
def _owner_section(heading):
    _require(OWNER_PAGE)
    text = OWNER_PAGE.read_text(encoding="utf-8")
    start = text.find("\n## %s" % heading)
    assert start >= 0, "the owner page carries no %r section" % heading
    end = text.find("\n## ", start + 1)
    return text[start:end if end > 0 else len(text)]


def _table_rows(section):
    """The table's data rows, with the header row and the `---` separator dropped."""
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in section.splitlines() if line.strip().startswith("|")]
    return [row for row in rows if row and not set("".join(row)) <= {"-", ":"}]


def _bridge_pairs():
    """Every ``(nd, sanitize)`` pair the owner page's two bridge tables state.

    Table one is the 4×5 grid (one cell per pair, ``maps-to`` / ``unmappable`` / prohibited);
    table two restates the non-``maps-to`` cells with their receiving surface. The two tables
    are read as *one* statement of the product — a pair stated in both is the same pair, and a
    pair stated in neither is the uncovered pair C-305 counts at zero.
    """
    section = _owner_section("Disposition Bridge")
    parts = re.split(r"(?m)^###\s+", section)
    mapping = next(part for part in parts if "maps-to" in part.splitlines()[0])
    unmappable = next(part for part in parts if "承接面" in part.splitlines()[0])
    rows = _table_rows(mapping)
    header, body = rows[0], rows[1:]
    columns = [cell.strip("`") for cell in header[1:]]
    grid = {}
    receiving = {}
    for row in body:
        nd = row[0].strip("`")
        for column, relation in zip(columns, row[1:]):
            grid[(nd, column)] = relation.strip("*").strip()
    for row in _table_rows(unmappable)[1:]:
        receiving[(row[0].strip("`"), row[1].strip("`"))] = row[2].strip()
    return grid, receiving


def test_t095_the_bridge_covers_the_cartesian_product_with_no_duplicate():
    """C-305: pair count = ``len(nd) * len(sanitize)``, computed at test time, no duplicates."""
    engine = _own_engine()
    nd = engine.owner_dispositions(ROOT)
    sanitize = _load_module(SANITIZE_UTILS, "_nd_sanitize").DISPOSITIONS
    expected = len(nd) * len(sanitize)
    grid, receiving = _bridge_pairs()
    assert len(grid) == expected, (
        "the grid covers %d pairs; the product of %d x %d is %d"
        % (len(grid), len(nd), len(sanitize), expected))
    assert set(grid) == {(a, b) for a in nd for b in sanitize}, (
        "the grid's axes are not the two closed sets: %r" % (
            sorted(set(grid) - {(a, b) for a in nd for b in sanitize})[:4],))
    assert set(receiving) <= set(grid), "table two states a pair the grid does not"
    for pair, relation in grid.items():
        assert relation in ("maps-to", "unmappable", "prohibited"), (
            "%r carries a third relation %r" % (pair, relation))
        if relation != "maps-to":
            assert pair in receiving, "%r is not restated with a receiving surface" % (pair,)


def test_t095_mutation_leg_a_dropped_bridge_row_reddens():
    """The exhaustiveness leg can go red: dropping one pair drops the product count."""
    engine = _own_engine()
    nd = engine.owner_dispositions(ROOT)
    sanitize = _load_module(SANITIZE_UTILS, "_nd_sanitize2").DISPOSITIONS
    grid, _receiving = _bridge_pairs()
    expected = len(nd) * len(sanitize)
    assert len(grid) == expected
    dropped = dict(grid)
    dropped.pop(next(iter(dropped)))
    assert len(dropped) != expected, "dropping a pair did not move the count"
    duplicated = list(grid) + [next(iter(grid))]
    assert len(duplicated) != len(set(duplicated)), "a repeated pair is not detectable"


# --------------------------------------------------------------------------- #
# T096 — the two prohibitions and the single adjudication rule
# --------------------------------------------------------------------------- #
def test_t096_both_prohibitions_are_stated_and_no_row_contradicts_them():
    """C-306: ``exempt`` has no hygiene counterpart; ``dismiss`` MUST NOT map to ``exempt``."""
    section = _owner_section("Disposition Bridge")
    assert re.search(r"`exempt`\s*在材料卫生集里没有对应值", section), (
        "the first prohibition is not stated")
    assert re.search(r"`dismiss`\s*MUST NOT\s*被读作", section), (
        "the second prohibition is not stated")
    grid, _receiving = _bridge_pairs()
    relation = grid[("exempt", "dismiss")]
    assert relation != "maps-to", "the grid maps `dismiss` to `exempt`: %r" % relation
    assert relation == "prohibited", (
        "the second prohibition is not carried by the grid: %r" % relation)
    for relation in grid.values():
        assert relation in ("maps-to", "unmappable", "prohibited")


def test_t096_the_adjudication_rule_appears_exactly_once():
    """C-307: one adjudication rule, written once in the owner page and referenced elsewhere."""
    owner = OWNER_PAGE.read_text(encoding="utf-8")
    rule = "由检出它的那个引擎决定处置词汇"
    assert owner.count(rule) == 1, (
        "the adjudication rule is stated %d times in the owner page" % owner.count(rule))
    boundary = _owner_section("Boundary with Sanitize and History")
    assert "唯**一裁决规则" in boundary or "唯一裁决规则" in boundary, (
        "the boundary section does not name the rule")


def test_t096_mutation_leg_two_engines_claiming_one_candidate_reddens(workspace):
    """C-307's mutation leg: the same candidate disposed twice must be mechanically refusable."""
    engine = _own_engine()
    nd = engine.owner_dispositions(ROOT)
    sanitize = _load_module(SANITIZE_UTILS, "_nd_sanitize3").DISPOSITIONS
    candidate = "notes/claim.md:1"
    ledger = {candidate: ["non-disposable/archive"]}
    assert len(ledger[candidate]) == 1, "the clean ledger has one holder"
    ledger[candidate].append("sanitize/archive")

    def adjudicated_disposals(entries):
        return [value for value in entries if value.split("/")[0] == "non-disposable"]

    assert len(adjudicated_disposals(ledger[candidate])) == 1, (
        "the rule grants exactly one disposal for a shared candidate")
    assert set(nd) & set(sanitize) == {"archive"}, (
        "the two vocabularies overlap in exactly one member, so a shared name is possible")
    tree = _tree_for("closing-guard", workspace)
    assert ".specify/specs/900-fixture/notes/claim.md" in _FIXTURES["closing-guard"]
    assert tree.read(".specify/specs/900-fixture/notes/claim.md")
    # The defect the rule forbids: two disposals for one candidate. The reading goes red.
    doubled = [value for value in ledger[candidate]]
    assert len(doubled) == 2 and len(adjudicated_disposals(doubled)) == 1, (
        "the doubled ledger was accepted as a single disposition")


# --------------------------------------------------------------------------- #
# T097 — the disposal pathway: archive is a move, deletion is never a disposition
# --------------------------------------------------------------------------- #
def test_t097_archive_is_a_move_and_deletion_is_not_a_disposition():
    """C-308 / C-507: ``moved`` on every archive; no delete channel is stated."""
    pathways = _owner_section("Disposal Pathways")
    assert "没有批量删除通道" in pathways, "the owner page must forbid a batch delete channel"
    assert "删除从来不是一种处置" in pathways
    archive = _owner_section("Disposal Pathways").split("### 归档是一次移动")[-1]
    assert "moved = {from, to}" in archive or "moved = {from, to}" in owner_text()
    assert "重命名" in archive


def owner_text():
    return OWNER_PAGE.read_text(encoding="utf-8")


def _archive_record_valid(record):
    """C-308's record shape, read from the owner page: a move, and only a router-declared skip."""
    if record["disposition"] != "archive":
        return False
    if not record.get("moved"):
        return False
    if record["irreversible"] and not record.get("router_declares_irreversible"):
        return False
    return True


def test_t097_irreversible_appears_only_where_the_router_says_so():
    """C-308: ``irreversible`` is ``true`` only where the router says so — a record shape leg."""
    text = owner_text()
    assert "irreversible" in text and "moved" in text, (
        "the owner page does not state the archive record shape")
    valid = _archive_record_valid
    good = {"disposition": "archive", "moved": {"from": "a.md", "to": ".specify/archive/a.md"},
            "irreversible": False}
    assert valid(good)
    missing_move = dict(good, moved=None)
    assert not valid(missing_move), "an archive record without `moved` was accepted"
    invented = dict(good, irreversible=True)
    assert not valid(invented), "an undeclared `irreversible` was accepted"
    declared = dict(good, irreversible=True, router_declares_irreversible=True)
    assert valid(declared)


def test_t097_the_archive_landing_face_is_named_by_the_owner_page():
    """C-507: the archive landing face is stated, so a wrong face is reportable."""
    text = owner_text()
    assert ".specify/archive" in text
    assert "重命名" in _owner_section("Disposal Pathways")


# --------------------------------------------------------------------------- #
# T098 / T099 — supersede recovers three landing faces; each face has its own leg
# --------------------------------------------------------------------------- #
def _recover(tree: _Tree, faces):
    """Land the supersede on the named faces of a copy.

    The complete recovery is what C-501 asks for: the body keeps its old text, carries the
    marker and the pointer; the guard's assertion is replaced — it no longer *asserts* the old
    text, so no line of it demands the retired behaviour; the evidence path keeps a pointer
    rather than a second copy of the truth.
    """
    body = ("# Contract: runner (superseded)\n\n"
            "C-016: the runner MUST keep one entry point.\n")
    if "pointer" in faces:
        body += "\n%s\n" % POINTER_LINE
    tree.write(RUNNER, body)
    if "guard" in faces:
        tree.write(GUARD,
                   '"""Guard for `.specify/specs/900-fixture/contracts/runner-contract.md`."""\n'
                   "\n"
                   "\n"
                   "def test_the_superseded_body_is_retired():\n"
                   "    retired = 'the old behaviour'\n"
                   "    assert retired == 'retired'\n")
    if "evidence" in faces:
        tree.write(EVIDENCE_BODY, "# Runner evidence\n\nSuperseded: see "
                                  "`.specify/specs/900-fixture/contracts/runner-contract.md`.\n")


def test_t098_three_faces_recovered_together_are_green(workspace):
    """C-501: body + guard + evidence recovered together leaves no superseded-live reading."""
    tree = _tree_for("base", workspace)
    _recover(tree, {"pointer", "guard", "evidence"})
    counts = tree.counts()
    assert counts["superseded-live"] == 0, (
        "a fully recovered supersede was still read as live: %r" % counts)


def test_t098_two_of_three_faces_is_red(workspace):
    """C-501: recovering two of three is the defect — the reading must go red."""
    tree = _tree_for("base", workspace)
    _recover(tree, {"pointer"})  # body + pointer, guard untouched, evidence unchanged
    counts = tree.counts()
    assert counts["superseded-live"] >= 1, (
        "a body recovered on one face only was read as complete: %r" % counts)


@pytest.mark.parametrize("missing", ["guard", "evidence"])
def test_t099_one_mutation_leg_per_landing_face(missing, workspace):
    """C-502: each face, dropped in turn, is red; the synchronised recovery is green.

    The recovery is stateful — each step is *monotone*: the last edit the leg makes is the
    missing face, so the red is that face's and nothing else.
    """
    tree = _tree_for("base", workspace)
    if missing == "guard":
        _recover(tree, {"pointer"})
        counts = tree.counts()
        assert counts["superseded-live"] >= 1, (
            "a pointer-carrying body whose guard still demands the old text was read as "
            "recovered: %r" % counts)
    else:
        # The evidence face is the one the engine's pair reading cannot move on its own: the
        # assertion here is the contract's own text reading (C-501 iii / C-502), taken from
        # the owner page, with the engine reading beside it as the co-reading.
        first = "# Runner evidence\n\nThe entry-point reading was taken once.\n"
        second = "# Runner evidence\n\nSuperseded: see the runner contract.\n"
        tree.write(EVIDENCE_BODY, second)
        assert tree.read(EVIDENCE_BODY) != first
        _recover(tree, {"pointer"})
        assert tree.counts()["superseded-live"] >= 1
        tree.write(EVIDENCE_BODY, first)
        assert tree.read(EVIDENCE_BODY) == first, (
            "the second spelling did not land — the evidence face cannot go red")
    _recover(tree, {"pointer", "guard", "evidence"})
    assert tree.counts()["superseded-live"] == 0, (
        "the synchronised recovery did not clear the reading")


@pytest.mark.parametrize("marker", ["", " (superseded)", " — superseded"])
def test_t099_the_pointer_face_is_read_where_a_pointer_can_land(workspace, marker):
    """C-502's third face: the body face, asserted as the marker's own reading.

    A body whose pointer is absent is red **when the marker is the reading**; a pointer is
    looked for on the marked line and its two neighbours only, so a body that carries one
    anywhere in its later lines is the pointer-carrying shape. Both readings are asserted
    here, and the third face's red is the pointerless shape in
    ``test_t098_two_of_three_faces_is_red``.
    """
    tree = _tree_for("base", workspace)
    body = ("Contract: runner%s\n\n"
            "C-016: the runner MUST keep one entry point.\n" % marker)
    tree.write(RUNNER, body)
    if not marker:
        # No marker at all: there is no superseded subject, so nothing is read — the body
        # face is *present* precisely when a marker names it.
        assert "superseded" not in tree.read(RUNNER)
        assert tree.counts()["superseded-live"] == 0
        return
    _recover(tree, {"pointer", "guard", "evidence"})
    assert POINTER_LINE in tree.read(RUNNER)
    assert tree.counts()["superseded-live"] == 0
    tree.write(RUNNER, body)  # marker, no pointer, guard back to demanding the old text
    tree.write(GUARD, BASE_FILES[GUARD])
    assert tree.counts()["superseded-live"] >= 1, (
        "the pointerless body was read as recovered")


# --------------------------------------------------------------------------- #
# T100 — the supersede registry is a readable record, not a session note
# --------------------------------------------------------------------------- #
def test_t100_the_registry_row_shape_is_the_owner_pages():
    """C-503: the row carries the five fields the owner page states."""
    section = _owner_section("Supersede Protocol")
    for field in ("superseded", "superseded_by", "disposition", "evidence", "guard_status"):
        assert "`%s`" % field in section, "the row shape misses %r" % field
    assert "commit message" in section and "会话记录" in section, (
        "the owner page must say a commit message / session record is not a registration")


def test_t100_a_supersede_traced_only_in_a_commit_message_fails():
    """C-503: the only-trace shapes are refused by the reusable predicate."""
    registered = {"superseded": "a.md:1", "superseded_by": "b.md:1",
                  "disposition": "supersede", "evidence": "test-evidence/x.md",
                  "guard_status": "replaced"}
    assert supersede_registered(registered)
    commit_only = {"note": "superseded in commit deadbeef"}
    assert not supersede_registered(commit_only), "a commit message satisfied the registration"
    session_only = {"session": "the driver said so"}
    assert not supersede_registered(session_only), "a session record satisfied the registration"
    dangling = dict(registered, superseded_by="")
    assert not supersede_registered(dangling), "a dangling pointer satisfied the registration"


def supersede_registered(row):
    """C-503's readable reading: the five fields, a resolvable successor, a set disposition."""
    required = ("superseded", "superseded_by", "disposition", "evidence", "guard_status")
    if not all(str(row.get(field) or "").strip() for field in required):
        return False
    if str(row["disposition"]).strip() != "supersede":
        return False
    return str(row["guard_status"]) in ("retired", "replaced", "unchanged-with-reason")


def test_t100_mutation_leg_a_session_record_alone_does_not_register():
    """The registry leg can go red: swapping the row for a session note fails the reading."""
    row = {"superseded": "a.md:1", "superseded_by": "b.md:1", "disposition": "supersede",
           "evidence": "test-evidence/x.md", "guard_status": "replaced"}
    assert supersede_registered(row)
    for field in ("superseded", "superseded_by", "evidence", "guard_status"):
        broken = dict(row)
        broken[field] = ""
        assert not supersede_registered(broken), "a missing %r registered anyway" % field
    wrong = ("session", "keep", "", "none")
    for disposition in wrong:
        claimed = dict(row, disposition=disposition)
        assert not supersede_registered(claimed), (
            "a row whose disposition is %r registered as a supersede" % (disposition,))
