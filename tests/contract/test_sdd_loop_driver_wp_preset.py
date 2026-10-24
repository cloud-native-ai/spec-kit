"""Contract tests for the stage-team preset and adapter — ST-01…ST-12.

The preset is a driver-owned Markdown asset loaded by explicit path. It is
field-compatible with ``skills/internal/create-team/references/team-presets.md``
but is not a catalog preset: ``create-team`` and ``run-team`` are unchanged and
no team directory is ever persisted.

Clause map: ST-01 location/catalog, ST-02 frontmatter, ST-03 body sections,
ST-04 seats, ST-05 seat-to-execution mapping, ST-06 pattern selection, ST-07
continuous excluded, ST-08 run-scoped adapter, ST-09 no persisted team, ST-10
create-team/run-team unchanged, ST-11 provenance, ST-12 graph over preset.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from fixtures import wp_driver_sim, wp_fixtures

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
PRESET = SKILL_ROOT / "templates" / "stage-team-preset.md"
MODEL = SKILL_ROOT / "references" / "decomposition-model.md"
CREATE_TEAM = REPO_ROOT / "skills" / "internal" / "create-team"
RUN_TEAM = REPO_ROOT / "skills" / "internal" / "run-team"
CATALOG = CREATE_TEAM / "templates" / "teams"
TEAMS_DIR = REPO_ROOT / ".specify" / "teams"

MANDATORY_SECTIONS = (
    "## Goal Skeleton",
    "## Static Structure",
    "## Dynamic Structure",
    "## Instantiation",
    "## Constraints & Hard Rules",
    "## Known Pitfalls",
)
SEATS = {
    "stage-planner": ("executor", "Worker", "persistent"),
    "stage-worker": ("executor", "Worker", "temporary"),
    "stage-verifier": ("evaluator", "Worker", "temporary"),
    "stage-integrator": ("executor", "Worker", "temporary"),
}
PRESET_FIELDS = {
    "preset_id",
    "name",
    "pattern",
    "summary",
    "when_to_use",
    "signals",
    "inputs",
    "members",
    "config",
    "provenance",
}


def _preset_text() -> str:
    assert PRESET.is_file(), "missing stage-team preset: %s" % PRESET
    return PRESET.read_text(encoding="utf-8")


def _frontmatter_text() -> str:
    match = re.match(r"^---\n(.*?)\n---\n", _preset_text(), re.DOTALL)
    assert match, "the preset must open with YAML frontmatter"
    return match.group(1)


def _frontmatter() -> dict:
    return yaml.safe_load(_frontmatter_text())


def _body() -> str:
    return _preset_text().split("\n---\n", 1)[1]


def _section(name: str) -> str:
    body = _body()
    marker = "## %s" % name
    start = body.index(marker)
    rest = body[start + len(marker) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading == -1 else rest[:next_heading]


def _model_text() -> str:
    assert MODEL.is_file(), "missing runtime owner: %s" % MODEL
    return MODEL.read_text(encoding="utf-8")


def _team_entries():
    return sorted(str(path.relative_to(TEAMS_DIR)) for path in TEAMS_DIR.rglob("*"))


def _attribute_lines(text: str):
    for line in text.splitlines():
        if "continuous" in line.lower():
            yield line


def _team_skill_files():
    for root in (CREATE_TEAM, RUN_TEAM):
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix in {
                ".md",
                ".py",
                ".json",
                ".yaml",
                ".yml",
            }:
                yield path


def test_st_01_preset_lives_at_the_driver_owned_path_and_is_not_catalogued():
    """ST-01: driver-owned path, explicit load, not in the create-team catalog."""
    assert PRESET.is_file(), "missing stage-team preset: %s" % PRESET
    assert CATALOG not in PRESET.parents
    assert not (CATALOG / PRESET.name).exists()
    for path in _team_skill_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert "sdd-stage-team" not in text, path
        assert "stage-team-preset.md" not in text, path
    assert "templates/stage-team-preset.md" in _model_text()


def test_st_02_frontmatter_carries_the_preset_contract_fields():
    """ST-02: schema-compatible frontmatter with parallel as the default shape."""
    frontmatter = _frontmatter()
    assert PRESET_FIELDS <= set(frontmatter)
    assert frontmatter["preset_id"] == "sdd-stage-team"
    assert frontmatter["pattern"] == "parallel"
    assert frontmatter["name"].strip()
    assert frontmatter["summary"].strip()
    assert frontmatter["when_to_use"].strip()
    assert isinstance(frontmatter["signals"], list) and frontmatter["signals"]
    inputs = frontmatter["inputs"]
    assert [item["name"] for item in inputs] == [
        "stage",
        "wp_graph",
        "line",
        "slot_cap",
    ]
    assert [bool(item["required"]) for item in inputs] == [True, True, True, False]
    assert frontmatter["config"]["default_pattern"] == "parallel"
    assert frontmatter["config"]["slot_cap_default"] == 2


def test_st_03_body_carries_the_six_mandatory_sections():
    """ST-03: six mandatory body sections and a run-scoped Instantiation."""
    body = _body()
    for heading in MANDATORY_SECTIONS:
        assert heading in body, heading
    instantiation = _section("Instantiation").lower()
    assert "run-scoped" in instantiation
    assert "do not create a team directory" in instantiation
    assert "do not persist a team definition" in instantiation


def test_st_04_roster_defines_exactly_the_four_standard_seats():
    """ST-04: stage-planner, stage-worker, stage-verifier, stage-integrator."""
    members = _frontmatter()["members"]
    assert [member["role"] for member in members] == list(SEATS)
    for member in members:
        expected = SEATS[member["role"]]
        assert (
            member["stage"],
            member["type"],
            member["lifecycle"],
        ) == expected, member["role"]
        assert member["responsibility"].strip(), member["role"]


def test_st_05_seat_to_execution_mapping_is_declared():
    """ST-05: planner=driver, one worker per package, fresh verifier, one integrator."""
    text = (_preset_text() + "\n" + _model_text()).lower()
    assert "the driver itself" in text
    assert "one execution per work package" in text
    assert "fresh-context" in text
    assert "never the package executor" in text
    assert "one execution per decomposed stage attempt" in text
    assert "never dispatches another coordinator" in text


def test_st_05_adapter_maps_each_package_to_one_worker_execution():
    """ST-05: the adapter's projection carries the derived lifetimes."""
    plan = wp_fixtures.make_two_package_plan()
    projection = wp_driver_sim.adapt_stage_team(plan)
    workers = [
        seat for seat in projection["seats"] if seat["role"] == "stage-worker"
    ]
    assert [seat["wp_id"] for seat in workers] == ["plan-wp01", "plan-wp02"]
    assert all(seat["lifetime"] == "one-package" for seat in workers)
    assert all(seat["execution_form"] == "native" for seat in workers)

    verifier = [
        seat for seat in projection["seats"] if seat["role"] == "stage-verifier"
    ][0]
    assert verifier["stage"] == "evaluator"
    assert verifier["lifetime"] == "one-verdict"

    integrator = [
        seat for seat in projection["seats"] if seat["role"] == "stage-integrator"
    ][0]
    assert integrator["lifetime"] == "one-stage-attempt"

    planner = [
        seat for seat in projection["seats"] if seat["role"] == "stage-planner"
    ][0]
    assert planner["lifetime"] == "stage"
    assert planner["execution_form"] == "driver"


