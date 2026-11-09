"""The seam-bypass guard for Feature 092 — Non-Disposable.

Subject: **one** closure, stated in ``contracts/four-stage-command.contract.md`` C-410 and read
as the *same* reading as C-407 (the contract says so in its own words: "which is the same reading
as the execute-segment rule in clause C-407, not a second one"):

    An execute run that touches a path not named in a confirmed design row is a red reading;
    a path a confirmed design row does name is a green reading; and every edit the seam makes
    carries before/after readings.

Three things this file is *not*:

* **Not a second seam.** The stage names, the step positions and the confirmation granularity are
  owned by ``skills/internal/manage-history/SKILL.md`` and restated nowhere here — this file
  reaches them by reading that one file, and a leg fails if the pointer stops resolving.
* **Not an engine leg.** ``non-disposable-check.py`` judges the *review surface*; the seam's
  no-bypass rule is a property of the **execute run's own path set**. The engine has no
  "seam" class and this file does not ask it for one.
* **Not a guard of the guard.** The reading is implemented here as a small predicate over a
  declared confirmed-row set and an observed touched-path set. The mutation legs are what make
  the predicate falsifiable: each leg flips exactly one side of the reading and the assertion is
  required to move. A predicate that would go green either way (a check that cannot go red when
  its subject breaks) is the defect this file exists to catch.

**Fixture data stated here, in this file.** The trees are materialised per leg under a temp root
and never touch the fixture directory (the sibling guard's convention):

======================================  ==================================================
tree name                               what it states
======================================  ==================================================
``confirmed``                           three confirmed design rows (spec body, owner page,
                                        guard) and an execute run whose touched set is exactly
                                        those three — the *green* half of the pair
``bypass``                              the same three rows, plus one path no row names —
                                        the *red* half of the pair
``stale-row``                           a row whose confirmation has expired: the path is
                                        named, the row is not confirmed — still red
``alias``                               a path named in a non-normalised spelling (``./``, a
                                        ``//``) that normalises onto a confirmed row — green
``subpath``                             a directory row that does not cover an unlisted child —
                                        red (a row names the file it names, not its subtree)
======================================  ==================================================

**Red-first, in this file's own record.** Every leg has a mutation leg beside it. The predicate
is falsified two ways — by widening what counts as confirmed and by narrowing what counts as
touched — and both mutations are asserted to redden. That is the evidence that the green legs
above are earned rather than vacuous.

Owner-page clause text is read from ``.specify/shared/definitions/non-disposable-definitions.md``
§ ``## Seam Bypass``; the framework-source half is ``shared/definitions/…``. The two are a
byte-equal mirror pair (``plan.md`` § Mirror Obligations), and this file asserts they agree rather
than reading one and trusting the other.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".specify" / "specs" / "092-non-disposable" / "contracts" / \
    "four-stage-command.contract.md"
SKILL = ROOT / "skills" / "internal" / "manage-history" / "SKILL.md"
OWNER_SOURCE = ROOT / "shared" / "definitions" / "non-disposable-definitions.md"
OWNER_MIRROR = ROOT / ".specify" / "shared" / "definitions" / "non-disposable-definitions.md"

#: The clause this whole file reads. Spelled once so that a renamed clause is a named failure.
CLAUSE = "C-410"

#: The owner-page section that must carry the rule's *statement* (the contract fixes how the guard
#: reads the rule; the owner page states it once, and the skill and contract point at it).
OWNER_SECTION = "Seam Bypass"


# ------------------------------------------------------------------------------------------- #
# the reading — a predicate over a declared confirmed set and an observed touched set
# ------------------------------------------------------------------------------------------- #
def _normalise(path: str) -> str:
    """Repo-relative POSIX spelling of ``path``, with ``.`` / ``..`` / ``//`` folded.

    Normalisation is where an alias is caught — ``./a/b`` and ``a//b`` are the same path as
    ``a/b``, and a reading that compared raw strings would call a legal write a bypass. It is
    also deliberately **not** a wildcard: a directory name normalises to itself and covers only
    itself.
    """
    parts = []
    for part in path.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == ".." and parts and parts[-1] != "..":
            parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _confirmed_paths(rows):
    """The path set a *confirmed* design row names.

    A row is a mapping with ``path``, ``confirmed`` and — when confirmed — ``readings`` (the
    before/after pair the rule requires). An unconfirmed row contributes nothing: the rule is
    "named **and** confirmed", and dropping the confirmation side is one of the two mutations
    the legs below perform.
    """
    named = set()
    for row in rows:
        if not row.get("confirmed"):
            continue
        for path in row.get("paths", (row.get("path"),)):
            if path:
                named.add(_normalise(path))
    return named


def seam_reading(rows, touched):
    """The seam's no-bypass reading: ``(verdict, offending_paths, reason)``.

    ``verdict`` is ``"green"`` exactly when every normalised touched path is named by a
    confirmed design row and every confirmed row that names a touched path carries its
    before/after readings. Anything else is ``"red"``, and the offenders are named — a red
    reading that does not point at the path is not actionable and does not meet C-410's "MUST
    carry before/after readings" obligation either.
    """
    confirmed = _confirmed_paths(rows)
    normalised_touched = sorted({_normalise(path) for path in touched})

    outside = [path for path in normalised_touched if path not in confirmed]
    if outside:
        return "red", outside, "touched a path no confirmed design row names"

    missing_rows = []
    for row in rows:
        if not row.get("confirmed"):
            continue
        if not any(_normalise(p) in normalised_touched for p in row.get("paths", (row.get("path"),)) if p):
            continue
        readings = row.get("readings") or {}
        if not readings.get("before") or not readings.get("after"):
            missing_rows.append(_normalise(row.get("path") or row["paths"][0]))
    if missing_rows:
        return "red", sorted(missing_rows), "a confirmed row's edit carries no before/after readings"

    return "green", [], "every touched path is named by a confirmed design row, with readings"


# ------------------------------------------------------------------------------------------- #
# fixture trees — stated here, materialised per leg
# ------------------------------------------------------------------------------------------- #
_ROWS = (
    ("spec body", ".specify/specs/092-non-disposable/requirements.md"),
    ("owner page", "shared/definitions/non-disposable-definitions.md"),
    ("guard", "tests/contract/test_non_disposable_seam_bypass.py"),
)

_READINGS = {"before": "F-092-SEAM-before", "after": "F-092-SEAM-after"}


def _row(path, confirmed=True, readings=_READINGS, paths=None):
    row = {"path": path, "confirmed": confirmed, "readings": dict(readings)}
    if paths is not None:
        row["paths"] = list(paths)
    return row


def _tree_files(name):
    """Each fixture tree as ``{relpath: text}``; legs read the same data they materialise."""
    rows = [_row(path) for _, path in _ROWS]
    touched = [path for _, path in _ROWS]
    if name == "confirmed":
        pass
    elif name == "bypass":
        touched = touched + [".specify/specs/092-non-disposable/plan.md"]
    elif name == "stale-row":
        rows = [_row(path, confirmed=(i < 2)) for i, (_, path) in enumerate(_ROWS)]
    elif name == "alias":
        touched = ["./" + touched[0], touched[1].replace("/", "//", 1), touched[2]]
    elif name == "subpath":
        rows = [_row(".specify/specs/092-non-disposable/", paths=[".specify/specs/092-non-disposable/"])]
        touched = [".specify/specs/092-non-disposable/plan.md"]
    else:  # pragma: no cover - a typo in a leg is a KeyError with the tree's name
        raise KeyError(name)
    files = {"rows.json": json.dumps({"rows": rows, "touched": touched}, indent=1)}
    for _, path in _ROWS:
        files[path] = "# fixture body for %s\n" % path
    return files


class _Tree:
    """A writable materialisation of one fixture tree — never the fixture directory itself."""

    def __init__(self, name: str, workspace: Path):
        self.name = name
        self.path = workspace / name
        for relpath, text in _tree_files(name).items():
            target = self.path / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")

    def data(self):
        return json.loads((self.path / "rows.json").read_text(encoding="utf-8"))

    def reading(self, mutate=None):
        data = self.data()
        rows, touched = data["rows"], data["touched"]
        if mutate == "unconfirmed-rows":
            for row in rows:
                row["confirmed"] = True
        elif mutate == "drop-touched":
            touched = touched[:1]
        elif mutate == "raw-strings":
            return _raw_seam_reading(rows, touched)
        return seam_reading(rows, touched)


def _raw_seam_reading(rows, touched):
    """The *un*normalised comparison — kept only so a leg can prove normalisation carries weight."""
    confirmed = {row["path"] for row in rows if row.get("confirmed")}
    outside = [path for path in touched if path not in confirmed]
    return ("red", outside, "raw string comparison") if outside else ("green", [], "raw")


@pytest.fixture()
def workspace():
    with tempfile.TemporaryDirectory(prefix="nd-seam-") as directory:
        yield Path(directory)


@pytest.fixture()
def tree(request, workspace):
    return _Tree(request.param, workspace)


# ------------------------------------------------------------------------------------------- #
# the authority artifacts resolve — a pointer that stops resolving is a named failure
# ------------------------------------------------------------------------------------------- #
def test_t156_the_contract_clause_and_the_skill_seam_both_exist():
    """C-410 is a live clause, and the skill it fixes still carries the seam it talks about."""
    for path in (CONTRACT, SKILL):
        assert path.exists(), "the seam's authority artifact is missing at %s" % path
    contract_text = CONTRACT.read_text(encoding="utf-8")
    assert "## %s " % CLAUSE in contract_text, "the contract no longer carries %s" % CLAUSE
    clause = contract_text.split("## %s " % CLAUSE, 1)[1]
    clause = clause.split("\n## ", 1)[0]
    assert "confirmed design" in clause, "C-410 stopped naming the confirmed-design-row reading"
    assert "before/after readings" in clause, "C-410 stopped requiring the readings"

    skill_text = SKILL.read_text(encoding="utf-8")
    assert "No bypass" in skill_text, "the skill dropped its no-bypass rule"
    assert "confirmed" in skill_text.lower(), "the skill's rule stopped naming confirmation"


def test_t156_the_owner_page_states_the_rule_and_its_mirror_agrees():
    """The rule's statement lives on the owner page; the ``.specify/`` half is its mirror."""
    for path in (OWNER_SOURCE, OWNER_MIRROR):
        assert path.exists(), "owner page missing at %s" % path
    source = OWNER_SOURCE.read_text(encoding="utf-8")
    assert "\n## %s\n" % OWNER_SECTION in source, \
        "the owner page carries no § %r — the rule has no owner-side statement" % OWNER_SECTION
    section = source.split("\n## %s\n" % OWNER_SECTION, 1)[1].split("\n## ", 1)[0]
    assert "confirmed design row" in section, "§ %s stopped naming the design row" % OWNER_SECTION
    assert "改动前后的读数" in section, "§ %s stopped requiring the readings" % OWNER_SECTION
    assert "§ Capture Rule" in section, \
        "§ %s stopped pointing at the readings' owner (§ Capture Rule) — a copy would drift" % OWNER_SECTION
    assert OWNER_MIRROR.read_text(encoding="utf-8") == source, \
        "the owner page's .specify/ mirror drifted — it is generated, never hand-edited"


