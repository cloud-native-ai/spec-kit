"""Contract tests for the handoff contract (`handoff.md`) — feature 094, C-53…C-70.

Tasks rows T049 (three-way key pair, SC-006), T059 (shape and location), T060
(cite, never copy) and T061 (dangling-key refusal + reverse `handoff_ref`). This is a
template-only surface: the contract's shape is authored prose in
`skills/internal/create-team/references/handoff-contract-template.md`, so the assertions
are **structural contract tests over the template and over a fixture repository** — never
unit tests of a service (tasks.md § Tests Mode).

T049's guard builds a fixture tree (`.specify/anchoring/<goal>/goal.md`,
`.specify/teams/<team>/team.md`, `<spec-dir>/handoff.md`) whose handoff instance is
**instantiated from the authored template**, then resolves the three-way key pair in both
directions (C-60).

T061's guard drives the engine action that writes the reverse keys. The contracts fix the
behaviour (`handoff-dangling-key`, exit 2; `handoff_ref` written through the engine's
binding discipline), not the entry name; this module pins `handoff-ref --handoff <path>`
and discloses the pin in `notes/implement-wp04.md`. Until that engine action lands in
`scripts/python/goal-utils.py` (a file outside this package's write domain) the guard is
red-first by design.
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
READER = REPO_ROOT / "scripts/python/declaration_reader.py"
TEMPLATE = REPO_ROOT / "skills/internal/create-team/references/handoff-contract-template.md"

FIXTURE_SPEC = "900-fixture"
GOAL_SLUG = "demo-goal"
TEAM_SLUG = "demo-crew"
HANDOFF_REL = f".specify/specs/{FIXTURE_SPEC}/handoff.md"

SECTION_ORDER = ["Status", "Goal", "Targets", "Task Reference", "Territory",
                 "Acceptance Criteria", "Writeback", "Crew"]


def _load_reader():
    spec = importlib.util.spec_from_file_location("declaration_reader_094_handoff", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dr = _load_reader()


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


@pytest.fixture()
def sandbox():
    """The sanctioned scratch root (`.specify/.tmp/`), one directory per test."""
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="handoff-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# Template extraction and fixture seeding
# ---------------------------------------------------------------------------
def _template_text() -> str:
    assert TEMPLATE.is_file(), (
        "the handoff contract template is missing: "
        f"{TEMPLATE.relative_to(REPO_ROOT)} (tasks row T059, ruling N-3)")
    return TEMPLATE.read_text(encoding="utf-8")


def _shape_from_template() -> str:
    """The one `handoff/v1` shape block the template carries."""
    text = _template_text()
    blocks = re.findall(r"```markdown\n(.*?)```", text, re.DOTALL)
    assert len(blocks) == 1, (
        "the template MUST carry exactly one ```markdown shape block; "
        f"found {len(blocks)}")
    return blocks[0]


def _split_frontmatter(text: str) -> tuple[str, str]:
    assert text.startswith("---\n"), "the handoff shape starts with its YAML frontmatter"
    end = text.find("\n---", 3)
    assert end != -1, "the handoff frontmatter is not closed"
    return text[3:end], text[end + 4:]


def _frontmatter(text: str) -> dict:
    raw, _body = _split_frontmatter(text)
    body = dr.parse_subset(raw, "handoff-frontmatter")
    assert isinstance(body, dict), "the handoff frontmatter does not parse as a mapping"
    return body


def _instantiate(shape: str, goal_slug: str, team_slug: str) -> str:
    instance = shape
    for placeholder, value in (("<goal-slug>", goal_slug),
                               ("<team-slug>", team_slug),
                               ("<YYYY-MM-DD>", "2026-11-09")):
        instance = instance.replace(placeholder, value)
    assert "<goal-slug>" not in instance and "<team-slug>" not in instance
    return instance


def _section(body: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
    assert match, f"section `## {heading}` is missing"
    return match.group(1)


def _binding_block(owner: str, owner_id: str, origin: str = "null") -> str:
    return (f"binding:\n"
            f"  owner: {owner}\n"
            f"  owner_id: {owner_id}\n"
            f"  origin: {origin}\n")


def _seed_goal(root: Path, slug: str, *, handoff_ref: str | None = None) -> Path:
    path = root / ".specify/anchoring" / slug / "anchor.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ref_line = f"handoff_ref: {handoff_ref}\n" if handoff_ref else ""
    path.write_text(
        "---\n"
        "status: active\n"
        "created: 2026-11-09\n"
        "updated: 2026-11-09\n"
        f"{_binding_block('human', 'human')}"
        f"{ref_line}"
        "---\n\n"
        f"# Anchor: {slug}\n\n"
        "## Objective\n\nHold the fixture goal still while the contract cites it.\n\n"
        "## Success Criteria\n\n1. The contract resolves.\n",
        encoding="utf-8")
    return path


def _seed_team(root: Path, slug: str, *, goal_slug: str,
               handoff_ref: str | None = None) -> Path:
    path = root / ".specify/teams" / slug / "team.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ref_line = f"handoff_ref: {handoff_ref}\n" if handoff_ref else ""
    path.write_text(
        "---\n"
        f"name: {slug}\n"
        f"slug: {slug}\n"
        f"goal_slug: {goal_slug}\n"
        "lifecycle_state: active\n"
        f"{_binding_block('sdd-run', 'r20261109T064500Z-094a', FIXTURE_SPEC)}"
        f"{ref_line}"
        "pattern: serial\n"
        "members:\n"
        "  - agent: agent-stage-executor-template\n"
        "    role: stage-executor\n"
        "    lifecycle: temporary\n"
        "---\n\n"
        f"# Team: {slug}\n",
        encoding="utf-8")
    return path


def _seed_spec(root: Path) -> Path:
    spec_dir = root / ".specify/specs" / FIXTURE_SPEC
    spec_dir.mkdir(parents=True, exist_ok=True)
    return spec_dir


# ---------------------------------------------------------------------------
# T049 / C-53 / C-58 / C-59 / C-60 / SC-006 — the three-way key pair
# ---------------------------------------------------------------------------
def test_the_three_way_keys_resolve_in_both_directions(sandbox):
    shape = _shape_from_template()
    spec_dir = _seed_spec(sandbox)
    handoff = spec_dir / "handoff.md"
    handoff.write_text(_instantiate(shape, GOAL_SLUG, TEAM_SLUG), encoding="utf-8")
    goal_path = _seed_goal(sandbox, GOAL_SLUG, handoff_ref=HANDOFF_REL)
    team_path = _seed_team(sandbox, TEAM_SLUG, goal_slug=GOAL_SLUG,
                           handoff_ref=HANDOFF_REL)

    front = _frontmatter(handoff.read_text(encoding="utf-8"))
    # Forward direction: the contract names both definitions; each key resolves (C-58).
    resolved_goal = sandbox / ".specify/anchoring" / front["goal_slug"] / "anchor.md"
    resolved_team = sandbox / ".specify/teams" / front["team_slug"] / "team.md"
    assert resolved_goal.is_file(), (
        f"goal_slug {front['goal_slug']!r} does not resolve under .specify/anchoring/")
    assert resolved_team.is_file(), (
        f"team_slug {front['team_slug']!r} does not resolve under .specify/teams/")
    assert front["goal_slug"] == GOAL_SLUG
    assert front["team_slug"] == TEAM_SLUG

    # Reverse direction: both definitions carry handoff_ref back at the same file (C-59).
    goal_front = _frontmatter(goal_path.read_text(encoding="utf-8"))
    team_front = _frontmatter(team_path.read_text(encoding="utf-8"))
    assert goal_front.get("handoff_ref"), "the goal definition lacks its handoff_ref"
    assert team_front.get("handoff_ref"), "the team definition lacks its handoff_ref"
    goal_target = (sandbox / str(goal_front["handoff_ref"])).resolve()
    team_target = (sandbox / str(team_front["handoff_ref"])).resolve()
    assert goal_target == team_target == handoff.resolve(), (
        "the two handoff_ref values MUST point at the same contract file (C-60)")

    # Both directions agree on identity: the objects the contract names are the ones
    # whose own frontmatter points back.
    assert resolved_goal.parent.name == front["goal_slug"]
    assert resolved_team.parent.name == front["team_slug"]
    assert str(team_front.get("goal_slug")) == front["goal_slug"]

    # C-53: one contract per spec, a fixed relative path, no variant names.
    assert sorted(p.name for p in spec_dir.iterdir()) == ["handoff.md"]


# ---------------------------------------------------------------------------
# T059 / C-54 / C-55 — the eight mandatory sections, in order
# ---------------------------------------------------------------------------
def test_the_contract_carries_its_eight_sections_in_order():
    shape = _shape_from_template()
    front_raw, body = _split_frontmatter(shape)
    front = dr.parse_subset(front_raw, "handoff-shape")
    assert front["contract"] == "handoff/v1", "the frontmatter carries contract: handoff/v1"
    for key in ("state", "goal_slug", "team_slug", "created", "updated", "supersedes"):
        assert key in front, f"the handoff frontmatter lacks mandatory key {key!r} (C-55)"

    sections = re.findall(r"^## (.+)$", body, re.MULTILINE)
    assert sections == SECTION_ORDER, (
        "the contract MUST carry exactly these sections, in this order (C-54); "
        f"got {sections}")

    text = _template_text()
    assert "None." in text, (
        "an empty section MUST be the single line `None.`, never omitted (C-54)")
    for terminal in ("fulfilled", "abandoned"):
        assert terminal in text, f"the state machine names its terminal state {terminal!r}"
    assert "never deleted" in text or "retained" in text, (
        "a terminal handoff is retained, never deleted (C-55)")
    assert "<spec-dir>/handoff.md" in text, (
        "the fixed relative path `<spec-dir>/handoff.md` is declared (C-53)")
    assert "tasks" in text and "implement" in text, (
        "production by the tasks stage and consumption by implement are declared (C-68)")


# ---------------------------------------------------------------------------
# T060 / C-56 / C-57 — cite, never copy
# ---------------------------------------------------------------------------
def test_the_contract_cites_and_never_copies_task_rows(sandbox):
    shape = _shape_from_template()
    _front_raw, body = _split_frontmatter(shape)

    goal_section = _section(body, "Goal")
    assert "goal_slug" in goal_section, (
        "`## Goal` cites the goal definition by goal_slug only (C-56)")
    targets_section = _section(body, "Targets")
    assert "T-NNN" in targets_section, (
        "`## Targets` cites the goal's T-NNN ids (C-56)")
    task_ref = _section(body, "Task Reference")
    assert re.search(r"range|explicit", task_ref, re.IGNORECASE), (
        "`## Task Reference` references id ranges or an explicit id list (C-57)")

    text = _template_text()
    assert "task-copy-in-handoff" in text, (
        "the template names the refused defect for a copied task row (C-57)")

    # An instantiated contract cites the goal by slug and never restates its prose.
    instance = _instantiate(shape, GOAL_SLUG, TEAM_SLUG)
    inst_body = _split_frontmatter(instance)[1]
    assert GOAL_SLUG in _section(inst_body, "Goal")
    assert "Hold the fixture goal still while the contract cites it." not in inst_body, (
        "the contract MUST NOT restate the goal's objective (C-56)")
    # A task-row line in the contract is the defect C-57 refuses.
    reference_line = ("Reference the task table by id ranges or an explicit id list "
                      "(for example `T001–T010`).")
    assert reference_line in instance, "the shape's Task Reference citation moved"
    defect = instance.replace(reference_line, "- [ ] T001 deliver the fixture row")
    assert re.search(r"^- \[[ xX>~]\] T", defect, re.MULTILINE), (
        "the defect predicate is a line beginning with `- [ ] T`")


# ---------------------------------------------------------------------------
# T061 / C-58 / C-59 — a dangling key is refused; the reverse keys are engine-written
# ---------------------------------------------------------------------------
def test_a_dangling_handoff_key_is_refused_at_creation(sandbox):
    """Red-first by design while the engine action is unowned (see module docstring).

    The contracts fix the behaviour, not the entry name; this module pins
    `handoff-ref --handoff <path>` as the engine entry that validates both keys and
    writes the reverse `handoff_ref` through the binding discipline (C-5/C-6/C-59).
    """
    shape = _shape_from_template()
    spec_dir = _seed_spec(sandbox)
    handoff = spec_dir / "handoff.md"
    handoff.write_text(_instantiate(shape, GOAL_SLUG, TEAM_SLUG), encoding="utf-8")
    _seed_goal(sandbox, GOAL_SLUG)

    # The team named by team_slug exists nowhere: the contract names a team that does
    # not exist and MUST be refused at creation (C-58).
    proc = _run(sandbox, "handoff-ref", "--handoff", str(handoff))
    assert proc.returncode == 2, (
        "a dangling handoff key exits 2 (handoff-dangling-key): "
        f"got {proc.returncode}: {proc.stdout!r} {proc.stderr!r}")
    combined = proc.stdout + proc.stderr
    assert "handoff-dangling-key" in combined, (
        f"the refusal names the dangling-key label; got {combined!r}")
    assert TEAM_SLUG in combined, "the refusal names the unresolvable key value"

    # Once both keys resolve, the reverse handoff_ref lands on both definitions and
    # every other byte of each file stays identical (C-6's discipline applied to C-59).
    team_path = _seed_team(sandbox, TEAM_SLUG, goal_slug=GOAL_SLUG)
    goal_path = sandbox / ".specify/anchoring" / GOAL_SLUG / "anchor.md"
    before = {goal_path: goal_path.read_text(encoding="utf-8").splitlines(),
              team_path: team_path.read_text(encoding="utf-8").splitlines()}

    proc = _run(sandbox, "handoff-ref", "--handoff", str(handoff))
    assert proc.returncode == 0, (
        f"the reverse-key write failed: {proc.stdout!r} {proc.stderr!r}")
    for path, original in before.items():
        lines = path.read_text(encoding="utf-8").splitlines()
        refs = [line for line in lines if line.startswith("handoff_ref:")]
        assert refs == [f"handoff_ref: {HANDOFF_REL}"], (
            f"{path.name} MUST carry exactly one handoff_ref pointing at the contract; "
            f"got {refs}")
        assert [line for line in lines if not line.startswith("handoff_ref:")] == original, (
            f"{path.name} changed outside the handoff_ref line")
