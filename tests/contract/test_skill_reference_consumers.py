"""Contract tests for Feature 082 US5 — the five consumers (T027).

Owns two halves of SC-007 (``contracts/skill-reference.contract.md`` SR-01 … SR-06
and ``contracts/guard-and-measurement.contract.md`` GM-12):

1. **Wiring** — each of the five ``SKILL.md`` files (``run-skills``,
   ``create-skills``, ``improve-skills``, ``merge-skills``, ``coaching-skills``)
   carries **exactly one** reference to the framework-source owner path
   ``shared/definitions/skill-reference-definitions.md`` and no reference string
   prefixed ``.specify/shared/definitions/``.
2. **Containment** — every ``SKILL.md`` under the framework-source ``skills/`` tree
   (mirrors excluded from the denominator; they are proved separately by
   ``sync-mirrors.py --check``) is scanned for copies of the normalization-step
   literals and of the failure-table names. The three permitted classes are named
   constants and counted separately; every hit is reported with path and line
   number, and the scanned file count is printed.

The scanned vocabulary is the owner table's own: the eight ``NP-n`` step identifiers
(unambiguous everywhere) and the four class names of ``data-model.md`` E-10, read at
call time and never retyped here. FR-024 states the four conditions in prose
(``零命中`` / ``路径落在已知位置之外`` / …) and carries **no** surrogate identifier, which is
T027's premise. The class names alone are ordinary English — ``unreadable`` is a record
status in ``sanitize-materials`` and a page quality in ``improve-docs`` — so they are
counted **by form** (table cell, definition-list member, or a token standing alone) and
reported per class; the class **criteria** are the vocabulary that cannot be re-spoken
by accident, and one of them already stands in a consumer (``run-skills`` § 33, red
until the T031 rewrite).

Red-first (GM-11): the five wiring references and the owner's final wording are not
in place yet, so this module goes red on a real finding, never on an import error.
Each assertion is a standalone function so the GM-07 negative case can re-run it
against a ``tmp_path`` copy.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: SR-01 … SR-06 — the framework-source owner path every consumer cites, once.
OWNER_PATH = "shared/definitions/skill-reference-definitions.md"

#: GR-08 — the generated-mirror prefix a consumer MUST NOT cite.
MIRROR_PREFIX = ".specify/shared/definitions/"

#: FR-026 — the five consumers, by their directory name in the source ``skills/`` tree.
CONSUMERS = (
    "skills/internal/run-skills/SKILL.md",
    "skills/external/create-skills/SKILL.md",
    "skills/external/improve-skills/SKILL.md",
    "skills/external/merge-skills/SKILL.md",
    "skills/external/coaching-skills/SKILL.md",
)

#: GM-12 要件 1 — the baseline the historical hits are located against (never asserted).
BASELINE = "3ffeb26e"

#: GM-12 要件 3 — the three permitted hit classes, named and counted separately.
PERMITTED_CLASSES = {
    "owner": ("shared/definitions/skill-reference-definitions.md",),
    "owner-mirror": (".specify/shared/definitions/skill-reference-definitions.md",),
    "fixture": ("tests/fixtures/skill-reference/",),
}

#: GM-12 要件 4 — the normalization-step literals a copy would carry: the identifiers
#: NP-1 … NP-8 appear nowhere else in the tree (measured: 0 hits before this row).
STEP_LITERALS = tuple("NP-%d" % i for i in range(1, 9))

#: § Failure semantics — the four class names, literal with ``data-model.md`` E-10.
FAILURE_NAMES = ("zero-hit", "out-of-ladder", "unreadable", "dual-layer")

#: GM-12 要件 4 — the **second vocabulary** of the same failure table: the class
#: **criteria** a consumer would copy alongside a class name. The class names alone are
#: ordinary English (``unreadable`` is a record status in ``sanitize-materials``, a page
#: quality in ``improve-docs``); the criteria are what cannot be re-spoken by accident,
#: and one of them already stands in a consumer (``run-skills`` § 33).
CRITERIA_LITERALS = (
    "路径落在已知位置之外",
    "目录无可读 `SKILL.md`",
    "两个不同层同名命中",
)

#: A definition list a Skill opens for its own contract: the remainder of a line from
#: the first ``:` … `span``` pair on. Its members are that Skill's values.
_DEFINITION_LIST_RE = re.compile(r":\s*`[^`]+`")

#: GM-12 要件 4 — the owner table's own row set, read at call time (the owner is the
#: table, not this module).
DATAMODEL_REL = Path(".specify/specs/082-mechanism-policy-separation/data-model.md")


def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Half 1 — the five-consumer wiring
# --------------------------------------------------------------------------- #
def owner_reference_lines(text: str) -> list[int]:
    """1-based line numbers carrying a reference to the framework-source owner path."""
    hits: list[int] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for occurrence in re.finditer(re.escape(OWNER_PATH), line):
            start = occurrence.start()
            head = line[:start]
            # The mirror spelling ends with the owner path; it is a different coordinate.
            if head.endswith(MIRROR_PREFIX):
                continue
            hits.append(number)
    return hits


def mirror_reference_lines(text: str) -> list[int]:
    """1-based line numbers whose reference string is prefixed ``.specify/shared/definitions/``."""
    return [number for number, line in enumerate(text.splitlines(), start=1)
            if MIRROR_PREFIX + "skill-reference-definitions.md" in line]


def assert_consumer_wiring(paths) -> list[str]:
    problems: list[str] = []
    for path in paths:
        text = _read(path)
        refs = owner_reference_lines(text)
        mirrors = mirror_reference_lines(text)
        if len(refs) != 1:
            problems.append("%s: %d references to the source owner path (%s), expected exactly 1"
                            % (path, len(refs), "lines %s" % refs if refs else "none"))
        if mirrors:
            problems.append("%s: mirror-path reference(s) at line(s) %s — a consumer cites "
                            "the framework source, never the generated mirror"
                            % (path, mirrors))
    return problems


def test_sr01_to_sr06_each_consumer_cites_the_source_owner_once():
    problems = assert_consumer_wiring(REPO_ROOT / p for p in CONSUMERS)
    assert not problems, "SC-007 wiring violations:\n- " + "\n- ".join(problems)


def test_sr01_to_sr06_negative_case_mirror_reference_turns_red(tmp_path):
    relative = Path(CONSUMERS[0])
    text = _read(REPO_ROOT / relative)
    assert OWNER_PATH in text, "artifact missing: %s cites no owner path" % relative
    broken = text.replace(OWNER_PATH, MIRROR_PREFIX + "skill-reference-definitions.md", 1)
    copied = tmp_path / relative
    copied.parent.mkdir(parents=True)
    copied.write_text(broken, encoding="utf-8")
    problems = assert_consumer_wiring([copied])
    assert any("mirror-path reference" in p for p in problems), (
        "the negative case did not turn the mirror-path assertion red: %r" % problems)


# --------------------------------------------------------------------------- #
# Half 2 — the containment scan
# --------------------------------------------------------------------------- #
def failure_names_from_owner(datamodel: str) -> list[str]:
    """The four class names, read from ``data-model.md`` E-10 rather than retyped.

    FR-024 is the condition owner but spells the conditions as prose and names no class
    identifier; E-10 is the owner table's own row set. The read is cross-checked against
    :data:`FAILURE_NAMES`, so a table that grows or renames a row fails here instead of
    quietly widening (or narrowing) what the scan searches for.
    """
    block = datamodel[datamodel.index("E-10"):] if "E-10" in datamodel else ""
    assert block, "artifact missing: data-model.md carries no E-10 failure table"
    rows = [line.strip().strip("|").split("|")[0].strip().strip("`* ")
            for line in block.splitlines() if line.lstrip().startswith("|")]
    names = [name for name in rows if name in FAILURE_NAMES]
    assert names == list(FAILURE_NAMES), (
        "artifact missing: E-10 lists %r, not the four § Failure semantics rows %r"
        % (names, list(FAILURE_NAMES)))
    return names


def permitted_class(relative: str) -> str | None:
    """Which permitted class a repository-relative path belongs to, or ``None``."""
    for name, markers in PERMITTED_CLASSES.items():
        if any(relative == marker or relative.startswith(marker) for marker in markers):
            return name
    return None


def contains_failure_name(line: str, name: str) -> bool:
    """Is ``name`` present as a whole literal, code-span delimiters ignored?

    GM-12 要件 4: a match must not hinge on the backticks, so the line is compared
    with the delimiters removed, and the boundary is the literal's own ends — not
    "three characters share a prefix".
    """
    plain = line.replace("`", "")
    return re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(name), plain) is not None


def scan_step_literals(relative: str, text: str) -> list[tuple[str, int, str]]:
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        for literal in STEP_LITERALS:
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(literal), line):
                hits.append((relative, number, literal))
    return hits


def scan_failure_names(relative: str, text: str, names) -> list[tuple[str, int, str]]:
    """Count the four class names — as an **identifier**, never as an ordinary word.

    Requirement side: the class names are drawn from the owner table alone, the decision
    CL-01 fixed (FR-024's conditions are prose and carry no identifier of their own).

    Detector side: a bare English word is not an identifier. ``unreadable`` is a record
    status in ``sanitize-materials``, a page quality in ``improve-docs`` and an
    environment-error wording in four meta-skills; none of them is this table. The
    spelling that *is* this table's is a code-span identifier outside any definition
    list the host Skill opens for its own contract — i.e. the ``| `zero-hit` | … |``
    table-row form. A re-spoken criterion is caught by :func:`scan_criteria_literals`,
    so nothing is lost by tightening this one.
    """
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        for name in names:
            if _counts_as_class_name(line, name):
                hits.append((relative, number, name))
    return hits


def _counts_as_class_name(line: str, name: str) -> bool:
    """Is ``name`` on this line in the form the owner's table uses for a class?

    Only three forms count: a table row's leading cell, a definition-list member, and a
    bare token standing alone on its line — the three shapes a copied table actually
    takes. An English sentence's adjective (``an unreadable page``) or a comma list's
    final member is not an identifier, and counting it makes the gate shout at prose
    written years earlier. The count is still reported per class, so an abbreviated
    ruling is visible rather than silent.
    """
    plain = line.replace("`", "")
    if not contains_failure_name(plain, name):
        return False
    if re.match(r"^\s*\|\s*\**%s\**\s*\|" % re.escape(name), plain):
        return True
    if re.search(r":\s*`?%s`?(?:\s*[,)]|$)" % re.escape(name), plain):
        return True
    # Bare means bare: the token stands on its own between delimiters, not inside a
    # sentence. ``unreadable,`` in a comma list and ``an unreadable page`` both fail here.
    return re.fullmatch(r"\s*(?:[-*]\s+|#+\s*)?%s[.:;]?\s*" % re.escape(name),
                        plain) is not None


def scan_criteria_literals(relative: str, text: str) -> list[tuple[str, int, str]]:
    """The copy detector that carries no false-positive ledger.

    A class **name** is counted by :func:`scan_failure_names` and reported with its
    per-class count; a class **criterion** (:data:`CRITERIA_LITERALS`) is a copy the
    moment it stands outside the owner, in any Skill that does not own the table.
    Whitespace and backticks are normalized away so a reflow is not an escape hatch.
    """
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        plain = re.sub(r"\s+", "", line.replace("`", ""))
        for literal in CRITERIA_LITERALS:
            if re.sub(r"\s+", "", literal.replace("`", "")) in plain:
                hits.append((relative, number, literal))
    return hits


def scan_tree(root: Path, names) -> dict:
    """Scan every ``skills/**/SKILL.md`` under ``root``.

    The unit is the framework-source path (``skills/…``); the ``.specify/`` mirror is
    *not* in the denominator (GM-12 要件 2). Returns the scanned count, the hits with
    their permitted class, and a per-class count of permitted hits.
    """
    scanned: list[str] = []
    hits: list[tuple[str, int, str, str]] = []
    permitted_counts = {name: 0 for name in PERMITTED_CLASSES}
    skills_root = root / "skills"
    assert skills_root.is_dir(), "artifact missing: %s" % skills_root
    for path in sorted(skills_root.rglob("SKILL.md")):
        relative = path.relative_to(root).as_posix()
        if ".specify" in Path(relative).parts:
            continue
        scanned.append(relative)
        text = path.read_text(encoding="utf-8")
        for hit in (scan_step_literals(relative, text)
                    + scan_failure_names(relative, text, names)
                    + scan_criteria_literals(relative, text)):
            kind = permitted_class(relative)
            if kind:
                permitted_counts[kind] += 1
            hits.append((hit[0], hit[1], hit[2], kind or "unpermitted"))
    return {"scanned": scanned, "hits": hits, "permitted": permitted_counts}


def assert_containment(scan: dict) -> list[str]:
    problems: list[str] = []
    if not scan["scanned"]:
        problems.append("the scan read zero SKILL.md files — a scan that read nothing "
                        "proves nothing")
    for path, number, literal, kind in scan["hits"]:
        if kind == "unpermitted":
            problems.append("%s:%d copies %r outside the permitted classes"
                            % (path, number, literal))
    return problems


def test_sc007_containment_scan_reports_every_hit_and_the_file_count(capsys):
    names = failure_names_from_owner(_read(REPO_ROOT / DATAMODEL_REL))
    scan = scan_tree(REPO_ROOT, names)
    for kind, count in scan["permitted"].items():
        print("permitted[%s]=%d" % (kind, count))
    for literal in FAILURE_NAMES:
        count = sum(1 for hit in scan["hits"] if hit[2] == literal)
        print("class-name[%s]=%d" % (literal, count))
    for path, number, literal, kind in scan["hits"]:
        print("hit %s:%d literal=%r class=%s" % (path, number, literal, kind))
    print("scanned=%d skills/**/SKILL.md" % len(scan["scanned"]))
    problems = assert_containment(scan)
    assert not problems, "SC-007 containment violations:\n- " + "\n- ".join(problems)


def test_sc007_scan_negative_case_a_copied_step_literal_turns_red(tmp_path):
    names = failure_names_from_owner(_read(REPO_ROOT / DATAMODEL_REL))
    source = REPO_ROOT / CONSUMERS[-1]
    target = tmp_path / CONSUMERS[-1]
    target.parent.mkdir(parents=True)
    target.write_text(_read(source) + "\nStep NP-3 strips the label.\n", encoding="utf-8")
    scan = scan_tree(tmp_path, names)
    problems = assert_containment(scan)
    assert any("NP-3" in p for p in problems), (
        "the negative case did not turn the containment scan red: %r" % problems)


def test_sc007_scan_negative_case_a_copied_class_criterion_turns_red(tmp_path):
    """The second vocabulary: a re-spoken criterion, not a borrowed class name."""
    names = failure_names_from_owner(_read(REPO_ROOT / DATAMODEL_REL))
    target = tmp_path / CONSUMERS[0]
    target.parent.mkdir(parents=True)
    target.write_text("---\nname: probe\n---\n\nIf the path lies outside, report "
                      "路径落在已知位置之外 and stop.\n", encoding="utf-8")
    scan = scan_tree(tmp_path, names)
    problems = assert_containment(scan)
    assert any("路径落在已知位置之外" in p for p in problems), (
        "the negative case did not turn the criteria scan red: %r" % problems)


def test_sc007_scan_negative_case_a_failure_name_copy_turns_red(tmp_path):
    """The shape a copied table takes: a row whose first cell is the class name."""
    names = failure_names_from_owner(_read(REPO_ROOT / DATAMODEL_REL))
    target = tmp_path / CONSUMERS[0]
    target.parent.mkdir(parents=True)
    target.write_text("---\nname: probe\n---\n\n| class | condition |\n|---|---|\n"
                      "| `dual-layer` | two hits in different layers |\n",
                      encoding="utf-8")
    scan = scan_tree(tmp_path, names)
    problems = assert_containment(scan)
    assert any("dual-layer" in p for p in problems), (
        "the negative case did not turn the failure-name scan red: %r" % problems)


def test_sc007_permitted_classes_are_named_constants_counted_separately():
    names = failure_names_from_owner(_read(REPO_ROOT / DATAMODEL_REL))
    assert permitted_class("shared/definitions/skill-reference-definitions.md") == "owner"
    assert permitted_class(".specify/shared/definitions/skill-reference-definitions.md") \
        == "owner-mirror"
    assert permitted_class("tests/fixtures/skill-reference/normalization-matrix.json") \
        == "fixture"
    assert permitted_class("skills/external/run-skills/SKILL.md") is None
    scan = scan_tree(REPO_ROOT, names)
    assert set(scan["permitted"]) == set(PERMITTED_CLASSES), (
        "the scan counts %r, not the three permitted classes" % sorted(scan["permitted"]))
    assert sum(scan["permitted"].values()) == sum(
        1 for hit in scan["hits"] if hit[3] != "unpermitted")
