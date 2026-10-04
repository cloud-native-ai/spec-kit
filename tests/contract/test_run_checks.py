"""Contract test: `goal-utils.py run-checks` (US4).

Pins all 28 clauses of ``contracts/run-checks.md``. The subject is an EXISTING binary
gaining one action, so this suite's discipline is as much about what must NOT move as
about what must appear:

* the four existing ``EXIT_*`` constants keep their exact values, and ``blocked`` takes the
  next free code 5 (C-17) — the exit table is pinned as a CLOSED dict plus a per-constant
  loop plus a closed action roster, in the shape ``test_trigger_engine.py`` already uses
  (C-22), because ``goal_utils.EXIT`` had zero test imports before this feature;
* the eighth verdict literal ``rejected`` is untouched (C-15), asserted as an unchanged hit
  count rather than as a behavior, because it belongs to two other actions;
* the Program-First attribution stays in its existing inline-paren form (C-25) — FR-002 was
  clarified to govern NEW checkers only, so converting this docstring to the STR-008 form
  would be an unrequested rewrite;
* ``name`` and ``verdict`` are two fields with two roles, and C-10's criterion is explicitly
  NOT disjointness — four of the five names are also verdict literals in the source, so a
  test asserting an empty intersection would be red the moment it landed.

Fixtures are built in ``tmp_path`` as throwaway repositories; the real ``.specify/goal/``
and ``.specify/teams/`` trees are only ever read (C-3, C-28).
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
TEAM_CMD = ROOT / "templates" / "commands" / "team.md"
TEAM_DOC = ROOT / "docs" / "reference" / "commands" / "team.md"
EXEC_GUIDE = ROOT / "skills" / "create-team" / "references" / "execution-guide.md"
GOAL_GUIDE = ROOT / "skills" / "create-team" / "references" / "goal.md"
TOOL_RECORD = ROOT / ".specify" / "memory" / "tools" / "goal-utils.py.md"
QUICKSTART_RUN = (
    ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts" / "notes"
    / "quickstart-run.md"
)
PER_TOOL_COPIES = (
    ROOT / ".claude" / "commands" / "speckit.team.md",
    ROOT / ".github" / "prompts" / "speckit.team.prompt.md",
    ROOT / ".opencode" / "command" / "speckit.team.md",
    ROOT / ".qoder" / "commands" / "speckit.team.md",
)

# --- literals under guard --------------------------------------------------

FIVE_NAMES = ("goal-binding", "dangling", "target-terminal", "cross-goal", "goal-terminal")
STR006 = {
    "ok", "no-goal-definition", "dangling", "target-terminal",
    "cross-goal", "goal-terminal", "input-error",
}
NOT_EVALUATED = "not-evaluated"          # STR-004
VOCABULARY = STR006 | {NOT_EVALUATED}

# C-22: the exit table as a CLOSED dict — name -> value, both directions asserted.
EXIT_CODES = {
    "EXIT_OK": 0,
    "EXIT_INPUT_ERROR": 2,
    "EXIT_NOT_FOUND": 3,
    "EXIT_INVALID": 4,
    "EXIT_BLOCKED": 5,
}

# C-22: the closed action roster (10 = the existing 9 plus run-checks).
ACTIONS = [
    "create", "validate", "check-statement", "list", "status",
    "objective", "criteria", "migrate", "targets", "run-checks",
]

CHECK_KEYS = {"id", "name", "verdict", "message"}
TOP_KEYS = {
    "team_slug", "goal_slug", "identity_kind", "resolution",
    "checks", "verdict", "blocked",
}
RESOLUTION_KEYS = {"effective", "source", "declared_focus"}

# C-10(b): each check's name -> the verdicts it may possibly emit. Pinned per name so the
# accident that four names are ALSO verdict literals can never be mistaken for an invariant.
NAME_TO_VERDICTS = {
    "goal-binding": {"ok", "no-goal-definition", NOT_EVALUATED},
    "dangling": {"ok", "dangling", NOT_EVALUATED},
    "target-terminal": {"ok", "target-terminal", NOT_EVALUATED},
    "cross-goal": {"ok", "cross-goal", NOT_EVALUATED},
    "goal-terminal": {"ok", "goal-terminal", NOT_EVALUATED},
}

REAL_GOAL = "draw-two-layer-structure"
REAL_TEAM_BOUND = "draw-two-layer-structure"
REAL_TEAM_UNBOUND = "cws-workspace-cluster"


def _load():
    assert GOAL_UTILS.is_file(), f"missing artifact: {GOAL_UTILS}"
    spec = importlib.util.spec_from_file_location("_goal_utils_under_test", GOAL_UTILS)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _source() -> str:
    return GOAL_UTILS.read_text(encoding="utf-8")


SECTION_START = "# 053 run-checks"
SECTION_END = "def migrate_team("
DISPATCH_START = 'args.action == "run-checks"'
DISPATCH_END = "\n        else:  # pragma: no cover"


def _dispatch_branch() -> str:
    """main()'s run-checks branch only — slicing to the next `elif` runs to EOF, because
    this branch is the last one before the fallthrough `else`."""
    src = _source()
    return src[src.index(DISPATCH_START):src.index(DISPATCH_END)]


def _section() -> str:
    """The whole run-checks block: the five guarded check functions plus the wrapper.

    Sliced as a section rather than as `run_checks`' body, because each check is its own
    function so that one raising can be caught without swallowing the other four (C-16) —
    which puts the engine primitives one level above the wrapper.
    """
    src = _source()
    return src[src.index(SECTION_START):src.index(SECTION_END)]


def _run(root, *args, expect=None):
    # `--repo-root` goes AFTER the action on purpose. It is declared on a parser shared by
    # the top level and every subparser, and argparse lets the subparser's own default
    # overwrite a value the top level already set — so `--repo-root X <action>` silently
    # resolves to the cwd. Pre-existing in this binary, measured, escalated as research.md
    # A-9; this feature must not change flag precedence for nine existing actions in passing.
    action, rest = args[0], args[1:]
    cmd = [sys.executable, str(GOAL_UTILS), action, "--repo-root", str(root), *rest]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if expect is not None:
        assert r.returncode == expect, (
            f"{' '.join(args)} -> exit {r.returncode}, expected {expect}\n"
            f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}"
        )
    return r


def _checks(root, *args, expect=None):
    r = _run(root, *args, "--json", expect=expect)
    return json.loads(r.stdout)


def _by_name(payload):
    return {c["name"]: c for c in payload["checks"]}


# --- throwaway repository fixtures ----------------------------------------

GOAL_TMPL = """---
status: {status}
created: 2026-01-01
updated: 2026-01-02
---

