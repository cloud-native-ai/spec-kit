"""Contract test: template neutrality, gate-budget neutrality, and no new machinery.

Pins all 19 clauses of ``contracts/neutrality-budget.md``. This is the suite that guards
what the feature must NOT do, so almost every assertion here is a negative proposition —
and a negative proposition is only evidence if it can go red. Each test therefore carries
either a positive control (the same probe run against something that MUST hit) or a
sentinel proving the probe scanned a non-empty population. Without that, "zero hits" is
indistinguishable from "the grep never ran", which is the exact blindness FR-040 exists to
prevent.

The gate-budget half has an integer headroom of ZERO: the cap is
``baseline["total"] * 0.25`` = 93 * 0.25 = 23.25 and the total is 23, so one added blocking
phrase anywhere in the scanned surface puts the repository over cap with no room to negotiate.
That is why C-7's only legal route is wording design, and why this suite checks the wording
of every file the feature landed inside that surface.
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
SCRIPTS = ROOT / "scripts" / "python"
SCANNER = SCRIPTS / "scan-confirmation-gates.py"
SPEC = ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts"

# The window anchor GATE-6 requires be named explicitly, recorded at implement start in
# notes/pre-change-measurements.md § 1 — an unanchored window is how 052's GATE-3 went void.
BASE_SHA = "ad190d46de960efd70e61a4719a16561a89b7e9d"

GATE_TOTAL = 23
GATE_VIOLATIONS = 0
CAP_BASELINE_TOTAL = 93
CAP_FACTOR = 0.25
BLOCKING_PATTERN_COUNT = 17

# C-2: the feature's landing points under templates/, asserted per file, never merged.
TEMPLATE_LANDING_POINTS = (
    ROOT / "templates" / "tasks-template.md",
    ROOT / "templates" / "commands" / "requirements.md",
    ROOT / "templates" / "commands" / "tasks.md",
)

REPO_PROPER_NAMES = re.compile(r"spec-kit|specify-cli|specify_cli|cloud-native-ai",
                               re.IGNORECASE)

# C-8: every path this feature wrote that sits inside the scanned surface.
SCANNED_LANDING_POINTS = (
    "shared/definitions/contract-clause-definitions.md",
    "shared/definitions/goal-definitions.md",
    "shared/guidelines/requirements-guidelines.md",
    "shared/constants/clarify-taxonomy.md",
    "templates/tasks-template.md",
    "templates/commands/requirements.md",
    "templates/commands/tasks.md",
)

# C-3: real artifacts a contract or script may name as an example — in specs/ or scripts/
# comments, never in templates/, which ships to every consuming project.
# SPECIFIC real artifacts. The bare path prefix `.specify/specs/` is deliberately absent:
# templates legitimately carry it as a path CONVENTION (four of them do), and a convention
# is not an example naming this repository's own spec — measured, and narrowing the needle
# is what keeps this a neutrality check rather than a false positive generator.
REAL_ARTIFACT_EXAMPLES = (
    "013-portable-skill-creation",
    "031-task-complexity-rubric",
    "053-machine-decidable-artifacts",
    "050-proactive-flow-trigger",
    "044-reduce-confirmation-flows",
)

NEW_SCRIPTS = (
    "validate-requirements.py",
    "clause_extract.py",
    "account-clause-coverage.py",
)


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scg_under_test", SCANNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _summary():
    r = subprocess.run([sys.executable, str(SCANNER), "--summary"],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    total = int(re.search(r"blocking confirmation gates:\s*(\d+)", r.stdout).group(1))
    violations = int(re.search(r"violations[^:]*:\s*(\d+)", r.stdout).group(1))
    return total, violations, r.stdout


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=str(ROOT))


def _window_diff(*paths) -> str:
    return _git("diff", f"{BASE_SHA}..HEAD", "--", *paths).stdout


# =========================================================================== #
# C-1 … C-3 — template neutrality
# =========================================================================== #


@pytest.mark.parametrize("path", TEMPLATE_LANDING_POINTS,
                         ids=lambda p: p.relative_to(ROOT).as_posix())
def test_c1_c2_each_template_landing_point_is_project_neutral(path):
    """Per file, not as a merged count (C-2): a merged 0 hides which file leaked."""
    assert path.is_file(), f"sentinel: the landing point moved: {path}"
    hits = [(i, l.strip()[:90]) for i, l in
            enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if REPO_PROPER_NAMES.search(l)]
    assert hits == [], (
        f"{path.relative_to(ROOT)} ships to every consuming project, so a repository proper "
        f"name in it leaks this project into other people's specs: {hits}"
    )
    # positive control: the probe does fire on a name it should find
    assert REPO_PROPER_NAMES.search("distributed as specify-cli from spec-kit"), (
        "sentinel: the proper-name probe matches nothing, so the zero above proves nothing"
    )


def test_c3_no_real_artifact_is_named_as_an_example_in_templates():
    offenders = []
    for path in sorted((ROOT / "templates").rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in REAL_ARTIFACT_EXAMPLES:
            if needle in text:
                offenders.append(f"{path.relative_to(ROOT)}: {needle}")
    assert offenders == [], (
        f"templates are factory-shipped, so an example naming this repository's own spec "
        f"directory is unresolvable in any consuming project: {offenders}"
    )
    # the same examples ARE legitimate in the spec's own contracts — that is the contrast
    contract = (SPEC / "contracts" / "clause-coverage.md").read_text(encoding="utf-8")
    assert "013-portable-skill-creation" in contract, (
        "sentinel: the misnomer example moved out of the contract too, so this test no "
        "longer separates the two locations"
    )


# =========================================================================== #
# C-4 … C-11 — the gate budget, whose integer headroom is zero
# =========================================================================== #


def test_c4_budget_total_and_violations_after_the_feature_landed():
    total, violations, out = _summary()
    assert total == GATE_TOTAL, (
        f"the feature changed the blocking-gate total from {GATE_TOTAL} to {total}; the "
        f"integer headroom is zero so this is a violation, not a rounding: {out}"
    )
    assert violations == GATE_VIOLATIONS, out


def test_c5_the_cap_leaves_zero_integer_headroom():
    baseline = json.loads(
        (ROOT / ".specify" / "specs" / "044-reduce-confirmation-flows" / "baseline.json")
        .read_text(encoding="utf-8"))
    assert baseline["total"] == CAP_BASELINE_TOTAL, (
        f"the cap's frozen baseline moved; the derived cap and every pin keyed on it must be "
        f"re-derived together, not adjusted to fit: {baseline['total']}"
    )
    cap = baseline["total"] * CAP_FACTOR
    assert cap == 23.25, cap
    total, _violations, _out = _summary()
    assert total <= cap, f"over cap: {total} > {cap}"
    assert int(cap) == total, (
        f"headroom is zero: total {total} already equals floor(cap {cap}), so one added "
        "blocking phrase anywhere in the scanned surface puts the repository over cap"
    )


def test_c6_the_cap_is_pinned_in_three_forms_with_meta_pins_over_them():
    ufc = (ROOT / "tests" / "contract" / "test_user_facing_comprehension_doc.py").read_text(
        encoding="utf-8")
    trigger = (ROOT / "tests" / "contract" / "test_proactive_trigger_section.py").read_text(
        encoding="utf-8")
    sweep = (ROOT / "tests" / "contract" / "test_confirmation_gates_sweep.py").read_text(
        encoding="utf-8")
    assert 'payload["total"] == 23' in ufc, "form ① the hardcoded literal pin is gone"
    assert 'payload["total"] == frozen["total"]' in trigger, (
        "form ② the equality-with-frozen-baseline pin is gone"
    )
    assert 'baseline["total"] * 0.25' in sweep, "form ③ the derived-cap pin is gone"

    # The meta-pins regex-match the three sites' SOURCE TEXT, so rewording a pin without
    # rewording its meta-pin turns a meta-pin red. Asserted as the four literal needles.
    fast_fail = (ROOT / "tests" / "contract" / "test_fast_fail_discipline.py").read_text(
        encoding="utf-8")
    meta_needles = (
        r"""re.search(r'payload\["total"\] == 23'""",
        r"""re.search(r'payload\["total"\] == frozen\["total"\]'""",
        r"""re.search(r'payload\["total"\] <= cap'""",
        r"""re.search(r'baseline\["total"\] \* 0\.25'""",
    )
    found = [n for n in meta_needles if n in fast_fail]
    assert len(found) == len(meta_needles) == 4, (
        f"expected the four meta-pins over the three cap sites, found {len(found)}: {found}"
    )


def test_c7_the_only_legal_route_is_wording_not_relaxation():
    """MUST NOT widen the scanned set, raise the cap, edit a baseline, or reword a pin."""
    for path in ("scripts/python/scan-confirmation-gates.py",
                 ".specify/specs/044-reduce-confirmation-flows/baseline.json",
                 ".specify/specs/050-proactive-flow-trigger/baseline-gates.json",
                 "tests/contract/test_user_facing_comprehension_doc.py",
                 "tests/contract/test_proactive_trigger_section.py",
                 "tests/contract/test_confirmation_gates_sweep.py"):
        diff = _window_diff(path)
        assert diff == "", (
            f"{path} changed inside this feature's window; the budget may only be met by "
            f"designing wording that does not match a blocking pattern:\n{diff[:600]}"
        )


def test_c8_the_scanned_surface_reaches_every_landing_point_and_skips_the_spec_dir():
    mod = _load_scanner()
    assert tuple(mod.SCAN_DIRS) == ("templates/commands", "skills", "shared"), mod.SCAN_DIRS
    assert tuple(mod.SCAN_ROOT_FILES) == ("templates",), mod.SCAN_ROOT_FILES
    assert ".specify" in mod.SKIP_DIR_PARTS, (
        "the spec directory must stay outside the surface, or this feature's own contracts "
        "would consume the budget they are measuring"
    )
    for rel in SCANNED_LANDING_POINTS:
        path = ROOT / rel
        assert path.is_file(), f"sentinel: a landing point is gone: {rel}"
        covered = any(rel.startswith(d.rstrip("/") + "/") or rel.startswith(d)
                      for d in mod.SCAN_DIRS) or rel in ("templates/tasks-template.md",)
        assert covered, f"{rel} was assumed to be inside the scanned surface but is not"
    assert not any(str(SPEC.relative_to(ROOT)).startswith(d) for d in mod.SCAN_DIRS)


def test_c9_c11_every_landed_file_in_the_surface_has_zero_blocking_hits():
    """C-9 guards the budget and C-11 guards 'no new stop-and-wait'; one measurement, two
    propositions, so both are asserted here rather than one being implied by the other."""
    mod = _load_scanner()
    assert len(mod.BLOCKING_PATTERNS) == BLOCKING_PATTERN_COUNT, (
        f"the pattern count moved from {BLOCKING_PATTERN_COUNT}; C-9 records that this "
        "number was wrong twice in this repository's own artifacts, so it is pinned"
    )
    scanned, offenders = 0, []
    for rel in SCANNED_LANDING_POINTS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        scanned += 1
        for lineno, line in enumerate(text.splitlines(), 1):
            if mod.BLOCKING_RE.search(line):
                offenders.append(f"{rel}:{lineno}: {line.strip()[:80]}")
    assert scanned == len(SCANNED_LANDING_POINTS) and scanned > 0
    assert offenders == [], (
        f"wording inside the scanned surface matches a blocking pattern, which adds a "
        f"stop-and-wait gate the budget has no room for: {offenders}"
    )
    # positive control: the probe fires on phrasing that really is a blocking gate
    assert mod.BLOCKING_RE.search("wait for user confirmation before writing"), (
        "sentinel: BLOCKING_RE matches nothing, so the zeros above prove nothing"
    )


def test_c10_the_scanner_and_its_mirror_are_untouched_in_the_window():
    assert _window_diff("scripts/python/scan-confirmation-gates.py") == ""
    assert _window_diff(".specify/scripts/python/scan-confirmation-gates.py") == ""
    # sentinel: the window anchor itself must resolve, or an empty diff means nothing
    assert _git("cat-file", "-e", BASE_SHA).returncode == 0, (
        f"the recorded BASE SHA does not exist, so every window diff above is vacuous"
    )
    assert _git("diff", "--stat", f"{BASE_SHA}..HEAD").stdout, (
        "sentinel: the window contains no commits at all, so 'unchanged' is trivially true"
    )


# =========================================================================== #
# C-12 … C-15 — no new machinery
# =========================================================================== #


def test_c12_the_status_state_machine_is_untouched():
    for path in ("shared/workflow/feature-integration.md",
                 "templates/feature-details-template.md"):
        diff = _window_diff(path)
        assert diff == "", (
            f"{path} owns a status state machine and changed inside this feature's window; "
            f"the feature adds checkers, not lifecycle states:\n{diff[:600]}"
        )
    text = (ROOT / "shared" / "workflow" / "feature-integration.md").read_text(encoding="utf-8")
    assert "Status State Machine" in text or "状态机" in text, (
        "sentinel: the state-machine section this clause protects is not where it was"
    )


def test_c13_no_new_script_daemonizes_or_polls():
    patterns = re.compile(r"watchdog|inotify|while\s+True\s*:|time\.sleep\(", re.IGNORECASE)
    for name in NEW_SCRIPTS:
        path = SCRIPTS / name
        assert path.is_file(), f"sentinel: a new script is missing: {name}"
        src = path.read_text(encoding="utf-8")
        hits = [l.strip()[:80] for l in src.splitlines() if patterns.search(l)]
        assert hits == [], f"{name} is not a one-call/one-output/exit tool: {hits}"
        # and it really is callable as one shot with an exit code
        mod_spec = importlib.util.spec_from_file_location("_ns_" + name, path)
        mod = importlib.util.module_from_spec(mod_spec)
        sys.modules[mod_spec.name] = mod
        mod_spec.loader.exec_module(mod)
        assert callable(getattr(mod, "main", None)), f"{name} has no single entry point"


def test_c14_the_two_channel_trigger_set_is_closed_and_ci_is_not_available():
    assert not (ROOT / ".github" / "workflows").exists(), (
        "a CI configuration appeared; CI is not one of the two channels a checker may be "
        "triggered through, so wiring one in would be an unrequested automatic surface"
    )
    for name in NEW_SCRIPTS:
        in_a_command = bool(subprocess.run(
            ["grep", "-rl", name, str(ROOT / "templates" / "commands")],
            capture_output=True, text=True).stdout.strip())
        in_a_test = bool(subprocess.run(
            ["grep", "-rl", name, str(ROOT / "tests")],
            capture_output=True, text=True).stdout.strip())
        assert in_a_command or in_a_test, (
            f"{name} is reachable through neither channel, so nothing would ever run it — "
            "a checker nobody calls is a claim, not a guard"
        )


def test_c15_the_wiring_lands_inside_existing_steps_not_a_new_phase():
    req = (ROOT / "templates" / "commands" / "requirements.md").read_text(encoding="utf-8")
    assert "validate-requirements.py" in req, (
        "FR-012's wiring must be present in the requirements command"
    )
    # it must sit inside the existing numbered validation step, not in a step of its own
    steps = re.findall(r"(?m)^(\d+)\.\s+\*\*(.+?)\*\*", req)
    assert steps, "sentinel: the command's numbered steps were not found"
    hosting = [n for n, heading in steps
               if n and _step_body(req, n).find("validate-requirements.py") >= 0]
    assert len(hosting) == 1, (
        f"the invocation must live in exactly one existing step, found in {hosting}"
    )
    tasks = (ROOT / "templates" / "commands" / "tasks.md").read_text(encoding="utf-8")
    assert "validate-tasks.py" in tasks, "US2 reuses the existing structural-validation step"


def _step_body(text: str, number: str) -> str:
    """The text of one numbered step, up to the next numbered step at the same indent."""
    start = re.search(rf"(?m)^{number}\.\s+", text)
    if not start:
        return ""
    nxt = re.search(rf"(?m)^\d+\.\s+\*\*", text[start.end():])
    return text[start.start():start.end() + (nxt.start() if nxt else len(text))]


# =========================================================================== #
# C-16 … C-19 — the three name-level baselines
# =========================================================================== #


def test_c16_the_test_baseline_is_a_sorted_name_list_in_the_spec_dir():
    baseline = SPEC / "baseline-failed.txt"
    assert baseline.is_file(), f"the frozen name-level baseline is missing: {baseline}"
    names = [l.strip() for l in baseline.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(names) >= 1, "sentinel: an empty baseline makes any comparison vacuous"
    assert names == sorted(names), "the list must be sorted so `comm -13` can consume it"
    assert all("::" in n for n in names), (
        f"every entry must be a test NAME, not a count: {names[:3]}"
    )
    runner = (ROOT / "scripts" / "bash" / "run-tests.sh").read_text(encoding="utf-8")
    assert "--names-out" in runner, "the capture flag this baseline was taken with is gone"


def test_c17_the_runner_does_not_store_a_baseline_or_run_comm_itself():
    runner = (ROOT / "scripts" / "bash" / "run-tests.sh").read_text(encoding="utf-8")
    executing = [l for l in runner.splitlines()
                 if "comm -13" in l and not l.lstrip().startswith("#")]
    assert executing == [], (
        f"run-tests.sh must not run the comparison itself — `comm -13` is the documented "
        f"consumer idiom, so each of this feature's three baselines is compared by its own "
        f"gate: {executing}"
    )
    assert any("comm -13" in l and l.lstrip().startswith("#")
               for l in runner.splitlines()), (
        "sentinel: the runner no longer documents the idiom either, so this test measured "
        "nothing"
    )


def test_c18_all_three_baselines_are_compared_by_name_set_not_by_count():
    tasks = (SPEC / "tasks.md").read_text(encoding="utf-8")
    gates = re.findall(r"(?m)^- (GATE-\d+): (.*)$", tasks)
    assert len(gates) >= 8, f"sentinel: the completion gate section moved: {len(gates)}"
    comparing = {name for name, body in gates if "comm -13" in body}
    assert {"GATE-1", "GATE-8"} <= comparing, (
        f"the test-name baseline and the coverage baseline must each be compared with a set "
        f"difference; found comm -13 only in {sorted(comparing)}"
    )
    for name, body in gates:
        if name in ("GATE-1", "GATE-8"):
            assert not re.search(r"==\s*\d+\s*$", body.strip()), (
                f"{name} reduced its criterion to an integer equality: {body[:120]}"
            )
    assert (SPEC / "coverage-baseline.txt").is_file(), (
        "the third baseline (uncovered clause names) must be landed, not only described"
    )


def test_c19_the_baseline_was_refrozen_not_inherited_from_the_contract_row():
    baseline = SPEC / "baseline-failed.txt"
    digest = hashlib.md5(baseline.read_bytes()).hexdigest()
    recorded = (SPEC / "notes" / "pre-change-measurements.md").read_text(encoding="utf-8")
    assert digest in recorded, (
        f"the frozen baseline's md5 {digest} is not recorded in pre-change-measurements.md, "
        "so the file and its capture record have drifted apart"
    )
    assert digest == "02177c0e6e5961c880f73d932007df92", (
        "C-19 records this md5 as the pre-change reference — the same 65 pre-existing "
        "failures 052 froze. A different digest means either the tree moved or the baseline "
        "was re-taken without re-recording it; both need a human look, not a silent accept."
    )
    names = [l.strip() for l in baseline.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(names) == 65, f"the frozen set holds {len(names)} names, expected 65"


def test_the_contract_still_has_the_clause_count_this_suite_pins():
    body = (SPEC / "contracts" / "neutrality-budget.md").read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", body)
    assert len(ids) == 19, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 20)), "clause ids are not contiguous"
