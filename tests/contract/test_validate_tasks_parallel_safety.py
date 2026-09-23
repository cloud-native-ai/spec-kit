"""Contract test: validate-tasks.py's `[P]` parallel-safety guard.

Subject: ``scripts/python/validate-tasks.py`` (a runnable artifact, so it is
exercised through its real ``validate()`` / ``main()``, never by re-implementing
its regexes here).

The guard's defect class (introspection F-04 iv): path extraction from a task
row's prose is heuristic, and the old form treated EVERY path token as a write
target — so two `[P]` rows that merely cite the same owner document were
reported as a parallel write conflict. The fix splits a row's paths into write
targets and pointer targets and reports on the write targets.

Three propositions are pinned, because a fix that only satisfies the first is
indistinguishable from a deleted guard:

* C-1 read-only pair      -> zero `parallel-safe` warnings (the fix)
* C-2 two real writers    -> still warned, with the two-writer wording (the
                             guard survives the fix)
* C-3 one writes/one cites-> still warned, with distinct read-only wording (no
                             signal the old guard emitted is dropped)

C-4 pins the check roster as LABELS, never as a count (a count is a second fact
free to drift from the list it summarizes); C-5 pins the exit-code table, which
nothing else in the suite owns.

The template-side duties that accompany the guard (adjudicate by actual write
target; never silence a warning by deleting the cited path) and the runtime
evidence landing points are pinned in the same file, because they land in the
same change: C-6..C-9.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = REPO_ROOT / "scripts" / "python" / "validate-tasks.py"
TASKS_CMD = REPO_ROOT / "templates" / "commands" / "tasks.md"
PLAN_CMD = REPO_ROOT / "templates" / "commands" / "plan.md"
PLAN_TPL = REPO_ROOT / "templates" / "plan-template.md"

# --- literals under guard --------------------------------------------------

WRITE_WORDING = "both WRITE"
READONLY_WORDING = "only references it as a read-only target"
ANTI_SILENCING = "never by deleting the cited path"

# The owner of the failing-test baseline path is implement.md's `**Test runs**`
# bullet. tasks.md must reach it by pointer and MUST NOT carry the literal —
# a second copy of that path is exactly the drift this asserts against.
BASELINE_POINTER = "`**Test runs**`"
BASELINE_OWNER_CMD = "templates/commands/implement.md"
BASELINE_PATH_LITERAL = "baseline-failed"

NOTES_LANDING_POINTS = (
    "<spec-dir>/notes/red-first-evidence.md",
    "<spec-dir>/notes/quickstart-run.md",
    "<spec-dir>/notes/pre-change-measurements.md",
)
REFREEZE_LITERAL = "**Re-freeze timing**"

EXEC_VERIFY_SCOPE = "any artifact this command produces"
TEARDOWN_DUTY = "**Teardown is verified to the same standard as setup**"
DISCLAIMER_PREMISES = "A disclaimer MUST also list the premises that example rests on"
TPL_RUN_AND_PASTE = "Every derived command printed here MUST have been actually run"
TPL_REGEX_SCOPE = "match non-target lines"
TPL_OWNER_POINTER = "Post-Generation Quality Gate"

EXPECTED_CHECKS = {
    "row-format",
    "id-unique",
    "blockedBy",
    "parallel-safe",
    "story-labels",
    "dod-format",
}


def _load_validator():
    """Load the real validator module — never a copy of its logic."""
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    spec = importlib.util.spec_from_file_location("_validate_tasks_under_test", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_tasks(tmp_path: Path, name: str, rows: list[str]) -> Path:
    path = tmp_path / name
    path.write_text(
        "# Tasks\n\n## Phase 1: Setup\n\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    return path


def _parallel_warnings(messages: list[str]) -> list[str]:
    return [m for m in messages if "parallel-safe" in m]


def _anti_vacuity(mod, path: Path, expected_ids: set[str]) -> None:
    """A clean verdict is only evidence if the rows really parsed as tasks.

    Two independent observations, because "zero warnings" is also what an
    unparsed or malformed file produces:

    1. the validator's own error channel is empty for the sample (so the rows are
       well-formed task rows it accepted), and the row IDs the sample declares
       are exactly the ones the test believes it wrote;
    2. a control pair written into the SAME file shape does warn — proving the
       phase heading and `[P]` detection are live for this sample, not skipped.
    """
    errors, _ = mod.validate(path)
    assert not errors, (
        f"sentinel: the sample is malformed, so a clean WARN verdict proves nothing: {errors}"
    )
    declared = set(re.findall(r"^- \[[ xX>~]\]\s+(T\d{3}[A-Za-z]?)\b",
                              path.read_text(encoding="utf-8"), re.M))
    assert declared == expected_ids, (
        f"sentinel: the sample declares {sorted(declared)}, the test expects "
        f"{sorted(expected_ids)} — the assertions below would run against a "
        "different population than they claim to"
    )
    control = path.parent / "control.md"
    control.write_text(
        "# Tasks\n\n## Phase 1: Setup\n\n"
        "- [ ] T001 [P] Add rule A assertions to tests/contract/control.py\n"
        "- [ ] T002 [P] Add rule B assertions to tests/contract/control.py\n",
        encoding="utf-8",
    )
    _, control_warnings = mod.validate(control)
    assert _parallel_warnings(control_warnings), (
        "sentinel: the control pair did not warn, so [P] same-write detection is "
        "not live for this file shape and the clean verdict above is vacuous"
    )


# --- C-1: two read-only citations of one owner are not a write conflict ----


READONLY_PAIR = [
    "- [ ] T001 [P] Add contract assertions to tests/contract/test_alpha.py "
    "per shared/guidelines/token-efficiency.md",
    "- [ ] T002 [P] Add contract assertions to tests/contract/test_beta.py "
    "per shared/guidelines/token-efficiency.md",
]

# Same defect class in the house's Chinese pointer idiom (`指向 <path> 的指针`).
READONLY_PAIR_CJK = [
    "- [ ] T001 [P] 在 templates/instructions-template.md 插入一节,引导句式含反引号路径 "
    "指向 shared/guidelines/token-efficiency.md",
    "- [ ] T002 [P] 在 templates/commands/todo.md 加一行,指向 shared/guidelines/token-efficiency.md 的指针",
]


@pytest.mark.parametrize(
    "rows",
    [pytest.param(READONLY_PAIR, id="per-governor"),
     pytest.param(READONLY_PAIR_CJK, id="cjk-zhixiang-governor")],
)
def test_c1_readonly_pair_is_not_a_write_conflict(tmp_path, rows):
    mod = _load_validator()
    path = _write_tasks(tmp_path, "readonly.md", rows)
    _anti_vacuity(mod, path, {"T001", "T002"})

    errors, warnings = mod.validate(path)
    assert _parallel_warnings(warnings) == [], (
        "two [P] rows that only CITE the same owner document were reported as a "
        f"parallel write conflict: {_parallel_warnings(warnings)}"
    )
    assert errors == []


# --- C-2: two real writers are still reported (the guard survives) --------


WRITE_PAIR = [
    "- [ ] T001 [P] Add contract assertions for rule A to tests/contract/test_shared.py",
    "- [ ] T002 [P] Add contract assertions for rule B to tests/contract/test_shared.py",
]


def test_c2_write_pair_is_still_reported(tmp_path):
    mod = _load_validator()
    path = _write_tasks(tmp_path, "write.md", WRITE_PAIR)
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = mod.validate(path)
    hits = _parallel_warnings(warnings)
    assert len(hits) == 1, f"expected exactly one two-writer warning, got {hits}"
    assert WRITE_WORDING in hits[0], f"two-writer wording lost: {hits[0]}"
    assert ANTI_SILENCING in hits[0], (
        "the two-writer warning must carry the anti-silencing remedy: "
        "'never by deleting the cited path'"
    )
    assert "tests/contract/test_shared.py" in hits[0]


def test_c2_guard_not_weakened_by_a_readonly_marker_elsewhere_in_the_row(tmp_path):
    """A row that says `read-only` about one file still owns its write target."""
    mod = _load_validator()
    path = _write_tasks(tmp_path, "mixed_prose.md", [
        "- [ ] T001 [P] Keep shared/guidelines/token-efficiency.md read-only and "
        "instead add the assertions to tests/contract/test_shared.py",
        "- [ ] T002 [P] Add contract assertions for rule B to tests/contract/test_shared.py",
    ])
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = mod.validate(path)
    hits = _parallel_warnings(warnings)
    assert len(hits) == 1 and WRITE_WORDING in hits[0], (
        "a read-only marker earlier in the row demoted the row's real write "
        f"target and the two-writer conflict went unreported: {hits}"
    )


PROBE_THEN_WRITE_ROW = (
    "- [ ] T001 [P] grep the roster, then rewrite tests/contract/probe.py"
)


def test_c2b_write_verb_in_the_probe_window_cancels_the_demotion(tmp_path):
    """`grep ..., then rewrite <path>` keeps <path> a write target.

    The probe verb sits INSIDE the classifier's window here, so WRITE_VERB is
    the only thing standing between this row and a demoted write target — a
    sample with the probe verb further away would pass with the cancellation
    deleted, i.e. would not be a check at all.
    """
    mod = _load_validator()

    write, pointer = mod._classify_paths(PROBE_THEN_WRITE_ROW)
    assert "tests/contract/probe.py" in write, (
        "a probe verb earlier in the row demoted the row's real write target"
    )
    assert "tests/contract/probe.py" not in pointer

    path = _write_tasks(tmp_path, "probe_then_write.md", [
        PROBE_THEN_WRITE_ROW,
        "- [ ] T002 [P] Add the mirrored assertions to tests/contract/probe.py",
    ])
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = mod.validate(path)
    hits = _parallel_warnings(warnings)
    assert len(hits) == 1 and WRITE_WORDING in hits[0], (
        "the two-writer conflict went unreported (or was mislabelled as "
        f"write-vs-cite) because a probe verb demoted a real write target: {hits}"
    )


def test_c2c_probe_target_itself_is_a_pointer_target():
    """The other half of C-2b: the demotion does fire where it should."""
    mod = _load_validator()
    write, pointer = mod._classify_paths(
        "- [ ] T003 [P] assert grep of the roster in shared/roster.md returns no matches"
    )
    assert "shared/roster.md" in pointer, (
        "a `grep ... in <path>` probe target was classified as a write target, "
        "which is the false-positive class this fix exists to remove"
    )
    assert "shared/roster.md" not in write


# --- C-3: one writes, one cites — still reported, distinct wording --------


MIXED_PAIR = [
    "- [ ] T001 [P] Rewrite shared/guidelines/token-efficiency.md with the new escalation ladder",
    "- [ ] T002 [P] Add a contract test in tests/contract/test_token.py asserting grep of the "
    "section list in shared/guidelines/token-efficiency.md returns no matches",
]


def test_c3_write_versus_cite_is_still_reported(tmp_path):
    mod = _load_validator()
    path = _write_tasks(tmp_path, "mixed.md", MIXED_PAIR)
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = mod.validate(path)
    hits = _parallel_warnings(warnings)
    assert len(hits) == 1, f"expected exactly one write-vs-cite warning, got {hits}"
    assert READONLY_WORDING in hits[0], (
        "the write-vs-cite warning must be labelled distinctly from the "
        f"two-writer case: {hits[0]}"
    )
    assert WRITE_WORDING not in hits[0], (
        "write-vs-cite must not claim two writers — that is a false machine "
        f"verdict the adjudicator would have to overturn: {hits[0]}"
    )


# --- C-4: the check roster is pinned as labels, not as a count ------------


def test_c4_check_roster_is_unchanged_by_this_fix():
    """This fix refines `parallel-safe`; it adds no check and removes none.

    Pinned as a label set so a future check must be declared here deliberately
    rather than slipping in silently.
    """
    mod = _load_validator()
    doc = mod.__doc__ or ""
    labels = set(re.findall(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", doc, re.M))
    assert labels, "sentinel: no check labels parsed from the docstring — the roster check is blind"
    assert labels == EXPECTED_CHECKS, (
        f"validate-tasks.py's documented check roster drifted: {sorted(labels)}"
    )


def test_c4b_parallel_safe_entry_documents_write_targets():
    mod = _load_validator()
    lines = (mod.__doc__ or "").splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("  parallel-safe")), None)
    assert start is not None, "sentinel: the parallel-safe docstring entry is gone"
    # the entry is a wrapped block: its first line plus every continuation line
    # up to the next check label
    end = next(
        (i for i in range(start + 1, len(lines))
         if re.match(r"^  [A-Za-z][A-Za-z-]*\s{2,}", lines[i]) or not lines[i].strip()),
        len(lines),
    )
    entry = "\n".join(lines[start:end])
    assert len(entry.splitlines()) > 1, (
        "sentinel: the entry read as a single line, so the continuation the "
        "assertions below key on was never extracted"
    )
    assert "must not WRITE" in entry, (
        "the roster still describes the pre-fix semantics ('must not name the "
        "same file'), which is what made read-only citations look like conflicts"
    )
    assert "pointer target" in entry, "the entry must name the write/pointer split"


# --- C-5: the exit-code table ---------------------------------------------


def test_c5_exit_code_table(tmp_path, capsys):
    mod = _load_validator()

    clean = _write_tasks(tmp_path, "clean.md", [
        "- [ ] T001 Do one thing in a/one.py",
        "- [ ] T002 Do another thing in b/two.py",
    ])
    assert mod.main([str(clean)]) == 0, "0 = no errors (warnings allowed)"

    warn = _write_tasks(tmp_path, "warn.md", WRITE_PAIR)
    assert mod.main([str(warn)]) == 0, "a warning-only file must still exit 0"

    bad = _write_tasks(tmp_path, "bad.md", [
        "- [ ] T001 Do one thing in a/one.py",
        "- [ ] T001 Duplicate id in b/two.py",
    ])
    assert mod.main([str(bad)]) == 1, "1 = at least one error"

    empty = tmp_path / "empty.md"
    empty.write_text("# Tasks\n\nno task rows here\n", encoding="utf-8")
    assert mod.main([str(empty)]) == 2, "2 = no task rows found"

    missing = tmp_path / "absent.md"
    assert mod.main([str(missing)]) == 2, "2 = file missing"
    capsys.readouterr()


def test_c5b_json_mode_reports_the_same_verdict(tmp_path, capsys):
    mod = _load_validator()
    path = _write_tasks(tmp_path, "mixed.md", MIXED_PAIR)
    rc = mod.main([str(path), "--json"])
    out = capsys.readouterr().out
    assert rc == 0
    import json as _json
    payload = _json.loads(out)
    assert payload["status"] == "PASS"
    assert payload["errors"] == []
    assert len(_parallel_warnings(payload["warnings"])) == 1


# --- C-6..C-9: the template-side duties that land with the guard ----------


def test_c6_tasks_command_carries_the_write_target_adjudication_duty():
    text = TASKS_CMD.read_text(encoding="utf-8")
    assert "actual write targets" in text, (
        "step 5 must tell the adjudicator to judge a parallel-safe WARN by the "
        "rows' actual write targets, since the machine classification is heuristic"
    )
    assert "MUST NOT silence a WARN by deleting the referenced path" in text, (
        "step 5 lost the anti-silencing duty — deleting the cited path removes "
        "the evidence of a conflict without removing the conflict"
    )
    assert "two parallel tasks **writing** the same file" in text, (
        "step 5's roster still describes the pre-fix semantics ('naming the same "
        "file'), which is what made read-only citations look like conflicts"
    )


def test_c7_tasks_command_points_at_the_baseline_owner_without_copying_it():
    text = TASKS_CMD.read_text(encoding="utf-8")
    assert BASELINE_POINTER in text, (
        "tasks.md must point at implement.md's `**Test runs**` bullet, the owner "
        "of the failing-test baseline path"
    )
    assert BASELINE_OWNER_CMD in text, "the pointer must name the owner file"
    assert BASELINE_PATH_LITERAL not in text, (
        "tasks.md restated the baseline path literal — that is a second copy of a "
        "fact owned by implement.md and will drift from it"
    )


def test_c8_tasks_command_pins_the_notes_landing_points_and_refreeze_timing():
    text = TASKS_CMD.read_text(encoding="utf-8")
    for point in NOTES_LANDING_POINTS:
        assert point in text, f"tasks.md lost the fixed evidence landing point {point!r}"
    assert REFREEZE_LITERAL in text, (
        "tasks.md must state when a frozen measurement is re-captured, otherwise "
        "the landing point is written once and cited stale forever"
    )


def test_c9_plan_surfaces_carry_the_run_and_paste_duty_once():
    """Owner/placement split: plan.md owns the duty, the template specializes it."""
    cmd = PLAN_CMD.read_text(encoding="utf-8")
    tpl = PLAN_TPL.read_text(encoding="utf-8")

    assert EXEC_VERIFY_SCOPE in cmd, (
        "execution-verify must cover every artifact this command produces, not a "
        "named subset — an unlisted artifact is where an unrun command survives"
    )
    assert TEARDOWN_DUTY in cmd, "teardown must be verified to the same standard as setup"
    assert DISCLAIMER_PREMISES in cmd, (
        "a per-example disclaimer must also list the premises the example rests on, "
        "so the next phase knows what to re-probe"
    )

    assert TPL_RUN_AND_PASTE in tpl, "the backfill note lost the run-and-paste duty"
    assert TPL_REGEX_SCOPE in tpl, (
        "the backfill note must require a pattern-derived count to declare whether "
        "the pattern can also match non-target lines"
    )
    assert TPL_OWNER_POINTER in tpl, (
        "the template must reach plan.md's execution-verify rule by pointer rather "
        "than restate it"
    )
    assert cmd.count(TEARDOWN_DUTY) == 1 and tpl.count(TEARDOWN_DUTY) == 0, (
        "the teardown duty must live in exactly one place — plan.md"
    )


def test_c10_tasks_premise_command_must_actually_run():
    text = TASKS_CMD.read_text(encoding="utf-8")
    assert "MUST be actually run at generation time" in text, (
        "the premise re-derivation command must be executed at generation time "
        "with its real output pasted — a printed command is a claim, not a measurement"
    )
    assert "write the trap form down too" in text, (
        "when a more naive measurement form would give a different answer, the trap "
        "form must be written down alongside it"
    )