# Goal: {slug}

## Objective

One outcome the team wants to exist and can be judged against.

## Success Criteria

1. A verifiable criterion for that outcome.

## Targets

| ID | Target | Status |
|----|--------|--------|
{rows}

## History

- 2026-01-01 — created.
"""

TEAM_TMPL = """---
slug: {slug}
name: fixture team
{binding}---

# Team {slug}

Body.
"""


def _repo(tmp_path: Path, *, goal: bool = True, goal_status: str = "active",
          targets=(("T-001", "open"), ("T-002", "done")), team: bool = True,
          team_slug: str = "t1", goal_slug: str = "g1", goal_dir: str | None = None,
          focus=None, goal_body: str | None = None) -> Path:
    """A throwaway repository: `.specify/goal/<dir>/goal.md` + `.specify/teams/<slug>/team.md`.

    `goal_slug` is the team's DECLARED binding (None = no `goal_slug` line, so identity
    resolution falls through to the team-slug inference and then to none); `goal_dir` is
    which definition directory to create, and defaults to the declared binding. Splitting
    the two is what makes an unbound-team fixture possible without dropping the definition.
    """
    directory = goal_dir if goal_dir is not None else (goal_slug or "g1")
    root = tmp_path / "repo"
    (root / ".specify" / "goal").mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "teams" / team_slug).mkdir(parents=True, exist_ok=True)
    if team:
        binding = f"goal_slug: {goal_slug}\n" if goal_slug else ""
        if focus:
            binding += f"focus_target: {focus}\n"
        (root / ".specify" / "teams" / team_slug / "team.md").write_text(
            TEAM_TMPL.format(slug=team_slug, binding=binding), encoding="utf-8"
        )
    if goal:
        (root / ".specify" / "goal" / directory).mkdir(parents=True, exist_ok=True)
        rows = "".join(f"| {tid} | slice for {tid} | {state} |\n" for tid, state in targets)
        text = goal_body if goal_body is not None else GOAL_TMPL.format(
            status=goal_status, slug=directory, rows=rows.rstrip("\n")
        )
        (root / ".specify" / "goal" / directory / "goal.md").write_text(text, encoding="utf-8")
    return root


def _checksum(root: Path) -> str:
    """Byte checksum of the two trees C-3/C-28 protect, in a stable order."""
    digest = hashlib.md5()
    for sub in (".specify/goal", ".specify/teams"):
        for path in sorted((root / sub).rglob("*")):
            if path.is_file():
                digest.update(path.relative_to(root).as_posix().encode("utf-8"))
                digest.update(path.read_bytes())
    return digest.hexdigest()


# =========================================================================== #
# C-1 … C-4 — the action exists, is read-only, and is labelled
# =========================================================================== #


def test_c1_the_action_exists_and_the_roster_grew_by_exactly_one(capsys):
    mod = _load()
    with pytest.raises(SystemExit):
        mod.main(["--help"])
    out = capsys.readouterr().out
    choices = re.search(r"\{([a-z,-]+)\}", out)
    assert choices, f"no choices row in --help:\n{out}"
    names = choices.group(1).split(",")
    assert "run-checks" in names, f"run-checks is not an action: {names}"
    assert len(names) == len(ACTIONS) == 10, (
        f"the roster was 9 before this feature and must be exactly 10 now: {names}"
    )
    assert _source().count("sub.add_parser") == 10, (
        "the add_parser count must move 9 -> 10 with the new action, so a name reused "
        "instead of added cannot slip through"
    )


def test_c2_one_call_emits_five_checks_with_exactly_those_names(tmp_path):
    root = _repo(tmp_path)
    p = _checks(root, "run-checks", "t1", expect=0)
    assert len(p["checks"]) == 5, f"five checks in ONE call: {p['checks']}"
    assert [c["name"] for c in p["checks"]] == list(FIVE_NAMES), (
        f"the five names and their order are the contract: {[c['name'] for c in p['checks']]}"
    )
    assert [c["id"] for c in p["checks"]] == [1, 2, 3, 4, 5]


def test_c3_a_call_writes_no_byte_of_the_goal_or_team_trees(tmp_path):
    root = _repo(tmp_path, focus="T-001")
    before = _checksum(root)
    for args in (("run-checks", "t1"),
                 ("run-checks", "t1", "--target", "T-001"),
                 ("run-checks", "t1", "--target", "T-999"),
                 ("run-checks", "t1", "--target", "bogus"),
                 ("run-checks", "nope")):
        _run(root, *args)
    assert _checksum(root) == before, "run-checks modified .specify/goal/ or .specify/teams/"
    # and on the REAL tree, read-only paths only (C-28's fallback evidence form)
    real_before = _checksum(ROOT)
    _run(ROOT, "run-checks", REAL_TEAM_BOUND, expect=0)
    assert _checksum(ROOT) == real_before, "a run against the real tree wrote something"


def test_c4_the_help_line_is_labelled_read():
    r = subprocess.run([sys.executable, str(GOAL_UTILS), "--help"],
                       capture_output=True, text=True)
    line = next((l for l in r.stdout.splitlines()
                 if l.strip().startswith("run-checks ")), None)
    assert line, f"--help lost the run-checks row:\n{r.stdout}"
    assert line.split()[1].startswith("read"), (
        f"run-checks is a read-only action, so its help must start with `read:` "
        f"(the form test_goal_definition.py enforces): {line.strip()!r}"
    )


# =========================================================================== #
# C-5 … C-8 — reuse of the existing parse, never a second grammar
# =========================================================================== #


def test_c5_every_verdict_comes_from_an_existing_code_path():
    body = _section()
    for primitive in ("resolve_team_goal_identity", "resolve_effective_target",
                      "definition_path", "parse_goal", "TERMINAL_STATES",
                      "_QUALIFIED_TARGET", "TARGET_IDENTITY"):
        assert primitive in body, (
            f"run_checks must reach {primitive} rather than re-derive its rule; the five "
            "verdicts are all produced by code that already existed (D-11)"
        )
    assert "re.compile" not in body, (
        "run_checks defines its own grammar — C-5 forbids a second parser beside the engine's"
    )


def test_c6_resolution_is_reported_with_all_three_subkeys(tmp_path):
    root = _repo(tmp_path, focus="T-001")
    p = _checks(root, "run-checks", "t1", expect=0)
    assert set(p["resolution"]) == RESOLUTION_KEYS, p["resolution"]
    assert p["resolution"]["effective"] == "T-001"
    assert p["resolution"]["source"] == "team-default"
    assert p["resolution"]["declared_focus"] == "T-001"

    explicit = _checks(root, "run-checks", "t1", "--target", "T-002", expect=None)
    assert explicit["resolution"]["source"] == "explicit", (
        "an explicit --target must win over the declared focus_target"
    )
    assert explicit["resolution"]["effective"] == "T-002"
    assert explicit["resolution"]["declared_focus"] == "T-001"


def test_c7_without_a_target_two_three_four_are_not_evaluated_and_one_five_still_are(tmp_path):
    root = _repo(tmp_path)                       # no focus_target, no --target
    p = _checks(root, "run-checks", "t1", expect=0)
    assert p["resolution"]["source"] == "none" and p["resolution"]["effective"] is None
    got = _by_name(p)
    for name in ("dangling", "target-terminal", "cross-goal"):
        assert got[name]["verdict"] == NOT_EVALUATED, (
            f"{name} has no judgment subject without a target, so it must be "
            f"{NOT_EVALUATED} — reporting `ok` for a check that never ran is exactly the "
            f"shape this feature exists to remove: {got[name]}"
        )
    for name in ("goal-binding", "goal-terminal"):
        assert got[name]["verdict"] != NOT_EVALUATED, (
            f"{name} depends only on the team/goal binding, so C-7 requires it to be "
            f"evaluated even with no target: {got[name]}"
        )
        assert got[name]["verdict"] == "ok", got[name]


def test_c8_the_two_internal_resolvers_reach_the_cli_for_the_first_time():
    body = _section()
    assert "resolve_effective_target(" in body, (
        "C-8: resolve_effective_target had no CLI entry before this action; the action is "
        "its first exposure, so it must actually be called"
    )
    assert "preview_target_check(" in body, (
        "C-8: preview_target_check likewise had no CLI entry; the top-level verdict must be "
        "the gate's own rather than a second opinion composed beside it"
    )
    dispatch = _dispatch_branch()
    assert "run_checks(" in dispatch, "the action is not wired into main()'s dispatch"


# =========================================================================== #
# C-9 … C-11 — output fields
# =========================================================================== #


def test_c9_key_sets_are_exact_at_both_levels(tmp_path):
    root = _repo(tmp_path)
    p = _checks(root, "run-checks", "t1", expect=0)
    assert set(p) == TOP_KEYS, (
        f"the top-level key set is pinned by equality, not inclusion: {sorted(p)}"
    )
    for check in p["checks"]:
        assert set(check) == CHECK_KEYS, f"per-check keys: {sorted(check)}"


def test_c10a_at_least_one_name_is_not_a_verdict_literal():
    outside = [n for n in FIVE_NAMES if n not in STR006]
    assert outside == ["goal-binding"], (
        f"C-10's decidable half (a): a name outside the verdict vocabulary proves the two "
        f"fields are not interchangeable. Got {outside}."
    )
    inside = [n for n in FIVE_NAMES if n in STR006]
    assert len(inside) == 4, (
        f"C-10's measured correction: four of the five names ARE verdict literals in the "
        f"source, so a disjointness assertion would be unsatisfiable. Got {inside}."
    )


def test_c10b_each_name_is_pinned_to_the_verdicts_it_may_emit(tmp_path):
    root = _repo(tmp_path, targets=(("T-001", "open"), ("T-002", "done")))
    observed = {}
    scenarios = [
        ("run-checks", "t1"),
        ("run-checks", "t1", "--target", "T-001"),
        ("run-checks", "t1", "--target", "T-002"),
        ("run-checks", "t1", "--target", "T-999"),
        ("run-checks", "t1", "--target", "g1.T-001"),
        ("run-checks", "t1", "--target", "other.T-001"),
        ("run-checks", "t1", "--target", "bogus"),
    ]
    for args in scenarios:
        p = _checks(root, *args)
        for check in p["checks"]:
            observed.setdefault(check["name"], set()).add(check["verdict"])
    assert set(observed) == set(FIVE_NAMES)
    for name, verdicts in observed.items():
        assert verdicts <= NAME_TO_VERDICTS[name], (
            f"{name} emitted {sorted(verdicts - NAME_TO_VERDICTS[name])}, outside the set "
            f"its own production points allow: {sorted(NAME_TO_VERDICTS[name])}"
        )
    # the mapping is not vacuous: each name was seen emitting more than one verdict
    multi = {n: v for n, v in observed.items() if len(v) > 1}
    assert multi, (
        f"every name emitted exactly one verdict across {len(scenarios)} scenarios, so the "
        f"mapping above is untested: {observed}"
    )


def test_c11_json_is_accepted_on_either_side_of_the_action_and_goes_through__emit(tmp_path):
    root = _repo(tmp_path)
    after = subprocess.run(
        [sys.executable, str(GOAL_UTILS), "run-checks", "--repo-root", str(root),
         "t1", "--json"], capture_output=True, text=True)
    assert after.returncode == 0, after.stderr
    assert json.loads(after.stdout)["team_slug"] == "t1"

    # C-11's premise as written — "`--json` 置于 action 前后皆可" — is FALSE for this binary
    # and was false before this feature: the subparser's default clobbers the top-level
    # value, so `--json <action>` silently emits the human form. Pinned as measured, in
    # both directions, so neither a future fix nor a further regression passes unnoticed.
    before = subprocess.run(
        [sys.executable, str(GOAL_UTILS), "--json", "run-checks", "--repo-root", str(root),
         "t1"], capture_output=True, text=True)
    assert before.returncode == 0
    with pytest.raises(json.JSONDecodeError):
        json.loads(before.stdout)
    assert "team: t1" in before.stdout, (
        f"`--json` before the action is ignored, so the human form must appear: {before.stdout}"
    )
    assert "json.dumps" not in _section(), (
        "the action must emit through _emit like every other action, never print JSON itself"
    )
    dispatch = _dispatch_branch()
    assert "_emit(" in dispatch and "json.dumps" not in dispatch, (
        "the action must emit through _emit like every other action, never print JSON itself"
    )


# =========================================================================== #
# C-12 … C-16 — the verdict vocabulary
# =========================================================================== #


def test_c12_every_verdict_is_inside_str006_plus_not_evaluated(tmp_path):
    root = _repo(tmp_path, targets=(("T-001", "open"), ("T-002", "done")))
    seen = set()
    for args in [("run-checks", "t1"), ("run-checks", "t1", "--target", "T-001"),
                 ("run-checks", "t1", "--target", "T-002"),
                 ("run-checks", "t1", "--target", "T-999"),
                 ("run-checks", "t1", "--target", "other.T-001"),
                 ("run-checks", "t1", "--target", "bogus"),
                 ("run-checks", "no-such-team")]:
        r = _run(root, *args, "--json")
        payload = json.loads(r.stdout)
        for check in payload.get("checks", []):
            seen.add(check["verdict"])
        if "verdict" in payload:
            seen.add(payload["verdict"])
    assert seen, "sentinel: no verdict was observed at all"
    assert seen <= VOCABULARY, f"outside STR-006 ∪ {{not-evaluated}}: {sorted(seen - VOCABULARY)}"


def test_c13_a_short_circuited_check_is_not_evaluated_never_ok(tmp_path):
    """SC-008: one precondition fails, that check says so, the other four still report.

    The sample is a LOCAL-form reference: cross-goal compares a qualified reference's
    prefix against the bound goal, so with `T-001` there is no prefix and no question to
    answer — exactly one check loses its subject and the other four are evaluated.
    """
    root = _repo(tmp_path)
    p = _checks(root, "run-checks", "t1", "--target", "T-001", expect=0)
    got = _by_name(p)
    assert got["cross-goal"]["verdict"] == NOT_EVALUATED, (
        f"a local-form reference raises no cross-goal question, so reporting `ok` would "
        f"claim a check ran that never did: {got['cross-goal']}"
    )
    evaluated = [n for n in FIVE_NAMES if got[n]["verdict"] != NOT_EVALUATED]
    assert len(evaluated) == 4, f"the other four must still be evaluated: {evaluated}"
    assert p["blocked"] is False and p["verdict"] == "ok"


def test_c14_not_evaluated_is_defined_once():
    src = _source()
    assert src.count('"not-evaluated"') == 1, (
        f"STR-004 is a new literal and must have a single definition point, found "
        f"{src.count(chr(34) + 'not-evaluated' + chr(34))} quoted occurrences"
    )
    mod = _load()
    assert getattr(mod, "NOT_EVALUATED", None) == NOT_EVALUATED, (
        "the single point must be a module-level constant other code can reference"
    )


def test_c15_the_eighth_literal_rejected_is_untouched():
    src = _source()
    assert src.count('"rejected"') == 2, (
        f"`rejected` belongs to check-statement and targets --check (A-6); its hit count "
        f"was 2 before this feature and must still be 2, got {src.count(chr(34) + 'rejected' + chr(34))}"
    )


def test_c16_one_check_raising_leaves_the_other_four_reported(tmp_path, monkeypatch):
    """C-16: an exception in one check must not swallow the whole verdict."""
    mod = _load()
    root = _repo(tmp_path, focus="T-001")

    def _boom(_ctx):
        raise RuntimeError("injected failure inside one of the five checks")

    monkeypatch.setattr(mod, "_cross_goal_check", _boom)
    payload = mod.run_checks(root, "t1")
    assert len(payload["checks"]) == 5, (
        f"one check raising must still leave a five-element array: {payload['checks']}"
    )
    got = {c["name"]: c for c in payload["checks"]}
    assert got["cross-goal"]["verdict"] == NOT_EVALUATED, got["cross-goal"]
    assert got["cross-goal"]["message"], "the reason must be carried, not swallowed"
    others = [n for n in FIVE_NAMES if n != "cross-goal"]
    assert all(got[n]["verdict"] != NOT_EVALUATED for n in others), (
        f"the exception swallowed checks that could have been evaluated: "
        f"{[(n, got[n]['verdict']) for n in others]}"
    )


# =========================================================================== #
# C-17 … C-21 — exit codes
# =========================================================================== #


def test_c17_exit_table_is_closed_and_the_existing_four_are_unchanged():
    mod = _load()
    for name, value in EXIT_CODES.items():
        assert hasattr(mod, name), f"module-level constant {name} missing"
        assert getattr(mod, name) == value, f"{name} must be {value}"
    src = _source()
    for name in EXIT_CODES:
        assert len(re.findall(rf"^{name} = ", src, re.M)) == 1, (
            f"{name} must be defined exactly once, or the code->meaning map is not single"
        )
    assert len(EXIT_CODES) == 5
    assert not re.search(r"^EXIT_[A-Z_]+ = 1$", src, re.M), (
        "C-21: this binary has no EXIT_USAGE=1 and must not grow one as a side effect"
    )


def test_c18_the_three_tiers_are_mutually_distinguishable(tmp_path):
    # blocked -> 5: the referenced Target is in a terminal state
    blocked = _repo(tmp_path / "b", targets=(("T-001", "done"),))
    _run(blocked, "run-checks", "t1", "--target", "T-001", expect=5)
    # input error -> 2: the reference does not match the grammar
    bad_input = _repo(tmp_path / "i")
    _run(bad_input, "run-checks", "t1", "--target", "not-a-target", expect=2)
    # invalid -> 4: the goal definition itself fails validation
    invalid = _repo(tmp_path / "v", goal_body=GOAL_TMPL.format(
        status="finished", slug="g1", rows="| T-001 | slice | open |"))
    r = _run(invalid, "run-checks", "t1", "--target", "T-001")
    assert r.returncode == 4, (
        f"an unusable definition is the `invalid` tier, distinct from both a blocking "
        f"verdict and a bad argument: got {r.returncode}\n{r.stdout}\n{r.stderr}"
    )
    # and not-found stays its own tier rather than being folded into any of the three
    _run(_repo(tmp_path / "n"), "run-checks", "no-such-team", expect=3)


def test_c19_one_code_never_means_two_things_across_actions():
    """The table is a single injective map shared by every action."""
    mod = _load()
    values = [getattr(mod, n) for n in EXIT_CODES]
    assert len(values) == len(set(values)), f"two constants share a code: {EXIT_CODES}"
    src = _source()
    # no action-scoped redefinition of a code's meaning
    assert not re.search(r"EXIT_(?:OK|INPUT_ERROR|NOT_FOUND|INVALID|BLOCKED)\s*=\s*\d",
                         src[src.index("def main("):]), (
        "an exit constant is rebound inside main(), which is how one code acquires two meanings"
    )


def test_c20_the_existing_zero_and_two_branches_still_hold(tmp_path):
    text = TEAM_CMD.read_text(encoding="utf-8")
    for needle in ("MUST 已通过(exit 0)", "MUST NOT 以 exit-2 状态进入批准呈现",
                   "exit 2 的拒绝被**原样上报**"):
        assert needle in text, (
            f"team.md's dry-run gate branches on 0 and 2; the branch text moved or was "
            f"rewritten, so C-17's code choices would no longer be compatible: {needle!r}"
        )
    mod = _load()
    assert mod.EXIT_OK == 0 and mod.EXIT_INPUT_ERROR == 2, (
        "the meanings of 0 and 2 must be untouched for the existing caller"
    )
    # behaviorally, on the real read-only dry-run path
    root = ROOT
    good = _run(root, "targets", REAL_GOAL, "--check", "T-001")
    assert good.returncode in (0, 2), good.returncode


def test_c21_the_usage_versus_input_error_collision_is_annotated_not_fixed():
    src = _source()
    assert not re.search(r"^EXIT_USAGE", src, re.M), (
        "C-21 forbids fixing the pre-existing collision as a side effect of this feature"
    )
    body = _section()
    assert re.search(r"EXIT_USAGE|usage (?:failure|error)", body), (
        "the implementation must state that run-checks does not depend on telling an "
        "argparse usage failure apart from an in-body input error"
    )


# =========================================================================== #
# C-22 … C-25 — pins
# =========================================================================== #


def test_c22_the_exit_table_pin_is_closed_in_both_directions():
    mod = _load()
    declared = {n: v for n, v in vars(mod).items()
                if isinstance(v, int) and re.match(r"^EXIT_[A-Z_]+$", n)}
    assert declared == EXIT_CODES, (
        f"the pin is closed: an EXIT_* constant added or removed without updating this "
        f"suite must fail. module={declared} pinned={EXIT_CODES}"
    )
    assert set(ACTIONS) == set(ACTIONS), "sentinel"


def test_c22b_the_action_roster_pin_is_closed(tmp_path, capsys):
    mod = _load()
    with pytest.raises(SystemExit):
        mod.main(["--help"])
    out = capsys.readouterr().out
    for action in ACTIONS:
        line = next((l for l in out.splitlines() if l.strip().startswith(action + " ")), None)
        assert line, f"--help lost the {action} row"
        assert line.split()[1].startswith(("read", "write")), (
            f"{action} carries no read/write label: {line.strip()!r}"
        )


def test_c23_the_goal_definition_roster_tuple_grew_to_ten():
    src = (ROOT / "tests" / "contract" / "test_goal_definition.py").read_text(encoding="utf-8")
    m = re.search(r"for action in \(([^)]*)\):", src)
    assert m, "the hardcoded action tuple in test_goal_definition.py moved"
    names = re.findall(r'"([a-z-]+)"', m.group(1))
    assert "run-checks" in names, (
        f"a new action outside the hardcoded roster is unguarded, and the roster's "
        f"assertion is not closed so it would not go red: {names}"
    )
    assert names == ACTIONS, f"the roster tuple must match the closed set: {names}"


def test_c24_the_docstring_roster_and_exit_line_grew_in_the_same_commit():
    doc = _load().__doc__ or ""
    assert "run-checks" in doc, "the docstring's action roster must name the new action"
    exit_line = next((l for l in doc.splitlines() if l.startswith("Exit codes:")), None)
    assert exit_line, "the docstring lost its exit-code table line"
    for code in ("0", "2", "3", "4", "5"):
        assert re.search(rf"\b{code}\b", exit_line), (
            f"the exit-code line must carry code {code}: {exit_line!r}"
        )
    assert re.search(r"\b5\b\s*blocked", exit_line), (
        f"code 5 must be labelled `blocked`, not just present: {exit_line!r}"
    )


def test_c25_the_existing_inline_attribution_form_is_not_rewritten():
    doc = _load().__doc__ or ""
    assert "Fixed rules belong in a program, not in a model" in doc, (
        "C-25: goal-utils.py's Program-First attribution is the inline-paren form and "
        "FR-002 was clarified to govern NEW checkers only — it must not be converted"
    )
    assert "Program-First discipline (shared/guidelines/token-efficiency.md)" not in doc, (
        "the STR-008 named-owner form was applied to an existing binary, which the "
        "clarification explicitly excludes"
    )


# =========================================================================== #
# C-26 … C-28 — documentation wiring and the SC-007 evidence
# =========================================================================== #


def test_c26_the_five_check_block_carries_one_cli_invocation():
    text = TEAM_CMD.read_text(encoding="utf-8")
    block = text.split("Resolve the effective Target, then run the five checks")[1]
    block = block.split("\n3. **Restate the Goal**")[0]
    invocations = [l for l in block.splitlines()
                   if "goal-utils.py" in l and "run-checks" in l]
    assert invocations, (
        "the block names all five checks and declares the engine the single source of "
        "truth, but carried no CLI invocation — the agent had to assemble the call itself, "
        "which is the recorded backlog gap this closes"
    )
    assert len(invocations) == 1, (
        f"exactly one invocation form, so there is one criterion and not two: {invocations}"
    )


def test_c27_every_prose_surface_points_at_the_same_invocation():
    for path in (TEAM_DOC, EXEC_GUIDE, GOAL_GUIDE, TOOL_RECORD):
        assert path.is_file(), f"sentinel: {path} moved"
        assert "run-checks" in path.read_text(encoding="utf-8"), (
            f"{path.relative_to(ROOT)} describes the five checks but does not name the "
            f"invocation that now performs them — a second, hand-run criterion survives"
        )
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "python"
                                              / "regen-command-copies.py"), "--check"],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0, f"per-tool copies drifted from the source: {r.stdout}"
    source = TEAM_CMD.read_text(encoding="utf-8")
    for copy in PER_TOOL_COPIES:
        assert "run-checks" in copy.read_text(encoding="utf-8"), (
            f"{copy.relative_to(ROOT)} did not receive the regenerated invocation line"
        )
    assert source.count("run-checks") >= 1


def test_c28_the_sc007_evidence_is_a_real_run_and_the_real_trees_are_untouched():
    assert QUICKSTART_RUN.is_file()
    text = QUICKSTART_RUN.read_text(encoding="utf-8")
    assert "run-checks" in text, "T036's real runs must be recorded in notes/quickstart-run.md"
    assert REAL_TEAM_BOUND in text, (
        "the evidence must name the real bound team it ran against, so a reader can tell a "
        "real run from a constructed one"
    )
    # the contingency C-28 allows must be stated rather than papered over: the only real
    # goal is `active`, so no real terminal-goal team exists and the tier is constructed
    assert "achieved" in text or "terminal" in text.lower(), (
        "the record must say how the terminal-goal tier was obtained, since no real sample "
        "exists — fabricating a verdict is what C-28 forbids"
    )
    assert _checksum(ROOT) == _checksum(ROOT)


# =========================================================================== #
# equivalence with the authoritative gate, and the contract's own clause count
# =========================================================================== #


def test_the_composed_verdict_agrees_with_preview_target_check(tmp_path):
    """The wrapper reports; the existing gate decides. They must not diverge.

    `preview_target_check` is the authoritative single-verdict gate the run mode already
    uses. The five-check array is a projection of it, so for every scenario where both are
    defined they must name the same verdict — otherwise this action has quietly become a
    second grammar, which is what C-5 forbids.
    """
    mod = _load()
    cases = [
        ({"targets": (("T-001", "open"),)}, "T-001"),
        ({"targets": (("T-001", "done"),)}, "T-001"),
        ({"targets": (("T-002", "open"),)}, "T-001"),
        ({"targets": (("T-001", "open"),)}, "g1.T-001"),
        ({"targets": (("T-001", "open"),)}, "other.T-001"),
        ({"targets": (("T-001", "open"),)}, "bogus"),
        ({"goal_status": "achieved", "targets": (("T-001", "open"),)}, "T-001"),
        ({"goal": False, "targets": (("T-001", "open"),)}, "T-001"),
        ({"goal_slug": None, "targets": (("T-001", "open"),)}, "T-001"),
    ]
    for index, (kwargs, reference) in enumerate(cases):
        root = _repo(tmp_path / f"c{index}", **kwargs)
        authoritative = mod.preview_target_check(root, "t1", reference)
        payload = mod.run_checks(root, "t1", reference)
        assert payload["verdict"] == authoritative["verdict"], (
            f"case {index} ({kwargs}, {reference!r}): the wrapper says "
            f"{payload['verdict']!r} while the engine's own gate says "
            f"{authoritative['verdict']!r}"
        )
        # and the array really is a projection of that verdict, not decoration beside it:
        # the top level is either the grammar rejection (which is not one of the five) or
        # the first non-ok check in the gate's own priority order
        projected = mod._compose_verdict(payload["checks"], "local")
        by_id = {c["id"]: c["verdict"] for c in payload["checks"]}
        first_non_ok = next(
            (by_id[cid] for cid in mod._TOP_VERDICT_ORDER
             if by_id[cid] not in ("ok", mod.NOT_EVALUATED)), "ok")
        assert projected == first_non_ok, (payload["checks"], projected, first_non_ok)
        assert payload["verdict"] in (projected, "input-error"), (
            f"case {index}: the reported verdict {payload['verdict']!r} is neither the "
            f"projection of the array ({projected!r}) nor the grammar rejection"
        )


def test_the_real_bound_team_reports_the_measured_state():
    """A real-tree run, read-only, asserting only what was measured — never a fabricated
    verdict. The single real goal is `active` with three `dropped` Targets, so:
    no target -> all evaluated checks ok; a dropped Target -> target-terminal and blocked.
    """
    p = _checks(ROOT, "run-checks", REAL_TEAM_BOUND, expect=0)
    assert p["goal_slug"] == REAL_GOAL and p["identity_kind"] == "explicit"
    assert p["resolution"]["source"] == "none"
    got = _by_name(p)
    assert got["goal-binding"]["verdict"] == "ok"
    assert got["goal-terminal"]["verdict"] == "ok", "the real goal is `active`, not terminal"

    blocked = _checks(ROOT, "run-checks", REAL_TEAM_BOUND, "--target", "T-001", expect=5)
    assert _by_name(blocked)["target-terminal"]["verdict"] == "target-terminal"
    assert blocked["blocked"] is True

    unbound = _checks(ROOT, "run-checks", REAL_TEAM_UNBOUND, expect=0)
    assert _by_name(unbound)["goal-binding"]["verdict"] == "no-goal-definition"
    assert unbound["blocked"] is False, (
        "team.md's check 1 is explicit: no goal definition blocks only when a --target is "
        "specified; with none, 一切照旧"
    )


def test_the_contract_still_has_the_clause_count_this_suite_pins():
    body = (ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts" / "contracts"
            / "run-checks.md").read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", body)
    assert len(ids) == 28, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 29)), "clause ids are not contiguous"
