"""Contract tests for Feature 082 US5 — SC-009 failure semantics (T029).

One assertion per failure class, each also asserting the paired report carries both
the **raw** and the **normalized** identifier (FR-025), plus the mutual-exclusion
assertions of § Failure semantics:

* an out-of-ladder input is **never** reported as ``zero-hit``;
* an unreadable directory is **never** reported as ``out-of-ladder``.

The ``dual-layer`` case is built from two genuinely different **layers** in
``tmp_path`` — never from a source-and-mirror pair, which is one hit (GR-05(c) /
V-33). :func:`check_failures` is the assertion function the GM-07 negative case
re-runs on a relabelled copy.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER_REL = Path("tests/contract/skill_reference_matrix.py")

#: § Failure semantics — the four classes, closed.
FAILURE_CLASSES = ("zero-hit", "out-of-ladder", "unreadable", "dual-layer")

#: The two exclusion pairs SC-009 names as "never report one as the other".
EXCLUSIONS = (("out-of-ladder", "zero-hit"), ("unreadable", "out-of-ladder"))


def _helper(path=None):
    """Load the test-only implementation, from the live tree or a ``tmp_path`` copy."""
    path = REPO_ROOT / HELPER_REL if path is None else Path(path)
    assert path.is_file(), "artifact missing: %s" % path
    spec = importlib.util.spec_from_file_location("skill_reference_matrix", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _scratch_two_layers(root: Path, name: str = "twin-skill") -> Path:
    """Two **different** layers carrying the same name (dev-canonical + installed)."""
    for layer_dir in ("skills/external", ".specify/skills"):
        target = root / layer_dir / name
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text(
            "---\nname: %s\ndescription: layered fixture\n---\n\nbody\n" % name,
            encoding="utf-8")
    return root


def _scratch_unreadable(root: Path, name: str = "hollow-skill") -> Path:
    target = root / "skills/external" / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text("no frontmatter here\n", encoding="utf-8")
    return root


def cases() -> list[dict]:
    """One input per failure class, each with its expected class and report items."""
    return [
        {"case": "zero-hit", "raw": "no-such-skill-xyz", "class": "zero-hit",
         "items": ("raw", "normalized", "searched_coordinates"), "where": "live"},
        {"case": "out-of-ladder", "raw": "../../etc/passwd", "class": "out-of-ladder",
         "items": ("raw", "normalized", "path", "known_locations"), "where": "live"},
        {"case": "unreadable", "raw": "skills/external/hollow-skill", "class": "unreadable",
         "items": ("raw", "normalized", "path", "defect"), "where": "unreadable"},
        {"case": "dual-layer", "raw": "twin-skill", "class": "dual-layer",
         "items": ("raw", "normalized", "candidate_paths"), "where": "two-layers"},
    ]


def _run(case: dict, tmp_root: Path, helper_path=None) -> dict:
    module = _helper(helper_path)
    if case["where"] == "unreadable":
        root = _scratch_unreadable(tmp_root / case["case"])
        return module.normalize(case["raw"], repo_root=root)
    if case["where"] == "two-layers":
        root = _scratch_two_layers(tmp_root / case["case"])
        return module.normalize(case["raw"], repo_root=root)
    return module.normalize(case["raw"], repo_root=REPO_ROOT)


def check_failures(cases_, tmp_root: Path, helper_path=None) -> tuple[list[str], dict]:
    """Assert every case's class, its paired report, and the mutual exclusions."""
    problems: list[str] = []
    reports: dict = {}
    for case in cases_:
        result = _run(case, tmp_root, helper_path)
        reports[case["case"]] = result
        if result.get("outcome") != "failure":
            problems.append("%s: reported %r, not the failure class %r"
                            % (case["case"], result.get("outcome"), case["class"]))
            continue
        if result.get("failure_class") != case["class"]:
            problems.append("%s: reported class %r, expected %r"
                            % (case["case"], result.get("failure_class"), case["class"]))
        report = result.get("report_items") or {}
        for item in case["items"]:
            if item not in report:
                problems.append("%s: the report omits the required item %r"
                                % (case["case"], item))
        # FR-025 — every class reports both halves of the pair.
        if report.get("raw") != case["raw"]:
            problems.append("%s: the report's raw half is %r, not the input %r"
                            % (case["case"], report.get("raw"), case["raw"]))
        if report.get("normalized") != result.get("normalized"):
            problems.append("%s: the report's normalized half is missing or differs from "
                            "the decision's normalized identifier" % case["case"])
        if result.get("decision_class") != "failure":
            problems.append("%s: the decision class is %r, not 'failure'"
                            % (case["case"], result.get("decision_class")))
    expected_class = {case["case"]: case["class"] for case in cases_}
    for expected, forbidden in EXCLUSIONS:
        result = reports.get(expected)
        if result is None:
            continue
        if result.get("outcome") != "failure":
            continue
        # The exclusion is about the *input's own* class: the case built to close as
        # `expected` must never close as `forbidden`, whatever the row now demands.
        actual = result.get("failure_class")
        if expected_class.get(expected) == expected and actual == forbidden:
            problems.append("%s was reported as %r — the classes are mutually exclusive"
                            % (expected, forbidden))
    twin = reports.get("dual-layer") or {}
    paths = (twin.get("report_items") or {}).get("candidate_paths") or []
    if twin and len(paths) < 2:
        problems.append("dual-layer reports %d candidate path(s); two different layers "
                        "must yield two" % len(paths))
    return problems, reports