# ------------------------------------------------------------------------------------------- #
# the pair: confirmed-row path green, un-named path red
# ------------------------------------------------------------------------------------------- #
@pytest.mark.parametrize("tree", ["confirmed"], indirect=True)
def test_t156_a_confirmed_row_path_is_green(tree):
    """C-410 green half: an execute run touching only confirmed-row paths reads green."""
    verdict, offenders, _ = tree.reading()
    assert verdict == "green", "confirmed-row paths read red: %r" % (offenders,)
    assert offenders == []


@pytest.mark.parametrize("tree", ["bypass"], indirect=True)
def test_t156_a_path_no_confirmed_row_names_is_red(tree):
    """C-410 red half: one un-named path is enough to redden the reading, and it is named."""
    verdict, offenders, reason = tree.reading()
    assert verdict == "red"
    assert offenders == [".specify/specs/092-non-disposable/plan.md"], offenders
    assert "no confirmed design row" in reason


def test_t156_the_pair_is_one_predicate_not_two(workspace):
    """The green and the red halves differ by exactly one row-less path — not by a second rule."""
    green = _Tree("confirmed", workspace).data()
    red = _Tree("bypass", workspace).data()
    assert green["rows"] == red["rows"], "the pair's row sets differ; the pair is not controlled"
    assert set(red["touched"]) - set(green["touched"]) == {
        ".specify/specs/092-non-disposable/plan.md"}


