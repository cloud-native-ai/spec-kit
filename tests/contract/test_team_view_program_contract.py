"""Contract tests for the team-view program interface (103-team-view, T006 — first segment).

Contract: `.specify/specs/103-team-view/contracts/team-view-program.contract.md`
C-24 (read-only), C-26 (closed CLI surface), C-27 (script interface), C-28 (closed exit
codes), C-29 (output modes / E9 envelope). FR-005, FR-014; INV-14; A-5, A-7.

Every invocation is a subprocess of the program under test; fixture trees are built under
pytest ``tmp_path`` and never under the repository's ``.specify/teams/``.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.team_view_fixtures import build_team, snapshot

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"

pytestmark = pytest.mark.contract

ENVELOPE_KEYS = {
    "tool", "version", "mode", "repo_root", "scope", "as_of",
    "overview", "team", "errors", "degraded",
}


def run_program(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(PROGRAM), *args],
        cwd=str(cwd) if cwd is not None else None,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.fixture()
def archive(tmp_path):
    """A minimal but complete fixture repo root with one team."""
    build_team(tmp_path, "team-a")
    return tmp_path


class TestScriptInterface:
    @pytest.mark.parametrize("flag", ["-h", "--help"])
    def test_help_exits_zero_with_zero_writes(self, archive, flag):
        before = snapshot(archive)
        result = run_program(flag, "--repo-root", str(archive))
        assert result.returncode == 0, result.stderr
        assert "usage" in result.stdout.lower()
        assert snapshot(archive) == before

    def test_version_exits_zero_with_zero_writes(self, archive):
        before = snapshot(archive)
        result = run_program("--version", "--repo-root", str(archive))
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip().startswith("team-view.py ")
        assert snapshot(archive) == before

    def test_help_carries_the_four_required_labels(self):
        result = run_program("--help")
        assert result.returncode == 0
        lowered = result.stdout.lower()
        for label in ("usage", "options", "side-effects:", "exit-codes:"):
            assert label in lowered, "help lacks the %s label" % label

    def test_help_declares_the_closed_surface_and_not_target(self):
        result = run_program("--help")
        for declared in ("--repo-root", "--scope", "--spec-dir", "--json", "--version"):
            assert declared in result.stdout, "help lacks %s" % declared
        assert "--target" not in result.stdout


class TestInputRejection:
    def test_undeclared_target_option_rejected(self, archive):
        result = run_program("team-a", "--target", "T-001", "--repo-root", str(archive))
        assert result.returncode == 2
        assert result.stdout.strip() == ""
        assert "target" in (result.stderr + result.stdout).lower()

    def test_extra_positional_rejected(self, archive):
        result = run_program("team-a", "team-b", "--repo-root", str(archive))
        assert result.returncode == 2
        # an absent/unstartable program must not look green through a coincidental exit 2
        assert "unrecognized arguments" in result.stderr.lower()

    def test_invalid_scope_value_rejected(self, archive):
        result = run_program("team-a", "--scope", "bogus", "--repo-root", str(archive))
        assert result.returncode == 2
        assert "bogus" in result.stderr.lower()

    def test_no_slug_auto_scope_rejected(self, archive):
        result = run_program("--scope", "auto", "--repo-root", str(archive))
        assert result.returncode == 2
        assert "auto" in (result.stderr + result.stdout).lower()

    @pytest.mark.parametrize("layer", ["anchor", "goals"])
    def test_non_team_scope_named_not_applicable(self, archive, layer):
        result = run_program("team-a", "--scope", layer, "--repo-root", str(archive))
        assert result.returncode == 2
        assert layer in (result.stderr + result.stdout).lower()


class TestExitCodeClosedSet:
    def test_behavioural_exits_stay_inside_the_closed_set(self, archive):
        # a missing/unstartable program must not look green through a coincidental exit 2
        probe = run_program("--version", "--repo-root", str(archive))
        assert probe.returncode == 0 and probe.stdout.strip().startswith("team-view.py ")
        scenarios = [
            ("--help",),
            ("--version",),
            ("team-a", "--target", "T-001"),
            ("team-a", "team-b"),
            ("team-a", "--scope", "bogus"),
            ("--scope", "auto"),
            ("team-a", "--scope", "anchor"),
            ("--bogus-option",),
        ]
        observed = set()
        for args in scenarios:
            result = run_program(*args, "--repo-root", str(archive))
            observed.add(result.returncode)
            assert result.returncode in {0, 2, 3, 4, 5}, args
        assert 2 in observed

    def test_source_declares_only_closed_set_exits(self):
        source = PROGRAM.read_text(encoding="utf-8")
        literals = set()
        for pattern in (r"sys\.exit\(\s*(\d+)\s*\)", r"SystemExit\(\s*(\d+)\s*\)",
                        r"raise SystemExit\(\s*(\d+)\s*\)"):
            literals.update(int(value) for value in re.findall(pattern, source))
        assert literals <= {0, 2, 3, 4, 5}, "exits outside the closed set: %s" % sorted(literals)


class TestReadOnlySurface:
    def test_program_never_invokes_run_checks(self):
        source = PROGRAM.read_text(encoding="utf-8")
        assert "run-checks" not in source
        assert "run_checks" not in source

    def test_program_source_has_no_write_mode_opens(self):
        source = PROGRAM.read_text(encoding="utf-8")
        for pattern in (
            r"open\([^)]*['\"][wax]",
            r"\.write_text\(",
            r"\.write_bytes\(",
            r"mkdir\(",
            r"unlink\(",
            r"rmtree\(",
        ):
            assert not re.search(pattern, source), "write-capable call found: %s" % pattern


class TestJsonEnvelope:
    def test_single_team_envelope_carries_the_declared_keys(self, archive):
        result = run_program("team-a", "--repo-root", str(archive), "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert set(payload) == ENVELOPE_KEYS
        assert payload["tool"] == "team-view"
        assert payload["mode"] == "single"
        assert payload["scope"]["requested"] == "teams"
        assert payload["degraded"] is False


class TestOverviewEnvelope:
    """US2 (T021): the no-slug envelope — C-29, FR-007, data model E9."""

    def test_overview_envelope_carries_mode_sorting_and_counts(self, tmp_path):
        build_team(tmp_path, "bravo-team")
        build_team(tmp_path, "alpha-team")
        result = run_program("--repo-root", str(tmp_path), "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert set(payload) == ENVELOPE_KEYS
        assert payload["mode"] == "overview"
        assert payload["team"] is None
        overview = payload["overview"]
        assert "rows" in overview
        assert "total" in overview
        assert "corrupt_total" in overview
        slugs = [row["slug"] for row in overview["rows"]]
        assert slugs == sorted(slugs), "overview rows are not slug-ascending: %r" % slugs
        assert slugs == ["alpha-team", "bravo-team"]
        assert overview["total"] == 2
        assert overview["corrupt_total"] == 0
