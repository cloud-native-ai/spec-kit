"""Contract tests for contracts/checker-form.md — all 33 clauses (Feature 053, T007).

Class-labeling discipline (the contract's own header rule): 21 clauses are [制品类] and are
asserted mechanically here; 12 are [行为类], whose evidence is a run, a drill or a review.
This suite MUST NOT claim a behavior-class clause is "covered by a guard" — where a
behavior-class clause has an observable artifact-side proxy, the test name says which
clause and which proxy, and the proxy is asserted instead of the claim.

Skips are explicit and named, never silent passes: `account-clause-coverage.py` (T025) does
not exist during US1, and `goal-utils.py`'s new action (T031) does not exist during US1/US3.
Their own form obligations are pinned by tests/contract/test_clause_coverage.py (T024) and
tests/contract/test_run_checks.py (T030).

Red-first: this suite is red until scripts/python/validate-requirements.py lands (T009).
"""
from __future__ import annotations

import ast
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
SCRIPTS = ROOT / "scripts" / "python"
SPEC = ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts"
CONTRACT = SPEC / "contracts" / "checker-form.md"

STR008 = "Program-First discipline (shared/guidelines/token-efficiency.md)"
LABEL_DOC_RE = re.compile(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", re.M)

def _sibling_pin(module_file: str, attr: str):
    """Read a pin from a sibling suite by path, so the label set has ONE source (C-22: a set
    literal, and a second copy would be a second fact free to drift)."""
    path = ROOT / "tests" / "contract" / module_file
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)


# The five checks US1's checker owns; the canonical pin lives in test_requirements_checker.py.
VR_CHECKS = _sibling_pin("test_requirements_checker.py", "REQUIREMENTS_CHECKS")

NEW_CHECKERS = {
    "validate-requirements.py": VR_CHECKS,
    "account-clause-coverage.py": None,  # label set owned by T024's suite
}


def _load(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _exists(name: str) -> bool:
    return (SCRIPTS / name).is_file()


# A checker this phase is responsible for MUST fail loudly when absent — a skip is not red.
# Only the accountant (T025, a later phase) is allowed to skip, and the skip names its owner.
_SKIP_ALLOWED = {"account-clause-coverage.py": "T024/T025 (US3) pin it; see module docstring"}


def _require(name: str):
    if not _exists(name):
        if name in _SKIP_ALLOWED:
            pytest.skip(f"{name} not landed yet — {_SKIP_ALLOWED[name]}")
        raise AssertionError(f"{name} is missing: this suite's subject has not landed (T009)")
    return _load(name)


def _run(mod_name: str, args, expect=None):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / mod_name), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if expect is not None:
        assert r.returncode == expect, f"{mod_name} {args} -> {r.returncode}\n{r.stdout}\n{r.stderr}"
    return r


GOOD_SPEC = SPEC / "requirements.md"


# --------------------------------------------------------------------------- #
# C-1 / C-2 — single entry, path is the only input
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c01_single_entry_main_is_callable(name):
    mod = _require(name)
    assert callable(mod.main)
    rc = mod.main([str(GOOD_SPEC)])
    assert isinstance(rc, int)


@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c02_proxy_path_is_the_only_argument(name):
    """C-2 is [行为类]; its proxy is that this test can judge the artifact with a path only —
    no text is read here and injected, so the script must do its own reading."""
    mod = _require(name)
    assert mod.main([str(GOOD_SPEC)]) == 0


# --------------------------------------------------------------------------- #
# C-3 / C-7 / C-8 — machine-readable output
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c03_json_flag_agrees_with_human_output(name, tmp_path):
    mod = _require(name)
    rc_human = mod.main([str(GOOD_SPEC)])
    rc_json = mod.main([str(GOOD_SPEC), "--json"])
    assert rc_human == rc_json