def test_sc009_one_assertion_per_failure_class(capsys, tmp_path):
    problems, reports = check_failures(cases(), tmp_path)
    for name, result in reports.items():
        print("%s -> %s report=%r" % (name, result.get("failure_class"),
                                      result.get("report_items")))
    assert not problems, "SC-009 violations:\n- " + "\n- ".join(problems)


def test_sc009_mutual_exclusion_out_of_ladder_is_not_zero_hit(tmp_path):
    problems, reports = check_failures(cases(), tmp_path)
    # Both halves are load-bearing: the input must *be* judged (a missing class is a
    # different defect), and it must not land on the other class of its pair.
    assert reports["out-of-ladder"].get("failure_class") == "out-of-ladder", (
        "the exclusion pair was not exercised: the input closed as %r"
        % reports["out-of-ladder"].get("failure_class"))
    assert not any("out-of-ladder was reported as 'zero-hit'" in p for p in problems), (
        "an out-of-ladder input was reported as zero-hit")


def test_sc009_mutual_exclusion_unreadable_is_not_out_of_ladder(tmp_path):
    problems, reports = check_failures(cases(), tmp_path)
    assert reports["unreadable"].get("failure_class") == "unreadable", (
        "the exclusion pair was not exercised: the input closed as %r"
        % reports["unreadable"].get("failure_class"))
    assert not any("unreadable was reported as 'out-of-ladder'" in p for p in problems), (
        "an unreadable directory was reported as out-of-ladder")


def test_sc009_dual_layer_case_uses_two_distinct_layers(tmp_path):
    root = _scratch_two_layers(tmp_path / "layers")
    module = _helper()
    result = module.normalize("twin-skill", repo_root=root)
    paths = (result.get("report_items") or {}).get("candidate_paths") or []
    layers = {module.layer_of(path) for path in paths}
    assert result.get("failure_class") == "dual-layer", (
        "the fixture did not close as dual-layer: %r" % result.get("failure_class"))
    assert layers == {"dev-canonical", "installed"}, (
        "the dual-layer fixture spans %r, not two distinct layers" % layers)


def test_sc009_negative_case_relabelling_a_class_turns_red(tmp_path):
    """Relabel the out-of-ladder branch in a ``tmp_path`` copy of the implementation.

    The copy is broken at the string level (GM-07): the ladder's ``out-of-ladder``
    return is relabelled ``zero-hit``. The same assertion function must then report
    the exclusion — the class pair closes on one side, so the assertion goes red.
    """
    source = (REPO_ROOT / HELPER_REL).read_text(encoding="utf-8")
    ladder_line = ('return failure(raw, text, "out-of-ladder", path=text, '
                   'known_locations=found)')
    assert ladder_line in source, (
        "artifact missing: the out-of-ladder return is not in the implementation")
    broken_source = source.replace(
        ladder_line,
        'return failure(raw, text, "zero-hit", searched_coordinates=found)', 1)
    assert broken_source != source, "the relabelling changed nothing"
    broken = tmp_path / "skill_reference_matrix.py"
    broken.write_text(broken_source, encoding="utf-8")
    problems, reports = check_failures(cases(), tmp_path / "run", helper_path=broken)
    assert reports["out-of-ladder"].get("failure_class") == "zero-hit", (
        "the relabelled copy still closed as %r — the negative case did not relabel "
        "the class it claims to"
        % reports["out-of-ladder"].get("failure_class"))
    assert any("out-of-ladder was reported as 'zero-hit'" in p for p in problems), (
        "relabelling one failure class did not turn the exclusion assertion red: %r"
        % problems)


# --- The owner document carries the exclusion, in the direction a machine can see -----
#
# `check_failures` runs the test-only implementation against the matrix's expectations;
# it cannot see whether the *owner document* states the exclusion. GR-06 makes the
# document the rule and the executable its projection, so the rule is read here too: the
# owner's mutual-exclusivity sentence is matched against the closed pair set above rather
# than retyped, and the negative case re-labels a copy of the owner and re-runs *this*
# assertion.

OWNER_REL = Path("shared/definitions/skill-reference-definitions.md")