def test_st_06_pattern_selection_is_graph_derived():
    """ST-06: iteration needs a repair loop; parallel is read-only independent only."""
    text = (_preset_text() + "\n" + _model_text()).lower()
    assert "graph-derived" in text
    assert "repair_loop" in text
    assert "every package is read-only" in text
    assert "any write package or any dependency edge" in text
    assert "serial" in text


def test_st_06_adapter_selects_parallel_only_for_independent_read_only_graphs():
    """ST-06: a write package or a dependency edge forces serial."""
    parallel = wp_fixtures.make_two_package_plan()
    assert wp_driver_sim.adapt_stage_team(parallel)["pattern"] == "parallel"

    with_write = wp_fixtures.make_plan(
        packages=[
            wp_fixtures.make_package("plan-wp01"),
            wp_fixtures.make_write_package("plan-wp02"),
        ],
        pattern="serial",
        slot_cap=1,
    )
    assert wp_driver_sim.adapt_stage_team(with_write)["pattern"] == "serial"

    dependent = wp_fixtures.make_two_package_plan()
    dependent["packages"][1]["depends_on"] = ["plan-wp01"]
    assert wp_driver_sim.adapt_stage_team(dependent)["pattern"] == "serial"

    iteration = wp_fixtures.make_two_package_plan(
        pattern="iteration",
        slot_cap=1,
        repair_loop={
            "max_iterations": 3,
            "stop_condition": "zero open findings",
            "findings_source": "review.md",
        },
    )
    assert wp_driver_sim.adapt_stage_team(iteration)["pattern"] == "iteration"


