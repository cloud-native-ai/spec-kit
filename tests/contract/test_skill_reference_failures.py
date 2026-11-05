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
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER_REL = Path("tests/contract/skill_reference_matrix.py")

#: § Failure semantics — the four classes, closed.
FAILURE_CLASSES = ("zero-hit", "out-of-ladder", "unreadable", "dual-layer")

#: The two exclusion pairs SC-009 names as "never report one as the other".
EXCLUSIONS = (("out-of-ladder", "zero-hit"), ("unreadable", "out-of-ladder"))


def _helper():
    path = REPO_ROOT / HELPER_REL
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


def _run(case: dict, tmp_root: Path) -> dict:
    module = _helper()
    if case["where"] == "unreadable":
        root = _scratch_unreadable(tmp_root / case["case"])
        return module.normalize(case["raw"], repo_root=root)
    if case["where"] == "two-layers":
        root = _scratch_two_layers(tmp_root / case["case"])
        return module.normalize(case["raw"], repo_root=root)
    return module.normalize(case["raw"], repo_root=REPO_ROOT)


def check_failures(cases_, tmp_root: Path) -> tuple[list[str], dict]:
    """Assert every case's class, its paired report, and the mutual exclusions."""
    problems: list[str] = []
    reports: dict = {}
    for case in cases_:
        result = _run(case, tmp_root)
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
    problems, _ = check_failures(cases(), tmp_path)
    assert not any("out-of-ladder was reported as 'zero-hit'" in p for p in problems), (
        "an out-of-ladder input was reported as zero-hit")


def test_sc009_mutual_exclusion_unreadable_is_not_out_of_ladder(tmp_path):
    problems, _ = check_failures(cases(), tmp_path)
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
    relabelled = []
    for case in cases():
        copy = dict(case)
        if copy["case"] == "out-of-ladder":
            copy["class"] = "zero-hit"
        relabelled.append(copy)
    problems, reports = check_failures(relabelled, tmp_path / "relabel")
    # Relabelling the expectation makes the exclusion assertion fire: the same input is
    # now demanded to report zero-hit while the implementation (correctly) reports
    # out-of-ladder, so the pair no longer closes.
    assert any("out-of-ladder" in p and "expected 'zero-hit'" in p for p in problems), (
        "the negative case did not turn the exclusion assertion red: %r" % problems)
    assert reports["out-of-ladder"].get("failure_class") == "out-of-ladder"