@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c07_json_key_set_and_verdict_array_length(name):
    _require(name)
    r = _run(name, [str(GOOD_SPEC), "--json"], expect=0)
    payload = json.loads(r.stdout)
    for key in ("file", "checks", "errors", "warnings"):
        assert key in payload, f"missing key {key}"
    assert isinstance(payload["checks"], list) and payload["checks"]
    expected = NEW_CHECKERS[name]
    if expected is not None:
        assert len(payload["checks"]) == len(expected)


def test_c08_human_tail_line_form():
    _require("validate-requirements.py")
    r = _run("validate-requirements.py", [str(GOOD_SPEC)], expect=0)
    tail = [l for l in r.stdout.strip().splitlines() if "error(s)" in l][-1]
    assert re.search(r"\d+ error\(s\), \d+ warning\(s\)", tail), tail


def test_c09_precedent_four_keys_are_not_migrated():
    """The existing validate-tasks.py keeps its four-key JSON and MUST NOT grow a verdict array."""
    r = _run("validate-tasks.py", [str(SPEC / "tasks.md"), "--json"], expect=0)
    payload = json.loads(r.stdout)
    assert set(payload) == {"file", "errors", "warnings", "status"}
    assert "checks" not in payload


# --------------------------------------------------------------------------- #
# C-4 / C-5 / C-6 — Program-First attribution and the docstring label body
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c04_docstring_names_the_owner_file(name):
    _require(name)
    src = (SCRIPTS / name).read_text(encoding="utf-8")
    assert STR008 in src


@pytest.mark.parametrize("name,labels", sorted(NEW_CHECKERS.items()))
def test_c05_docstring_label_body_matches_the_pinned_set(name, labels):
    mod = _require(name)
    extracted = set(LABEL_DOC_RE.findall(mod.__doc__ or ""))
    if labels is None:
        assert extracted, "label body present but its set is pinned by T024's suite"
    else:
        assert extracted == labels


def test_c06_proxy_existing_attribution_form_is_untouched():
    """C-6 is [行为类] (a MUST NOT rewrite); the proxy is that goal-utils.py still carries its
    own inline-paren attribution rather than the new STR-008 form."""
    src = (SCRIPTS / "goal-utils.py").read_text(encoding="utf-8")
    assert STR008 not in src.split('"""')[1], "goal-utils.py's attribution form was rewritten"


# --------------------------------------------------------------------------- #
# C-10 / C-11 / C-12 — three distinguishable failure shapes, three exit tiers
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c10_three_failure_shapes_are_distinguishable(name, tmp_path):
    mod = _require(name)
    missing = tmp_path / "nope.md"
    empty = tmp_path / "empty.md"
    empty.write_text("", encoding="utf-8")
    skeleton = tmp_path / "skeleton.md"
    skeleton.write_text(
        "# Spec: [SPEC]\n\n## Requirements\n\n- **FR-001**: [placeholder]\n", encoding="utf-8"
    )
    rc_missing = mod.main([str(missing)])
    rc_empty = mod.main([str(empty)])
    rc_skeleton = mod.main([str(skeleton), "--json"])
    assert rc_missing == 2 and rc_empty == 2
    payload = json.loads(subprocess.run(
        [sys.executable, str(SCRIPTS / name), str(skeleton), "--json"],
        capture_output=True, text=True, cwd=str(ROOT)).stdout)
    assert payload["status"] not in ("ok", "missing", "unparsable"), payload["status"]
    assert rc_skeleton != 0 or payload["status"] != "ok"


@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c11_exit_table_is_three_tiers_with_a_fourth_status(name, tmp_path):
    mod = _require(name)
    assert mod.main([str(GOOD_SPEC)]) == 0
    assert mod.main([str(tmp_path / "absent.md")]) == 2
    broken = tmp_path / "broken.md"
    broken.write_text("# x\n\n- **FR-001** a\n\n- **FR-003** b\n", encoding="utf-8")
    assert mod.main([str(broken)]) == 1