def test_st_07_continuous_is_excluded_from_the_preset_and_adapter():
    """ST-07: continuous never appears as a selectable pattern."""
    for text in (_preset_text(), _model_text()):
        for line in _attribute_lines(text):
            lowered = line.lower()
            assert any(
                marker in lowered
                for marker in ("never", "excluded", "not selected", "no ")
            ), line
    plans = [
        wp_fixtures.make_two_package_plan(),
        wp_fixtures.make_plan(
            packages=[wp_fixtures.make_single_package_plan()["packages"][0]]
        ),
    ]
    assert {
        wp_driver_sim.adapt_stage_team(plan)["pattern"] for plan in plans
    } <= {"parallel", "serial", "iteration"}


def test_st_08_adapter_binds_the_graph_into_a_run_scoped_plan_fence():
    """ST-08: substitute stage, line, hash, slot cap, pattern, and seat mapping."""
    model = _model_text().lower()
    for phrase in (
        "run-scoped",
        "plan fence",
        "plan hash",
        "slot cap",
        "package-to-seat mapping",
        "no team directory",
        "no goal binding",
        "no team run report",
    ):
        assert phrase in model, phrase

    plan = wp_fixtures.make_two_package_plan()
    projection = wp_driver_sim.adapt_stage_team(plan)
    assert projection["preset_id"] == "sdd-stage-team"
    assert projection["stage"] == plan["stage"]
    assert projection["line_id"] == plan["line_id"]
    assert projection["plan_hash"] == plan["plan_hash"]
    assert projection["slot_cap"] == plan["slot_cap"]
    assert projection["pattern"] == plan["pattern"]
    assert projection["team_directory"] is None


def test_st_09_no_team_directory_is_persisted_by_the_adapter():
    """ST-09: no .specify/teams/<slug>/team.md per stage, attempt, or run."""
    text = (_preset_text() + "\n" + _model_text()).lower()
    assert ".specify/teams/<slug>/team.md" in text
    before = _team_entries()
    plan = wp_fixtures.make_two_package_plan()
    projection = wp_driver_sim.adapt_stage_team(plan)
    assert projection["team_directory"] is None
    assert _team_entries() == before
    assert not (TEAMS_DIR / plan["stage"]).exists()


def test_st_10_create_team_and_run_team_are_not_modified():
    """ST-10: no catalog entry and no preset reference from the team skills."""
    assert not (CATALOG / "sdd-stage-team.md").exists()
    for path in _team_skill_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert "preset: sdd-stage-team" not in text, path
        assert "stage-team-preset" not in text, path


def test_st_11_provenance_records_source_shape_and_first_run_obligation():
    """ST-11: baseline/vocabulary provenance plus the first-run evidence duty."""
    provenance = _frontmatter()["provenance"].lower()
    for phrase in (
        "070",
        "baseline",
        "role × stage × type",
        "not from a create-team catalog run",
        "first decomposed stage",
        "coordination report",
    ):
        assert phrase in provenance, phrase


def test_st_12_graph_derived_values_take_precedence_over_preset_defaults():
    """ST-12: the graph-derived pattern and resolved slot cap always win."""
    model = _model_text().lower()
    assert "graph-derived" in model
    assert "take precedence" in model

    preset = _frontmatter()
    assert preset["pattern"] == "parallel"
    assert preset["config"]["slot_cap_default"] == 2

    write_plan = wp_fixtures.make_plan(
        packages=[
            wp_fixtures.make_package("plan-wp01"),
            wp_fixtures.make_write_package("plan-wp02"),
        ],
        pattern="serial",
        slot_cap=1,
    )
    projection = wp_driver_sim.adapt_stage_team(write_plan)
    assert projection["pattern"] == "serial"
    assert projection["pattern"] != preset["pattern"]
    assert projection["slot_cap"] == 1
    assert projection["slot_cap"] != preset["config"]["slot_cap_default"]
    worker_seat = [
        seat for seat in projection["seats"] if seat["role"] == "stage-worker"
    ][1]
    assert worker_seat["wp_id"] == "plan-wp02"
    assert worker_seat["stage"] == "executor"