# ------------------------------------------------------------------------------------------- #
# confirmation is load-bearing, and normalisation is load-bearing
# ------------------------------------------------------------------------------------------- #
@pytest.mark.parametrize("tree", ["stale-row"], indirect=True)
def test_t156_a_named_but_unconfirmed_row_is_still_red(tree):
    """The rule is "named **and** confirmed" — a named path whose row was never confirmed reddens."""
    verdict, offenders, reason = tree.reading()
    assert verdict == "red", "an unconfirmed row's path read green — confirmation is not load-bearing"
    assert offenders == ["tests/contract/test_non_disposable_seam_bypass.py"], offenders
    assert "no confirmed design row" in reason


@pytest.mark.parametrize("tree", ["alias"], indirect=True)
def test_t156_an_alias_of_a_confirmed_path_is_green(tree):
    """``./x`` and ``x//y`` are the same path as ``x`` — a raw-string reading would call them bypasses."""
    verdict, offenders, _ = tree.reading()
    assert verdict == "green", "a legal alias read red: %r" % (offenders,)
    raw_verdict, raw_offenders, _ = tree.reading(mutate="raw-strings")
    assert raw_verdict == "red" and raw_offenders, \
        "normalisation carries no weight: the raw reading agrees with the normalised one"


@pytest.mark.parametrize("tree", ["subpath"], indirect=True)
def test_t156_a_directory_row_does_not_cover_an_unlisted_child(tree):
    """A row names the file it names; a directory name is not a subtree grant (no wildcard)."""
    verdict, offenders, _ = tree.reading()
    assert verdict == "red"
    assert offenders == [".specify/specs/092-non-disposable/plan.md"], offenders