#: How an owner sentence names a class inside a CJK sentence.
_OWNER_SPELLINGS = {
    "zero-hit": ("`zero-hit`",),
    "out-of-ladder": ("越界", "out-of-ladder"),
    "unreadable": ("不可读", "unreadable"),
    "dual-layer": ("`dual-layer`",),
}


def _owner_text(repo_root: Path) -> tuple[Path, str]:
    path = repo_root / OWNER_REL
    assert path.is_file(), "artifact missing: %s" % path
    return path, path.read_text(encoding="utf-8")


def assert_owner_states_exclusions(text: str) -> list[str]:
    """GR-06 — the owner states every pair of :data:`EXCLUSIONS` as mutually exclusive.

    The unit is the sentence carrying whole literals — ``out-of-ladder`` names a class,
    ``an out-of-ladder input`` is an instance of one. Matching the bare literals instead
    would let "an unreadable directory MUST NOT be reported as …" satisfy a requirement
    about **out-of-ladder**, i.e. a green with nothing under it.
    """
    problems: list[str] = []
    flat = re.sub(r"\s+", " ", text)
    stated = "mutually exclusive" in flat
    if not stated:
        problems.append("the owner never says the four classes are mutually exclusive")
        return problems
    for left, right in EXCLUSIONS:
        # The span is split **at the conjunction**: "A must not be reported as B, and C
        # must not be reported as D" is two statements, and reading it whole lets the
        # second half satisfy a requirement about the first half's pair. The clause's own
        # subject is the text after its last ``;``/``:`` — checked, not assumed.
        half_left, half_right = _OWNER_HALVES[left], _OWNER_HALVES[right]
        ok = any(
            _states_exclusion(clause, half_left, left, right)
            for sentence in re.split(r"(?<=[.。])\s*", flat)
            for clause in re.split(r",\s*(?:and\s+)?|\s+and\s+", sentence))
        if not ok:
            problems.append("%s / %s: the owner states no exclusion naming both"
                            % (left, right))
    return problems


#: Which half of an exclusion clause names which side (GR-06's own sentence shape:
#: "<subject> MUST NOT be reported as `<other>`").
_OWNER_HALVES = {
    "out-of-ladder": "subject",
    "zero-hit": "object",
    "unreadable": "subject",
    "dual-layer": "object",
}


def _states_exclusion(clause: str, half: str, left: str, right: str) -> bool:
    """Does ``clause`` say ``left`` is never reported as ``right``, in that direction?

    ``half`` is the side the clause's *subject* names. When the subject names
    ``right``, the forbidden object must be ``left`` — the pair is stated in the other
    direction, which is still the same exclusion; when it names ``left``, the forbidden
    object must be ``right``.
    """
    if "MUST NOT be reported as" not in clause:
        return False
    subject, _, obj = clause.partition("MUST NOT be reported as")
    phrase = _subject_phrase(subject)
    said = lambda name: any(s in phrase for s in _OWNER_SPELLINGS[name])  # noqa: E731
    forbidden = lambda name: any(s in obj for s in _OWNER_SPELLINGS[name])  # noqa: E731
    if half == "subject":
        return said(left) and not said(right) and forbidden(right)
    return said(right) and forbidden(left)


def _subject_phrase(subject: str) -> str:
    """The subject of a clause, from its last clause boundary to the verb.

    A table row's pipe, a colon/semicolon and a full stop all end the previous
    statement; the subject is what follows the last of them. The scan is over the
    subject **span** itself, not over the clause, so the verb's own colon-free tail
    cannot shorten the phrase.
    """
    end = 0
    for match in re.finditer(r"[;；:.|]", subject):
        end = match.end()
    return subject[end:]


def test_gr06_owner_states_each_exclusion_pair():
    _, text = _owner_text(REPO_ROOT)
    problems = assert_owner_states_exclusions(text)
    assert not problems, "GR-06 owner violations:\n- " + "\n- ".join(problems)


def test_gr06_negative_case_relabelled_owner_sentence_turns_red(tmp_path):
    """Relabel one class in a `tmp_path` copy of the owner; the rule must go red."""
    _, text = _owner_text(REPO_ROOT)
    before = assert_owner_states_exclusions(text)
    assert not before, "the negative case needs a green owner: %r" % before
    relabelled_text = re.sub(
        r"an out-of-ladder input MUST NOT be reported as\s+`zero-hit`",
        "an unreadable directory MUST NOT be reported as `dual-layer`",
        text)
    assert relabelled_text != text, "the negative case's subject sentence is not in the owner"
    copy = tmp_path / OWNER_REL
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_text(relabelled_text, encoding="utf-8")
    _, relabelled = _owner_text(tmp_path)
    problems = assert_owner_states_exclusions(relabelled)
    assert any("out-of-ladder / zero-hit" in p for p in problems), (
        "relabelling the owner's sentence did not turn the exclusion assertion red: %r"
        % problems)
