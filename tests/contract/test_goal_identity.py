"""Contract tests for goal identity resolution (`goal_slug`).

Pins `data-model.md` § 1.3 invariants GI-1…GI-4 and FR-031 / FR-034 / SC-013.

Goal identity is what makes `.specify/goal/<goal-slug>/summary/` a *goal* index
rather than a relocated team index, so its resolution order and its stability
under goal-prose edits are contract surface.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify/specs/036-team-summary"
REQUIREMENTS = SPEC_DIR / "requirements.md"
DATA_MODEL = SPEC_DIR / "data-model.md"

SKILL_CANONICAL = REPO_ROOT / "skills/create-team/SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".specify/skills/create-team/SKILL.md"
TEAMS_DIR = REPO_ROOT / ".specify/teams"

# Same DDL identifier grammar the item ids obey; goal_slug is also a directory name.
DDL_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")

pytestmark = pytest.mark.contract


# --------------------------------------------------------------------------
# Resolution logic (GI-1, FR-031, FR-034)
# --------------------------------------------------------------------------


def resolve_goal_identity(frontmatter: dict) -> tuple[str, str]:
    """Return (goal_slug, identity) where identity is 'explicit' or 'inferred'.

    Explicit declaration wins; absent declaration falls back to the team slug and
    is marked inferred. Goal prose is never an input — that is GI-1.
    """
    declared = frontmatter.get("goal_slug")
    if declared:
        return declared, "explicit"
    return frontmatter["slug"], "inferred"


def test_explicit_goal_slug_wins() -> None:
    slug, identity = resolve_goal_identity(
        {"slug": "team-a", "goal_slug": "harvest-insights", "goal": "some prose"}
    )
    assert (slug, identity) == ("harvest-insights", "explicit")


def test_absent_goal_slug_falls_back_to_team_slug_marked_inferred() -> None:
    slug, identity = resolve_goal_identity({"slug": "team-a", "goal": "some prose"})
    assert (slug, identity) == ("team-a", "inferred")


def test_two_teams_declaring_the_same_goal_slug_resolve_to_one_goal() -> None:
    """FR-031: same value means same goal regardless of which team declared it."""
    a = resolve_goal_identity({"slug": "team-a", "goal_slug": "shared-goal"})
    b = resolve_goal_identity({"slug": "team-b", "goal_slug": "shared-goal"})
    assert a[0] == b[0] == "shared-goal"
    assert a[1] == b[1] == "explicit"


def test_goal_prose_edit_does_not_change_the_resolved_identity() -> None:
    """GI-1 / FR-019: the delivery directory must not migrate when goal text changes."""
    before = resolve_goal_identity(
        {"slug": "team-a", "goal_slug": "stable-goal", "goal": "original objective"}
    )
    after = resolve_goal_identity(
        {"slug": "team-a", "goal_slug": "stable-goal", "goal": "deliberately rewritten"}
    )
    assert before == after


def test_inferred_identity_also_survives_goal_prose_edits() -> None:
    before = resolve_goal_identity({"slug": "team-a", "goal": "original"})
    after = resolve_goal_identity({"slug": "team-a", "goal": "rewritten"})
    assert before == after == ("team-a", "inferred")


# --------------------------------------------------------------------------
# Grammar and path safety
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value", ["harvest-insights", "goal.v2", "a", "team-a", "Goal_1"]
)
def test_valid_goal_slugs_satisfy_the_ddl_grammar_and_are_path_safe(value: str) -> None:
    assert DDL_IDENTIFIER.match(value), value
    assert "/" not in value and value not in {".", ".."}


@pytest.mark.parametrize(
    "value", ["改进目标", "goal slug", "-leading-dash", "a/b", "..", ".", ""]
)
def test_invalid_goal_slugs_are_rejected(value: str) -> None:
    path_safe = "/" not in value and value not in {".", ".."} and value != ""
    assert not (DDL_IDENTIFIER.match(value) and path_safe), value


def test_delivery_directory_is_derived_from_goal_not_team() -> None:
    slug, _ = resolve_goal_identity({"slug": "team-a", "goal_slug": "shared-goal"})
    assert f".specify/goal/{slug}/summary/" == ".specify/goal/shared-goal/summary/"


# --------------------------------------------------------------------------
# Structural: the field is documented where teams are authored
# --------------------------------------------------------------------------


@pytest.mark.parametrize("path", [SKILL_CANONICAL, SKILL_MIRROR], ids=["canonical", "mirror"])
def test_goal_slug_is_documented_in_the_team_schema(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert "goal_slug" in text, f"goal_slug absent from the persisted team schema in {path}"


@pytest.mark.parametrize("path", [SKILL_CANONICAL, SKILL_MIRROR], ids=["canonical", "mirror"])
def test_goal_slug_is_distinguished_from_team_slug(path: Path) -> None:
    """The two coexist with different meanings and must not be conflated.

    Checked per line rather than by character window: the frontmatter schema and
    the explanatory bullets are legitimately far apart in the file, so proximity
    is not a valid proxy for "the distinction is stated".
    """
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if "goal_slug" in ln]
    assert lines, f"goal_slug absent from {path}"
    distinguishing = [
        ln
        for ln in lines
        if ("team slug" in ln or "team's identity" in ln or "not the team" in ln)
    ]
    assert distinguishing, (
        "no line states how goal_slug differs from the team slug; "
        f"lines mentioning goal_slug were: {lines}"
    )


def test_data_model_documents_the_gi_invariants() -> None:
    text = DATA_MODEL.read_text(encoding="utf-8")
    missing = [tag for tag in ("GI-1", "GI-2", "GI-3", "GI-4") if tag not in text]
    assert not missing, f"goal-identity invariants {missing} undocumented"


def test_requirements_declare_goal_identity_as_explicit_not_derived() -> None:
    text = REQUIREMENTS.read_text(encoding="utf-8")
    fr031 = re.search(r"^\- \*\*FR-031\*\*: (.+)$", text, re.M)
    assert fr031, "FR-031 missing"
    assert "MUST NOT" in fr031.group(1), "FR-031 must forbid deriving identity from prose"


# --------------------------------------------------------------------------
# Reality check on the repository's real teams (FR-034 inference path)
# --------------------------------------------------------------------------


def _frontmatter_field(team_md: Path, field: str) -> str | None:
    text = team_md.read_text(encoding="utf-8")
    match = re.search(rf"^{field}:\s*(\S+)\s*$", text, re.M)
    return match.group(1) if match else None


@pytest.mark.skipif(not TEAMS_DIR.is_dir(), reason="no teams directory")
def test_existing_teams_resolve_without_requiring_migration() -> None:
    """FR-034: pre-existing teams must summarize with zero up-front changes."""
    teams = sorted(p for p in TEAMS_DIR.glob("*/team.md"))
    assert teams, "expected at least one persisted team"
    for team_md in teams:
        slug = _frontmatter_field(team_md, "slug") or team_md.parent.name
        declared = _frontmatter_field(team_md, "goal_slug")
        resolved, identity = resolve_goal_identity(
            {"slug": slug, **({"goal_slug": declared} if declared else {})}
        )
        assert DDL_IDENTIFIER.match(resolved), f"{team_md}: unusable goal identity {resolved!r}"
        assert identity in {"explicit", "inferred"}
        if declared is None:
            assert identity == "inferred" and resolved == slug