# ------------------------------------------------------------------------------------------- #
# mutation legs — the predicate is falsified on both sides
# ------------------------------------------------------------------------------------------- #
@pytest.mark.parametrize("tree", ["stale-row"], indirect=True)
def test_t156_mutation_leg_widening_confirmation_reddens_to_green(tree):
    """Falsify the confirmation side: confirmed becomes unconditional and the red half turns green."""
    verdict, _, _ = tree.reading()
    assert verdict == "red", "the leg starts from a reading that is not red"
    mutated = tree.reading(mutate="unconfirmed-rows")
    assert mutated[0] == "green", "widening 'confirmed' did not move the reading"


@pytest.mark.parametrize("tree", ["bypass"], indirect=True)
def test_t156_mutation_leg_narrowing_the_touched_set_reddens_to_green(tree):
    """Falsify the touched side: drop the un-named path and the red half turns green."""
    verdict, _, _ = tree.reading()
    assert verdict == "red", "the leg starts from a reading that is not red"
    mutated = tree.reading(mutate="drop-touched")
    assert mutated[0] == "green", "narrowing the touched set did not move the reading"


@pytest.mark.parametrize("tree", ["confirmed"], indirect=True)
def test_t156_mutation_leg_dropping_the_readings_reddens_the_green_half(tree):
    """The readings half is load-bearing too: a confirmed row without readings cannot read green."""
    data = tree.data()
    assert seam_reading(data["rows"], data["touched"])[0] == "green"
    stripped = [dict(row, readings={}) for row in data["rows"]]
    verdict, offenders, reason = seam_reading(stripped, data["touched"])
    assert verdict == "red", "a confirmed row with no before/after readings still read green"
    assert len(offenders) == len(_ROWS)
    assert "before/after readings" in reason


def test_t156_the_predicate_is_still_a_predicate():
    """A guard that reddens everything or greenlights everything is not a guard."""
    rows = [_row(".specify/specs/092-non-disposable/requirements.md")]
    assert seam_reading(rows, [".specify/specs/092-non-disposable/requirements.md"])[0] == "green"
    assert seam_reading(rows, [".specify/specs/092-non-disposable/tasks.md"])[0] == "red"
    assert seam_reading([], [])[0] == "green", "an empty run touches nothing and is not a bypass"
    assert seam_reading([], ["anything.md"])[0] == "red", "an unconfirmed-only tree must never green"


# ------------------------------------------------------------------------------------------- #
# the readings requirement is visible in the seam's own carrier
# ------------------------------------------------------------------------------------------- #
def test_t156_the_execute_segment_requires_readings_before_the_first_write():
    """Capture Rule → execute: the seam's own step order names the readings *before* the writes."""
    text = SKILL.read_text(encoding="utf-8")
    start = text.find("执行段 — 执行 (execute)")
    assert start >= 0, "the skill carries no execute segment"
    segment = text[start:]
    readings = segment.find("Capture Rule")
    groups = segment.find("Group by group")
    assert 0 <= readings < groups, \
        "the execute segment no longer takes the Capture Rule readings before the first write"


def test_t156_the_guard_file_declares_no_second_seam():
    """C-410 is one reading: this file points at the seam, it does not restate the four stages.

    The stage labels are *built* so that this assertion does not match its own source — a leg
    that reads its own literal would go red on the fix, which is the mirror of the defect it
    guards against.
    """
    text = Path(__file__).read_text(encoding="utf-8")
    labels = ("0", "A", "B")
    restated = ["Step " + label for label in labels if len(text.split("Step " + label)) > 2]
    assert not restated, "the four-stage seam is restated here: %r" % restated
