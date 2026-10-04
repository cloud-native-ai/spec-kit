"""Contract test: the `[subjects: <glob>]` criterion-subject reference form (US5).

Subjects: ``shared/definitions/goal-definitions.md`` (the concept owner, which gains one
section) and ``scripts/python/goal-utils.py`` (which derives the member set at parse time).
A third file is named by C-14 — ``skills/create-team/scripts/build-summary-input.py`` keeps
its own local criteria reader, and this suite pins the disposition the owner doc records for
it rather than letting the two derivations drift apart silently.

The defect this closes is visible in this repository's own history: the one real
enumeration-style criterion was rewritten from "六个绘图技能" to "七个绘图技能" and back as
the member set changed (``.specify/goal/draw-two-layer-structure/goal.md`` History), because a
member list retyped into prose has to be edited every time the directory changes. A derived
set cannot go stale — but only if the derivation is honest about what it cannot see, which is
what C-10's documented limitation and C-5/C-6's two distinguishable failure states are for.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
GOAL_UTILS = ROOT / "scripts" / "python" / "goal-utils.py"
OWNER_DOC = ROOT / "shared" / "definitions" / "goal-definitions.md"
OWNER_DOC_MIRROR = ROOT / ".specify" / "shared" / "definitions" / "goal-definitions.md"
SUMMARY_SCRIPT = ROOT / "skills" / "create-team" / "scripts" / "build-summary-input.py"
CONTRACT = (
    ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts" / "contracts"
    / "criterion-subject.md"
)
REAL_GOAL = ROOT / ".specify" / "goal" / "draw-two-layer-structure" / "goal.md"

# --- C-17: the reference form and its two failure tiers, as a constant table ---

SUBJECT_REF = r"\[subjects:\s*([^\]]+)\]"
BRACE_ENUM = r"\{[^}]*,[^}]*\}"
PROBLEM_PREFIXES = {
    "missing": "SUBJECT MISSING:",
    "empty": "SUBJECT EMPTY:",
    "conflict": "SUBJECT CONFLICT:",
}
DERIVE_STATES = {"absent", "ok", "missing", "empty", "conflict"}

# The eight H2 sections the owner doc had before US5 (measured 2026-10-02: 137 lines,
# 9 headings). C-4 requires the new section be an ADDITION, so every one of these must
# survive with its heading intact.
PREEXISTING_SECTIONS = (
    "## What a Goal Is",
    "## Goal vs Requirement",
    "## Criteria Authority Boundary",
    "## Singularity Rule",
    "## Target Decomposition (目标切片)",
    "## Storage & Goal Archive",
    "## Goal–Team Binding",
    "## Terminology Boundaries",
)


def _load(path=GOAL_UTILS, name=None):
    path = Path(path)
    assert path.is_file(), f"missing artifact: {path}"
    spec = importlib.util.spec_from_file_location(
        name or ("_mod_" + re.sub(r"\W", "_", path.stem)), path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _goal_utils():
    return _load(GOAL_UTILS, "_goal_utils_us5")


def _run(*args, expect=None, cwd=ROOT):
    r = subprocess.run([sys.executable, str(GOAL_UTILS), *args],
                       capture_output=True, text=True, cwd=str(cwd))
    if expect is not None:
        assert r.returncode == expect, (
            f"goal-utils.py {' '.join(args)} -> {r.returncode}, expected {expect}\n"
            f"{r.stdout}\n{r.stderr}"
        )
    return r


GOAL_TMPL = """---
status: active
created: 2026-01-01
updated: 2026-01-02
---

# Goal: {slug}

## Objective

One outcome the team wants to exist and can be judged against.

## Success Criteria

{criteria}

## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | a slice | open |

## History