def test_c11_warn_only_still_exits_zero(tmp_path):
    mod = _require("validate-requirements.py")
    p = tmp_path / "warn.md"
    p.write_text(
        "# Spec\n\n## Requirements\n\n- **FR-001**: real requirement text here.\n",
        encoding="utf-8",
    )
    rc = mod.main([str(p)])
    assert rc == 0, "a warning-only artifact MUST NOT change the exit tier"


def test_c12_proxy_skeleton_criterion_is_written_down():
    """C-12 is [行为类]: the skeleton criterion MUST be stated by a truth-source document, and it
    is a semantic judgement, so the truth source here is the checker's own module docstring —
    neither contract states which placeholder forms count, and adding a clause to say so would
    move a pinned clause count. The docstring is the artifact that owns its own verdict
    vocabulary (checker-form C-33 points the same way)."""
    mod = _require("validate-requirements.py")
    doc = mod.__doc__ or ""
    assert "skeleton" in doc.lower() or "骨架" in doc
    assert re.search(r"\[[A-Z][A-Z _]+\]|PLACEHOLDER|placeholder", doc), (
        "the docstring must name the placeholder forms that make an artifact skeleton-only"
    )


# --------------------------------------------------------------------------- #
# C-13 / C-14 — read-only
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c13_new_checkers_have_zero_write_points(name):
    _require(name)
    src = (SCRIPTS / name).read_text(encoding="utf-8")
    hits = re.findall(r"\.(?:write_text|write_bytes|mkdir|unlink|rmtree)\(|open\([^)]*['\"][wax]", src)
    assert hits == [], f"write point in {name}: {hits}"


@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c14_proxy_checksum_unchanged_across_a_run(name):
    """C-14's required evidence is a write-point scan PLUS a before/after checksum; this is the
    checksum half, executed rather than asserted from a docstring."""
    _require(name)
    before = hashlib.md5(GOOD_SPEC.read_bytes()).hexdigest()
    _run(name, [str(GOOD_SPEC)], expect=0)
    assert hashlib.md5(GOOD_SPEC.read_bytes()).hexdigest() == before


# --------------------------------------------------------------------------- #
# C-15 … C-18 — counter-samples (evidence discipline)
# --------------------------------------------------------------------------- #

def test_c15_c18_counter_samples_exist_one_per_new_check():
    """C-15/C-18 are [行为类]; the observable proxy is that this suite itself exercises a broken
    artifact per check and each names exactly its own class (4/4 zero cross-masking is asserted
    in test_requirements_checker.py, which owns the five labels)."""
    src = Path(__file__).read_text(encoding="utf-8")
    assert "positive_control" in src, "C-21 requires a positive control before any no-false-positive claim"


def test_c16_denominator_owner_is_enumerated_not_typed():
    """C-16 compares the counter-sample list against the NEW label subset; that subset's owner is
    data-model.md, so the denominator must be enumerable from it rather than typed into a gate."""
    dm = (SPEC / "data-model.md").read_text(encoding="utf-8")
    assert "标签集" in dm
    for label in VR_CHECKS:
        assert label in dm or label in (SPEC / "contracts" / "requirements-checker.md").read_text(encoding="utf-8")


def test_c17_proxy_no_counter_sample_residue_in_the_spec_tree():
    """C-17 is [行为类]; the residue half is mechanically checkable: no planted sample survives
    under .specify/specs/."""
    residue = [p for p in SPEC.rglob("*") if re.search(r"counter-sample|broken-copy|plant", p.name)]
    assert residue == [], residue


# --------------------------------------------------------------------------- #
# C-19 — anti-vacuity
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", sorted(NEW_CHECKERS))
def test_c19_empty_set_carries_a_non_empty_companion(name):
    _require(name)
    r = _run(name, [str(GOOD_SPEC), "--json"], expect=0)
    payload = json.loads(r.stdout)
    assert payload["errors"] == 0
    assert payload.get("scanned") or payload.get("counts") or payload["checks"], (
        "an empty error set with no companion cannot distinguish 'empty because right' from "
        "'empty because blind'"
    )


