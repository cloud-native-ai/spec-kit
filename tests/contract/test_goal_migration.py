"""Contract tests for the goal delivery-directory migration (037-goal-registry, T004).

Source contract: .specify/specs/037-goal-registry/contracts/goal-writeset-migration.contract.md

The migration is scoped **by face**. Live surfaces must reach zero residual references
to the pre-migration root; historical surfaces must keep theirs, because the
2026-08-04 clarification quotes the old path verbatim as the user's directive and
rewriting it would falsify the record (RS-1).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
OLD_PATH_NEEDLE = "project/goal"

#: Faces that MUST NOT retain a reference after the migration.
LIVE_SURFACES = (
    "skills/create-team/SKILL.md",
    "skills/create-team/references/summary-mapping.md",
    "skills/create-team/scripts/build-summary-input.py",
    "templates/commands/team.md",
    # 2026-08-17: .specify/templates/commands/ mirror retired.
    ".specify/skills/create-team/SKILL.md",
    ".specify/skills/create-team/references/summary-mapping.md",
    ".specify/skills/create-team/scripts/build-summary-input.py",
    ".claude/commands/speckit.team.md",
    ".github/prompts/speckit.team.prompt.md",
    ".qoder/commands/speckit.team.md",
    ".opencode/command/speckit.team.md",
    "docs/reference/commands/team.md",
    ".specify/memory/tools/build-summary-input.py.md",
)

#: Prefixes whose files are history and MUST be left alone (RS-1).
HISTORICAL_PREFIXES = (
    ".specify/specs/036-team-summary/",
    ".specify/specs/037-goal-registry/",
    ".specify/memory/feedback/",
    ".specify/memory/features",
)

#: Migration guards must *name* the old path in order to assert its absence, so they
#: are not offenders. Listed explicitly — never filtered by a silent pattern.
GUARD_FILES = (
    "tests/contract/test_goal_migration.py",
    "tests/contract/test_goal_writeset.py",
    "tests/contract/test_summary_trigger.py",
    "tests/contract/test_summary_writeset.py",
)

pytestmark = pytest.mark.contract


def _tracked_files_containing(needle: str) -> list[str]:
    """Every non-binary file in the repo containing ``needle``, repo-relative."""
    proc = subprocess.run(
        [
            "grep", "-rl", needle, ".",
            "--exclude-dir=.git",
            "--exclude-dir=.venv",
            "--exclude-dir=node_modules",
            "--exclude-dir=__pycache__",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    # grep exits 1 when there are no matches, which is a legitimate end state here.
    if proc.returncode not in (0, 1):
        pytest.fail(f"grep failed ({proc.returncode}): {proc.stderr}")
    return sorted(
        line[2:] if line.startswith("./") else line
        for line in proc.stdout.splitlines()
        if line.strip()
    )


def _is_historical(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in HISTORICAL_PREFIXES)


def _is_guard(path: str) -> bool:
    return path in GUARD_FILES


class TestLiveSurfacesAreMigrated:
    """RS-1: the live face reaches zero; each surface is checked by name."""

    @pytest.mark.parametrize("relpath", LIVE_SURFACES)
    def test_live_surface_has_no_residual_reference(self, relpath):
        path = REPO_ROOT / relpath
        assert path.is_file(), f"expected live surface missing: {relpath}"
        text = path.read_text(encoding="utf-8")
        assert OLD_PATH_NEEDLE not in text, (
            f"{relpath} still references the pre-migration path '{OLD_PATH_NEEDLE}'"
        )

    def test_no_live_face_file_retains_the_old_path(self):
        """Catches live surfaces the explicit list above does not enumerate."""
        offenders = [
            p for p in _tracked_files_containing(OLD_PATH_NEEDLE)
            if not _is_historical(p) and not _is_guard(p)
        ]
        assert offenders == [], (
            "live-face files still reference the pre-migration path "
            f"(historical faces and the {len(GUARD_FILES)} migration guards are "
            "excluded by design):\n  " + "\n  ".join(offenders)
        )


class TestHistoricalFacesArePreserved:
    """RS-1: history is not rewritten — the old string is expected to survive there."""

    def test_the_user_directive_quoting_the_old_path_survives_verbatim(self):
        spec = REPO_ROOT / ".specify/specs/037-goal-registry/requirements.md"
        text = spec.read_text(encoding="utf-8")
        assert "使用.specify/goal/收编.specify/project/goal/" in text, (
            "the 2026-08-04 user directive quoting the old path must remain verbatim "
            "in the Clarifications record; rewriting it falsifies history"
        )

    def test_historical_face_is_not_empty(self):
        """A zero historical count would mean history was scrubbed."""
        historical = [
            p for p in _tracked_files_containing(OLD_PATH_NEEDLE) if _is_historical(p)
        ]
        assert historical, (
            "no historical file retains the old path — the append-only record appears "
            "to have been rewritten"
        )


class TestMigrationTargetShape:
    """MG-1/MG-3: exactly one goal index, and pre-existing artifacts untouched."""

    def test_project_tree_holds_no_goal_subdirectory(self):
        assert not (REPO_ROOT / ".specify/project/goal").exists(), (
            ".specify/project/goal/ must not exist after the migration"
        )

    def test_pre_existing_project_artifacts_are_preserved(self):
        project = REPO_ROOT / ".specify/project"
        if not project.is_dir():
            pytest.skip(".specify/project/ not present in this checkout")
        assert (project / "project.md").is_file(), (
            "the manage-project era project.md must not be moved or deleted"
        )
