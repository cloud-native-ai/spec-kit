"""Contract tests for the crew territory — feature 094, C-61…C-67 (SC-007).

Tasks rows T050 (a crew write onto a spec artifact is refused by the territory check)
and T062 (the expansion is recorded and forbids the four spec artifacts). The check is
the `create-team` territory surface pinned by `quickstart.md` S-7:
`skills/internal/create-team/scripts/territory-check.py`. The refusal MUST NOT depend on
the crew's cooperation: it is decided by the team definition's closed `territory` lists,
with a non-zero exit and a refusal text naming the path and the seat (FR-036).

T062's guard is structural: the expansion procedure is authored prose in
`skills/internal/improve-team/SKILL.md`, so the test asserts the recorded procedure — one
record per team, granted entries inside the spec directory and out of the two archive
layers, the four spec artifacts forced into `territory.forbidden`, and the writeback as
one record per task.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TERRITORY_CHECK = REPO_ROOT / "skills/internal/create-team/scripts/territory-check.py"
IMPROVE_TEAM = REPO_ROOT / "skills/internal/improve-team/SKILL.md"

FIXTURE_SPEC = "900-fixture"
PARTIAL_SPEC = ".specify/specs/" + FIXTURE_SPEC
GOAL_SLUG = "demo-goal"
TEAM_SLUG = "demo-crew"
FOUR_SPEC_ARTIFACTS = ("requirements.md", "tasks.md", "verification.md", "handoff.md")


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TERRITORY_CHECK), *args],
        capture_output=True, text=True, cwd=str(cwd or REPO_ROOT))


@pytest.fixture()
def sandbox():
    """The sanctioned scratch root (`.specify/.tmp/`), one directory per test."""
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="territory-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _seed_crew(root: Path) -> Path:
    """A serial crew whose territory is the handoff expansion's post-state (C-61…C-63)."""
    spec_dir = root / ".specify/specs" / FIXTURE_SPEC
    spec_dir.mkdir(parents=True, exist_ok=True)
    for artifact in FOUR_SPEC_ARTIFACTS:
        (spec_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

    team = root / ".specify/teams" / TEAM_SLUG / "team.md"
    team.parent.mkdir(parents=True, exist_ok=True)
    team.write_text(
        "---\n"
        f"name: {TEAM_SLUG}\n"
        f"slug: {TEAM_SLUG}\n"
        f"goal_slug: {GOAL_SLUG}\n"
        "lifecycle_state: active\n"
        "territory:\n"
        "  write:\n"
        f"    - {PARTIAL_SPEC}/src/**\n"
        f"  read:\n"
        f"    - {PARTIAL_SPEC}/**\n"
        "  forbidden:\n"
        f"    - {PARTIAL_SPEC}/requirements.md\n"
        f"    - {PARTIAL_SPEC}/tasks.md\n"
        f"    - {PARTIAL_SPEC}/verification.md\n"
        f"    - {PARTIAL_SPEC}/handoff.md\n"
        "    - .specify/anchoring/**\n"
        "    - .specify/teams/**\n"
        "pattern: serial\n"
        "members:\n"
        "  - agent: agent-stage-executor-template\n"
        "    role: stage-executor\n"
        "    lifecycle: temporary\n"
        "---\n\n"
        f"# Team: {TEAM_SLUG}\n",
        encoding="utf-8")
    return team


# ---------------------------------------------------------------------------
# T050 / C-62 / SC-007 — the four spec artifacts are refused, with path and seat named
# ---------------------------------------------------------------------------
def test_a_crew_write_onto_a_spec_artifact_is_refused_by_the_territory_check(sandbox):
    assert TERRITORY_CHECK.is_file(), (
        "the create-team territory check is missing: "
        f"{TERRITORY_CHECK.relative_to(REPO_ROOT)} (quickstart S-7)")
    team = _seed_crew(sandbox)

    for artifact in FOUR_SPEC_ARTIFACTS:
        path = f"{PARTIAL_SPEC}/{artifact}"
        proc = _run("--team", str(team), "--path", path, "--repo-root", str(sandbox))
        assert proc.returncode != 0, (
            f"a crew write onto {artifact} MUST be refused, got exit "
            f"{proc.returncode}: {proc.stdout!r} {proc.stderr!r}")
        combined = proc.stdout + proc.stderr
        assert path in combined, f"the refusal names the path; got {combined!r}"
        assert TEAM_SLUG in combined, f"the refusal names the seat; got {combined!r}"

    # A granted path inside the spec directory is allowed (C-61/C-63).
    proc = _run("--team", str(team), "--path", f"{PARTIAL_SPEC}/src/impl.py",
                "--repo-root", str(sandbox))
    assert proc.returncode == 0, (
        "a write inside the granted territory is allowed: "
        f"{proc.stdout!r} {proc.stderr!r}")

    # The two archive layers are outside every granted write scope (C-63).
    for archive_path in (f".specify/anchoring/{GOAL_SLUG}/goal.md",
                         f".specify/teams/{TEAM_SLUG}/team.md"):
        proc = _run("--team", str(team), "--path", archive_path,
                    "--repo-root", str(sandbox))
        assert proc.returncode != 0, (
            f"the archive layer is never a crew write target: {archive_path}")

    # An explicit negative always wins: a broad write grant covering the whole spec
    # directory still refuses the four artifacts (C-62 — never cooperation-dependent).
    broad = team.read_text(encoding="utf-8").replace(
        f"    - {PARTIAL_SPEC}/src/**", f"    - {PARTIAL_SPEC}/**")
    team.write_text(broad, encoding="utf-8")
    proc = _run("--team", str(team), "--path", f"{PARTIAL_SPEC}/tasks.md",
                "--repo-root", str(sandbox))
    assert proc.returncode != 0, (
        "territory.forbidden outranks a broad territory.write grant (C-62)")


# ---------------------------------------------------------------------------
# T062 / C-61 / C-65 / C-67 — the expansion is recorded in improve-team
# ---------------------------------------------------------------------------
def test_the_territory_expansion_is_recorded_and_forbids_the_four_spec_artifacts():
    assert IMPROVE_TEAM.is_file(), f"improve-team SKILL.md is missing: {IMPROVE_TEAM}"
    text = IMPROVE_TEAM.read_text(encoding="utf-8")

    match = re.search(
        r"^## Handoff Territory Expansion\n(.*?)(?=^## |\Z)",
        text, re.MULTILINE | re.DOTALL)
    assert match, (
        "improve-team MUST record the handoff territory expansion procedure "
        "(tasks row T062)")
    section = match.group(1)

    assert "one record per team" in section, (
        "the expansion is one explicit, disclosed record per team (C-61)")
    assert "territory.write" in section, (
        "the contract's `## Territory` expands into the team's territory.write (C-61)")
    for artifact in FOUR_SPEC_ARTIFACTS:
        assert artifact in section, (
            f"{artifact} MUST be forced into territory.forbidden (C-62)")
    assert "territory.forbidden" in section
    assert ".specify/anchoring/" in section and ".specify/teams/" in section, (
        "granted entries stay out of the two archive layers (C-63)")
    assert "writeback/<T-NNN>.yaml" in section, (
        "the writeback is one record per completed task (C-65)")
    assert "handoff.md" in text and "team_slug" in text, (
        "the section consumes the contract through team_slug (C-58/C-61)")