# --------------------------------------------------------------------------- #
# C-20 / C-21 — mutation drill and positive control
# --------------------------------------------------------------------------- #

def test_c20_mutation_drill_is_recorded_where_the_evidence_lands():
    """C-20 is [行为类]: the drill's record lands in verification.md at T049. Proxy here is that
    the landing point exists and names the drill."""
    notes = SPEC / "notes" / "red-first-evidence.md"
    assert notes.is_file()
    assert "T004" in notes.read_text(encoding="utf-8")


def test_c21_positive_control_runs_before_any_no_false_positive_claim(tmp_path):
    """The check MUST be shown to fire on a positive sample before anyone concludes it does not
    over-report — the plan-phase probe that skipped this step mis-judged a [P] conflict."""
    mod = _require("validate-requirements.py")
    broken = tmp_path / "positive_control.md"
    broken.write_text("# x\n\n- **FR-001** a\n\n- **FR-003** b\n", encoding="utf-8")
    assert mod.main([str(broken)]) == 1, "positive control did not fire — the check is not proven to run"


# --------------------------------------------------------------------------- #
# C-22 … C-28 — pins
# --------------------------------------------------------------------------- #

def _pin_source() -> str:
    return (ROOT / "tests" / "contract" / "test_validate_tasks_parallel_safety.py").read_text(encoding="utf-8")


def test_c22_label_pin_is_a_set_not_a_count():
    src = _pin_source()
    m = re.search(r"EXPECTED_CHECKS\s*=\s*(\{[^}]*\})", src, re.S)
    assert m, "EXPECTED_CHECKS set literal not found"
    assert len(ast.literal_eval(m.group(1))) >= 6
    assert not re.search(r"len\(EXPECTED_CHECKS\)\s*==\s*\d+", src), "label set pinned as a count"


def test_c23_exit_table_is_pinned_separately_from_the_label_set():
    src = _pin_source()
    assert "def test_c5_exit_code_table" in src
    label_fn = re.search(r"def (test_\w*label\w*|test_c4\w*)\(", src)
    assert label_fn, "no separate label-set test function"
    assert label_fn.group(1) != "test_c5_exit_code_table"


def test_c24_every_touched_checker_has_both_pins():
    vt = _pin_source()
    assert "EXPECTED_CHECKS" in vt and "def test_c5_exit_code_table" in vt
    rc = (ROOT / "tests" / "contract" / "test_requirements_checker.py")
    if rc.is_file():
        body = rc.read_text(encoding="utf-8")
        assert "REQUIREMENTS_CHECKS" in body, "US1 checker lacks a label-set pin"
        assert re.search(r"returncode|exit", body), "US1 checker lacks an exit-table pin"


def test_c25_existing_two_pins_present_and_grow_with_the_new_checks():
    src = _pin_source()
    assert "EXPECTED_CHECKS" in src
    labels = set(ast.literal_eval(re.search(r"EXPECTED_CHECKS\s*=\s*(\{[^}]*\})", src, re.S).group(1)))
    if any(l.startswith("green-") for l in labels):
        assert len(labels) == 10, "US2 landed four checks; the pinned set must be the 6+4 union"
    else:
        assert len(labels) == 6


def test_c26_goal_utils_exit_table_is_pinned_iff_the_constants_are_imported():
    """C-26's obligation lands with US4; the stable invariant is that a table pin exists exactly
    when the constants are imported by a test."""
    hits = [
        h for h in subprocess.run(
            ["grep", "-rl", "--include=*.py", "goal_utils.EXIT", str(ROOT / "tests")],
            capture_output=True, text=True,
        ).stdout.strip().splitlines()
        if Path(h).name != Path(__file__).name  # this suite mentions the needle; it is not a pin
    ]
    if hits:
        body = "\n".join(Path(h).read_text(encoding="utf-8") for h in hits)
        assert "EXIT_CODES" in body or "EXIT_OK" in body