- 2026-01-01 — created.
"""


def _repo(tmp_path: Path, criteria: str, *, dirs=("skills/draw-a", "skills/draw-b"),
          slug: str = "g1") -> Path:
    """A throwaway repo with a goal whose criteria block is `criteria`."""
    root = tmp_path / "repo"
    (root / ".specify" / "goal" / slug).mkdir(parents=True, exist_ok=True)
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
        (root / d / "SKILL.md").write_text("# skill\n", encoding="utf-8")
    body = "\n".join(f"{i}. {c}" for i, c in enumerate(criteria.splitlines(), 1) if c.strip())
    (root / ".specify" / "goal" / slug / "goal.md").write_text(
        GOAL_TMPL.format(slug=slug, criteria=body), encoding="utf-8"
    )
    return root


# =========================================================================== #
# C-1 … C-4 — the owner document gains one section and loses nothing
# =========================================================================== #


def test_c1_owner_doc_gains_a_criterion_subject_section():
    text = OWNER_DOC.read_text(encoding="utf-8")
    headings = [l for l in text.splitlines() if re.match(r"^#{2,3}\s", l)]
    hits = [h for h in headings if "判据主体" in h or "Criterion Subject" in h]
    assert hits, (
        f"the owner doc must declare the reference form in its own section; headings are "
        f"{headings}"
    )
    assert len(hits) == 1, f"exactly one such section, got {hits}"
    assert re.match(r"^#{2,3}\s", hits[0]), "the section must be an H2 or H3"


def test_c2_the_literal_is_defined_once_and_reached_by_one_regex():
    text = OWNER_DOC.read_text(encoding="utf-8")
    assert text.count("[subjects: <glob>]") == 1, (
        f"the literal form is the owner's to define exactly once; found "
        f"{text.count('[subjects: <glob>]')} definitions, and a second one is a second "
        "source free to drift"
    )
    src = GOAL_UTILS.read_text(encoding="utf-8")
    compiled = [l.strip() for l in src.splitlines()
                if "re.compile" in l and "subjects:" in l]
    assert len(compiled) == 1, (
        f"exactly one parser regex may reference the form, got {compiled}"
    )
    assert re.search(SUBJECT_REF, "[subjects: skills/draw-*]"), (
        "sentinel: the pinned regex shape does not match the literal it is supposed to parse"
    )
    assert _goal_utils().SUBJECT_REF.pattern == SUBJECT_REF, (
        "the single regex must be the one whose shape is pinned here"
    )


def test_c3_the_section_is_an_addition_and_no_existing_form_was_rewritten():
    """C-3's premise: before US5 the owner doc carried no glob/directory-reference form at
    all (measured 2026-10-02: the probe returns nothing). So every hit the probe makes now
    must sit inside the new section — a hit anywhere else means an existing section was
    rewritten rather than left alone."""
    lines = OWNER_DOC.read_text(encoding="utf-8").splitlines()
    for heading in PREEXISTING_SECTIONS:
        assert heading in lines, f"an existing section was removed or renamed: {heading}"

    start = next(i for i, l in enumerate(lines)
                 if re.match(r"^#{2,3}\s", l) and ("判据主体" in l or "Criterion Subject" in l))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s", lines[i])),
               len(lines))
    probe = re.compile(r"glob|\*/|directory-reference|<dir>|rglob|iterdir")
    outside = [(i + 1, l.strip()[:90]) for i, l in enumerate(lines)
               if not (start <= i < end) and probe.search(l)]
    assert outside == [], (
        f"glob/directory machinery appears outside the new section, so an existing section "
        f"was rewritten: {outside}"
    )
    inside = [l for l in lines[start:end] if probe.search(l)]
    assert inside, (
        f"sentinel: the new section itself carries no glob form, so this test measured "
        f"nothing (section is lines {start + 1}..{end})"
    )


def test_c4_the_owner_doc_is_still_linked_not_parsed_and_its_pins_still_hold():
    """C-4: the file is a concept authority, so US5 adds to it and changes no semantics.

    The observable proxies are the two pins that already read it: goal-utils' docstring
    reference, and test_goal_targets_engine's AUTHORITY constant.
    """
    assert "goal-definitions.md" in GOAL_UTILS.read_text(encoding="utf-8"), (
        "the engine's docstring must still name the concept authority"
    )
    engine_suite = (ROOT / "tests" / "contract" / "test_goal_targets_engine.py").read_text(
        encoding="utf-8")
    assert 'AUTHORITY = ".specify/shared/definitions/goal-definitions.md"' in engine_suite
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q",
         "tests/contract/test_goal_targets_engine.py::test_command_links_to_the_concept_authority"],
        capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0, f"C-18's pin went red:\n{r.stdout[-800:]}"


# =========================================================================== #
# C-5 … C-7 — derivation and its two distinguishable failures
# =========================================================================== #


def test_c5_and_c6_the_two_failure_states_are_distinguishable(tmp_path):
    mod = _goal_utils()

    missing = _repo(tmp_path / "m", "Every skill under [subjects: nope/*] renders a diagram.")
    empty_dir = _repo(tmp_path / "e", "Every skill under [subjects: skills/zzz-*] renders.",
                      dirs=("skills/draw-a",))
    good = _repo(tmp_path / "g", "Every skill under [subjects: skills/draw-*] renders.")

    d_missing = mod.derive_subjects(
        "Every skill under [subjects: nope/*] renders a diagram.", missing)
    d_empty = mod.derive_subjects(
        "Every skill under [subjects: skills/zzz-*] renders.", empty_dir)
    d_good = mod.derive_subjects("Every skill under [subjects: skills/draw-*] renders.", good)

    assert d_missing["state"] == "missing", d_missing
    assert d_empty["state"] == "empty", d_empty
    assert d_good["state"] == "ok" and d_good["paths"], d_good
    assert d_missing["state"] != d_empty["state"], (
        "a glob whose literal prefix does not exist and a glob that exists but matches "
        "nothing are different facts with different remedies; collapsing them means the "
        "author cannot tell a typo from an emptied directory"
    )

    # C-7's anti-vacuity half, both directions: the parser really ran and produced a set
    assert d_good["glob"] == "skills/draw-*"
    assert sorted(d_good["paths"]) == ["skills/draw-a", "skills/draw-b"]
    assert d_empty["paths"] == [], (
        "sentinel: the empty tier must be reached WITH an empty derived set, not by the "
        "derivation failing to run"
    )
    assert d_missing["glob"] == "nope/*", "sentinel: the glob was not even read"

    # and through the CLI, where the prefixes and the non-zero exit are observable
    for root, prefix in ((empty_dir, PROBLEM_PREFIXES["empty"]),
                         (missing, PROBLEM_PREFIXES["missing"])):
        r = _run("validate", "g1", "--repo-root", str(root), "--json")
        assert r.returncode != 0, f"{prefix} must not validate clean: {r.stdout}"
        payload = json.loads(r.stdout)
        assert any(p.startswith(prefix) for p in payload["problems"]), (
            f"the reported problem must start with {prefix!r}: {payload['problems']}"
        )


def test_c6_empty_subjects_is_reported_with_the_str010_prefix(tmp_path):
    root = _repo(tmp_path, "Every skill under [subjects: skills/none-*] renders.",
                 dirs=("skills/draw-a",))
    r = _run("validate", "g1", "--repo-root", str(root))
    assert r.returncode != 0
    line = next((l for l in r.stdout.splitlines() if "SUBJECT EMPTY:" in l), None)
    assert line, f"STR-010's prefix must reach the human output too:\n{r.stdout}"
    assert re.search(r"SUBJECT EMPTY:\s*\S", line), (
        f"the prefix must be followed by something a reader can act on: {line!r}"
    )
    assert "skills/none-*" in line, f"the message must name the glob: {line!r}"


def test_c7_both_tiers_have_counter_samples_and_a_positive_control(tmp_path):
    """A guard that cannot go red proves nothing, so the working case is asserted too."""
    mod = _goal_utils()
    root = _repo(tmp_path, "\n".join([
        "Every skill under [subjects: skills/draw-*] renders a diagram.",
        "Nothing under [subjects: absent/*] renders.",
        "Nothing under [subjects: skills/zzz-*] renders either.",
    ]))
    data = mod.parse_goal(root / ".specify" / "goal" / "g1" / "goal.md")
    states = [s["state"] for s in data["subjects"]]
    assert states == ["ok", "missing", "empty"], (
        f"one parse must derive all three states side by side: {states}"
    )
    ok, problems = mod.validate_goal(root / ".specify" / "goal" / "g1" / "goal.md", root)
    assert not ok
    joined = "\n".join(problems)
    assert PROBLEM_PREFIXES["missing"] in joined and PROBLEM_PREFIXES["empty"] in joined
    assert PROBLEM_PREFIXES["missing"] != PROBLEM_PREFIXES["empty"]


# =========================================================================== #
# C-8 … C-10 — the conflict rule and its honest boundary
# =========================================================================== #


def test_c8_reference_plus_brace_enumeration_is_a_conflict(tmp_path):
    root = _repo(tmp_path,
                 "Seven skills ([subjects: skills/draw-*] and draw-{a,b}) render diagrams.")
    r = _run("validate", "g1", "--repo-root", str(root), "--json")
    assert r.returncode != 0
    problems = json.loads(r.stdout)["problems"]
    assert any(p.startswith(PROBLEM_PREFIXES["conflict"]) for p in problems), (
        f"one criterion must not carry both a derived set and a retyped member list — "
        f"silently picking one is how the two come to disagree: {problems}"
    )


def test_c9_the_real_enumeration_criterion_is_the_evidence_for_that_rule():
    text = REAL_GOAL.read_text(encoding="utf-8")
    assert REAL_GOAL.is_file(), "sentinel: the only real goal definition moved"
    braces = re.findall(r"\{[^}]*,[^}]*\}", text)
    assert braces, (
        "the conflict rule was derived from a measured enumeration form; if the real corpus "
        "no longer contains one, the rule's evidence needs re-measuring"
    )
    history = text.split("## History")[1]
    assert re.search(r"六个绘图技能|七个绘图技能", history), (
        "the History section is the cautionary exhibit: the same criterion was rewritten as "
        "its member set changed, which is the churn a derived set removes"
    )


def test_c10_the_undetectable_case_is_documented_and_not_claimed(tmp_path):
    """C-10: a prose enumeration carries no machine-decidable marker, and saying otherwise
    would be exactly the over-claim the artifact/behavior clause split forbids."""
    for path in (OWNER_DOC, CONTRACT):
        text = path.read_text(encoding="utf-8")
        assert re.search(r"检不出|not detectable|undecidable|不可机械判定", text), (
            f"{path.name} must state the boundary: a brace-free prose enumeration beside a "
            "reference form cannot be detected mechanically"
        )
    mod = _goal_utils()
    root = _repo(tmp_path, "所有绘图技能 [subjects: skills/draw-*] 都能出图。")
    derived = mod.derive_subjects("所有绘图技能 [subjects: skills/draw-*] 都能出图。", root)
    assert derived["state"] == "ok", (
        f"a prose enumeration beside the reference is NOT a conflict and must not be "
        f"reported as one — claiming otherwise would be claiming coverage we do not have: "
        f"{derived}"
    )


# =========================================================================== #
# C-11 … C-13 — backward compatibility and the SC-009 demonstration
# =========================================================================== #


def _parse_names(root: Path, mod):
    """The name-level parse fingerprint of every goal definition under `root`."""
    out = []
    for path in sorted((root / ".specify" / "goal").glob("*/goal.md")):
        try:
            data = mod.parse_goal(path)
        except Exception as exc:                      # a parse failure is a name too
            out.append(f"{path.parent.name}: ERROR {type(exc).__name__}")
            continue
        out.append(f"{path.parent.name}: status={data['status']} "
                   f"criteria={len(data['criteria'])} targets={len(data['targets'])} "
                   f"objective={hashlib.md5(data['objective'].encode()).hexdigest()[:8]}")
    return sorted(out)


def test_c11_and_c12_existing_definitions_parse_identically_with_a_nonzero_companion():
    """SC-010's name-level comparison, plus the companion that keeps it from being vacuous.

    There is exactly ONE real goal definition, so "the failure set is empty" is nearly
    vacuous on its own — C-12 requires the scan to prove it scanned something.
    """
    mod = _goal_utils()
    names = _parse_names(ROOT, mod)
    assert len(names) >= 1, (
        f"sentinel: no goal definition was scanned, so an empty delta proves nothing: {names}"
    )
    assert not [n for n in names if "ERROR" in n], f"a real definition failed to parse: {names}"
    # the pre-change shape, restated as an invariant: a pure-enumeration criterion derives
    # no subject set at all, so nothing about its parse can have moved
    data = mod.parse_goal(REAL_GOAL)
    assert data["subjects"] == [], (
        f"the real goal's criteria are pure enumeration and must derive nothing: "
        f"{data['subjects']}"
    )
    assert data["criteria"], "sentinel: the real goal has no criteria to compare"
    ok, problems = mod.validate_goal(REAL_GOAL, ROOT)
    assert ok, f"US5 must not invalidate an existing definition: {problems}"


def test_c13_the_reference_form_moves_and_the_enumeration_does_not(tmp_path):
    """SC-009, both ways, in a throwaway copy of a skills tree."""
    mod = _goal_utils()
    reference = "Every skill under [subjects: skills/draw-*] renders a diagram."
    enumeration = "Seven skills (draw-diagram and draw-{a,b,c,d,e,f}) render diagrams."

    root = _repo(tmp_path, f"{reference}\n{enumeration}",
                 dirs=("skills/draw-a", "skills/draw-b", "skills/draw-c"))
    before = [s["paths"] for s in mod.parse_goal(
        root / ".specify" / "goal" / "g1" / "goal.md")["subjects"]]
    criteria_before = mod.parse_goal(root / ".specify" / "goal" / "g1" / "goal.md")["criteria"]

    # remove one member, then add one back — in the copy only
    (root / "skills" / "draw-c" / "SKILL.md").unlink()
    (root / "skills" / "draw-c").rmdir()
    after_remove = [s["paths"] for s in mod.parse_goal(
        root / ".specify" / "goal" / "g1" / "goal.md")["subjects"]]

    (root / "skills" / "draw-d").mkdir()
    (root / "skills" / "draw-d" / "SKILL.md").write_text("# skill\n", encoding="utf-8")
    after_add = [s["paths"] for s in mod.parse_goal(
        root / ".specify" / "goal" / "g1" / "goal.md")["subjects"]]

    assert sorted(before[0]) == ["skills/draw-a", "skills/draw-b", "skills/draw-c"]
    assert sorted(after_remove[0]) == ["skills/draw-a", "skills/draw-b"], (
        f"the derived set must follow the directory: {after_remove[0]}"
    )
    assert sorted(after_add[0]) == ["skills/draw-a", "skills/draw-b", "skills/draw-d"]

    criteria_after = mod.parse_goal(root / ".specify" / "goal" / "g1" / "goal.md")["criteria"]
    enum_before = next(c for c in criteria_before if "Seven skills" in c)
    enum_after = next(c for c in criteria_after if "Seven skills" in c)
    assert enum_before == enum_after, (
        "the enumeration form must NOT move — that immobility beside a moving derived set "
        "is the whole demonstration"
    )
    assert REAL_GOAL.is_file() and "draw-c" not in str(ROOT / "skills"), (
        "sentinel: the demonstration must run in the copy, never the real skills tree"
    )


# =========================================================================== #
# C-14 … C-16 — the second parser and the fifth exit-code convention
# =========================================================================== #


def test_c14_the_second_parser_is_named_with_its_disposition():
    named_in = []
    for path in (OWNER_DOC, CONTRACT):
        if "build-summary-input.py" in path.read_text(encoding="utf-8"):
            named_in.append(path.name)
    assert named_in, (
        "C-14 forbids silence: the owner doc or this contract must name "
        "skills/create-team/scripts/build-summary-input.py and state what it does about the "
        "reference form"
    )
    text = OWNER_DOC.read_text(encoding="utf-8")
    assert "build-summary-input.py" in text, (
        "the disposition belongs in the owner doc, where the next reader of the reference "
        "form will look, not only in a spec contract"
    )


def test_c15_the_local_parser_stays_local_and_the_two_derivations_agree(tmp_path):
    src = SUMMARY_SCRIPT.read_text(encoding="utf-8")
    assert "cross-tree import breaks once installed" in src, (
        "the comment that makes the local parse deliberate must survive — without it the "
        "next reader 'fixes' the duplication with an import that breaks once installed"
    )
    assert not re.search(r"^\s*(?:from|import)\s+goal_utils|import goal-utils", src, re.M), (
        "C-15: the disposition must not be an import across the two mirrored trees"
    )

    summary = _load(SUMMARY_SCRIPT, "_build_summary_input_us5")
    engine = _goal_utils()
    criterion = "Every skill under [subjects: skills/draw-*] renders a diagram."
    root = _repo(tmp_path, criterion, dirs=("skills/draw-a", "skills/draw-b"))

    derived = engine.derive_subjects(criterion, root)
    rendered = summary.expand_subjects(criterion, root)
    for member in derived["paths"]:
        assert member in rendered, (
            f"the summary reader shows a criterion whose derived member {member!r} is "
            f"absent from its rendering — the two derivations have drifted: {rendered!r}"
        )
    assert "[subjects:" not in rendered, (
        f"an opaque tag must not reach a summary reader who has no way to resolve it "
        f"(Principle XV): {rendered!r}"
    )
    # and a criterion with no reference is rendered byte-identically
    plain = "Seven skills render diagrams."
    assert summary.expand_subjects(plain, root) == plain


def test_c16_the_fifth_exit_code_convention_is_recorded_not_unified():
    text = OWNER_DOC.read_text(encoding="utf-8")
    assert "build-summary-input.py" in text and re.search(r"EXIT_NO_MATERIAL|退出码", text), (
        "the owner doc must record that build-summary-input.py keeps its own exit-code "
        "table whose 3/4 mean something different from goal-utils' — otherwise a reader "
        "assumes one table covers the repository"
    )
    src = SUMMARY_SCRIPT.read_text(encoding="utf-8")
    assert "EXIT_NO_MATERIAL" in src and "EXIT_SERIALIZED" in src, (
        "sentinel: that second table moved, so the recorded divergence is about nothing"
    )
    gu = _goal_utils()
    assert gu.EXIT_NOT_FOUND == 3 and gu.EXIT_INVALID == 4, (
        "the two tables must stay divergent and documented, not silently unified as a side "
        "effect of this feature"
    )


# =========================================================================== #
# C-17 … C-19 — pins
# =========================================================================== #


def test_c17_the_regex_and_states_are_pinned_as_a_table_not_as_prose():
    mod = _goal_utils()
    table = {
        "SUBJECT_REF": SUBJECT_REF,
        "BRACE_ENUM": BRACE_ENUM,
    }
    for name, pattern in table.items():
        assert hasattr(mod, name), f"module-level constant {name} missing"
        assert getattr(mod, name).pattern == pattern, (
            f"{name} drifted from the pinned shape: {getattr(mod, name).pattern!r}"
        )
    for state in DERIVE_STATES:
        assert state in mod.SUBJECT_STATES, (
            f"the derivation's state vocabulary is closed and must contain {state!r}: "
            f"{sorted(mod.SUBJECT_STATES)}"
        )
    assert set(mod.SUBJECT_STATES) == DERIVE_STATES, (
        f"a state was added or removed without updating this pin: {sorted(mod.SUBJECT_STATES)}"
    )
    for key, prefix in PROBLEM_PREFIXES.items():
        assert prefix in mod.SUBJECT_PROBLEM_PREFIXES.values(), f"{key} lost its prefix"
    assert len(set(mod.SUBJECT_PROBLEM_PREFIXES.values())) == len(PROBLEM_PREFIXES), (
        "the three prefixes must stay mutually distinct, or the tiers collapse"
    )


def test_c18_the_engine_suite_that_reads_the_owner_doc_stays_green():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/contract/test_goal_targets_engine.py"],
        capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0, f"the AUTHORITY pin broke:\n{r.stdout[-1200:]}"


def test_c19_the_gate_budget_survives_the_new_section():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "python" / "scan-confirmation-gates.py"),
         "--summary"], capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    total = int(re.search(r"blocking confirmation gates:\s*(\d+)", r.stdout).group(1))
    violations = int(re.search(r"violations[^:]*:\s*(\d+)", r.stdout).group(1))
    assert total == 23, (
        f"the owner doc sits in shared/, inside the scanned surface, and the integer "
        f"headroom is 0: total moved to {total}"
    )
    assert violations == 0


def test_the_mirror_of_the_owner_doc_matches_and_the_clause_count_holds():
    assert OWNER_DOC_MIRROR.is_file(), f"the runtime mirror is missing: {OWNER_DOC_MIRROR}"
    assert OWNER_DOC.read_text(encoding="utf-8") == OWNER_DOC_MIRROR.read_text(
        encoding="utf-8"), "the owner doc and its .specify mirror diverged"
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", CONTRACT.read_text(encoding="utf-8"))
    assert len(ids) == 19, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 20))