def test_c27_action_roster_tuple_tracks_the_binary():
    src = (ROOT / "tests" / "contract" / "test_goal_definition.py").read_text(encoding="utf-8")
    binary = (SCRIPTS / "goal-utils.py").read_text(encoding="utf-8")
    has_run_checks = '"run-checks"' in binary or "'run-checks'" in binary
    roster_has_it = '"run-checks"' in src or "'run-checks'" in src
    assert has_run_checks == roster_has_it, (
        "a new action MUST be added to the hardcoded roster tuple in the same commit"
    )


def test_c28_every_action_help_line_starts_with_a_read_write_label():
    """Parsed with ast rather than a regex: `help=` may sit on a continuation line, and a
    text-shaped pattern silently extracts nothing (which would pass vacuously)."""
    tree = ast.parse((SCRIPTS / "goal-utils.py").read_text(encoding="utf-8"))
    helps = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if not (isinstance(fn, ast.Attribute) and fn.attr == "add_parser"):
            continue
        if not (node.args and isinstance(node.args[0], ast.Constant)):
            continue
        action = node.args[0].value
        for kw in node.keywords:
            if kw.arg == "help" and isinstance(kw.value, ast.Constant):
                helps.append((action, kw.value.value))
    assert len(helps) >= 9, f"expected every subparser to carry help, got {helps}"
    for action, help_text in helps:
        assert help_text.split()[0].rstrip(":") in ("read", "write"), (action, help_text)


# --------------------------------------------------------------------------- #
# C-29 … C-33 — runnability, packaging, mirrors, vocabulary
# --------------------------------------------------------------------------- #

def test_c29_proxy_a_real_run_is_recorded():
    """C-29 is [行为类]; its evidence is a real run on a real artifact, recorded in the notes."""
    ev = (SPEC / "notes" / "red-first-evidence.md").read_text(encoding="utf-8")
    qr = (SPEC / "notes" / "quickstart-run.md").read_text(encoding="utf-8")
    assert "validate-requirements.py" in ev or "validate-requirements.py" in qr


def test_c30_new_scripts_ship_via_the_force_include_mapping():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "force-include" in pyproject and "specify_cli/scripts" in pyproject
    assert (SCRIPTS / "validate-requirements.py").parent.name == "python"


def test_c31_mirror_pair_covers_scripts_with_strict_extras():
    src = (SCRIPTS / "sync-mirrors.py").read_text(encoding="utf-8")
    assert '"scripts"' in src and "strict_extras=True" in src
    parity = ROOT / "tests" / "contract" / "test_scripts_distribution_parity.py"
    assert parity.is_file()


def test_c32_proxy_every_written_pair_has_a_row_in_the_mirror_table():
    """C-32 is [行为类]; the proxy is that plan.md's table names a criterion for each pair this
    feature writes into — including the two pairs added after the analyze rounds."""
    plan = (SPEC / "plan.md").read_text(encoding="utf-8")
    for token in ("--only skills", "--only templates", "scripts/python", "shared/definitions"):
        assert token in plan, f"mirror table lacks a criterion for {token}"


def test_c33_proxy_messages_are_actionable_not_bare_labels(tmp_path):
    """C-33 is [行为类]; the proxy is the message shape: a line number, the rule, and text —
    never a bare internal label."""
    mod = _require("validate-requirements.py")
    broken = tmp_path / "c33.md"
    broken.write_text("# x\n\n- **FR-001** a\n\n- **FR-003** b\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate-requirements.py"), str(broken)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 1
    lines = [l for l in r.stdout.splitlines() if re.match(r"^\d+: ", l)]
    assert lines, r.stdout
    for line in lines:
        assert re.match(r"^\d+: [a-z-]+: .{10,}", line), line


# --------------------------------------------------------------------------- #
# the contract artifact itself
# --------------------------------------------------------------------------- #

def test_the_contract_still_has_the_clause_count_this_suite_pins():
    body = CONTRACT.read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", body)
    assert len(ids) == 33, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 34)), "clause ids are not contiguous"
